import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FolioInfoDialogComponent } from './folio-info-dialog.component';

describe('FolioInfoDialogComponent', () => {
  let component: FolioInfoDialogComponent;
  let fixture: ComponentFixture<FolioInfoDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FolioInfoDialogComponent]
    });
    fixture = TestBed.createComponent(FolioInfoDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
