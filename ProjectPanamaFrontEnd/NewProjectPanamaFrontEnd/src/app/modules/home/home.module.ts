import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeRoutingModule } from './home-routing.module';
import { HomeOwnersComponent } from './components/owners/home-owners/home-owners.component';
import { HomeUsersComponent } from './components/users/home-users/home-users.component';
import { SharedModule } from '../shared/shared.module';
import { OwnersModule } from '../options/owners/owners.module';

@NgModule({
  declarations: [
  
    HomeOwnersComponent,
    HomeUsersComponent
  ],
  imports: [
    CommonModule,
    HomeRoutingModule,
    SharedModule,
    OwnersModule
  ]
})
export class HomeModule { }
