import { Component, OnInit, Inject } from '@angular/core';
import {
  MatDialog,
  MatDialogRef,
  MAT_DIALOG_DATA,
} from '@angular/material/dialog';
import {
  OperacionesLiquidacionOtrosGastosComponent,
  OtrosGastosResult,
} from '../operaciones-otros-gastos/operaciones-liquidacion-otros-gastos/operaciones-liquidacion-otros-gastos.component';

export interface LiquidationDetail {
  inscripcion: number;
  rentaDiaria: number;
  otrasDeudas: number;
  panapass: number;
  totalDeudas: number;
  siniestros: number;
  otrosGastos: number;
  montoDevolver: number;
  montoDeudar: number;
}

@Component({
  selector: 'app-operaciones-liquidacion-cuenta',
  templateUrl: './operaciones-liquidacion-cuenta.component.html',
  styleUrls: ['./operaciones-liquidacion-cuenta.component.css'],
})
export class OperacionesLiquidacionCuentaComponent implements OnInit {
  // Variables de estado
  isLoading: boolean = true;

  // Almacenar los items de otros gastos modificados
  otrosGastosItems: any[] = [];

  // Inicializamos la data en null o con valores en 0 para evitar errores en template antes de cargar
  data: LiquidationDetail = {
    inscripcion: 0,
    rentaDiaria: 0,
    otrasDeudas: 0,
    panapass: 0,
    totalDeudas: 0,
    siniestros: 0,
    otrosGastos: 0,
    montoDevolver: 0,
    montoDeudar: 0,
  };

  constructor(
    public dialogRef: MatDialogRef<OperacionesLiquidacionCuentaComponent>,
    @Inject(MAT_DIALOG_DATA) public incomingData: any, // Por si pasas ID de conductor, etc.
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.getLiquidationData();
  }

  // Simulación de petición al Backend
  getLiquidationData(): void {
    this.isLoading = true;

    // Simulamos un delay de 1.5 segundos
    setTimeout(() => {
      // AQUÍ ESTÁN TUS DATOS QUEMADOS
      // Estos valores coinciden con la lógica: Fondos - Deudas = Devolver
      this.data = {
        inscripcion: 200.0, // Fondo
        rentaDiaria: 72.0, // Deuda
        otrasDeudas: 10.5, // Deuda
        panapass: 5.5, // Deuda
        siniestros: 20.0, // Deuda
        // Totales calculados (simulados)
        totalDeudas: 88.0, // 72 + 10.50 + 5.50
        otrosGastos: 0.0, // Input disabled

        // Resultados
        montoDevolver: 112.0, // 200 - 88
        montoDeudar: 0.0,
      };

      this.isLoading = false;
    }, 1500);
  }

  // Acción para el botón del "ojo" o "más" en Otros Gastos
  openOtrosGastos(): void {
    const dialogRef = this.dialog.open(
      OperacionesLiquidacionOtrosGastosComponent,
      {
        width: '850px',
        maxWidth: '95vw',
        maxHeight: '85vh',
        data: {
          gastosItems: this.otrosGastosItems, // Pasar los items guardados para persistir
        },
      }
    );

    dialogRef.afterClosed().subscribe((result: OtrosGastosResult | null) => {
      if (result) {
        // Guardar los items modificados
        this.otrosGastosItems = result.items;

        // Actualizar el valor de otros gastos
        this.data.otrosGastos = result.totalOtrosGastos;

        // Recalcular los montos
        this.recalcularMontos();

        console.log('Otros gastos actualizados:', result);
      }
    });
  }

  // Recalcula los montos después de actualizar otros gastos
  private recalcularMontos(): void {
    const totalFondos = this.data.inscripcion;
    const totalDeudas = this.data.totalDeudas + this.data.otrosGastos;

    if (totalFondos >= totalDeudas) {
      this.data.montoDevolver = totalFondos - totalDeudas;
      this.data.montoDeudar = 0;
    } else {
      this.data.montoDevolver = 0;
      this.data.montoDeudar = totalDeudas - totalFondos;
    }
  }

  // Acción de Imprimir
  imprimir(): void {
    console.log('Imprimiendo liquidación...');
    window.print(); // Funcionalidad nativa básica del navegador
  }

  // Acción de Confirmar/Aceptar
  aceptar(): void {
    console.log('Liquidación aceptada');
    // Retornamos la data incluyendo los otros gastos modificados
    this.dialogRef.close({
      accepted: true,
      data: this.data,
      otrosGastosItems: this.otrosGastosItems,
    });
  }
}
