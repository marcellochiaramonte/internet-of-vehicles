export class Metric {
    metricId: MetricId;
    metricName: string;
    metricType: string;
}

export enum MetricId {
    LOCATION = 0,
    SOC = 1
}