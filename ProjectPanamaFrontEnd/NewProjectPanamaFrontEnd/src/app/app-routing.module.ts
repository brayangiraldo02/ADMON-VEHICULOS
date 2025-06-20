// import { NgModule } from '@angular/core';
// import { RouterModule, Routes } from '@angular/router';
// import { LoginComponent } from './modules/users/login/login.component';
// import { AuthGuard } from './guards/auth.guard';
// import { NoAuthGuard } from './guards/no-auth.guard';
// import { StatevehiclefleetComponent } from './modules/tasks/statevehiclefleet/statevehiclefleet.component';
// import { PdfViewerComponent } from './modules/others/pdf-viewer/pdf-viewer.component';
// import { FeespaidComponent } from './modules/tasks/feespaid/feespaid.component';
// import { OpcionesGerenciaComponent } from './modules/options/users/gerencia/opciones-gerencia/opciones-gerencia.component';
// import { OpcionesTramitesComponent } from './modules/options/users/tramites/opciones-tramites/opciones-tramites.component';
// import { OpcionesChapisteriaComponent } from './modules/options/users/chapisteria/opciones-chapisteria/opciones-chapisteria.component';
// import { OpcionesGastosComponent } from './modules/options/users/gastos/opciones-gastos/opciones-gastos.component';
// import { OpcionesTallerComponent } from './modules/options/users/taller/opciones-taller/opciones-taller.component';
// import { OpcionesOperacionesComponent } from './modules/options/users/operaciones/opciones-operaciones/opciones-operaciones.component';
// import { OpcionesLlaveroComponent } from './modules/options/users/llavero/opciones-llavero/opciones-llavero.component';
// import { OpcionesReclamosComponent } from './modules/options/users/reclamos/opciones-reclamos/opciones-reclamos.component';
// import { OpcionesCntComponent } from './modules/options/users/cnt/opciones-cnt/opciones-cnt.component';
// import { OpcionesUtilidadesComponent } from './modules/options/users/utilidades/opciones-utilidades/opciones-utilidades.component';
// import { OpcionesCarteraComponent } from './modules/options/users/cartera/opciones-cartera/opciones-cartera.component';
// import { OpcionesAlmacenComponent } from './modules/options/users/almacen/opciones-almacen/opciones-almacen.component';
// import { OwnersTableComponent } from './modules/tasks/owners/owners-table/owners-table.component';
// import { OwnersResumeComponent } from './modules/tasks/owners/owners-resume/owners-resume.component';
// import { OwnersAddnewComponent } from './modules/tasks/owners/owners-addnew/owners-addnew.component';
// import { DriversTableComponent } from './modules/tasks/drivers/drivers-table/drivers-table.component';
// import { DriversResumeComponent } from './modules/tasks/drivers/drivers-resume/drivers-resume.component';
// import { DriversAddnewComponent } from './modules/tasks/drivers/drivers-addnew/drivers-addnew.component';
// import { VehiclesTableComponent } from './modules/tasks/vehicles/vehicles-table/vehicles-table.component';
// import { VehiclesResumeComponent } from './modules/tasks/vehicles/vehicles-resume/vehicles-resume.component';
// import { VehiclesAddnewComponent } from './modules/tasks/vehicles/vehicles-addnew/vehicles-addnew.component';
// import { VehiclesDocumentationComponent } from './modules/tasks/vehicles/vehicles-documentation/vehicles-documentation.component';
// import { DriversDocumentationComponent } from './modules/tasks/drivers/drivers-documentation/drivers-documentation.component';
// import { OwnersGuard } from './guards/owners.guard';
// import { UsersGuard } from './guards/users.guard';
// import { LayoutComponent } from './modules/navigation/components/layout/layout.component';

