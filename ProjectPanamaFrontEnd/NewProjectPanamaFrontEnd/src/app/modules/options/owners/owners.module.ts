import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OwnersFeespaidComponent } from './components/owners-feespaid/owners-feespaid.component';
import { OwnersPandgstatusComponent } from './components/owners-pandgstatus/owners-pandgstatus.component';
import { OwnersPartsrelationshipComponent } from './components/owners-partsrelationship/owners-partsrelationship.component';
import { OwnersPurchasevalueandpiqueraComponent } from './components/owners-purchasevalueandpiquera/owners-purchasevalueandpiquera.component';
import { OwnersRelationshiprevenuesComponent } from './components/owners-relationshiprevenues/owners-relationshiprevenues.component';
import { OwnersStatusfleetdetailComponent } from './components/owners-statusfleetdetail/owners-statusfleetdetail.component';
import { OwnersStatusfleetsummaryComponent } from './components/owners-statusfleetsummary/owners-statusfleetsummary.component';
import { ReactiveFormsModule } from '@angular/forms';
import { OwnersRelationshiprevenuesgeneralComponent } from './components/owners-relationshiprevenuesgeneral/owners-relationshiprevenuesgeneral.component';



@NgModule({
  declarations: [
    OwnersFeespaidComponent,
    OwnersPandgstatusComponent,
    OwnersPartsrelationshipComponent,
    OwnersPurchasevalueandpiqueraComponent,
    OwnersRelationshiprevenuesComponent,
    OwnersStatusfleetdetailComponent,
    OwnersStatusfleetsummaryComponent,
    OwnersRelationshiprevenuesgeneralComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  exports: [
    OwnersFeespaidComponent,
    OwnersPandgstatusComponent,
    OwnersPartsrelationshipComponent,
    OwnersPurchasevalueandpiqueraComponent,
    OwnersRelationshiprevenuesComponent,
    OwnersRelationshiprevenuesgeneralComponent,
    OwnersStatusfleetdetailComponent,
    OwnersStatusfleetsummaryComponent
  ]
})
export class OwnersModule { }
