import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacionesCambiarPatioVehiculoComponent } from './operaciones-cambiar-patio-vehiculo.component';

describe('OperacionesCambiarPatioVehiculoComponent', () => {
  let component: OperacionesCambiarPatioVehiculoComponent;
  let fixture: ComponentFixture<OperacionesCambiarPatioVehiculoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacionesCambiarPatioVehiculoComponent]
    });
    fixture = TestBed.createComponent(OperacionesCambiarPatioVehiculoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
