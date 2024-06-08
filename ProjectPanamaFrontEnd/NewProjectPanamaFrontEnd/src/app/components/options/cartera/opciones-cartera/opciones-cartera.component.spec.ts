import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpcionesCarteraComponent } from './opciones-cartera.component';

describe('OpcionesCarteraComponent', () => {
  let component: OpcionesCarteraComponent;
  let fixture: ComponentFixture<OpcionesCarteraComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OpcionesCarteraComponent]
    });
    fixture = TestBed.createComponent(OpcionesCarteraComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
