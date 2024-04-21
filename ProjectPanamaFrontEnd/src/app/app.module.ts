import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './main/login/login.component';
import { ProfileComponent } from './main/profile/profile.component';
import { InterceptorService } from './services/interceptor-service.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CardsStatusComponent } from './main/cards-status/cards-status.component';
import { NavbarComponent } from './main/navbar/navbar.component';
import { SidebarComponent } from './main/sidebar/sidebar.component';
import { CarsComponent } from './main/cars/cars.component';
import { DriversComponent } from './main/drivers/drivers.component';
import { FleetComponent } from './main/fleet/fleet.component';
import { FinancialBoxComponent } from './main/financial-box/financial-box.component';
import { CollectionComponent } from './main/collection/collection.component';
import { FormalitiesComponent } from './main/formalities/formalities.component';
import { MainComponent } from './main/main.component';
import { StoreComponent } from './main/store/store.component';
import { WorkshopComponent } from './main/workshop/workshop.component';
import { BodyworkComponent } from './main/bodywork/bodywork.component';
import { KeyRingComponent } from './main/key-ring/key-ring.component';
import { WalletComponent } from './main/wallet/wallet.component';
import { ManagementComponent } from './main/management/management.component';
import { BoardComponent } from './main/board/board.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    ProfileComponent,
    CardsStatusComponent,
    NavbarComponent,
    SidebarComponent,
    CarsComponent,
    DriversComponent,
    FleetComponent,
    FinancialBoxComponent,
    CollectionComponent,
    FormalitiesComponent,
    MainComponent,
    StoreComponent,
    WorkshopComponent,
    BodyworkComponent,
    KeyRingComponent,
    WalletComponent,
    ManagementComponent,
    BoardComponent

  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: InterceptorService,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
