import { Vehicle } from "./Vehicle";
import { MetricId } from "./metric";

export class VehicleEvent {
    timestamp: number;
    value: string;
    metric: MetricId;
    vehicle: Vehicle;
}