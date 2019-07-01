import { Injectable, Inject } from '@angular/core';
import { HTTPBase } from './http.abstract';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LatestGameService extends HTTPBase {

  constructor(@Inject(HttpClient) http: HttpClient) {
    super(http, 'games/latest');
  }

  public list(queryStrings: object = {}) {
    return this.get(null, queryStrings);
  }

}
