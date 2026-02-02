import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VehicleRepairRoutingModule } from './vehicle-repair-routing.module';
import { TableVehicleRepairComponent } from './components/table-vehicle-repair/table-vehicle-repair.component';
import { MaterialModule } from '../../shared/material/material.module';

@NgModule({
  declarations: [TableVehicleRepairComponent],
  imports: [CommonModule, VehicleRepairRoutingModule, MaterialModule],
})
export class VehicleRepairModule {}
