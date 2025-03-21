import { Component, OnInit } from '@angular/core';
import { WebsocketService } from 'src/app/service/websocket.service';

@Component({
  selector: 'app-live-data',
  templateUrl: './live-data.component.html',
  styleUrls: ['./live-data.component.scss']
})
export class LiveDataComponent implements OnInit {

  // constructor(private websocketService: WebsocketService) { }

  ngOnInit(): void {
  }

}
