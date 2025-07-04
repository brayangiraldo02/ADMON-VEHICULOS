import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LoginComponent } from './modules/users/login/login.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { StatevehiclefleetComponent } from './modules/tasks/statevehiclefleet/statevehiclefleet.component';
import { PdfViewerComponent } from './modules/others/pdf-viewer/pdf-viewer.component';
import { FeespaidComponent } from './modules/tasks/feespaid/feespaid.component';
import { OpcionesGerenciaComponent } from './modules/options/users/gerencia/opciones-gerencia/opciones-gerencia.component';
import { OpcionesTramitesComponent } from './modules/options/users/tramites/opciones-tramites/opciones-tramites.component';
import { OpcionesChapisteriaComponent } from './modules/options/users/chapisteria/opciones-chapisteria/opciones-chapisteria.component';
import { OpcionesGastosComponent } from './modules/options/users/gastos/opciones-gastos/opciones-gastos.component';
import { OpcionesTallerComponent } from './modules/options/users/taller/opciones-taller/opciones-taller.component';
import { OpcionesOperacionesComponent } from './modules/options/users/operaciones/opciones-operaciones/opciones-operaciones.component';
import { OpcionesLlaveroComponent } from './modules/options/users/llavero/opciones-llavero/opciones-llavero.component';
import { OpcionesReclamosComponent } from './modules/options/users/reclamos/opciones-reclamos/opciones-reclamos.component';
import { OpcionesCntComponent } from './modules/options/users/cnt/opciones-cnt/opciones-cnt.component';
import { OpcionesUtilidadesComponent } from './modules/options/users/utilidades/opciones-utilidades/opciones-utilidades.component';
import { OpcionesCarteraComponent } from './modules/options/users/cartera/opciones-cartera/opciones-cartera.component';
import { OpcionesAlmacenComponent } from './modules/options/users/almacen/opciones-almacen/opciones-almacen.component';
import { OwnersTableComponent } from './modules/tasks/owners/owners-table/owners-table.component';
import { OwnersVehiclesComponent } from './modules/tasks/owners/owners-vehicles/owners-vehicles.component';
import { OwnersResumeComponent } from './modules/tasks/owners/owners-resume/owners-resume.component';
import { OwnersAddnewComponent } from './modules/tasks/owners/owners-addnew/owners-addnew.component';
import { OwnersReportsComponent } from './modules/tasks/owners/owners-reports/owners-reports.component';
import { OwnersDeleteComponent } from './modules/tasks/owners/owners-delete/owners-delete.component';
import { DriversTableComponent } from './modules/tasks/drivers/drivers-table/drivers-table.component';
import { DriversResumeComponent } from './modules/tasks/drivers/drivers-resume/drivers-resume.component';
import { DriversDeleteComponent } from './modules/tasks/drivers/drivers-delete/drivers-delete.component';
import { DriversAddnewComponent } from './modules/tasks/drivers/drivers-addnew/drivers-addnew.component';
import { VehiclesTableComponent } from './modules/tasks/vehicles/vehicles-table/vehicles-table.component';
import { VehiclesResumeComponent } from './modules/tasks/vehicles/vehicles-resume/vehicles-resume.component';
import { VehiclesDeleteComponent } from './modules/tasks/vehicles/vehicles-delete/vehicles-delete.component';
import { VehiclesAddnewComponent } from './modules/tasks/vehicles/vehicles-addnew/vehicles-addnew.component';
import { VehiclesDocumentationComponent } from './modules/tasks/vehicles/vehicles-documentation/vehicles-documentation.component';
import { DriversDocumentationComponent } from './modules/tasks/drivers/drivers-documentation/drivers-documentation.component';
import { OperacionesEntregaVehiculoConductorComponent } from './modules/options/users/operaciones/operaciones-entrega-vehiculo-conductor/operaciones-entrega-vehiculo-conductor.component';
import { SharedModule } from './modules/shared/shared.module';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    StatevehiclefleetComponent,
    PdfViewerComponent,
    FeespaidComponent,
    OpcionesGerenciaComponent,
    OpcionesTramitesComponent,
    OpcionesChapisteriaComponent,
    OpcionesGastosComponent,
    OpcionesTallerComponent,
    OpcionesOperacionesComponent,
    OpcionesLlaveroComponent,
    OpcionesReclamosComponent,
    OpcionesCntComponent,
    OpcionesUtilidadesComponent,
    OpcionesCarteraComponent,
    OpcionesAlmacenComponent,
    OwnersTableComponent,
    OwnersVehiclesComponent,
    OwnersResumeComponent,
    OwnersAddnewComponent,
    OwnersReportsComponent,
    OwnersDeleteComponent,
    DriversTableComponent,
    DriversResumeComponent,
    DriversDeleteComponent,
    DriversAddnewComponent,
    VehiclesTableComponent,
    VehiclesResumeComponent,
    VehiclesDeleteComponent,
    VehiclesAddnewComponent,
    VehiclesDocumentationComponent,
    DriversDocumentationComponent,
    OperacionesEntregaVehiculoConductorComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    SharedModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
