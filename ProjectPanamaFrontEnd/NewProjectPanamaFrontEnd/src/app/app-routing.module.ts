import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UsersHomeComponent } from './components/main/home/users/users-home.component';
import { LoginComponent } from './components/users/login/login.component';
import { AuthGuard } from './guards/auth.guard';
import { NoAuthGuard } from './guards/no-auth.guard';
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
import { OwnersResumeComponent } from './components/tasks/owners/owners-resume/owners-resume.component';
import { OwnersAddnewComponent } from './components/tasks/owners/owners-addnew/owners-addnew.component';
import { DriversTableComponent } from './components/tasks/drivers/drivers-table/drivers-table.component';
import { DriversResumeComponent } from './components/tasks/drivers/drivers-resume/drivers-resume.component';
import { DriversAddnewComponent } from './components/tasks/drivers/drivers-addnew/drivers-addnew.component';
import { VehiclesTableComponent } from './components/tasks/vehicles/vehicles-table/vehicles-table.component';
import { VehiclesResumeComponent } from './components/tasks/vehicles/vehicles-resume/vehicles-resume.component';
import { VehiclesAddnewComponent } from './components/tasks/vehicles/vehicles-addnew/vehicles-addnew.component';
import { VehiclesDocumentationComponent } from './components/tasks/vehicles/vehicles-documentation/vehicles-documentation.component';
import { DriversDocumentationComponent } from './components/tasks/drivers/drivers-documentation/drivers-documentation.component';
import { OwnersHomeComponent } from './components/main/home/owners-home/owners-home.component';

const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent, canActivate: [NoAuthGuard]},
  { path: 'users-home', component: UsersHomeComponent, canActivate: [AuthGuard]},
  { path: 'owners-home', component: OwnersHomeComponent, canActivate: [AuthGuard]},
  { path: 'statevehiclefleet', component: StatevehiclefleetComponent, canActivate: [AuthGuard]},
  { path: 'vehicles', component: VehiclesTableComponent, canActivate: [AuthGuard]},
  { path: 'vehicle/:code', component: VehiclesResumeComponent, canActivate: [AuthGuard]},
  { path: 'new-vehicle', component: VehiclesAddnewComponent, canActivate: [AuthGuard]},
  { path: 'feespaid', component: FeespaidComponent, canActivate: [AuthGuard]},
  { path: 'owners', component: OwnersTableComponent, canActivate: [AuthGuard]},
  { path: 'owner/:code', component: OwnersResumeComponent, canActivate: [AuthGuard]},
  { path: 'new-owner', component: OwnersAddnewComponent, canActivate: [AuthGuard]},
  { path: 'drivers', component: DriversTableComponent, canActivate: [AuthGuard]},
  { path: 'driver/:code', component: DriversResumeComponent, canActivate: [AuthGuard]},
  { path: 'new-driver', component: DriversAddnewComponent, canActivate: [AuthGuard]},
  { path: 'operations', component: OpcionesOperacionesComponent, canActivate: [AuthGuard]},
  { path: 'procedures', component: OpcionesTramitesComponent, canActivate: [AuthGuard]},
  { path: 'warehouse', component: OpcionesAlmacenComponent, canActivate: [AuthGuard]},
  { path: 'workshop', component: OpcionesTallerComponent, canActivate: [AuthGuard]},
  { path: 'sheet-metal-work', component: OpcionesChapisteriaComponent, canActivate: [AuthGuard]},
  { path: 'keychain', component: OpcionesLlaveroComponent, canActivate: [AuthGuard]},
  { path: 'claims', component: OpcionesReclamosComponent, canActivate: [AuthGuard]},
  { path: 'wallet', component: OpcionesCarteraComponent, canActivate: [AuthGuard]},
  { path: 'management', component: OpcionesGerenciaComponent, canActivate: [AuthGuard]},
  { path: 'expenses', component: OpcionesGastosComponent, canActivate: [AuthGuard]},
  { path: 'cnt', component: OpcionesCntComponent, canActivate: [AuthGuard]},
  { path: 'utilities', component: OpcionesUtilidadesComponent, canActivate: [AuthGuard]},
  { path: 'pdf', component: PdfViewerComponent, canActivate: [AuthGuard]},
  { path: 'prueba', component: DriversDocumentationComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
