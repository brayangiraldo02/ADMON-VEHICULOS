import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-llavero',
  templateUrl: './opciones-llavero.component.html',
  styleUrls: ['./opciones-llavero.component.css']
})
export class OpcionesLlaveroComponent {
  options = [
    { name: 'Consultar Llavero de una Empresa', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Funcionarios para el Manejo de Llaves', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Préstamo de Llaves', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Devolución de Llaves', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Informe de Llaves Prestados', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Consultar Historial de una Llave', icon: 'info', url: 'hoalalalal', disabled: true }
  ];
}
