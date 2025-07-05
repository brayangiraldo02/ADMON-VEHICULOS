import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpcionesLlaveroComponent } from './opciones-llavero.component';

describe('OpcionesLlaveroComponent', () => {
  let component: OpcionesLlaveroComponent;
  let fixture: ComponentFixture<OpcionesLlaveroComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OpcionesLlaveroComponent]
    });
    fixture = TestBed.createComponent(OpcionesLlaveroComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
