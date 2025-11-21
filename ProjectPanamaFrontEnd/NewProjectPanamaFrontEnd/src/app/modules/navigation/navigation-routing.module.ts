// import { NgModule } from '@angular/core';
// import { RouterModule, Routes } from '@angular/router';
// import { LayoutComponent } from './components/layout/layout.component';

// const routes: Routes = [
//   {
//     path: '', // Esta es la ruta base para NavigationModule (ej. /prueba)
//     component: LayoutComponent, // LayoutComponent actúa como el contenedor
//     children: [
//       {
//         path: '', // Ruta vacía dentro de /prueba, redirige a /prueba/home
//         redirectTo: 'home',
//         pathMatch: 'full'
//       },
//       {
//         path: 'home', // Se accederá como /prueba/home
//         // Corregir la ruta de importación aquí:
//         loadChildren: () => import('../home/home.module').then(m => m.HomeModule),
//       },
//       // Aquí puedes agregar más rutas que usarán LayoutComponent
//     ]
//   }
// ];

// @NgModule({
//   imports: [RouterModule.forChild(routes)],
//   exports: [RouterModule]
// })
// export class NavigationRoutingModule { }

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LayoutComponent } from './components/layout/layout.component';
import { AuthGuard } from '../../guards/auth.guard'; // Asegúrate que la ruta al guard sea correcta

// Importa todos los componentes necesarios para las rutas
import { StatevehiclefleetComponent } from '../tasks/statevehiclefleet/statevehiclefleet.component';
import { FeespaidComponent } from '../tasks/feespaid/feespaid.component';
import { OpcionesGerenciaComponent } from '../options/users/gerencia/opciones-gerencia/opciones-gerencia.component';
import { OpcionesTramitesComponent } from '../options/users/tramites/opciones-tramites/opciones-tramites.component';
import { OpcionesChapisteriaComponent } from '../options/users/chapisteria/opciones-chapisteria/opciones-chapisteria.component';
import { OpcionesGastosComponent } from '../options/users/gastos/opciones-gastos/opciones-gastos.component';
import { OpcionesTallerComponent } from '../options/users/taller/opciones-taller/opciones-taller.component';
import { OpcionesOperacionesComponent } from '../options/users/operaciones/opciones-operaciones/opciones-operaciones.component';
import { OpcionesLlaveroComponent } from '../options/users/llavero/opciones-llavero/opciones-llavero.component';
import { OpcionesReclamosComponent } from '../options/users/reclamos/opciones-reclamos/opciones-reclamos.component';
import { OpcionesCntComponent } from '../options/users/cnt/opciones-cnt/opciones-cnt.component';
import { OpcionesUtilidadesComponent } from '../options/users/utilidades/opciones-utilidades/opciones-utilidades.component';
import { OpcionesCarteraComponent } from '../options/users/cartera/opciones-cartera/opciones-cartera.component';
import { OpcionesAlmacenComponent } from '../options/users/almacen/opciones-almacen/opciones-almacen.component';
import { OwnersTableComponent } from '../tasks/owners/owners-table/owners-table.component';
import { OwnersResumeComponent } from '../tasks/owners/owners-resume/owners-resume.component';
import { OwnersAddnewComponent } from '../tasks/owners/owners-addnew/owners-addnew.component';
import { DriversTableComponent } from '../tasks/drivers/drivers-table/drivers-table.component';
import { DriversResumeComponent } from '../tasks/drivers/drivers-resume/drivers-resume.component';
import { DriversAddnewComponent } from '../tasks/drivers/drivers-addnew/drivers-addnew.component';
import { VehiclesTableComponent } from '../tasks/vehicles/vehicles-table/vehicles-table.component';
import { VehiclesResumeComponent } from '../tasks/vehicles/vehicles-resume/vehicles-resume.component';
import { VehiclesAddnewComponent } from '../tasks/vehicles/vehicles-addnew/vehicles-addnew.component';
import { InspectionsTableComponent } from '../tasks/inspections/inspections-table/inspections-table.component';
import { inspectionsGuard } from 'src/app/guards/inspections.guard';
// VehiclesDocumentationComponent y DriversDocumentationComponent no estaban en tu app-routing, si las necesitas, impórtalas.

const routes: Routes = [
  {
    path: '', // Ruta base DENTRO del NavigationModule
    component: LayoutComponent,
    canActivate: [AuthGuard], // Protege todas las rutas hijas con AuthGuard
    children: [
      { path: '', redirectTo: 'home', pathMatch: 'full' }, // Redirección por defecto dentro del layout
      {
        path: 'home',
        loadChildren: () => import('../home/home.module').then(m => m.HomeModule),
      },
      { path: 'statevehiclefleet', component: StatevehiclefleetComponent },
      { path: 'vehicles', component: VehiclesTableComponent },
      { path: 'vehicle/:code', component: VehiclesResumeComponent },
      { path: 'new-vehicle', component: VehiclesAddnewComponent },
      { path: 'feespaid', component: FeespaidComponent },
      { path: 'owners', component: OwnersTableComponent },
      { path: 'owner/:code', component: OwnersResumeComponent },
      { path: 'new-owner', component: OwnersAddnewComponent },
      { path: 'drivers', component: DriversTableComponent },
      { path: 'driver/:code', component: DriversResumeComponent },
      { path: 'new-driver', component: DriversAddnewComponent },
      { path: 'operations', component: OpcionesOperacionesComponent },
      { path: 'procedures', component: OpcionesTramitesComponent },
      { path: 'warehouse', component: OpcionesAlmacenComponent },
      { path: 'workshop', component: OpcionesTallerComponent },
      { path: 'sheet-metal-work', component: OpcionesChapisteriaComponent },
      { path: 'keychain', component: OpcionesLlaveroComponent },
      { path: 'claims', component: OpcionesReclamosComponent },
      { path: 'wallet', component: OpcionesCarteraComponent },
      { path: 'management', component: OpcionesGerenciaComponent },
      { path: 'expenses', component: OpcionesGastosComponent },
      { path: 'cnt', component: OpcionesCntComponent },
      { path: 'utilities', component: OpcionesUtilidadesComponent },
      {
        path: 'cobros',
        loadChildren: () => import('../options/users/cobros/cobros.module').then(m => m.CobrosModule),
      },
      {
        path: 'inspections',
        component: InspectionsTableComponent,
        canActivate: [inspectionsGuard],
      },
      {
        path: 'inspections/:id',
        component: InspectionsTableComponent,
        canActivate: [inspectionsGuard],
      }
      // Las rutas 'pdf' y 'login' NO se definen aquí.
      // La ruta 'prueba' ya no es necesaria como tal, ya que su funcionalidad (cargar NavigationModule)
      // ahora la tiene el path: '' en app-routing.module.ts.
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class NavigationRoutingModule { }