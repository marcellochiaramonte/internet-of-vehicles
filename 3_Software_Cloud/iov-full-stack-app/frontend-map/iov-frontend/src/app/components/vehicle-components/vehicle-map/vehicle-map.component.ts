import { Component, ElementRef, HostListener, OnInit, ViewChild } from '@angular/core';
import { Observable } from 'ol';
import { Waypoint } from 'src/app/model/Waypoint';
import { LocationService } from 'src/app/service/location.service';

import { GeoService } from "../../../service/geo.service";
declare var ol: any;

@Component({
  selector: 'app-vehicle-map',
  templateUrl: './vehicle-map.component.html',
  styleUrls: ['./vehicle-map.component.scss']
})
export class VehicleMapComponent implements OnInit {

  @HostListener('mousemove', ['$event']) onMouseMove(event) {
    if (this.soc) {
      this.soc.nativeElement.style.left = event.clientX + 'px';
      this.soc.nativeElement.style.top = event.clientY + 'px';
    }

  }

  @ViewChild("soc") soc: ElementRef;

  geolocation: Geolocation;
  readonly uniLocation: [number, number] = [7.2628641, 51.4469531];
  carLocation: [number, number] = [7.2635669, 51.4476251];
  carId = '1234';
  selectedWaypoint: Waypoint;



  constructor(public geo: GeoService, private locationService: LocationService) {
    this.geo.selectedWaypoint.subscribe(wp => {
      this.selectedWaypoint = wp;
    });
  }

  ngOnInit() {
    console.log()
  }

  ngAfterViewInit() {
    this.geo.updateSize();
    this.geo.setCarMarker(this.carId, this.carLocation);
    this.geolocation = navigator.geolocation;
    this.findWaypoints();
    setInterval(() => this.showCurrentCarPosition(), 10000)

  }

  findWaypoints() {
    let now = Math.round(new Date().getTime() / 1000);
    let oneWeekAgo = now - 60 * 60 * 24 * 7;
    console.log('getting waypoints')
    this.locationService.findLocations(this.carId, oneWeekAgo, now).subscribe(res => {
      console.log(res)
      let sorted = res.sort((a, b) => a.timestamp - b.timestamp)
      let waypoints = []
      sorted.forEach(p => {
        waypoints.push({
          carId: this.carId,
          charging: 0,
          location: { latitude: p.latitude, longitude: p.longitude },
          stateOfCharge: 67
        })
      })
      this.geo.createWaypoints('1234', waypoints)
      if (sorted.length > 0) {
        let lastPosition = sorted[sorted.length - 1]
        if (lastPosition) {
          console.log(lastPosition)
          if (lastPosition.latitude !== this.carLocation[1] || lastPosition.longitude !== this.carLocation[0]) {
            this.carLocation = [lastPosition.longitude, lastPosition.latitude]
            this.geo.moveCar(this.carId, this.carLocation)
          }
        }
      }

    });
  }

  showCurrentCarPosition() {
    this.locationService.findCurrentLocation(this.carId).subscribe(res => {
      console.log('current location', res)
      let currentLocation = res;
      if (res) {
        if (currentLocation.latitude !== this.carLocation[1] || currentLocation.longitude !== this.carLocation[0]) {
          this.carLocation = [res.longitude, res.latitude]
          this.geo.moveCar(this.carId, this.carLocation)
          this.findWaypoints()
        }
      }


    })
  }

  locate() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(position => {
        // this.geo.setView(16, [position.coords.longitude, position.coords.latitude]);
        this.geo.setView(2, this.uniLocation);
      });
    }
  }

  centerOnCar() {
    this.geo.setView(16, this.carLocation);
  }

  changeCarLocation() {
    this.carLocation = [this.carLocation[0] * 1.00001, this.carLocation[1] * 1.00001];
    this.geo.moveCar('1234', this.carLocation);
  }


}
