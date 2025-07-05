import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-utilidades',
  templateUrl: './opciones-utilidades.component.html',
  styleUrls: ['./opciones-utilidades.component.css']
})
export class OpcionesUtilidadesComponent {
  tablas = [
    { name: 'Almacenes/Proveedores', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Centrales de Vehículos', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Ciudades', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Clientes (Ventas Contado)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Estados de Vehículos', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Festivos y Dominicales', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Inspectores', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Items - CxP de Conductores', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Items - Ficha Técnica', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Marcas de Vehículos', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Mecánicos', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Tipos de Documentos (Inv)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Vendedores', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Zonas', icon: 'info', url: 'hoalalalal', disabled: true },
  ];

  utilidades = [
    { name: 'Habilitar Documentos', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Anular Documentos', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Anular Recibos de Caja', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Cambiarle de Unidad al Conductor', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Cambiarle de Numero a una Unidad', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Cargar Saldos Iniciales de los Conductores', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Actualización de Plantillas', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Ver Mensajes de Error', icon: 'info', url: 'hoalalalal', disabled: true },
  ];

  seguridad = [
    { name: 'Usuarios del Sistema', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Permisos al Detalle', icon: 'info', url: 'hoalalalal', disabled: true }
  ];
}
