import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Game, GameParticipants } from 'src/app/models/game.model';
export interface Tile {
  color: string;
  cols: number;
  rows: number;
  text: string;
}
@Component({
  selector: 'app-slideshow',
  templateUrl: './slideshow.component.html',
  styleUrls: ['./slideshow.component.css']
})
export class SlideshowComponent implements OnInit {
  game: Game;
  participants: Object[];
  winningTeam = "";
  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    console.log(this.route.snapshot.data)
    this.game = this.route.snapshot.data.data.game;
    this.game.postgame.data = JSON.parse(this.game.postgame.data);
    let spells = {};
    Object.keys(this.route.snapshot.data.data.spells.data).forEach(key => {
      spells[this.route.snapshot.data.data.spells.data[key].key] = key;
    })

    let items = this.route.snapshot.data.data.items;
    let winningTeam = this.game.postgame.data.teams.find(team => team.win == "Win").teamId;
    this.participants = this.game.postgame.data.participants.map(participant => {
      participant.player = this.game.postgame.data.participantIdentities.find(x => x.participantId == participant.participantId).player;
      participant.champion = this.game.game_participants.find(x => x.summoner_name == participant.player.summonerName) || "Ashe";
      participant.won = participant.teamId == winningTeam;
      const spell1 = spells[participant.spell1Id];
      const spell2 = spells[participant.spell2Id];
      participant.spell1 = `https://ddragon.leagueoflegends.com/cdn/${this.game.version}/img/spell/${spell1}.png`
      participant.spell2 = `https://ddragon.leagueoflegends.com/cdn/${this.game.version}/img/spell/${spell2}.png`
      participant.championSquare = `https://ddragon.leagueoflegends.com/cdn/${this.game.version}/img/champion/${participant.champion}.png`
      participant.items = ["item0", "item1", "item2", "item3", "item4", "item5"].map(item => {
        return participant.stats[item] > 0 ? `https://ddragon.leagueoflegends.com/cdn/${this.game.version}/img/item/${participant.stats[item]}.png` : null;
      });
      participant.wardItem = participant.stats.item6 > 0 ? `https://ddragon.leagueoflegends.com/cdn/${this.game.version}/img/item/${participant.stats.item6}.png` : null;
      if (participant.stats.deaths === 0) {
        participant.kda = "Perfect";
      } else {
        participant.kda = ((participant.stats.kills + participant.stats.assists) / participant.stats.deaths).toFixed(2);
      }

      return participant
    });
    if (winningTeam == 200) {
      this.winningTeam = "Red"
    } else {
      this.winningTeam = "Blue"
    }

    console.log(this.game)
    console.log(this.participants)
  }

}
