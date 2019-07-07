import { Component, OnInit, Injectable, Input } from '@angular/core';
import { interval, timer } from 'rxjs';

@Component({
  selector: 'app-gifs',
  template: `
  <div style="width: 100%; height: 100%;">
    <img src="assets/gifs/t{{gifNumber}}.gif" style="width: 100%; height:100%;">
  </div>
  `,
  styles: [``]
})
export class GifsComponent implements OnInit {
  @Input() timer = 2;
  gifNumber = 0;
  numberOfGifs = 34;
  constructor() { }

  ngOnInit() {
    setInterval(() => {
      this.gifNumber = Math.floor(Math.random() * this.numberOfGifs + 1);
    }, (this.timer + .25) * 1000);
  }

}
