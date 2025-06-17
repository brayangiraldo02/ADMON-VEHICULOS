import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { InfoCompanyComponent } from './components/info-company/info-company.component';
import { FormsModule } from '@angular/forms';
import { ToolbarComponent } from './components/toolbar/toolbar.component';
import { MaterialModule } from './material/material.module';
import { SidenavComponent } from './components/sidenav/sidenav.component';

@NgModule({
  declarations: [
    HeaderComponent,
    FooterComponent,
    InfoCompanyComponent,
    ToolbarComponent,
    SidenavComponent,
  ],
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    MaterialModule
  ],
  exports: [
    HeaderComponent,
    FooterComponent,
    ToolbarComponent,
    SidenavComponent,
    MaterialModule
  ]
})
export class SharedModule { }
