import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoVehicleDialogComponent } from './info-vehicle-dialog.component';

describe('InfoVehicleDialogComponent', () => {
  let component: InfoVehicleDialogComponent;
  let fixture: ComponentFixture<InfoVehicleDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InfoVehicleDialogComponent]
    });
    fixture = TestBed.createComponent(InfoVehicleDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
