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
import { SlideshowComponent } from './components/postgame/slideshow/slideshow.component';
import { CarouselComponent } from './shared/carousel/carousel.component';
import { CarouselItemDirective } from './shared/carousel/carousel-item.directive';
import { CarouselItemElementDirective } from './shared/carousel/carousel-item-element.directive';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule, MatCheckboxModule, MatIconModule } from '@angular/material';
import { PostgameService } from './services/postgame.service';
import { PostgameStatsResolver } from './components/overlay/postgame-stats.resolver';
import { InfoComponent } from './components/overlay/info/info.component';


export const routes = [

  {
    path: 'overlay',
    // component: LeagueComponent,
    children: [
      {
        path: 'info',
        component: InfoComponent,
      },
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
  {
    path: 'postgame',
    component: SlideshowComponent,
    resolve: {
      stats: PostgameStatsResolver
    }
  }

  // Not found
  // { path: '**', redirectTo: 'my-recipes' }

];

@NgModule({
  declarations: [
    AppComponent,
    LeagueComponent,
    OddsComponent,
    SlideshowComponent,
    CarouselComponent, CarouselItemDirective, CarouselItemElementDirective, InfoComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AppRoutingModule,
    RouterModule.forChild(routes),
    MatIconModule, MatButtonModule, MatCheckboxModule
  ],
  providers: [
    CommonModule,
    LatestGameResolver, LatestGameService,
    PostgameService, PostgameStatsResolver
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
