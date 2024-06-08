import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-utilidades',
  templateUrl: './opciones-utilidades.component.html',
  styleUrls: ['./opciones-utilidades.component.css']
})
export class OpcionesUtilidadesComponent {
  tablas = [
    { name: 'Almacenes/Proveedores', icon: 'info', url: 'hoalalalal' },
    { name: 'Centrales de Vehículos', icon: 'info', url: 'hoalalalal' },
    { name: 'Ciudades', icon: 'info', url: 'hoalalalal' },
    { name: 'Clientes (Ventas Contado)', icon: 'info', url: 'hoalalalal' },
    { name: 'Estados de Vehículos', icon: 'info', url: 'hoalalalal' },
    { name: 'Festivos y Dominicales', icon: 'info', url: 'hoalalalal' },
    { name: 'Inspectores', icon: 'info', url: 'hoalalalal' },
    { name: 'Items - CxP de Conductores', icon: 'info', url: 'hoalalalal' },
    { name: 'Items - Ficha Técnica', icon: 'info', url: 'hoalalalal' },
    { name: 'Marcas de Vehículos', icon: 'info', url: 'hoalalalal' },
    { name: 'Mecánicos', icon: 'info', url: 'hoalalalal' },
    { name: 'Tipos de Documentos (Inv)', icon: 'info', url: 'hoalalalal' },
    { name: 'Vendedores', icon: 'info', url: 'hoalalalal' },
    { name: 'Zonas', icon: 'info', url: 'hoalalalal' },
  ];

  utilidades = [
    { name: 'Habilitar Documentos', icon: 'info', url: 'hoalalalal' },
    { name: 'Anular Documentos', icon: 'info', url: 'hoalalalal' },
    { name: 'Anular Recibos de Caja', icon: 'info', url: 'hoalalalal' },
    { name: 'Cambiarle de Unidad al Conductor', icon: 'info', url: 'hoalalalal' },
    { name: 'Cambiarle de Numero a una Unidad', icon: 'info', url: 'hoalalalal' },
    { name: 'Cargar Saldos Iniciales de los Conductores', icon: 'info', url: 'hoalalalal' },
    { name: 'Actualización de Plantillas', icon: 'info', url: 'hoalalalal' },
    { name: 'Ver Mensajes de Error', icon: 'info', url: 'hoalalalal' },
  ];

  seguridad = [
    { name: 'Usuarios del Sistema', icon: 'info', url: 'hoalalalal' },
    { name: 'Permisos al Detalle', icon: 'info', url: 'hoalalalal' }
  ];
}
