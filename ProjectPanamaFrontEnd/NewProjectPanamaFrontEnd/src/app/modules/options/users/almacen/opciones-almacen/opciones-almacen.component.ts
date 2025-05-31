import { Component } from '@angular/core';

@Component({
  selector: 'app-opciones-almacen',
  templateUrl: './opciones-almacen.component.html',
  styleUrls: ['./opciones-almacen.component.css']
})
export class OpcionesAlmacenComponent {
  conteos_aleatorios = [
    { name: 'Generar Informe para Conteos Aleatorios', icon: 'info', url: 'hoalalalal', disabled: true },
    { name: 'Registro de Conteos Aleatorios', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Informe Diferencias de Conteos', icon: 'info', url: 'hoalalalal', disabled: true  }
  ];

  inventario_fisico = [
    { name: 'Informe Para Toma de Inventario Físico', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Registro del Inventario Físico', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Informe Comparativo Físico Vs. Sistema', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Generar Ajustes (Entrada/Salida)', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Trasladar Inventario Físico Como Inicial', icon: 'info', url: 'hoalalalal', disabled: true  },
  ];

  movimientos = [
    { name: 'Compras Generales', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Devolución de Compras', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Cotizaciones', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Ordenes de Pedido', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Generar O. Trabajo desde Pedido', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Ordenes de Trabajo', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Devolución de Ordenes de Trabajo', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Generar Factura desde O. Trabajo', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Facturación (Contado)', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Devolución Facturas', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Ajustes de Entrada', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Ajustes de Salida', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Traslados de Entrada', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Traslados de Salida', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Consumos de Almacén', icon: 'info', url: 'hoalalalal', disabled: true  },
  ];

  especiales = [
    { name: 'Actualizar C.P.M e Indicadores', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Informe de Listas de Precios', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Balance de Productos', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Informe Consumo Promedio Mensual', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Solicitud de Pedidos', icon: 'info', url: 'hoalalalal', disabled: true  },
  ];

  consultas = [
    { name: 'Resumen O.Trabajo (Piezas/Gastos)', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Resumen Facturación (Contado)', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Total Ordenes Empresa/Grupo/Codigo', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Resumen de Ventas por Cliente', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Frecuencia Repuestos por Vehículo', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Evolución General O.Trabajo x Taller', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Utilidad Grupo/Codigo (Costo de Venta)', icon: 'info', url: 'hoalalalal', disabled: true  },
  ];

  generales = [
    { name: 'Generar Documentos Contables', icon: 'info', url: 'hoalalalal', disabled: true  },
    { name: 'Cierre Anual de Inventarios', icon: 'info', url: 'hoalalalal', disabled: true  },
  ]
}
