import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-gerencia',
  templateUrl: './opciones-gerencia.component.html',
  styleUrls: ['./opciones-gerencia.component.css']
})
export class OpcionesGerenciaComponent {

  options = [
    { name: 'Estado General de la Flota', icon: 'info', url: 'hoalalalal' },
    { name: 'Consolidado Estado de la Flota', icon: 'info', url: 'hoalalalal' },
    { name: 'Inventario por Grupo', icon: 'info', url: 'hoalalalal' },
    { name: 'Resumen Cierre de Caja', icon: 'info', url: 'hoalalalal' },
    { name: 'Informe de Ingresos y Egresos (PyG)', icon: 'info', url: 'hoalalalal' },
    { name: 'Informe de Recaudos por Empresa', icon: 'info', url: 'hoalalalal' },
    { name: 'Informe de Transferencia ADS a Empresas', icon: 'info', url: 'hoalalalal' },
    { name: 'Informe de Recaudos Día a Día', icon: 'info', url: 'hoalalalal' },
    { name: 'Informe de Recaudos Mes a Mes', icon: 'info', url: 'hoalalalal' }
  ];
}
