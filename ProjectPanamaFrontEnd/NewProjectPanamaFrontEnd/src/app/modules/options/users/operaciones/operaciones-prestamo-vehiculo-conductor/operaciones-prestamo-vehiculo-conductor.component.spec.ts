import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacionesPrestamoVehiculoConductorComponent } from './operaciones-prestamo-vehiculo-conductor.component';

describe('OperacionesPrestamoVehiculoConductorComponent', () => {
  let component: OperacionesPrestamoVehiculoConductorComponent;
  let fixture: ComponentFixture<OperacionesPrestamoVehiculoConductorComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacionesPrestamoVehiculoConductorComponent]
    });
    fixture = TestBed.createComponent(OperacionesPrestamoVehiculoConductorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
