import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OwnersPurchasevalueandpiqueraComponent } from './owners-purchasevalueandpiquera.component';

describe('OwnersPurchasevalueandpiqueraComponent', () => {
  let component: OwnersPurchasevalueandpiqueraComponent;
  let fixture: ComponentFixture<OwnersPurchasevalueandpiqueraComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OwnersPurchasevalueandpiqueraComponent]
    });
    fixture = TestBed.createComponent(OwnersPurchasevalueandpiqueraComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
