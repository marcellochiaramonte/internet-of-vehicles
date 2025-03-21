import { Injectable } from '@angular/core';
import { Observable } from 'ol';
import { Subject, Subscriber } from 'rxjs';
import { io } from "socket.io-client";
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {

  socket = io('http://localhost:3000');

  constructor() {
    console.debug('initialized websocket service')
    this.socket.on('data1', (res) => {
      console.debug(res);
    })
  }





}
