import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-info',
  template: `
  <div id="panel-1" class="panel">
    <div class="panel-container show">
        <div class="panel-content">
        <i class="fa fa-twitch fa-5x" style="color: #6441a4"></i>  <span class="info-item">https://www.twitch.tv/observerurf</span><br>
        <i class="fa fa-keyboard-o fa-5x"></i><span class="info-item" style="margin-left: -5px;">New here? !commands</span><br>
        <i class="fa fa-globe fa-5x"></i><span class="info-item" style="margin-left: 13px;">https://www.observerurf.com </span><br>
        </div>
    </div>
  </div>
  `,
  styles: [`
    .info-item{
      font-size: 2.25em;
      padding: 1em;
      position: absolute;
      margin-top: -17px;
    }
  `]
})
export class InfoComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
