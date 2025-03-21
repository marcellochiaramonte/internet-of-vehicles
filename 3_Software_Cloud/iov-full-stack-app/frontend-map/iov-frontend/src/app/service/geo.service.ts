import { Injectable } from '@angular/core';
import Map from 'ol/Map';
import View from 'ol/View';
import LayerTile from 'ol/layer/Tile';
import FullScreen from 'ol/control/FullScreen';
import ScaleLine from 'ol/control/ScaleLine';
import Attribution from 'ol/control/Attribution';
import SourceOsm from 'ol/source/OSM';
import SourceStamen from 'ol/source/Stamen';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import { fromLonLat, toLonLat } from 'ol/proj';
import { defaults as defaultControls, MousePosition } from 'ol/control';
import { defaults as defaultInteractions, PinchZoom } from 'ol/interaction';
import Style from 'ol/style/Style';
import { Fill, Icon, Stroke } from 'ol/style';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { BehaviorSubject } from 'rxjs';
import { ChargingStations } from '../../assets/charginStations';
import LineString from 'ol/geom/LineString';
import { Waypoint } from '../model/Waypoint';
import { createStringXY } from 'ol/coordinate';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'ol';
import { VehicleService } from './vehicle.service';

@Injectable({
  providedIn: 'root'
})
export class GeoService {
  activeCarsList: any[] = [];
  acitveCars: BehaviorSubject<any[]> = new BehaviorSubject(null);

  selectedWaypoint: BehaviorSubject<Waypoint> = new BehaviorSubject(null);

  waypoints: Waypoint[] = [];
  sensibilityWaypointMouse = 0.0015
  readonly uniLocation: [number, number] = [7.2628641, 51.4469531];

  /** OL-Map. */
  readonly map: Map;

  /** Basic layer. */
  readonly layerTile: LayerTile;

  /** Sources for basic layer. */
  readonly sources: { readonly osm: SourceOsm; readonly stamen: SourceStamen; };


  constructor(private vehicleService: VehicleService) {

    // this.vehicleService.getDemoData().subscribe(res => {
    //   this.createWaypoints('1234', res)
    //   console.log(res)
    // })

    this.sources = {
      osm: new SourceOsm(),
      stamen: new SourceStamen({ layer: 'toner' })
    };

    this.layerTile = new LayerTile({
      source: this.sources.osm
    });

    this.map = new Map({
      interactions: defaultInteractions().extend([
        new PinchZoom()
      ]),
      layers: [
        this.layerTile
      ],
      view: new View({
        center: fromLonLat(this.uniLocation),
        zoom: 16,
        constrainResolution: true
      }),
      controls: defaultControls().extend([
        this.createMouseControl(),
        new Attribution(),
        // new ZoomToExtent({
        //   extent: [
        //     813079.7791264898, 5929220.284081122,
        //     848966.9639063801, 5936863.986909639
        //   ]
        // }),
        new FullScreen(),
        new ScaleLine({
          bar: true,
          minWidth: 150
        })
      ])
    });
    this.addChargingStations();
    this.setMouseEventListener();
  }

  setMouseEventListener() {
    this.map.on('pointermove', (evt) => {
      let coords = toLonLat(evt.coordinate)
      // console.log(coords)
      let foundWaypoint = this.waypoints.find(wp => this.isMouseNearWaypoint(wp, coords))
      if (foundWaypoint) {
        if (this.selectedWaypoint.value === null) {
          this.selectedWaypoint.next(foundWaypoint);
        } else {
          if (foundWaypoint && foundWaypoint.location != this.selectedWaypoint.value.location) {
            this.selectedWaypoint.next(foundWaypoint);
            // console.log('soc:', foundWaypoint.stateOfCharge)
          }
        }
      } else {
        this.selectedWaypoint.next(null);
      }


    })
  }

  isMouseNearWaypoint(wp: Waypoint, coord) {
    // console.log(wp.location.latitude - coord[1])
    return Math.abs(wp.location.latitude - coord[1]) < this.sensibilityWaypointMouse && Math.abs(wp.location.longitude - coord[0]) < this.sensibilityWaypointMouse
  }

  removeLayer(layer: VectorLayer) {
    this.map.removeLayer(layer);
  }

