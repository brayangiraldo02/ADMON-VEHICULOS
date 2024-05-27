import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FeespaidComponent } from './feespaid.component';

describe('FeespaidComponent', () => {
  let component: FeespaidComponent;
  let fixture: ComponentFixture<FeespaidComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FeespaidComponent]
    });
    fixture = TestBed.createComponent(FeespaidComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
