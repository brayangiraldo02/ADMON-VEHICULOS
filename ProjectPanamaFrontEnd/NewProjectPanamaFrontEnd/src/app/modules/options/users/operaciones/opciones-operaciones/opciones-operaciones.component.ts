import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-operaciones',
  templateUrl: './opciones-operaciones.component.html',
  styleUrls: ['./opciones-operaciones.component.css']
})
export class OpcionesOperacionesComponent {
  options = [
    { name: 'Entrega de Vehículo al Conductor', icon: 'info', url: 'EntregaVehiculoConductor', disabled: false },
    { name: 'Generar Contrato y Declaración Jurada', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Crear Cuenta de Diario al Conductor (Anticipo de Cuenta)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Cambiar de Estado a un Vehículo', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Prestamo de Vehículo al Conductor', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Devolución de Vehículos Prestados', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Bajar Conductor del Vehículo (Culminación del Contrato)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Corregir Kilometraje Actual al Vehículo', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Apertura de Cuenta por Cobrar a un Conductor', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Hoja de Inspección del Vehículo', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Hoja de Vida del Vehículo', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Hoja de Vida del Conductor', icon: 'info', url: 'hoalalalal', disabled: true }
  ];

  selectOptionModal: string = '';

  entregaVehiculoConductor: boolean = false;

  constructor() { }

  ngOnInit(): void {
  }

  selectOption(option: string) {
    switch (option) {
      case 'EntregaVehiculoConductor':
        console.log('Entrega de Vehículo al Conductor');
        this.entregaVehiculoConductor = true;
        this.selectOptionModal = option;
        document.documentElement.style.overflow = 'hidden';
        document.body.style.overflow = 'hidden';
        break;
      case 'Generar Contrato y Declaración Jurada':
        console.log('Generar Contrato y Declaración Jurada');
        break;
      case 'Crear Cuenta de Diario al Conductor (Anticipo de Cuenta)':
        console.log('Crear Cuenta de Diario al Conductor (Anticipo de Cuenta)');
        break;
      case 'Cambiar de Estado a un Vehículo':
        console.log('Cambiar de Estado a un Vehículo');
        break;
      case 'Prestamo de Vehículo al Conductor':
        console.log('Prestamo de Vehículo al Conductor');
        break;
      case 'Devolución de Vehículos Prestados':
        console.log('Devolución de Vehículos Prestados');
        break;
      case 'Bajar Conductor del Vehículo (Culminación del Contrato)':
        console.log('Bajar Conductor del Vehículo (Culminación del Contrato)');
        break;
      case 'Corregir Kilometraje Actual al Vehículo':
        console.log('Corregir Kilometraje Actual al Vehículo');
        break;
      case 'Apertura de Cuenta por Cobrar a un Conductor':
        console.log('Apertura de Cuenta por Cobrar a un Conductor');
        break;
      case 'Hoja de Inspección del Vehículo':
        console.log('Hoja de Inspección del Vehículo');
        break;
      case 'Hoja de Vida del Vehículo':
        console.log('Hoja de Vida del Vehículo');
        break;
      case 'Hoja de Vida del Conductor':
        console.log('Hoja de Vida del Conductor');
        break;
    }
  }

  hideModal() {
    switch (this.selectOptionModal) {
      case 'EntregaVehiculoConductor':
        this.entregaVehiculoConductor = false;
        document.documentElement.style.overflow = '';
        document.body.style.overflow = '';
        break;
    }
  }
}
