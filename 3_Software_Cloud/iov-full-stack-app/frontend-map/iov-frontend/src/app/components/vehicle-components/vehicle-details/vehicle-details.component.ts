import { AfterViewInit, Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Vehicle } from 'src/app/model/Vehicle';
import { VehicleService } from 'src/app/service/vehicle.service';
import { MetricService } from 'src/app/service/metric.service';
import { ChartTypes } from '../line-chart/chartTypes';
import { FormControl, FormGroup } from '@angular/forms';
import * as moment from 'moment';
import { ChartService } from 'src/app/service/chart.service';

@Component({
  selector: 'app-vehicle-details',
  templateUrl: './vehicle-details.component.html',
  styleUrls: ['./vehicle-details.component.scss']
})
export class VehicleDetailsComponent implements OnInit, AfterViewInit {

  uuid: string;
  vehicle: Vehicle;

  range = new FormGroup({
    start: new FormControl(moment().subtract(6, 'days').startOf('day')),
    end: new FormControl(moment())
  });

  startUnixTime: number;
  endUnixTime: number;


  constructor(
    private vehicleService: VehicleService,
    private activatedRoute: ActivatedRoute,
    private metricService: MetricService,
    private chartService: ChartService) { }

  ngOnInit(): void {
    this.activatedRoute.paramMap.subscribe(res => {
      this.uuid = res.get('uuid');
      this.vehicleService.findVehicleByUuid(this.uuid).subscribe(res => {
        this.vehicle = res;
        this.setSOC();
        // console.log(res);
      });
    });
  }

  ngAfterViewInit() {

  }


  setSOC() {
    this.fixUTCTimeZone();
    this.metricService.findEventsByVehicleAndMetric(this.uuid, 110, this.startUnixTime, this.endUnixTime)
      .subscribe(res => {
        let seriesData = [];
        res.forEach(item => {
          let element: [number, number] = [item.timestamp * 1000, parseFloat(item.value)]
          seriesData.push(element)
        });
        this.chartService.socChart.next(seriesData);
        console.debug(res)
      });
  }

  fixUTCTimeZone() {
    this.startUnixTime = this.range.controls.start.value.startOf('day').unix();
    this.endUnixTime = this.range.controls.end.value.endOf('day').unix();
  }

  getChartType(charttype) {
    switch (charttype) {
      case 'SOC':
        return ChartTypes.BATTERY_SOC;
    }
  }

  changedEndDate() {
    if (this.range.valid && this.range.value.start && this.range.value.end) {
      this.setSOC();
    }
  }
}
