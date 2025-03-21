import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'ol';
import { environment } from '../../environments/environment';
import { Location } from '../model/Location';

@Injectable({
  providedIn: 'root'
})
export class LocationService {

  constructor(private http: HttpClient) { }

  findLocations(uuid: string, startTimestamp: number, endTimestamp: number) {
    const params = new HttpParams()
      .set('carId', uuid)
      .set('startTimestamp', Math.round(startTimestamp).toString())
      .set('endTimestamp', Math.round(endTimestamp).toString())

    return this.http.get<Location[]>(environment.apiEndpoint + "location/filter", { params });
  }

  findCurrentLocation(carId: string) {
    const params = new HttpParams()
      .set('carId', carId)
    return this.http.get<Location>(environment.apiEndpoint + "location/current", { params });

  }
}
