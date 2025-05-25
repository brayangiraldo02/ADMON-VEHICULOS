import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpcionesGerenciaComponent } from './opciones-gerencia.component';

describe('OpcionesGerenciaComponent', () => {
  let component: OpcionesGerenciaComponent;
  let fixture: ComponentFixture<OpcionesGerenciaComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OpcionesGerenciaComponent]
    });
    fixture = TestBed.createComponent(OpcionesGerenciaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
