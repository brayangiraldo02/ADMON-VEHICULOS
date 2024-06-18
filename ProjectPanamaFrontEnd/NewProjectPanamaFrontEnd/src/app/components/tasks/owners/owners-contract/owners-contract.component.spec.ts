import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OwnersContractComponent } from './owners-contract.component';

describe('OwnersContractComponent', () => {
  let component: OwnersContractComponent;
  let fixture: ComponentFixture<OwnersContractComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OwnersContractComponent]
    });
    fixture = TestBed.createComponent(OwnersContractComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
