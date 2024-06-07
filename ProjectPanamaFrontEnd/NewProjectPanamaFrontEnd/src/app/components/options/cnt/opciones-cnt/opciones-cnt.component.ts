import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-cnt',
  templateUrl: './opciones-cnt.component.html',
  styleUrls: ['./opciones-cnt.component.css']
})
export class OpcionesCntComponent {
  almacen = [
    { name: 'Resumen O.Trabajo (Piezas/Gastos)', icon: 'info', url: 'hoalalalal' },
    { name: 'Resumen Facturación (Contado)', icon: 'info', url: 'hoalalalal' },
    { name: 'Utilidad Grupo/Código (Costo de Venta)', icon: 'info', url: 'hoalalalal' },
    { name: 'Consecutivo de Documentos', icon: 'info', url: 'hoalalalal' },
    { name: 'Relación de Documentos (Detalle)', icon: 'info', url: 'hoalalalal' },
    { name: 'Inventario por Grupo (Año/Periodo)', icon: 'info', url: 'hoalalalal' },
    { name: 'Generar Documentos Contables (Peachtree)', icon: 'info', url: 'hoalalalal' }
  ];

  propietarios = [
    { name: 'Relación de Vehículos por Propietario', icon: 'info', url: 'hoalalalal' },
    { name: 'Estado de la Flota por Propietario', icon: 'info', url: 'hoalalalal' },
    { name: 'Reporte de Ingresos y Egresos (PyG)', icon: 'info', url: 'hoalalalal' }
  ];
}
