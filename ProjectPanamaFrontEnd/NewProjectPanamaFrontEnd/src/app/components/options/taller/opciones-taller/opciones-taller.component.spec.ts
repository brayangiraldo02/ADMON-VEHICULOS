import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpcionesTallerComponent } from './opciones-taller.component';

describe('OpcionesTallerComponent', () => {
  let component: OpcionesTallerComponent;
  let fixture: ComponentFixture<OpcionesTallerComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OpcionesTallerComponent]
    });
    fixture = TestBed.createComponent(OpcionesTallerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
