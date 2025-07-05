import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-cnt',
  templateUrl: './opciones-cnt.component.html',
  styleUrls: ['./opciones-cnt.component.css']
})
export class OpcionesCntComponent {
  almacen = [
    { name: 'Resumen O.Trabajo (Piezas/Gastos)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Resumen Facturación (Contado)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Utilidad Grupo/Código (Costo de Venta)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Consecutivo de Documentos', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Relación de Documentos (Detalle)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Inventario por Grupo (Año/Periodo)', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Generar Documentos Contables (Peachtree)', icon: 'info', url: 'hoalalalal', disabled: true }
  ];

  consultas = [
    { name: 'Provisional', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Copia Recibo', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Ventas Contado', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Consecutivo', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Detalle General', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Resumen Empresa', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Resumen Cajero', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Cajero/Empresa', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Transferencias', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Resumen Cierre', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Cuadre Caja', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Cierre Caja', icon: 'info', url: 'hoalalalal', disabled: true }
  ];
}
