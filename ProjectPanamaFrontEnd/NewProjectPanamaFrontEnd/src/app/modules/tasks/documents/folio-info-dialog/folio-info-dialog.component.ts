import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

export interface DialogData {
  documentName: string;
  message: string;
}

@Component({
  selector: 'app-folio-info-dialog',
  templateUrl: './folio-info-dialog.component.html',
  styleUrls: ['./folio-info-dialog.component.css']
})
export class FolioInfoDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: DialogData) {}
}
