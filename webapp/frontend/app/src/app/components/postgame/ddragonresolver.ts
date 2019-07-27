import { Injectable } from '@angular/core';
import { Resolve, ActivatedRouteSnapshot } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { map, mergeMap, catchError } from 'rxjs/operators';
import { LatestGameService } from 'src/app/services/latest-game.service';
import { Game } from 'src/app/models/game.model';
import { DdragonService } from 'src/app/services/ddragon.service';
import { forkJoin, of } from 'rxjs';
import { isNull } from 'util';

@Injectable()
export class PostGameResolver implements Resolve<any> {
    constructor(private latestGameService: LatestGameService, private ddragonService: DdragonService, private http: HttpClient) { }

    resolve(route: ActivatedRouteSnapshot) {
        let currentGame = null;
        return this.latestGameService.fetch(route.data ? route.data: null).pipe(
            catchError(x => of(null)),
            mergeMap((game: any) => {
                if(isNull(game)){
                    return of([null, null])
                }
                currentGame = game;
                return forkJoin([this.ddragonService.summonerSpells(game.version), this.ddragonService.items(game.version)]);
            }),
            map((results)=>{
                return {"spells": results[0], "items": results[1], "game": currentGame}
            })
        );

    }
}