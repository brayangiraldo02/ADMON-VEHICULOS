import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CobrosRoutingModule } from './cobros-routing.module';
import { InfoTableComponent } from './components/info-table/info-table.component';
import { AppModule } from 'src/app/app.module';

@NgModule({
  declarations: [
    InfoTableComponent
  ],
  imports: [
    CommonModule,
    CobrosRoutingModule,
    AppModule
  ]
})
export class CobrosModule { }
