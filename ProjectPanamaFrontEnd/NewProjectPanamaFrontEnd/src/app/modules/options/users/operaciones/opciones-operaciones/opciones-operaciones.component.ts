import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { OperacionesContratoDeclaracionJuradaComponent } from '../operaciones-contrato-declaracion-jurada/operaciones-contrato-declaracion-jurada.component';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { OperacionesCrearCuentaDiarioConductorComponent } from '../operaciones-crear-cuenta-diario-conductor/operaciones-crear-cuenta-diario-conductor.component';
import { OperacionesCambiarEstadoVehiculoComponent } from '../operaciones-cambiar-estado-vehiculo/operaciones-cambiar-estado-vehiculo.component';
import { OperacionesCambiarPatioVehiculoComponent } from '../operaciones-cambiar-patio-vehiculo/operaciones-cambiar-patio-vehiculo.component';
import { OperacionesCorregirKilometrajeActualComponent } from '../operaciones-corregir-kilometraje-actual/operaciones-corregir-kilometraje-actual.component';

@Component({
  selector: 'app-opciones-operaciones',
  templateUrl: './opciones-operaciones.component.html',
  styleUrls: ['./opciones-operaciones.component.css']
})
export class OpcionesOperacionesComponent {
  options = [
    { name: 'Entrega de Vehículo al Conductor', icon: 'info', url: 'EntregaVehiculoConductor', disabled: false },
    { name: 'Generar Contrato y Declaración Jurada', icon: 'info', url: 'ContratoDeclaracionJurada', disabled: false },
    { name: 'Crear Cuenta de Diario al Conductor (Anticipo de Cuenta)', icon: 'info', url: 'CrearCuentaDiarioConductor', disabled: false },
    { name: 'Cambiar de Estado a un Vehículo', icon: 'info', url: 'CambiarEstadoVehiculo', disabled: false },
    { name: 'Cambiar de Patio a un Vehículo', icon: 'info', url: 'CambiarPatioVehiculo', disabled: false },
    { name: 'Prestamo de Vehículo al Conductor', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Devolución de Vehículos Prestados', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Bajar Conductor del Vehículo (Culminación del Contrato)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Corregir Kilometraje Actual al Vehículo', icon: 'info', url: 'CorregirKilometrajeActualVehiculo', disabled: false },
    { name: 'Apertura de Cuenta por Cobrar a un Conductor', icon: 'info', url: 'hoalalalal', disabled: true },
  ];

  selectOptionModal: string = '';

  entregaVehiculoConductor: boolean = false;

  constructor(
    private dialog: MatDialog,
    private breakpointObserver: BreakpointObserver
  ) { }

  ngOnInit(): void {
  }

  selectOption(option: string) {
    const isSmallScreen = this.breakpointObserver.isMatched(Breakpoints.Small);
    const isXsmallScreen = this.breakpointObserver.isMatched(Breakpoints.XSmall);
    const dialogWidth = isSmallScreen || isXsmallScreen ? '90vw' : '60%';

    switch (option) {
      case 'EntregaVehiculoConductor':
        console.log('Entrega de Vehículo al Conductor');
        this.entregaVehiculoConductor = true;
        this.selectOptionModal = option;
        document.documentElement.style.overflow = 'hidden';
        document.body.style.overflow = 'hidden';
        break;
      case 'ContratoDeclaracionJurada':
        this.dialog.open(OperacionesContratoDeclaracionJuradaComponent,
          {
            width: dialogWidth,
          }
        );
        break;
      case 'CrearCuentaDiarioConductor':
        this.dialog.open(OperacionesCrearCuentaDiarioConductorComponent,
          {
            width: dialogWidth,
          }
        );
        break;
      case 'CambiarEstadoVehiculo':
        this.dialog.open(OperacionesCambiarEstadoVehiculoComponent,
          {
            width: dialogWidth,
          }
        );
        break;
      case 'CambiarPatioVehiculo':
        this.dialog.open(OperacionesCambiarPatioVehiculoComponent,
          {
            width: dialogWidth,
          }
        );
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
      case 'CorregirKilometrajeActualVehiculo':
        this.dialog.open(OperacionesCorregirKilometrajeActualComponent,
          {
            width: dialogWidth,
          }
        );
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
