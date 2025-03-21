export class Vehicle {
    make: string;
    model: string;
    id: string;
    licencePlate: string;
    iconColor: string;

    // vehicleStatus: VehicleStatus;
    carOn: boolean;
    soc: number;
    odometer: number;
    chargingState: number;

    eventList: Event[];


    locationList: Location[];
}

export class VehicleStatus {
    carOn: boolean;
    soc: number;
    odometer: number;
    chargingState: number;
}