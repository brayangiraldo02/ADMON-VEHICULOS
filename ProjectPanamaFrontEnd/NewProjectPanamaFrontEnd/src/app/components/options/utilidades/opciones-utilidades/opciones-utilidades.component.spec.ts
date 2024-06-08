import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpcionesUtilidadesComponent } from './opciones-utilidades.component';

describe('OpcionesUtilidadesComponent', () => {
  let component: OpcionesUtilidadesComponent;
  let fixture: ComponentFixture<OpcionesUtilidadesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OpcionesUtilidadesComponent]
    });
    fixture = TestBed.createComponent(OpcionesUtilidadesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
