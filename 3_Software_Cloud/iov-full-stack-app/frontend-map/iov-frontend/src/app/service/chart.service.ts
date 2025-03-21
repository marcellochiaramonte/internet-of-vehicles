import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChartService {

  constructor() { }

  socChart: BehaviorSubject<any> = new BehaviorSubject(null);


}
