import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpcionesChapisteriaComponent } from './opciones-chapisteria.component';

describe('OpcionesChapisteriaComponent', () => {
  let component: OpcionesChapisteriaComponent;
  let fixture: ComponentFixture<OpcionesChapisteriaComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OpcionesChapisteriaComponent]
    });
    fixture = TestBed.createComponent(OpcionesChapisteriaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
