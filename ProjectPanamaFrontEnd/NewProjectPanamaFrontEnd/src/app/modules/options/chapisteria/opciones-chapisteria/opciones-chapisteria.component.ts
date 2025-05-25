import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-chapisteria',
  templateUrl: './opciones-chapisteria.component.html',
  styleUrls: ['./opciones-chapisteria.component.css']
})
export class OpcionesChapisteriaComponent {
  options = [
    { name: 'Entrada Diaria de Vehículos (Cambiar Estado)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Solicitar Cotizaciones (Aprobación)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Generar Orden de Servicio desde Cotización Aprobada', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Salida de Vehículos Reparados (Cambiar Estado)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Listado General de Vehículos en Chapistería', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Informe de Costos Mano de Obra de Reparación de Vehículos', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Reporte Semanal de Trabajos Realizados en Chapisteria', icon: 'info', url: 'hoalalalal', disabled: true },
  ];
}
