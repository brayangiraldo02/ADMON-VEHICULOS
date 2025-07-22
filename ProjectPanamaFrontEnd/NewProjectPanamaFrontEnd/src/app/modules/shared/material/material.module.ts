import { NgModule } from '@angular/core';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatSortModule} from '@angular/material/sort';
import {MatTableModule} from '@angular/material/table';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import {MatMenuModule} from '@angular/material/menu';
import {MatDialogModule} from '@angular/material/dialog';
import {MatListModule} from '@angular/material/list';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import {MatToolbarModule} from '@angular/material/toolbar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatDividerModule } from '@angular/material/divider';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatNativeDateModule} from '@angular/material/core';
import { ClipboardModule } from '@angular/cdk/clipboard';

const materialModules = [
  MatFormFieldModule, 
  MatInputModule, 
  MatTableModule, 
  MatSortModule, 
  MatPaginatorModule,
  MatButtonModule,
  MatIconModule,
  MatSelectModule,
  MatMenuModule,
  MatDialogModule,
  MatListModule,
  MatProgressBarModule,
  MatSnackBarModule,
  MatToolbarModule,
  MatSidenavModule,
  MatDividerModule,
  MatAutocompleteModule,
  MatNativeDateModule,
  MatDatepickerModule,
  ClipboardModule
]

@NgModule({
  declarations: [],
  imports: [materialModules],
  exports: [materialModules]
})
export class MaterialModule { }
