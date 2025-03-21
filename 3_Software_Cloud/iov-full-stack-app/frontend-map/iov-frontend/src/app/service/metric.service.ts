import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { VehicleEvent } from 'src/app/model/Event';

@Injectable({
  providedIn: 'root'
})
export class MetricService {

  constructor(private http: HttpClient) { }

  findEventsByVehicleAndMetric(uuid: string, metricId: number, startTimestamp: number, endTimestamp: number): Observable<VehicleEvent[]> {
    const params = new HttpParams()
      .set('vehicleUuid', uuid)
      .set('metricId', metricId.toString())
      .set('startTimestamp', Math.round(startTimestamp).toString())
      .set('endTimestamp', Math.round(endTimestamp).toString())

    return this.http.get<VehicleEvent[]>(environment.apiEndpoint + "events/filter", { params });
  }

}