// const routes: Routes = [
//   { path: '', redirectTo: 'login', pathMatch: 'full' },
//   { path: 'login', component: LoginComponent, canActivate: [NoAuthGuard]},
//   // {
//   //   path: 'home',
//   //   loadChildren: () => import('./modules/home/home.module').then(m => m.HomeModule),
//   // },
//   // { path: 'owners-home', component: OwnersHomeComponent, canActivate: [OwnersGuard]},
//   { path: 'statevehiclefleet', component: StatevehiclefleetComponent, canActivate: [AuthGuard]},
//   { path: 'vehicles', component: VehiclesTableComponent, canActivate: [AuthGuard]},
//   { path: 'vehicle/:code', component: VehiclesResumeComponent, canActivate: [AuthGuard]},
//   { path: 'new-vehicle', component: VehiclesAddnewComponent, canActivate: [AuthGuard]},
//   { path: 'feespaid', component: FeespaidComponent, canActivate: [AuthGuard]},
//   { path: 'owners', component: OwnersTableComponent, canActivate: [AuthGuard]},
//   { path: 'owner/:code', component: OwnersResumeComponent, canActivate: [AuthGuard]},
//   { path: 'new-owner', component: OwnersAddnewComponent, canActivate: [AuthGuard]},
//   { path: 'drivers', component: DriversTableComponent, canActivate: [AuthGuard]},
//   { path: 'driver/:code', component: DriversResumeComponent, canActivate: [AuthGuard]},
//   { path: 'new-driver', component: DriversAddnewComponent, canActivate: [AuthGuard]},
//   { path: 'operations', component: OpcionesOperacionesComponent, canActivate: [AuthGuard]},
//   { path: 'procedures', component: OpcionesTramitesComponent, canActivate: [AuthGuard]},
//   { path: 'warehouse', component: OpcionesAlmacenComponent, canActivate: [AuthGuard]},
//   { path: 'workshop', component: OpcionesTallerComponent, canActivate: [AuthGuard]},
//   { path: 'sheet-metal-work', component: OpcionesChapisteriaComponent, canActivate: [AuthGuard]},
//   { path: 'keychain', component: OpcionesLlaveroComponent, canActivate: [AuthGuard]},
//   { path: 'claims', component: OpcionesReclamosComponent, canActivate: [AuthGuard]},
//   { path: 'wallet', component: OpcionesCarteraComponent, canActivate: [AuthGuard]},
//   { path: 'management', component: OpcionesGerenciaComponent, canActivate: [AuthGuard]},
//   { path: 'expenses', component: OpcionesGastosComponent, canActivate: [AuthGuard]},
//   { path: 'cnt', component: OpcionesCntComponent, canActivate: [AuthGuard]},
//   { path: 'utilities', component: OpcionesUtilidadesComponent, canActivate: [AuthGuard]},
//   {
//     path: 'cobros',
//     loadChildren: () => import('./modules/options/users/cobros/cobros.module').then(m => m.CobrosModule),
//     canActivate: [AuthGuard]
//   },
//   { path: 'pdf', component: PdfViewerComponent, canActivate: [UsersGuard]},
//   { path: 'prueba',
//     loadChildren: () => import('./modules/navigation/navigation.module').then(m => m.NavigationModule),
//   }
// ];

// @NgModule({
//   imports: [RouterModule.forRoot(routes)],
//   exports: [RouterModule]
// })
// export class AppRoutingModule { }

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './modules/users/login/login.component';
import { NoAuthGuard } from './guards/no-auth.guard';
import { PdfViewerComponent } from './modules/others/pdf-viewer/pdf-viewer.component';
import { UsersGuard } from './guards/users.guard';
// No es necesario importar LayoutComponent aquí
// No es necesario importar los componentes de tareas/opciones aquí

const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent,
    canActivate: [NoAuthGuard]
  },
  {
    path: 'pdf', // Ruta para el visor de PDF, sin el layout principal
    component: PdfViewerComponent,
    canActivate: [UsersGuard]
  },
  {
    path: '', // Ruta por defecto, carga el NavigationModule que contiene el LayoutComponent y las rutas principales
    loadChildren: () => import('./modules/navigation/navigation.module').then(m => m.NavigationModule),
    // Considera agregar canActivate: [AuthGuard] aquí si TODAS las rutas dentro de NavigationModule lo requieren
    // o manejarlo dentro de navigation-routing.module.ts como haremos.
  },
  // Considera una ruta comodín para manejar rutas no encontradas, por ejemplo, redirigir a login o a una página 404
  // { path: '**', redirectTo: 'login' } // O una página específica de "No encontrado"
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }