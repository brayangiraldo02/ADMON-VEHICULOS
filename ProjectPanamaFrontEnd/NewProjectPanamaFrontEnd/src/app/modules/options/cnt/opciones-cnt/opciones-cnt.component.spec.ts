import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpcionesCntComponent } from './opciones-cnt.component';

describe('OpcionesCntComponent', () => {
  let component: OpcionesCntComponent;
  let fixture: ComponentFixture<OpcionesCntComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OpcionesCntComponent]
    });
    fixture = TestBed.createComponent(OpcionesCntComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
