import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { VehicleMapComponent } from "./components/vehicle-components/vehicle-map/vehicle-map.component";
import { DashboardComponent } from './components/dashboard/dashboard/dashboard.component';
import { HttpClientModule } from '@angular/common/http';
import { NgApexchartsModule } from 'ng-apexcharts';
import { LineChartComponent } from './components/vehicle-components/line-chart/line-chart.component';
import { VehicleListComponent } from './components/vehicle-components/vehicle-list/vehicle-list.component';
import { MatListModule } from '@angular/material/list';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { VehicleDetailsComponent } from './components/vehicle-components/vehicle-details/vehicle-details.component';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { ReactiveFormsModule } from '@angular/forms';
import { MatMomentDateModule } from '@angular/material-moment-adapter';
import { LiveDataComponent } from './components/live-data/live-data/live-data.component';

@NgModule({
  declarations: [
    AppComponent,
    VehicleMapComponent,
    DashboardComponent,
    LineChartComponent,
    VehicleListComponent,
    VehicleDetailsComponent,
    LiveDataComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    NgApexchartsModule,
    MatListModule,
    MatTableModule,
    MatSortModule,
    MatDatepickerModule,
    MatInputModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatMomentDateModule,
  ],
  providers: [

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
