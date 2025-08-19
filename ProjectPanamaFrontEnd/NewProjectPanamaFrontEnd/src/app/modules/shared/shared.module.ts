import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { InfoCompanyComponent } from './components/info-company/info-company.component';
import { FormsModule } from '@angular/forms';
import { MaterialModule } from './material/material.module';
import { ConfirmActionDialogComponent } from './components/confirm-action-dialog/confirm-action-dialog.component';

@NgModule({
  declarations: [
    InfoCompanyComponent,
    ConfirmActionDialogComponent,
  ],
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    MaterialModule
  ],
  exports: [
  ]
})
export class SharedModule { }
