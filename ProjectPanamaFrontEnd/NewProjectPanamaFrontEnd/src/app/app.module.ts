import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MatCardModule } from '@angular/material/card';
import { MatDialogModule } from '@angular/material/dialog';
import {MatButtonModule} from '@angular/material/button';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HeaderComponent } from './components/main/header/header.component';
import { UsersHomeComponent } from './components/main/home/users-home/users-home.component';
import { LoginComponent } from './components/users/login/login.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FooterComponent } from './components/main/footer/footer.component';
import { StatevehiclefleetComponent } from './components/tasks/statevehiclefleet/statevehiclefleet.component';
import { PdfViewerComponent } from './components/others/pdf-viewer/pdf-viewer.component';
import { FeespaidComponent } from './components/tasks/feespaid/feespaid.component';
import { OpcionesGerenciaComponent } from './components/options/gerencia/opciones-gerencia/opciones-gerencia.component';
import { OpcionesTramitesComponent } from './components/options/tramites/opciones-tramites/opciones-tramites.component';
import { OpcionesChapisteriaComponent } from './components/options/chapisteria/opciones-chapisteria/opciones-chapisteria.component';
import { OpcionesGastosComponent } from './components/options/gastos/opciones-gastos/opciones-gastos.component';
import { OpcionesTallerComponent } from './components/options/taller/opciones-taller/opciones-taller.component';
import { OpcionesOperacionesComponent } from './components/options/operaciones/opciones-operaciones/opciones-operaciones.component';
import { OpcionesLlaveroComponent } from './components/options/llavero/opciones-llavero/opciones-llavero.component';
import { OpcionesReclamosComponent } from './components/options/reclamos/opciones-reclamos/opciones-reclamos.component';
import { OpcionesCntComponent } from './components/options/cnt/opciones-cnt/opciones-cnt.component';
import { OpcionesUtilidadesComponent } from './components/options/utilidades/opciones-utilidades/opciones-utilidades.component';
import { OpcionesCarteraComponent } from './components/options/cartera/opciones-cartera/opciones-cartera.component';
import { OpcionesAlmacenComponent } from './components/options/almacen/opciones-almacen/opciones-almacen.component';
import { OwnersTableComponent } from './components/tasks/owners/owners-table/owners-table.component';
import { OwnersVehiclesComponent } from './components/tasks/owners/owners-vehicles/owners-vehicles.component';
import { OwnersResumeComponent } from './components/tasks/owners/owners-resume/owners-resume.component';
import { OwnersAddnewComponent } from './components/tasks/owners/owners-addnew/owners-addnew.component';
import { OwnersReportsComponent } from './components/tasks/owners/owners-reports/owners-reports.component';
import { OwnersDeleteComponent } from './components/tasks/owners/owners-delete/owners-delete.component';
import { DriversTableComponent } from './components/tasks/drivers/drivers-table/drivers-table.component';
import { DriversResumeComponent } from './components/tasks/drivers/drivers-resume/drivers-resume.component';
import { DriversDeleteComponent } from './components/tasks/drivers/drivers-delete/drivers-delete.component';
import { DriversAddnewComponent } from './components/tasks/drivers/drivers-addnew/drivers-addnew.component';
import { VehiclesTableComponent } from './components/tasks/vehicles/vehicles-table/vehicles-table.component';
import { VehiclesResumeComponent } from './components/tasks/vehicles/vehicles-resume/vehicles-resume.component';
import { VehiclesDeleteComponent } from './components/tasks/vehicles/vehicles-delete/vehicles-delete.component';
import { VehiclesAddnewComponent } from './components/tasks/vehicles/vehicles-addnew/vehicles-addnew.component';
import { VehiclesDocumentationComponent } from './components/tasks/vehicles/vehicles-documentation/vehicles-documentation.component';
import { DriversDocumentationComponent } from './components/tasks/drivers/drivers-documentation/drivers-documentation.component';
import { OperacionesEntregaVehiculoConductorComponent } from './components/options/operaciones/operaciones-entrega-vehiculo-conductor/operaciones-entrega-vehiculo-conductor.component';
import { OwnersHomeComponent } from './components/main/home/owners-home/owners-home.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    UsersHomeComponent,
    LoginComponent,
    FooterComponent,
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
    OwnersHomeComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatCardModule,
    MatDialogModule,
    MatButtonModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
