import { Injectable } from '@angular/core';
import { Resolve, ActivatedRouteSnapshot } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { LatestGameService } from 'src/app/services/latest-game.service';
import { Game } from 'src/app/models/game.model';

@Injectable()
export class LatestGameResolver implements Resolve<any> {
    constructor(private latestGameService: LatestGameService, private http: HttpClient) { }

    resolve(route: ActivatedRouteSnapshot) {
        return this.latestGameService.list();
    }
}