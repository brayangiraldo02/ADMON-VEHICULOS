import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AuthGuardGuard } from './guard/auth-guard.guard';
import { LoginComponent } from './main/login/login.component';
import { ProfileComponent } from './main/profile/profile.component';
import { CardsStatusComponent } from './main/cards-status/cards-status.component';
import { NavbarComponent } from './main/navbar/navbar.component';
import { SidebarComponent } from './main/sidebar/sidebar.component';
import {  CarsComponent } from './main/cars/cars.component'
import {  DriversComponent } from './main/drivers/drivers.component'
import {  FleetComponent } from './main/fleet/fleet.component'
import { FinancialBoxComponent } from './main/financial-box/financial-box.component'
import { WorkshopComponent} from './main/workshop/workshop.component'
import { WalletComponent } from './main/wallet/wallet.component'
import { StoreComponent } from './main/store/store.component'
import { ManagementComponent } from './main/management/management.component'
import { KeyRingComponent } from './main/key-ring/key-ring.component'
import { FormalitiesComponent } from './main/formalities/formalities.component'
import { CollectionComponent } from './main/collection/collection.component'
import { BodyworkComponent } from './main/bodywork/bodywork.component'
import { BoardComponent } from './main/board/board.component'

const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'profile',
    component: ProfileComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'cardsStatus',
    component: CardsStatusComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'nav',
    component: NavbarComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'sidebar',
    component: SidebarComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'cars',
    component: CarsComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'drivers',
    component: DriversComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'fleet',
    component: FleetComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'boxs',
    component: FinancialBoxComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'taller',
    component: WorkshopComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'wallet',
    component: WalletComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'store',
    component: StoreComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'management',
    component: ManagementComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'key',
    component: KeyRingComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'tramite',
    component: FormalitiesComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'collec',
    component: CollectionComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'chapisteria',
    component: BodyworkComponent,
    canActivate: [AuthGuardGuard]
  },
  {
    path: 'board',
    component: BoardComponent,
    canActivate: [AuthGuardGuard]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
