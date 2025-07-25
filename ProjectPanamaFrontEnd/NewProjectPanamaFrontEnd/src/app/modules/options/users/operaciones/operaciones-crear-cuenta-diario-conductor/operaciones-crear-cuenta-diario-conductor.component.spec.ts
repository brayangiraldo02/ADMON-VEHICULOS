import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacionesCrearCuentaDiarioConductorComponent } from './operaciones-crear-cuenta-diario-conductor.component';

describe('OperacionesCrearCuentaDiarioConductorComponent', () => {
  let component: OperacionesCrearCuentaDiarioConductorComponent;
  let fixture: ComponentFixture<OperacionesCrearCuentaDiarioConductorComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacionesCrearCuentaDiarioConductorComponent]
    });
    fixture = TestBed.createComponent(OperacionesCrearCuentaDiarioConductorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
