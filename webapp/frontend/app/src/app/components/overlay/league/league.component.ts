import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Game, League } from 'src/app/models/game.model';

@Component({
  selector: 'app-league',
  template: `
  <img [src]="imagePath" class="center">
  <h2 class="center large-text">{{league | titlecase}}</h2>
  `,
  styles: [`
    .large-text{
      font-size: 4.5em;
      color: #edac1e;
      text-align: center;
      padding: .15em;
      margin-top: 0em;
    }
  `]
})
export class LeagueComponent implements OnInit {
  constructor(private route: ActivatedRoute) { }

  imagePath: string;
  league: string;
  ngOnInit() {
    let game: Game = this.route.snapshot.data.game as Game;
    this.league = game.league;
    switch (game.league) {
      case League.GRANDMASTER:
        this.imagePath = "assets/Emblem_Grandmaster.png";
        break;
      case League.CHALLENGER:
        this.imagePath = "assets/Emblem_Challenger.png";
        break;
      case League.MASTER:
        this.imagePath = "assets/Emblem_Master.png";
        break;
      case League.DIAMOND:
        this.imagePath = "assets/Emblem_Diamond.png";
        break;
      case League.PLATINUM:
        this.imagePath = "assets/Emblem_Platinum.png";
        break;
      case League.GOLD:
        this.imagePath = "assets/Emblem_Gold.png";
        break;
      case League.SILVER:
        this.imagePath = "assets/Emblem_Silver.png";
        break;
      case League.BRONZE:
        this.imagePath = "assets/Emblem_Bronze.png";
        break;
      case League.IRON:
        this.imagePath = "assets/Emblem_Iron.png";
        break;
      default:
        break;
    }
  }

}
