import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacionesContratoDeclaracionJuradaComponent } from './operaciones-contrato-declaracion-jurada.component';

describe('OperacionesContratoDeclaracionJuradaComponent', () => {
  let component: OperacionesContratoDeclaracionJuradaComponent;
  let fixture: ComponentFixture<OperacionesContratoDeclaracionJuradaComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacionesContratoDeclaracionJuradaComponent]
    });
    fixture = TestBed.createComponent(OperacionesContratoDeclaracionJuradaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
