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

  consultas = [
    { name: 'Provisional', icon: 'info', url: 'hoalalalal' },
    { name: 'Copia Recibo', icon: 'info', url: 'hoalalalal' },
    { name: 'Ventas Contado', icon: 'info', url: 'hoalalalal' },
    { name: 'Consecutivo', icon: 'info', url: 'hoalalalal' },
    { name: 'Detalle General', icon: 'info', url: 'hoalalalal' },
    { name: 'Resumen Empresa', icon: 'info', url: 'hoalalalal' },
    { name: 'Resumen Cajero', icon: 'info', url: 'hoalalalal' },
    { name: 'Cajero/Empresa', icon: 'info', url: 'hoalalalal' },
    { name: 'Transferencias', icon: 'info', url: 'hoalalalal' },
    { name: 'Resumen Cierre', icon: 'info', url: 'hoalalalal' },
    { name: 'Cuadre Caja', icon: 'info', url: 'hoalalalal' },
    { name: 'Cierre Caja', icon: 'info', url: 'hoalalalal' }
  ];
}
