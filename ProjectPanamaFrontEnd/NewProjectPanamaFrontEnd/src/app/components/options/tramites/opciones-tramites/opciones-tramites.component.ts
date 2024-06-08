import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-tramites',
  templateUrl: './opciones-tramites.component.html',
  styleUrls: ['./opciones-tramites.component.css']
})
export class OpcionesTramitesComponent {

  operaciones = [
    { name: 'Entrega de Vehículos a Conductores', icon: 'info', url: 'hoalalalal' },
    { name: 'Generar Contrato y Declaración Jurada', icon: 'info', url: 'hoalalalal' },
    { name: 'Cambiar de Estado a un Vehículo', icon: 'info', url: 'hoalalalal' },
    { name: 'Bajar Conductor del Vehículo (Culminación del contrato)', icon: 'info', url: 'hoalalalal' },
    { name: 'Corregir Kilometraje Actual al Vehículo', icon: 'info', url: 'hoalalalal' },
    { name: 'Apertura de Cuenta por Cobrar a un Conductor', icon: 'info', url: 'hoalalalal' },
  ];

  formatos_tramites = [
    { name: 'Cambio de Unidad', icon: 'info', url: 'hoalalalal' },
    { name: 'Memorial de Transferencia', icon: 'info', url: 'hoalalalal' },
    { name: 'Liberación y Retención', icon: 'info', url: 'hoalalalal' },
    { name: 'Actualización', icon: 'info', url: 'hoalalalal' }
  ];

  control_cupos = [
    { name: 'Organizaciones (Piqueras)', icon: 'info', url: 'hoalalalal' },
    { name: 'Revisión General de Cupos', icon: 'info', url: 'hoalalalal' }
  ];

  seguros = [
    { name: 'Tabla Aseguradoras', icon: 'info', url: 'hoalalalal' },
    { name: 'Actualización de Polizas', icon: 'info', url: 'hoalalalal' }
  ];

  seguimiento_traspasos = [
    { name: 'Generar Documento Finiquito', icon: 'info', url: 'hoalalalal' },
    { name: 'Firma y Escaneo Documentos después de Pagos', icon: 'info', url: 'hoalalalal' },
    { name: 'Preparar y Escaneo Documentos para Notariar', icon: 'info', url: 'hoalalalal' },
    { name: 'Reparar Documentos Originales para Traspaso', icon: 'info', url: 'hoalalalal' },
    { name: 'Realizar Trámite Traspaso (Municipio y Transito)', icon: 'info', url: 'hoalalalal' },
    { name: 'Entrega de Documentos (Nuevo Propietario)', icon: 'info', url: 'hoalalalal' }
  ];
}
