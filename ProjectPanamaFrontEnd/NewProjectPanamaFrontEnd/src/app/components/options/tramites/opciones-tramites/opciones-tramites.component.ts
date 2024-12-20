import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-tramites',
  templateUrl: './opciones-tramites.component.html',
  styleUrls: ['./opciones-tramites.component.css']
})
export class OpcionesTramitesComponent {

  operaciones = [
    { name: 'Entrega de Vehículos a Conductores', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Generar Contrato y Declaración Jurada', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Cambiar de Estado a un Vehículo', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Bajar Conductor del Vehículo (Culminación del contrato)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Corregir Kilometraje Actual al Vehículo', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Apertura de Cuenta por Cobrar a un Conductor', icon: 'info', url: 'hoalalalal', disabled: true },
  ];

  formatos_tramites = [
    { name: 'Cambio de Unidad', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Memorial de Transferencia', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Liberación y Retención', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Actualización', icon: 'info', url: 'hoalalalal', disabled: true }
  ];

  control_cupos = [
    { name: 'Organizaciones (Piqueras)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Revisión General de Cupos', icon: 'info', url: 'hoalalalal', disabled: true }
  ];

  seguros = [
    { name: 'Tabla Aseguradoras', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Actualización de Polizas', icon: 'info', url: 'hoalalalal', disabled: true }
  ];

  seguimiento_traspasos = [
    { name: 'Generar Documento Finiquito', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Firma y Escaneo Documentos después de Pagos', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Preparar y Escaneo Documentos para Notariar', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Reparar Documentos Originales para Traspaso', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Realizar Trámite Traspaso (Municipio y Transito)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Entrega de Documentos (Nuevo Propietario)', icon: 'info', url: 'hoalalalal', disabled: true }
  ];
}
