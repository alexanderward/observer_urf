import { Injectable, Inject } from '@angular/core';
import { HTTPBase } from './http.abstract';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PostgameService extends HTTPBase {

  constructor(@Inject(HttpClient) http: HttpClient) {
    super(http, 'games');
  }

  public fetch(id: number, queryStrings: object = {}) {
    return this.get(`${id}/postgame`, queryStrings);
  }

}
