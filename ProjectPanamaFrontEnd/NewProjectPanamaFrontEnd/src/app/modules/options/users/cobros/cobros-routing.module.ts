import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InfoTableComponent } from './components/info-table/info-table.component';

const routes: Routes = [
  {
    path: '',
    component: InfoTableComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CobrosRoutingModule { }
