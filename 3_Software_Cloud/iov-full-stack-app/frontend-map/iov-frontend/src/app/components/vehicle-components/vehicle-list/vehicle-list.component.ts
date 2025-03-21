import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { Router } from '@angular/router';
import { Vehicle, VehicleStatus } from 'src/app/model/Vehicle';
import { VehicleService } from 'src/app/service/vehicle.service';
@Component({
  selector: 'app-vehicle-list',
  templateUrl: './vehicle-list.component.html',
  styleUrls: ['./vehicle-list.component.scss']
})
export class VehicleListComponent implements OnInit {

  @ViewChild(MatSort) sort: MatSort;

  displayedColumns: string[] = ['id', 'model', 'make', 'carOn', 'soc', 'odometer', 'chargingState', 'iconColor'];

  dataSource: MatTableDataSource<Vehicle> = new MatTableDataSource();

  constructor(private vehicleService: VehicleService, private router: Router) {
  }

  ngOnInit(): void {
    this.vehicleService.findAllVehicles().subscribe(res => {
      res.forEach(v => {
        v.carOn = (Math.random() > 0.5);
        v.chargingState = Math.round((Math.random() * 2));
        v.odometer = Math.random() * 30000 + 30000;
        v.soc = Math.random() * 100;
      });
      console.log(res)
      this.dataSource = new MatTableDataSource(res);
      this.dataSource.sort = this.sort;
    });
  }

  navigateToVehicle(vehicle: Vehicle) {
    console.log(vehicle)
    this.router.navigateByUrl('vehicles/' + vehicle.id);

  }

  getCarStatusString(carOn: boolean) {
    return carOn ? 'On' : 'Off'
  }

  // "assets/img/car-'+ {{element.color} +'.png"

  getIcon(color: string) {
    if (color) {
      return 'assets/img/car-' + color + '.png';
    }
  }

}
