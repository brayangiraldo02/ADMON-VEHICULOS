import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OwnersFeespaidComponent } from './components/owners-feespaid/owners-feespaid.component';
import { OwnersPandgstatusUnitsComponent } from './components/pandgstatus/owners-pandgstatus-units/owners-pandgstatus-units.component';
import { OwnersPartsrelationshipComponent } from './components/owners-partsrelationship/owners-partsrelationship.component';
import { OwnersPurchasevalueandpiqueraComponent } from './components/owners-purchasevalueandpiquera/owners-purchasevalueandpiquera.component';
import { OwnersRelationshiprevenuesComponent } from './components/owners-relationshiprevenues/owners-relationshiprevenues.component';
import { OwnersStatusfleetdetailComponent } from './components/owners-statusfleetdetail/owners-statusfleetdetail.component';
import { OwnersStatusfleetsummaryComponent } from './components/owners-statusfleetsummary/owners-statusfleetsummary.component';
import { OwnersRelationshiprevenuesgeneralComponent } from './components/owners-relationshiprevenuesgeneral/owners-relationshiprevenuesgeneral.component';
import { OwnersPandgstatusOptionsDialogComponent } from './components/pandgstatus/owners-pandgstatus-options-dialog/owners-pandgstatus-options-dialog.component';
import { MaterialModule } from '../../shared/material/material.module';
import { OwnersPandgstatusGeneralComponent } from './components/pandgstatus/owners-pandgstatus-general/owners-pandgstatus-general.component';

@NgModule({
  declarations: [
    OwnersFeespaidComponent,
    OwnersPandgstatusUnitsComponent,
    OwnersPartsrelationshipComponent,
    OwnersPurchasevalueandpiqueraComponent,
    OwnersRelationshiprevenuesComponent,
    OwnersStatusfleetdetailComponent,
    OwnersStatusfleetsummaryComponent,
    OwnersRelationshiprevenuesgeneralComponent,
    OwnersPandgstatusOptionsDialogComponent,
    OwnersPandgstatusGeneralComponent,
  ],
  imports: [CommonModule, MaterialModule],
  exports: [
    OwnersFeespaidComponent,
    OwnersPandgstatusUnitsComponent,
    OwnersPandgstatusGeneralComponent,
    OwnersPartsrelationshipComponent,
    OwnersPurchasevalueandpiqueraComponent,
    OwnersRelationshiprevenuesComponent,
    OwnersRelationshiprevenuesgeneralComponent,
    OwnersStatusfleetdetailComponent,
    OwnersStatusfleetsummaryComponent,
  ],
})
export class OwnersModule {}
