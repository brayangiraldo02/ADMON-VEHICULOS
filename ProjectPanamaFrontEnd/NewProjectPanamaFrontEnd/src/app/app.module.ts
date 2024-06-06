import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MatCardModule } from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HeaderComponent } from './components/main/header/header.component';
import { HomeComponent } from './components/main/home/home.component';
import { LoginComponent } from './components/users/login/login.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FooterComponent } from './components/main/footer/footer.component';
import { StatevehiclefleetComponent } from './components/tasks/statevehiclefleet/statevehiclefleet.component';
import { PdfViewerComponent } from './components/others/pdf-viewer/pdf-viewer.component';
import { VehiclesComponent } from './components/tasks/vehicles/vehicles.component';
import { FeespaidComponent } from './components/tasks/feespaid/feespaid.component';
import { OpcionesGerenciaComponent } from './components/options/gerencia/opciones-gerencia/opciones-gerencia.component';
import { OpcionesTramitesComponent } from './components/options/tramites/opciones-tramites/opciones-tramites.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    HomeComponent,
    LoginComponent,
    FooterComponent,
    StatevehiclefleetComponent,
    PdfViewerComponent,
    VehiclesComponent,
    FeespaidComponent,
    OpcionesGerenciaComponent,
    OpcionesTramitesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatCardModule,
    MatButtonModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
