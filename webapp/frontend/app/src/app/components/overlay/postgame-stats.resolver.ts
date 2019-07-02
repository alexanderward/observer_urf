import { Injectable } from '@angular/core';
import { Resolve, ActivatedRouteSnapshot } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { map, mergeMap } from 'rxjs/operators';
import { LatestGameService } from 'src/app/services/latest-game.service';
import { Game } from 'src/app/models/game.model';
import { PostgameService } from 'src/app/services/postgame.service';

@Injectable()
export class PostgameStatsResolver implements Resolve<any> {
    constructor(private postgameService: PostgameService, private latestGameService: LatestGameService, private http: HttpClient) { }

    resolve(route: ActivatedRouteSnapshot) {
        return this.latestGameService.fetch().pipe(mergeMap((game: Game) => {
            return this.postgameService.fetch(+game.id);
        }))
        
    }
}