  moveCar(carId: string, newPosition: [number, number]) {
    let layer = this.acitveCars.getValue().find(car => car.carId === carId);
    this.removeLayer(layer.layer);
    this.activeCarsList = this.acitveCars.getValue().filter(item => item.carId !== carId);
    this.acitveCars.next(this.activeCarsList);
    this.setCarMarker(carId, newPosition);
  }

  addChargingStations() {
    let charginsStationList = []
    ChargingStations.forEach(cs => {
      let coords: [number, number] = [cs.AddressInfo.Longitude, cs.AddressInfo.Latitude]
      charginsStationList.push(coords)
    });
    this.createChargingStationMarker(charginsStationList);
  }

  setView(zoom: number, center: [number, number]) {
    this.map.getView().setZoom(zoom);
    this.map.getView().setCenter(fromLonLat(center));
  }

  updateSize(target = 'map') {
    this.map.setTarget(target);
    this.map.updateSize();
  }

  setSource(source: 'osm' | 'stamen') {
    this.layerTile.setSource(this.sources[source]);
  }

  setCarMarker(carId: string, coords: [number, number]) {
    let carIcon = new Feature({
      geometry: new Point(fromLonLat(coords)),
    });

    let vectorLayer = new VectorLayer({
      source: new VectorSource({
        features: [carIcon],
      }),
      style: new Style({
        image: new Icon({
          anchor: [0.5, 0.5],
          scale: [0.07, 0.07],
          src: 'assets/img/car-blue.png',
        }),
      })
    });
    this.activeCarsList.push({ layer: vectorLayer, carId: carId });
    this.acitveCars.next(this.activeCarsList);
    this.map.addLayer(vectorLayer);
  }

  createChargingStationMarker(coords: [number, number][]) {
    let features = []
    coords.forEach(coord => {
      features.push(new Feature({
        geometry: new Point(fromLonLat(coord)),
      }));
    });

    let vectorLayer = new VectorLayer({
      source: new VectorSource({
        features: features,
      }),
      style: new Style({
        image: new Icon({
          anchor: [0.5, 0.5],
          scale: [0.07, 0.07],
          src: 'assets/img/electric-station.svg',
        }),
      })
    });
    this.map.addLayer(vectorLayer);
  }

  createWaypoints(carId: string, waypoints) {
    // console.log(coords)

    let featuresToAdd = []
    waypoints.forEach(wp => {
      featuresToAdd.push(
        new Feature({
          geometry: new Point(fromLonLat([wp.location.longitude, wp.location.latitude])),
        }))
    });

    let lines: { 'start': Waypoint, 'end': Waypoint }[] = []
    if (waypoints.length > 1) {
      // console.log(coords.length)
      for (let i = 0; i < waypoints.length - 1; i++) {
        lines.push({ "start": waypoints[i], "end": waypoints[i + 1] })
      }
    }
    // console.log(lines)

    let lineFeatures = []
    lines.forEach(wp => {
      lineFeatures.push(
        new Feature({
          geometry: new LineString([fromLonLat([wp.start.location.longitude, wp.start.location.latitude]), fromLonLat([wp.end.location.longitude, wp.end.location.latitude])])
        })
      )
    })

    let lineLayer = new VectorLayer({
      source: new VectorSource({
        features: lineFeatures
      }),
      style: new Style({
        stroke: new Stroke({ color: 'black', width: 3 }),
      })
    });



    let vectorLayer = new VectorLayer({
      source: new VectorSource({
        features: featuresToAdd,
      }),
      style: new Style({
        image: new Icon({
          anchor: [0.5, 0.5],
          scale: [0.2, 0.2],
          src: 'assets/img/marker.png',
        }),
      })
    });

    this.map.addLayer(vectorLayer);
    this.map.addLayer(lineLayer);
  }

  createMouseControl() {
    return new MousePosition({
      coordinateFormat: createStringXY(6),
      projection: 'EPSG:4326',
      // comment the following two lines to have the mouse position
      // be placed within the map.
      className: 'custom-mouse-position',
      // target: document.getElementById('mouse-position'),
      undefinedHTML: '&nbsp;',
      // change: function (evt) {
      //   console.log(evt); //or anything to catch the event
      // },
    });
  }


}
