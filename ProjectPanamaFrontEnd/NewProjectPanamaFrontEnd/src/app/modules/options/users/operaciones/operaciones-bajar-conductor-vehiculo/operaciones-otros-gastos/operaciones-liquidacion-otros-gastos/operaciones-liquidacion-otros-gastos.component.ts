import { Component, Inject, OnInit } from '@angular/core';
import {
  MatDialog,
  MatDialogRef,
  MAT_DIALOG_DATA,
} from '@angular/material/dialog';
import { OperacionesExplicacionOtrosGastosComponent } from '../operaciones-explicacion-otros-gastos/operaciones-explicacion-otros-gastos.component';

export interface OtroGastoItem {
  codigo: string;
  nombre: string;
  explicacion: string;
  valor: number;
}

export interface OtrosGastosResult {
  items: OtroGastoItem[];
  totalOtrosGastos: number;
}

@Component({
  selector: 'app-operaciones-liquidacion-otros-gastos',
  templateUrl: './operaciones-liquidacion-otros-gastos.component.html',
  styleUrls: ['./operaciones-liquidacion-otros-gastos.component.css'],
})
export class OperacionesLiquidacionOtrosGastosComponent implements OnInit {
  // Columnas a mostrar en la tabla
  displayedColumns: string[] = ['codigo', 'nombre', 'explicacion', 'valor'];

  // Datos mockup basados en la imagen de referencia
  gastosItems: OtroGastoItem[] = [
    { codigo: '05', nombre: 'ABANDONO', explicacion: '', valor: 0 },
    { codigo: '11', nombre: 'CONFECCIÓN DE LLAVE', explicacion: '', valor: 0 },
    {
      codigo: '19',
      nombre: 'CUENTA POR PAGAR POR COLISIÓN CULPABLE',
      explicacion: '',
      valor: 0,
    },
    {
      codigo: '18',
      nombre: 'CUENTAS DIARIAS PASADAS A SINIESTRO',
      explicacion: '',
      valor: 0,
    },
    {
      codigo: '06',
      nombre: 'CUENTAS POR PAGAR (SINIESTRO)',
      explicacion: '',
      valor: 0,
    },
    {
      codigo: '07',
      nombre: 'CUENTAS POR PAGAR DEL SISTEMA NUEVO',
      explicacion: '',
      valor: 0,
    },
    {
      codigo: '13',
      nombre: 'DEDUCIBLE POR COLISIÓN',
      explicacion: '',
      valor: 0,
    },
    { codigo: '28', nombre: 'DESESTIMIENTO', explicacion: '', valor: 0 },
    { codigo: '29', nombre: 'DESPOJO', explicacion: '', valor: 0 },
    {
      codigo: '15',
      nombre: 'DEVOLUCIÓN DE DEPÓSITO EN GARANTÍA',
      explicacion: '',
      valor: 0,
    },
    { codigo: '16', nombre: 'DIARIOS PENDIENTES', explicacion: '', valor: 0 },
    { codigo: '41', nombre: 'FORROS DE VEHÍCULO', explicacion: '', valor: 0 },
    { codigo: '32', nombre: 'GASTO DE CAJA CHICA', explicacion: '', valor: 0 },
    { codigo: '62', nombre: 'LIMPIEZA DE VEHÍCULO', explicacion: '', valor: 0 },
    {
      codigo: '21',
      nombre: 'MANO DE OBRA DE CHAPISTERÍA',
      explicacion: '',
      valor: 0,
    },
    { codigo: '27', nombre: 'MOROSIDAD', explicacion: '', valor: 0 },
    { codigo: '01', nombre: 'NOTARÍA DE CONTRATO', explicacion: '', valor: 0 },
  ];

  selectedItem: OtroGastoItem | null = null;

  constructor(
    public dialogRef: MatDialogRef<OperacionesLiquidacionOtrosGastosComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { gastosItems?: OtroGastoItem[] },
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    // Si hay items guardados, aplicarlos a la lista
    if (this.data.gastosItems && this.data.gastosItems.length > 0) {
      this.data.gastosItems.forEach((savedItem) => {
        const item = this.gastosItems.find(
          (g) => g.codigo === savedItem.codigo
        );
        if (item) {
          item.explicacion = savedItem.explicacion;
          item.valor = savedItem.valor;
        }
      });
    }
  }

  // Abre el dialog de explicación cuando se hace click en un item
  openExplicacion(item: OtroGastoItem): void {
    this.selectedItem = item;

    const dialogRef = this.dialog.open(
      OperacionesExplicacionOtrosGastosComponent,
      {
        width: '450px',
        data: {
          codigo: item.codigo,
          nombre: item.nombre,
          explicacion: item.explicacion,
          valor: item.valor,
        },
      }
    );

    dialogRef
      .afterClosed()
      .subscribe(
        (result: { explicacion: string; valor: number } | undefined) => {
          if (result) {
            // Actualizar el item con los datos ingresados
            item.explicacion = result.explicacion;
            item.valor = result.valor;
          }
          this.selectedItem = null;
        }
      );
  }

  // Calcula el total de otros gastos
  get totalOtrosGastos(): number {
    return this.gastosItems.reduce((sum, item) => sum + item.valor, 0);
  }

  // Retorna solo los items que han sido modificados (tienen valor > 0 o explicación)
  get itemsModificados(): OtroGastoItem[] {
    return this.gastosItems.filter(
      (item) => item.valor > 0 || item.explicacion.trim() !== ''
    );
  }

  // Cierra el dialog y retorna los datos al componente padre
  aceptar(): void {
    const result: OtrosGastosResult = {
      items: this.itemsModificados,
      totalOtrosGastos: this.totalOtrosGastos,
    };
    this.dialogRef.close(result);
  }

  // Cierra el dialog sin guardar cambios
  salir(): void {
    this.dialogRef.close(null);
  }
}
