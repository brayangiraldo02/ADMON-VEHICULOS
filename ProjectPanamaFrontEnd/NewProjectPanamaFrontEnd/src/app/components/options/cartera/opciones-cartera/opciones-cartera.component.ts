import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-cartera',
  templateUrl: './opciones-cartera.component.html',
  styleUrls: ['./opciones-cartera.component.css']
})
export class OpcionesCarteraComponent {
  consultas = [
    { name: 'Relación de Notas Débito/Crédito', icon: 'info', url: 'hoalalalal' },
    { name: 'Relación de Cruces', icon: 'info', url: 'hoalalalal' },
    { name: 'Informe Cuotas Pagas de Conductores', icon: 'info', url: 'hoalalalal' },
    { name: 'Movimiento de Cuentas por Clientes', icon: 'info', url: 'hoalalalal' },
    { name: 'Estado de Cuenta de Clientes', icon: 'info', url: 'hoalalalal' },
    { name: 'Cartera General', icon: 'info', url: 'hoalalalal' },
    { name: 'Análisis de Vencimientos', icon: 'info', url: 'hoalalalal' },
    { name: 'Resumen por Cliente/Empresa', icon: 'info', url: 'hoalalalal' },
    { name: 'Resumen por Empresa', icon: 'info', url: 'hoalalalal' },
    { name: 'Actualizar Saldos Conductores (Cobros)', icon: 'info', url: 'hoalalalal' },
    { name: 'Cuadre de Cartera', icon: 'info', url: 'hoalalalal' },
    { name: 'Cierre del Periodo (Mensual)', icon: 'info', url: 'hoalalalal' }
  ];

  documentos = [
    { name: 'Documentos en Cartera', icon: 'info', url: 'hoalalalal' },
    { name: 'Notas Débito', icon: 'info', url: 'hoalalalal' },
    { name: 'Notas Crédito', icon: 'info', url: 'hoalalalal' },
    { name: 'Actualizar Cuotas Pagas de Conductores', icon: 'info', url: 'hoalalalal' }
  ];

  cruces = [
    { name: 'Cruce Ahorros con Diarios', icon: 'info', url: 'hoalalalal' },
    { name: 'Cruce Feriados con Diarios', icon: 'info', url: 'hoalalalal' },
    { name: 'Cruce Inscripción con Diarios', icon: 'info', url: 'hoalalalal' },
    { name: 'Cruce Inscripción con Siniestros', icon: 'info', url: 'hoalalalal' },
    { name: 'Trasladar Diarios a Siniestros', icon: 'info', url: 'hoalalalal' },
    { name: 'Llevar Saldo Siniestros a Nuevo Contrato', icon: 'info', url: 'hoalalalal' },
  ];
}
