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
import { ApiService } from 'src/app/services/api.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpErrorResponse } from '@angular/common/http';

export interface LiquidationDetail {
  registration: number;
  daily_rent: number;
  accidents: number;
  other_debts: number;
  panapass: number;
  total_debt: number;
  other_expenses: number;
  owed_to_driver: number;
  owed_by_driver: number;
}

interface dialogData {
  companyCode: string;
  vehicleNumber: string;
  driverNumber: string;
}

@Component({
  selector: 'app-operaciones-liquidacion-cuenta',
  templateUrl: './operaciones-liquidacion-cuenta.component.html',
  styleUrls: ['./operaciones-liquidacion-cuenta.component.css'],
})
export class OperacionesLiquidacionCuentaComponent implements OnInit {
  isLoading: boolean = true;

  // TODO: Modificar interface en any.
  otrosGastosItems: any[] = [];

  data: LiquidationDetail = {
    registration: 0,
    daily_rent: 0,
    other_debts: 0,
    panapass: 0,
    total_debt: 0,
    accidents: 0,
    other_expenses: 0,
    owed_to_driver: 0,
    owed_by_driver: 0,
  };

  constructor(
    public dialogRef: MatDialogRef<OperacionesLiquidacionCuentaComponent>,
    @Inject(MAT_DIALOG_DATA) public incomingData: dialogData, 
    private dialog: MatDialog,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.getLiquidationData();
  }

  getLiquidationData(): void {
    this.isLoading = true;

    if(this.incomingData.companyCode === '' || this.incomingData.vehicleNumber === '' || this.incomingData.driverNumber === '') {
      this.isLoading = false;
      this.openSnackbar('Error al obtener la información de la liquidación.');
      return;
    }

    this.apiService.getData(`operations/remove-driver/${this.incomingData.companyCode}/${this.incomingData.vehicleNumber}/${this.incomingData.driverNumber}`).subscribe({
      next: (data: LiquidationDetail) => {
        this.data = data;
        this.isLoading = false;
      },
      error: (error: HttpErrorResponse) => {
        this.isLoading = false;
        this.openSnackbar('Error al obtener la información de la liquidación.');
      },
    });
  }

  // Acción para el botón del "ojo" o "más" en Otros Gastos
  openOtrosGastos(): void {
    // const dialogRef = this.dialog.open(
    //   OperacionesLiquidacionOtrosGastosComponent,
    //   {
    //     width: '850px',
    //     maxWidth: '95vw',
    //     maxHeight: '85vh',
    //     data: {
    //       gastosItems: this.otrosGastosItems, // Pasar los items guardados para persistir
    //     },
    //   }
    // );

    // dialogRef.afterClosed().subscribe((result: OtrosGastosResult | null) => {
    //   if (result) {
    //     // Guardar los items modificados
    //     this.otrosGastosItems = result.items;

    //     // Actualizar el valor de otros gastos
    //     this.data.otrosGastos = result.totalOtrosGastos;

    //     // Recalcular los montos
    //     this.recalcularMontos();

    //     console.log('Otros gastos actualizados:', result);
    //   }
    // });
  }

  // Recalcula los montos después de actualizar otros gastos
  private recalcularMontos(): void {
    // const totalFondos = this.data.inscripcion;
    // const totalDeudas = this.data.totalDeudas + this.data.otrosGastos;

    // if (totalFondos >= totalDeudas) {
    //   this.data.montoDevolver = totalFondos - totalDeudas;
    //   this.data.montoDeudar = 0;
    // } else {
    //   this.data.montoDevolver = 0;
    //   this.data.montoDeudar = totalDeudas - totalFondos;
    // }
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

  openSnackbar(message: string) {
    this.snackBar.open(message, 'Cerrar', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'top',
    })
  }
}
