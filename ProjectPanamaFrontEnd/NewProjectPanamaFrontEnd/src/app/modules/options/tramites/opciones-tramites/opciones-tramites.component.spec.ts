import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpcionesTramitesComponent } from './opciones-tramites.component';

describe('OpcionesTramitesComponent', () => {
  let component: OpcionesTramitesComponent;
  let fixture: ComponentFixture<OpcionesTramitesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OpcionesTramitesComponent]
    });
    fixture = TestBed.createComponent(OpcionesTramitesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
