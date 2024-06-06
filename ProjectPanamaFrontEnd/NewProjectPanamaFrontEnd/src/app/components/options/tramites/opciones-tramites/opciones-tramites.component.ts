import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-tramites',
  templateUrl: './opciones-tramites.component.html',
  styleUrls: ['./opciones-tramites.component.css']
})
export class OpcionesTramitesComponent {

  operaciones = [
    { name: 'Entrega de Vehículos a Conductores', icon: '../../../../assets/icons/gerencia.svg', url: 'hoalalalal' },
    { name: 'Generar Contrato y Declaración Jurada', icon: '../../../../assets/icons/gastos.svg', url: 'hoalalalal' },
    { name: 'Cambiar de Estado a un Vehículo', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' },
    { name: 'Bajar Conductor del Vehículo (Culminación del contrato)', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' },
    { name: 'Corregir Kilometraje Actual al Vehículo', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' },
    { name: 'Apertura de Cuenta por Cobrar a un Conductor', icon: '../../../../assets/icons/gastos.svg', url: 'hoalalalal' },
  ];

  formatos_tramites = [
    { name: 'Cambio de Unidad', icon: '../../../../assets/icons/gerencia.svg', url: 'hoalalalal' },
    { name: 'Memorial de Transferencia', icon: '../../../../assets/icons/gastos.svg', url: 'hoalalalal' },
    { name: 'Liberación y Retención', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' },
    { name: 'Actualización', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' }
  ];

  control_cupos = [
    { name: 'Organizaciones (Piqueras)', icon: '../../../../assets/icons/gerencia.svg', url: 'hoalalalal' },
    { name: 'Revisión General de Cupos', icon: '../../../../assets/icons/gastos.svg', url: 'hoalalalal' }
  ];

  seguros = [
    { name: 'Tabla Aseguradoras', icon: '../../../../assets/icons/gerencia.svg', url: 'hoalalalal' },
    { name: 'Actualización de Polizas', icon: '../../../../assets/icons/gastos.svg', url: 'hoalalalal' }
  ];

  seguimiento_traspasos = [
    { name: 'Generar Documento Finiquito', icon: '../../../../assets/icons/gerencia.svg', url: 'hoalalalal' },
    { name: 'Firma y Escaneo Documentos después de Pagos', icon: '../../../../assets/icons/gastos.svg', url: 'hoalalalal' },
    { name: 'Preparar y Escaneo Documentos para Notariar', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' },
    { name: 'Reparar Documentos Originales para Traspaso', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' },
    { name: 'Realizar Trámite Traspaso (Municipio y Transito)', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal' },
    { name: 'Entrega de Documentos (Nuevo Propietario)', icon: '../../../../assets/icons/gastos.svg', url: 'hoalalalal' }
  ];
}
