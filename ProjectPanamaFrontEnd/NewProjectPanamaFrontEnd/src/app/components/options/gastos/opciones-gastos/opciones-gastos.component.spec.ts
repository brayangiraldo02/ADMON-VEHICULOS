import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpcionesGastosComponent } from './opciones-gastos.component';

describe('OpcionesGastosComponent', () => {
  let component: OpcionesGastosComponent;
  let fixture: ComponentFixture<OpcionesGastosComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OpcionesGastosComponent]
    });
    fixture = TestBed.createComponent(OpcionesGastosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
