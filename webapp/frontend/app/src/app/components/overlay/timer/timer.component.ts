import { Component, OnInit } from '@angular/core';
import { Observable, timer, Subscription, interval } from 'rxjs';
import { take, map } from 'rxjs/operators';

@Component({
  selector: 'app-timer',
  template: `<h2>{{counter | async}}</h2>`,
  styles: [`h2{color:black}`]
})
export class TimerComponent implements OnInit {

  private future: Date;
  private futureString: string;
  private diff: number;
  private $counter: Observable<number>;
  private subscription: Subscription;
  private message: string;

  constructor() {
    this.$counter = interval(1000).pipe(
      map((x) => {
        this.diff = Math.floor((this.future.getTime() - new Date().getTime()) / 1000);
        return x;
      })
    )
  }

  ngOnInit() {
  }

}
