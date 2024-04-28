import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardsStatusComponent } from './cards-status.component';

describe('CardsStatusComponent', () => {
  let component: CardsStatusComponent;
  let fixture: ComponentFixture<CardsStatusComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CardsStatusComponent]
    });
    fixture = TestBed.createComponent(CardsStatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
