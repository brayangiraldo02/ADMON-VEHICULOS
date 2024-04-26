import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FinancialBoxComponent } from './financial-box.component';

describe('FinancialBoxComponent', () => {
  let component: FinancialBoxComponent;
  let fixture: ComponentFixture<FinancialBoxComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FinancialBoxComponent]
    });
    fixture = TestBed.createComponent(FinancialBoxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
