import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LeagueComponent } from './components/overlay/league/league.component';
import { OddsComponent } from './components/overlay/odds/odds.component';
import { RouterModule } from '@angular/router';
import { LatestGameService } from './services/latest-game.service';
import { LatestGameResolver } from './components/overlay/latest-game.resolver';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

export const routes = [

  {
      path: 'overlay',
      // component: LeagueComponent,
      children: [
          {
              path: 'league',
              component: LeagueComponent,
              resolve: { game: LatestGameResolver }
          },
          {
            path: 'odds/:team_id',
            component: OddsComponent,
            resolve: { game: LatestGameResolver }
        },
      ]
  },

  // Not found
  // { path: '**', redirectTo: 'my-recipes' }

];

@NgModule({
  declarations: [
    AppComponent,
    LeagueComponent,
    OddsComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    RouterModule.forChild(routes)
  ],
  providers: [
    CommonModule,
    LatestGameResolver,
    LatestGameService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
