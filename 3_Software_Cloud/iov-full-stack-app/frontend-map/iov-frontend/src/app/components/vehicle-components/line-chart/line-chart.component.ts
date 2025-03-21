import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { ApexAxisChartSeries, ApexChart, ApexDataLabels, ApexFill, ApexMarkers, ApexTitleSubtitle, ApexTooltip, ApexXAxis, ApexYAxis, ChartComponent } from 'ng-apexcharts';
import { dataSeries } from "./data-series";
import { ChartTypes } from './chartTypes';
import { ChartService } from 'src/app/service/chart.service';

@Component({
  selector: 'app-line-chart',
  templateUrl: './line-chart.component.html',
  styleUrls: ['./line-chart.component.scss']
})
export class LineChartComponent implements OnInit {

  public series: ApexAxisChartSeries;
  public chart: ApexChart;
  public dataLabels: ApexDataLabels;
  public markers: ApexMarkers;
  public title: ApexTitleSubtitle;
  public fill: ApexFill;
  public yaxis: ApexYAxis;
  public xaxis: ApexXAxis;
  public tooltip: ApexTooltip;

  @Input() chartName: string;
  @Input() vehicleName: string;
  @Input() chartType: ChartTypes;

  constructor(private chartService: ChartService) { }

  ngOnInit(): void {

    this.chartService.socChart.subscribe(res => {
      if (res) {
        this.series = [
          {
            name: this.vehicleName,
            data: res
          }
        ];
        this.initChartData();
      }

    });
  }

  public initChartData(): void {

    this.chart = {
      type: "area",
      stacked: false,
      height: 350,
      zoom: {
        type: "x",
        enabled: true,
        autoScaleYaxis: true
      },
      toolbar: {
        autoSelected: "zoom"
      }
    };
    this.dataLabels = {
      enabled: false
    };
    this.markers = {
      size: 2
    };
    this.title = {
      text: this.chartName,
      align: "center"
    };
    // this.fill = {
    //   type: "gradient",
    //   gradient: {
    //     shadeIntensity: 1,
    //     inverseColors: false,
    //     opacityFrom: 0.5,
    //     opacityTo: 0,
    //     stops: [0, 90, 100]
    //   }
    // };
    if (this.chartType === ChartTypes.BATTERY_SOC) {
      this.yaxis = {
        max: 100,
        min: 0,
        labels: {
          formatter: function (val) {
            return (val).toFixed(0) + '%';
          }
        },
      };
    }

    this.xaxis = {
      type: "datetime"
    };
    this.tooltip = {
      shared: false,
      y: {
        formatter: function (val) {
          return val.toString() + "%";
        }
      }
    };
  }



}
