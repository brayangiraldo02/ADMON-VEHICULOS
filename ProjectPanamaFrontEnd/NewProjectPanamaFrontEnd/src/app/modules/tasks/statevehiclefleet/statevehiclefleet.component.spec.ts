import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatevehiclefleetComponent } from './statevehiclefleet.component';

describe('StatevehiclefleetComponent', () => {
  let component: StatevehiclefleetComponent;
  let fixture: ComponentFixture<StatevehiclefleetComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [StatevehiclefleetComponent]
    });
    fixture = TestBed.createComponent(StatevehiclefleetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
