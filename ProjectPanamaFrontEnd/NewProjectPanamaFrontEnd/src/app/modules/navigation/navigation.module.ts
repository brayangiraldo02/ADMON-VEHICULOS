import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { NavigationRoutingModule } from './navigation-routing.module';
import { LayoutComponent } from './components/layout/layout.component';
import { MaterialModule } from '../shared/material/material.module'; 
import { SharedModule } from '../shared/shared.module';
import { DevPreviewComponent } from './components/dev-preview/dev-preview.component'; // Assuming you have a SharedModule for common components, directives, etc.
import { ToolbarComponent } from './components/toolbar/toolbar.component';
import { SidenavComponent } from './components/sidenav/sidenav.component';
import { FooterComponent } from './components/footer/footer.component';

@NgModule({
  declarations: [
    LayoutComponent,
    DevPreviewComponent,
    ToolbarComponent,
    SidenavComponent,
    FooterComponent,
  ],
  imports: [
    CommonModule,
    NavigationRoutingModule,
    SharedModule
  ],
  exports: [
    LayoutComponent
  ]
})
export class NavigationModule { }
