import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Game, Team } from 'src/app/models/game.model';
import { isUndefined } from 'util';

@Component({
  selector: 'app-odds',
  template: `


  <div id="panel-1" class="panel">
      <div class="panel-hdr">
          <h2 class="panel-tag" [ngClass]="team_id == '200' ? 'red': 'blue'">
              Odds <span class="fw-300"></span>
          </h2>
      </div>
      <div class="panel-container show">
          <div class="panel-content">
            <div class="stats">{{odds}}%</div>
          </div>
      </div>
  </div>
  
  `,
  styles: [
    `

    `],
  encapsulation: ViewEncapsulation.None
})
export class OddsComponent implements OnInit {
  odds = "N/A";
  team_id;
  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    let game: Game = this.route.snapshot.data.game as Game;
    this.team_id = this.route.snapshot.params['team_id'];
    let team: Team = game.teams.find(x=>x.team_id == this.team_id);
    if(!isUndefined(team)){
      const sum: number = +game.teams.map(x=>x.win_rate).reduce((sum, x) => sum + x);
      this.odds = (+team.win_rate*100/sum).toFixed(2);
    }
  }

}
