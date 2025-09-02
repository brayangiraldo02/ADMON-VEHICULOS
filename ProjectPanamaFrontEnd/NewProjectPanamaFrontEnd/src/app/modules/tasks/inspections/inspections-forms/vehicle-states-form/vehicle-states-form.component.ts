import { Component } from '@angular/core';

@Component({
  selector: 'app-vehicle-states-form',
  templateUrl: './vehicle-states-form.component.html',
  styleUrls: ['./vehicle-states-form.component.css'],
})
export class VehicleStatesFormComponent {
  checklistItems = [
    { id: 'alfombra', label: 'Alfombra', value: null },
    { id: 'copas', label: 'Copas/Rines', value: null },
    { id: 'extinguidor', label: 'Extinguidor', value: null },
    { id: 'antena', label: 'Antena', value: null },
    { id: 'lamparas', label: 'Lámparas', value: null },
    { id: 'triangulo', label: 'Triángulo', value: null },
    { id: 'gato', label: 'Gato', value: null },
    { id: 'pipa', label: 'Pipa', value: null },
    { id: 'copas', label: 'Copas', value: null },
    { id: 'llanta-repuestos', label: 'Llanta de Repuestos', value: null },
    { id: 'placa-municipal', label: 'Placa Municipal', value: null },
    { id: 'caratula-radio', label: 'Carátula de Radio', value: null },
    { id: 'registro-vehiculo', label: 'Registro Vehículo', value: null },
    { id: 'revisado', label: 'Revisado', value: null },
    { id: 'pago-municipio', label: 'Pago Municipio', value: null },
    { id: 'formato-colisiones-menores', label: 'Formato de Colisiones Menores', value: null },
    { id: 'poliza-seguros', label: 'Póliza de Seguros', value: null },
    { id: 'luces-delanteras', label: 'Luces Delanteras', value: null },
    { id: 'luces-traseras', label: 'Luces Traseras', value: null },
    { id: 'vidrios', label: 'Vidrios', value: null },
    { id: 'retrovisor', label: 'Retrovisor', value: null },
    { id: 'gps', label: 'GPS', value: null },
  ];
}
