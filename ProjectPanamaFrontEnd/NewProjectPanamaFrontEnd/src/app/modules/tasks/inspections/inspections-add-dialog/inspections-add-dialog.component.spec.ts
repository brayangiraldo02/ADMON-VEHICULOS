import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InspectionsAddDialogComponent } from './inspections-add-dialog.component';

describe('InspectionsAddDialogComponent', () => {
  let component: InspectionsAddDialogComponent;
  let fixture: ComponentFixture<InspectionsAddDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InspectionsAddDialogComponent]
    });
    fixture = TestBed.createComponent(InspectionsAddDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
