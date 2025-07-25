import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacionesCambiarEstadoVehiculoComponent } from './operaciones-cambiar-estado-vehiculo.component';

describe('OperacionesCambiarEstadoVehiculoComponent', () => {
  let component: OperacionesCambiarEstadoVehiculoComponent;
  let fixture: ComponentFixture<OperacionesCambiarEstadoVehiculoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacionesCambiarEstadoVehiculoComponent]
    });
    fixture = TestBed.createComponent(OperacionesCambiarEstadoVehiculoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
