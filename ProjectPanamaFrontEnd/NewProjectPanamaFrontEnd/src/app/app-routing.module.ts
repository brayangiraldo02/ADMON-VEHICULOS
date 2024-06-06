import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/main/home/home.component';
import { LoginComponent } from './components/users/login/login.component';
import { AuthGuard } from './guards/auth.guard';
import { NoAuthGuard } from './guards/no-auth.guard';
import { StatevehiclefleetComponent } from './components/tasks/statevehiclefleet/statevehiclefleet.component';
import { PdfViewerComponent } from './components/others/pdf-viewer/pdf-viewer.component';
import { VehiclesComponent } from './components/tasks/vehicles/vehicles.component';
import { FeespaidComponent } from './components/tasks/feespaid/feespaid.component';
import { OpcionesGerenciaComponent } from './components/options/gerencia/opciones-gerencia/opciones-gerencia.component';
import { OpcionesTramitesComponent } from './components/options/tramites/opciones-tramites/opciones-tramites.component';

const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent, canActivate: [NoAuthGuard]},
  { path: 'home', component: HomeComponent, canActivate: [AuthGuard]},
  { path: 'statevehiclefleet', component: StatevehiclefleetComponent, canActivate: [AuthGuard]},
  { path: 'vehicles', component: VehiclesComponent, canActivate: [AuthGuard]},
  { path: 'feespaid', component: FeespaidComponent, canActivate: [AuthGuard]},
  { path: 'management', component: OpcionesGerenciaComponent, canActivate: [AuthGuard]},
  { path: 'procedures', component: OpcionesTramitesComponent, canActivate: [AuthGuard]},
  { path: 'pdf', component: PdfViewerComponent, canActivate: [AuthGuard]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
