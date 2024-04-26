import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KeyRingComponent } from './key-ring.component';

describe('KeyRingComponent', () => {
  let component: KeyRingComponent;
  let fixture: ComponentFixture<KeyRingComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [KeyRingComponent]
    });
    fixture = TestBed.createComponent(KeyRingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
