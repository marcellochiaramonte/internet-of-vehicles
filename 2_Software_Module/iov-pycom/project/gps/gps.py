from libraries.gps.micropyGPS import MicropyGPS
from machine import UART, RTC
import libraries.uasyncio as asyncio
from config.constants import gps_update_rate
from utime import ticks_diff, ticks_ms, time
from project.vehicles.metrics import LocationDataChange


class GPSReader:
    def __init__(self):
        self.data_available = False
        self.current_location = None
        self.gps_time_is_set = False
        self.gps_sentences = {}
        self.GPS_DEBUG = False
        self.minimal_deviation = 2.5e-04  # minimal decimal degrees to be considered new position

        self.uart = UART(1, baudrate=9600, bits=8, parity=None, stop=1, pins=("P21", "P22"))
        self.my_gps = MicropyGPS()
        self.rtc = RTC()
        self.reset_gps_sentences()
        self.create_loop_tasks()
        print("created gps reader object")

    def dprint(self, *args):
        if self.GPS_DEBUG:
            print(*args)

    def create_loop_tasks(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.poll_gps_reading())
        # loop.create_task(self.print_stuff())

    async def poll_gps_reading(self):
        # infinite loop that reads the GPS sentences every [gps_update_rate] seconds
        # after updating the [my_gps] instance of the GPS library, the [current_location] is updated
        while True:
            await self.receive_from_uart()
            await asyncio.sleep(gps_update_rate)

    async def receive_from_uart(self):
        self.reset_gps_sentences()  # resets the sentences dict
        self.uart.read()  # clears the buffer
        while not self.all_sentences_defined():
            try:
                buf = self.uart.readline()
                # print(buf)
                if buf != None:
                    self.data_available = True
                    # print("received buffer")
                    try:
                        buf_dec = buf.decode("utf-8")
                        sentence_id = buf_dec[1:6]
                        self.gps_sentences.update({sentence_id: buf_dec})  # updates the instance of GPS Library
                        for x in buf_dec:
                            self.my_gps.update(x)
                    except (UnicodeError):
                        print("unicode error")
            except OSError as e:
                print(e)
                print("error here")
            await asyncio.sleep(0.1)  # around 10 sentences per second

        self.read_gps_position()  # once all sentences are defined, update the current position property

    def read_gps_position(self):
        if self.data_available and self.my_gps.valid:
            curr_date = self.my_gps.date
            curr_time = self.my_gps.timestamp
            year = curr_date[2]
            month = curr_date[1]
            day = curr_date[0]
            hour = curr_time[0]
            minute = curr_time[1]
            second = int(curr_time[2])  # seconds are float, need to be casted

            self.rtc.init((year, month, day, hour, minute, second, 0, 0))  # updates the RealTimeClock
            self.gps_time_is_set = True

            self.dprint("\nunix time: ", time())
            self.dprint(
                "YYYY.MM.DD HH:MM:SS",
                "\n"
                + str(year)
                + "."
                + str(month)
                + "."
                + str(day)
                + " "
                + str(hour)
                + ":"
                + str(minute)
                + ":"
                + str(second),
            )
            self.dprint("latitude: ", self.my_gps.latitude[0])
            self.dprint("longitude: ", self.my_gps.longitude[0])

            if not self.current_location or self.location_changed():
                self.current_location = LocationDataChange(
                    timestamp=time(),  # UNIX Timestamp
                    latitude=self.my_gps.latitude[0],
                    longitude=self.my_gps.longitude[0],
                )

            # self.dprint("\nunix time: ", self.current_location.timestamp)
            # self.dprint("YYYY MM DD HH MM SS", "\n" + str(year), month, day, "  ", hour, minute, second)
            # self.dprint("latitude: ", self.current_location.latitude)
            # self.dprint("longitude: ", self.current_location.longitude)

    def location_changed(self):
        latitude_diff = abs(self.current_location.latitude - self.my_gps.latitude[0])
        longitude_diff = abs(self.current_location.longitude - self.my_gps.longitude[0])
        # self.dprint("lat dif", latitude_diff)
        # self.dprint("lon dif", longitude_diff)
        return latitude_diff > self.minimal_deviation or longitude_diff > self.minimal_deviation
        # if lat or lon changed more tha tdeviation, update the current position object

    def reset_gps_sentences(self):
        self.gps_sentences = {
            "GPRMC": "",
            "GPVTG": "",
            "GPGGA": "",
            "GPGSA": "",
            "GPGSV": "",
            "GPGLL": "",
        }

    def all_sentences_defined(self):
        return (
            self.gps_sentences["GPRMC"] != ""
            and self.gps_sentences["GPVTG"] != ""
            and self.gps_sentences["GPGGA"] != ""
            and self.gps_sentences["GPGSA"] != ""
            and self.gps_sentences["GPGSV"] != ""
            and self.gps_sentences["GPGLL"] != ""
        )

    async def print_stuff(self):
        while True:
            if self.data_available and self.my_gps.valid:
                # locations.append([my_gps.timestamp, my_gps.latitude, my_gps.longitude, my_gps.satellites_used])
                # if len(locations > 10):
                #     print(locations)
                print("time: ", self.my_gps.timestamp)

                print("latitude: ", self.my_gps.latitude)
                print("longitude: ", self.my_gps.longitude)

                # print("coord_format: ", self.my_gps.coord_format)

                print("speed x y z: ", self.my_gps.speed)
                print("course: ", self.my_gps.course)
                print("altitude: ", self.my_gps.altitude)

                # print("geoid_height: ", self.my_gps.geoid_height)

                print("satellites_in_view: ", self.my_gps.satellites_in_view)
                print("satellites_in_use: ", self.my_gps.satellites_in_use)
                print("satellites_used: ", self.my_gps.satellites_used)

                # print("last_sv_sentence: ", self.my_gps.last_sv_sentence)
                # print("total_sv_sentences: ", self.my_gps.total_sv_sentences)

                # print("satellite_data: ", self.my_gps.satellite_data)
                # print("hdop,pdop,vdop: ", self.my_gps.hdop, self.my_gps.pdop, self.my_gps.vdop)
                print("valid: ", self.my_gps.valid)
                # print("fix_stat: ", self.my_gps.fix_stat)
                # print("fix_type: ", self.my_gps.fix_type)
                print()
            await asyncio.sleep(2)
