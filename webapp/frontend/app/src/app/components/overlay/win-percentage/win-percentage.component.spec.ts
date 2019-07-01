import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WinPercentageComponent } from './win-percentage.component';

describe('WinPercentageComponent', () => {
  let component: WinPercentageComponent;
  let fixture: ComponentFixture<WinPercentageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WinPercentageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WinPercentageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
