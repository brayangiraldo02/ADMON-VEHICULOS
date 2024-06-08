import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpcionesOperacionesComponent } from './opciones-operaciones.component';

describe('OpcionesOperacionesComponent', () => {
  let component: OpcionesOperacionesComponent;
  let fixture: ComponentFixture<OpcionesOperacionesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OpcionesOperacionesComponent]
    });
    fixture = TestBed.createComponent(OpcionesOperacionesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
