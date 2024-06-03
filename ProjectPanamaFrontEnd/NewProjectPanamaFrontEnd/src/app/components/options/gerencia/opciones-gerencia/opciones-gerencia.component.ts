import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-gerencia',
  templateUrl: './opciones-gerencia.component.html',
  styleUrls: ['./opciones-gerencia.component.css']
})
export class OpcionesGerenciaComponent {

  options = [
    { name: 'Estado General de la Flota', icon: '../../../../assets/icons/gerencia.svg', url: 'hoalalalal' },
    { name: 'Consolidado Estado de la Flota', icon: '../../../../assets/icons/gastos.svg', url: 'hoalalalal' },
    { name: 'Inventario por Grupo', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' },
    { name: 'Resumen Cierre de Caja', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' },
    { name: 'Informe de Ingresos y Egresos (PyG)', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' },
    { name: 'Informe de Recaudos por Empresa', icon: '../../../../assets/icons/gastos.svg', url: 'hoalalalal' },
    { name: 'Informe de Transferencia ADS a Empresas', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' },
    { name: 'Informe de Recaudos Día a Día', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' },
    { name: 'Informe de Recaudos Mes a Mes', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' }
  ];
}
