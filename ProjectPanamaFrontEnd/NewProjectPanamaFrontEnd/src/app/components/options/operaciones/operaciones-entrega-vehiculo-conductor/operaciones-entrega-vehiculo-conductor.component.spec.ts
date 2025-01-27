import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacionesEntregaVehiculoConductorComponent } from './operaciones-entrega-vehiculo-conductor.component';

describe('OperacionesEntregaVehiculoConductorComponent', () => {
  let component: OperacionesEntregaVehiculoConductorComponent;
  let fixture: ComponentFixture<OperacionesEntregaVehiculoConductorComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacionesEntregaVehiculoConductorComponent]
    });
    fixture = TestBed.createComponent(OperacionesEntregaVehiculoConductorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
