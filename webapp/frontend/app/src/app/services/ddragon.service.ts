import { Injectable, Inject } from '@angular/core';
import { HTTPBase } from './http.abstract';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DdragonService extends HTTPBase {

  constructor(@Inject(HttpClient) http: HttpClient) {
    super(http, 'games/latest');
  }

  public items(version: string) {
    return this.get(`https://ddragon.leagueoflegends.com/cdn/${version}/data/en_US/item.json`, {}, true);
  }

  public summonerSpells(version: string) {
    return this.get(`https://ddragon.leagueoflegends.com/cdn/${version}/data/en_US/summoner.json`, {}, true);
  }

}
