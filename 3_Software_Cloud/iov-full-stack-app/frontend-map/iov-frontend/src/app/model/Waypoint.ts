export interface Waypoint {
    location: { latitude: number, longitude: number },
    stateOfCharge: number,
    carId: string,
    charging: boolean
}