import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard/dashboard.component';
import { LiveDataComponent } from './components/live-data/live-data/live-data.component';
import { LineChartComponent } from './components/vehicle-components/line-chart/line-chart.component';
import { VehicleDetailsComponent } from './components/vehicle-components/vehicle-details/vehicle-details.component';
import { VehicleListComponent } from './components/vehicle-components/vehicle-list/vehicle-list.component';
import { VehicleMapComponent } from "./components/vehicle-components/vehicle-map/vehicle-map.component";

const routes: Routes = [
  { path: '', component: VehicleListComponent, pathMatch: 'full' },
  { path: 'map', component: VehicleMapComponent },
  { path: 'battery', component: LineChartComponent },
  { path: 'vehicles', component: VehicleListComponent },
  { path: 'vehicles/:uuid', component: VehicleDetailsComponent },
  { path: 'live', component: LiveDataComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
