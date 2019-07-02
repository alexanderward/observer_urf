import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-slideshow',
  templateUrl: './slideshow.component.html',
  styleUrls: ['./slideshow.component.css']
})
export class SlideshowComponent implements OnInit {
  stats = {};
  items = [{ title: 'Slide 1' }, { title: 'Slide 2' }, { title: 'Slide 3' }];
  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.stats = JSON.parse(this.route.snapshot.data.stats.data);
    console.log(this.stats)
  }

}
