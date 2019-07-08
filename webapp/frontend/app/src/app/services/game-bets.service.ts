import { Injectable, Inject } from '@angular/core';
import { HTTPBase } from './http.abstract';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GameOddsService extends HTTPBase {

  constructor(@Inject(HttpClient) http: HttpClient) {
    super(http, 'games/odds');
  }

  public fetch(queryStrings: object = {}) {
    return this.get(null, queryStrings);
  }

}
