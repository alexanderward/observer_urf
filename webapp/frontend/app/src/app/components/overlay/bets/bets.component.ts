import { Component, OnInit, OnDestroy } from '@angular/core';
import { GameOddsService } from 'src/app/services/game-bets.service';
import { Subject, timer, interval } from 'rxjs';
import { takeUntil, switchMap } from 'rxjs/operators';
import { ActivatedRoute } from '@angular/router';
import { Game } from 'src/app/models/game.model';
import { isNull } from 'util';

@Component({
  selector: 'app-bets',
  templateUrl: './bets.component.html',
  styleUrls: ['./bets.component.css']
})
export class BetsComponent implements OnInit, OnDestroy {
  red = 0;
  blue = 0;
  unsubscribe = new Subject();

  redPercentage = 50;
  bluePercentage = 50;
  stopPollingMinutes = 3.5;
  intervalTime = 3000;
  timeSoFar = 0;
  constructor(private gameOddsService: GameOddsService, private route: ActivatedRoute) { }

  ngOnInit() {
    let game: Game = this.route.snapshot.data.game as Game;
    if (!isNull(game)) {
      interval(this.intervalTime).pipe(
        takeUntil(this.unsubscribe),
        switchMap(() => this.gameOddsService.fetch())
      ).subscribe(data => {
        this.timeSoFar += this.intervalTime;
        this.red = data['total']['red'];
        this.blue = data['total']['blue'];
        this.redPercentage = data['percentage']['red'];
        this.bluePercentage = data['percentage']['blue'];
        if (this.timeSoFar >= this.stopPollingMinutes * 1000 * 60) {
          this.unsubscribe.next();
        }
      })
    }

  }

  ngOnDestroy() {
    this.unsubscribe.next();
  }

}
