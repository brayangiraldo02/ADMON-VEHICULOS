import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VehiclesDocumentsComponent } from './vehicles-documents.component';

describe('VehiclesDocumentsComponent', () => {
  let component: VehiclesDocumentsComponent;
  let fixture: ComponentFixture<VehiclesDocumentsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [VehiclesDocumentsComponent]
    });
    fixture = TestBed.createComponent(VehiclesDocumentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
