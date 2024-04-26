import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BodyworkComponent } from './bodywork.component';

describe('BodyworkComponent', () => {
  let component: BodyworkComponent;
  let fixture: ComponentFixture<BodyworkComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BodyworkComponent]
    });
    fixture = TestBed.createComponent(BodyworkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
