import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { VehiclesRoutingModule } from './vehicles-routing.module';
import { MaterialModule } from 'src/app/modules/shared/material/material.module';
import { VehiclesTableComponent } from './components/vehicles-table/vehicles-table.component';


@NgModule({
  declarations: [
    VehiclesTableComponent
  ],
  imports: [
    CommonModule,
    VehiclesRoutingModule,
    MaterialModule
  ]
})
export class VehiclesModule { }
