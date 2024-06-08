import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-gastos',
  templateUrl: './opciones-gastos.component.html',
  styleUrls: ['./opciones-gastos.component.css']
})
export class OpcionesGastosComponent {
  gastos_generales = [
    { name: 'Gastos Generales (Caja Chica)', icon: 'info', url: 'hoalalalal' },
    { name: 'Devolución Gastos Generales', icon: 'info', url: 'hoalalalal' },
    { name: 'Informe Diario de Gastos', icon: 'info', url: 'hoalalalal' },
    { name: 'Informe Gastos por Empresa', icon: 'info', url: 'hoalalalal' },
    { name: 'Total Gastos por Empresa', icon: 'info', url: 'hoalalalal' },
    { name: 'Consecutivo de Gastos', icon: 'info', url: 'hoalalalal' },
    { name: 'Detalle de Gastos', icon: 'info', url: 'hoalalalal' },
    { name: 'Total Gastos Grupo/Código', icon: 'info', url: 'hoalalalal' },
  ];

  gastos_cheque = [
    { name: 'Gastos con Cheque', icon: 'info', url: 'hoalalalal' },
    { name: 'Saldos Pendientes por Empresa', icon: 'info', url: 'hoalalalal' },
    { name: 'Detalle de Gastos con Cheque', icon: 'info', url: 'hoalalalal' },
    { name: 'Relación Semanal (Consolidado)', icon: 'info', url: 'hoalalalal' },
    { name: 'Generar Planilla Semanal (Consolidado)', icon: 'info', url: 'hoalalalal' },
    { name: 'Relación Detalle por Empresa', icon: 'info', url: 'hoalalalal' },
  ];
}
