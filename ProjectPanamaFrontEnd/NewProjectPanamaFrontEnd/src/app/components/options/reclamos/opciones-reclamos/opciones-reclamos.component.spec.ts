import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpcionesReclamosComponent } from './opciones-reclamos.component';

describe('OpcionesReclamosComponent', () => {
  let component: OpcionesReclamosComponent;
  let fixture: ComponentFixture<OpcionesReclamosComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OpcionesReclamosComponent]
    });
    fixture = TestBed.createComponent(OpcionesReclamosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
