import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-operaciones',
  templateUrl: './opciones-operaciones.component.html',
  styleUrls: ['./opciones-operaciones.component.css']
})
export class OpcionesOperacionesComponent {
  options = [
    { name: 'Entrega de Vehículo al Conductor', icon: 'info', url: 'hoalalalal' },
    { name: 'Generar Contrato y Declaración Jurada', icon: 'info', url: 'hoalalalal' },
    { name: 'Crear Cuenta de Diario al Conductor (Anticipo de Cuenta)', icon: 'info', url: 'hoalalalal' },
    { name: 'Cambiar de Estado a un Vehículo', icon: 'info', url: 'hoalalalal' },
    { name: 'Prestamo de Vehículo al Conductor', icon: 'info', url: 'hoalalalal' },
    { name: 'Devolución de Vehículos Prestados', icon: 'info', url: 'hoalalalal' },
    { name: 'Bajar Conductor del Vehículo (Culminación del Contrato)', icon: 'info', url: 'hoalalalal' },
    { name: 'Corregir Kilometraje Actual al Vehículo', icon: 'info', url: 'hoalalalal' },
    { name: 'Apertura de Cuenta por Cobrar a un Conductor', icon: 'info', url: 'hoalalalal' },
    { name: 'Hoja de Inspección del Vehículo', icon: 'info', url: 'hoalalalal' },
    { name: 'Hoja de Vida del Vehículo', icon: 'info', url: 'hoalalalal' },
    { name: 'Hoja de Vida del Conductor', icon: 'info', url: 'hoalalalal' }
  ];
}
