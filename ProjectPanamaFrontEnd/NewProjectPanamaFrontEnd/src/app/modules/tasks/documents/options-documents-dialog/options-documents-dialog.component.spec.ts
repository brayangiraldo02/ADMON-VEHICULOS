import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OptionsDocumentsDialogComponent } from './options-documents-dialog.component';

describe('OptionsDocumentsDialogComponent', () => {
  let component: OptionsDocumentsDialogComponent;
  let fixture: ComponentFixture<OptionsDocumentsDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OptionsDocumentsDialogComponent]
    });
    fixture = TestBed.createComponent(OptionsDocumentsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
