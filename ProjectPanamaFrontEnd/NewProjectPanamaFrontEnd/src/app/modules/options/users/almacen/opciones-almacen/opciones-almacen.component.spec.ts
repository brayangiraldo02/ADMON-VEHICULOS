import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpcionesAlmacenComponent } from './opciones-almacen.component';

describe('OpcionesAlmacenComponent', () => {
  let component: OpcionesAlmacenComponent;
  let fixture: ComponentFixture<OpcionesAlmacenComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OpcionesAlmacenComponent]
    });
    fixture = TestBed.createComponent(OpcionesAlmacenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
