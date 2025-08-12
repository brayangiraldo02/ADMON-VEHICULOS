import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacionesDevolucionVehiculoPrestadoComponent } from './operaciones-devolucion-vehiculo-prestado.component';

describe('OperacionesDevolucionVehiculoPrestadoComponent', () => {
  let component: OperacionesDevolucionVehiculoPrestadoComponent;
  let fixture: ComponentFixture<OperacionesDevolucionVehiculoPrestadoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacionesDevolucionVehiculoPrestadoComponent]
    });
    fixture = TestBed.createComponent(OperacionesDevolucionVehiculoPrestadoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
