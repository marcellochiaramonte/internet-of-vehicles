import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Vehicle } from '../model/Vehicle';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Waypoint } from '../model/Waypoint';

@Injectable({
  providedIn: 'root'
})
export class VehicleService {

  constructor(private http: HttpClient) { }

  vehicleUuid = 'd1c9ef28-07bc-4bca-961e-e5750d5b4dbf';



  findAllVehicles(): Observable<Vehicle[]> {
    return this.http.get<Vehicle[]>(environment.apiEndpoint + "vehicles/all");
  }

  // findAllMockVehicles(): Observable<Vehicle[]> {
  //   return of(MockVehicles);
  // }

  // findMockVehicleByUuid(uuid: string): Observable<Vehicle> {
  //   return of(MockVehicles.find(vehicle => vehicle.uuid === uuid));
  // }

  findVehicleByUuid(uuid: string): Observable<Vehicle> {
    const params = new HttpParams()
      .set('id', uuid);
    return this.http.get<Vehicle>(environment.apiEndpoint + "vehicles/find", { params });
  }

  getDemoData(): Observable<Waypoint[]> {
    return this.http.get<Waypoint[]>('assets/data.json');
  }

}
