import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { NavigationEnd, Router } from '@angular/router';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  links = [
    // {
    //   name: "Home",
    //   link: ""
    // },
    {
      name: "Vehicles",
      link: "vehicles"
    },
    {
      name: "Map",
      link: "map"
    },

    // {
    //   name: "Live",
    //   link: "live"
    // },
  ];

}

