import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-reclamos',
  templateUrl: './opciones-reclamos.component.html',
  styleUrls: ['./opciones-reclamos.component.css']
})
export class OpcionesReclamosComponent {
  colisiones = [
    { name: 'Crear Caso de Colisión (Colilla o FUD)', icon: 'info', url: 'hoalalalal' },
    { name: 'Actualizar Colilla (Información Resolución)', icon: 'info', url: 'hoalalalal' },
    { name: 'Adjuntar Cotización de Reparación', icon: 'info', url: 'hoalalalal' },
    { name: 'Informe de Programación de Juicios', icon: 'info', url: 'hoalalalal' },
    { name: 'Detalle de Documentos Entregados', icon: 'info', url: 'hoalalalal' },
    { name: 'Hacer Seguimiento del Pago', icon: 'info', url: 'hoalalalal' },
    { name: 'Recibir Pago de la Aseguradora (Cerrar Caso)', icon: 'info', url: 'hoalalalal' },
    { name: 'Consultar Estado de un Caso', icon: 'info', url: 'hoalalalal' },
  ];

  panapass = [
    { name: 'Actualizar Información PanaPass de los Vehículos', icon: 'info', url: 'hoalalalal' },
    { name: 'Generar Archivo (CSV) para Consultar Saldos', icon: 'info', url: 'hoalalalal' },
    { name: 'Informe PanaPass por Empresa', icon: 'info', url: 'hoalalalal' }
  ];
}
