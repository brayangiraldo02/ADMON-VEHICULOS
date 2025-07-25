import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DriversDocumentsComponent } from './drivers-documents.component';

describe('DriversDocumentsComponent', () => {
  let component: DriversDocumentsComponent;
  let fixture: ComponentFixture<DriversDocumentsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DriversDocumentsComponent]
    });
    fixture = TestBed.createComponent(DriversDocumentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
