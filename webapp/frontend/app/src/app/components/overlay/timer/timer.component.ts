import { Component, OnInit, Input } from '@angular/core';
import { interval } from 'rxjs';
import { take, map } from 'rxjs/operators';
import { ActivatedRoute } from '@angular/router';
import { Game } from 'src/app/models/game.model';
import { isNull } from 'util';

@Component({
  selector: 'app-timer',
  template: `<div class="panel align-items-center justify-content-center">
  <div class="panel-container show">
      <div class="panel-content">
        <div *ngIf="!error">
          <h2 *ngIf="counter != 0">{{message}} {{countDown | async | formatTime}}</h2>
          <h2 *ngIf="counter == 0">{{postmessage}}</h2>
        </div>
        <div *ngIf="error"><h2>An error occurred.  Swimming over to the dev to fix issue.</h2></div>
      </div>
  </div>
</div>`,
  styles: [`h2{
    font-size: -webkit-xxx-large;
  }`]
})
export class TimerComponent implements OnInit {
  message;
  postmessage;
  countDown;
  hideIfError = true;
  error = false;
  counter = 3 * 60;
  tick = 1000;

  constructor(private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      this.message = params['message'];
      this.postmessage = params['postmessage'];
      this.hideIfError = params['hideIfError'];
    });
  }

  ngOnInit() {
    let game: Game = this.route.snapshot.data.game as Game;
    if (isNull(game) && this.hideIfError) {
      this.error = true;
    }
    this.countDown = interval(this.tick).pipe(
      take(this.counter),
      map(() => --this.counter)
    )
  }

}
