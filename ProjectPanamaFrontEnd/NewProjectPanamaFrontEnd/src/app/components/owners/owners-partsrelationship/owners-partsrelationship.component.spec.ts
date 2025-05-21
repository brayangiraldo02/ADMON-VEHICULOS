import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OwnersPartsrelationshipComponent } from './owners-partsrelationship.component';

describe('OwnersPartsrelationshipComponent', () => {
  let component: OwnersPartsrelationshipComponent;
  let fixture: ComponentFixture<OwnersPartsrelationshipComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OwnersPartsrelationshipComponent]
    });
    fixture = TestBed.createComponent(OwnersPartsrelationshipComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
