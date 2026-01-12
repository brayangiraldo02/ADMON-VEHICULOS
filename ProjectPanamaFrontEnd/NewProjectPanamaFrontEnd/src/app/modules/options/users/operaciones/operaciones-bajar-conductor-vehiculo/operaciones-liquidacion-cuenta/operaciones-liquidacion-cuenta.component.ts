import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

export interface LiquidationDetail {
  inscripcion: number;
  rentaDiaria: number;
  otrasDeudas: number;
  panapass: number;
  totalDeudas: number;
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

  // Inicializamos la data en null o con valores en 0 para evitar errores en template antes de cargar
  data: LiquidationDetail = {
    inscripcion: 0,
    rentaDiaria: 0,
    otrasDeudas: 0,
    panapass: 0,
    totalDeudas: 0,
    otrosGastos: 0,
    montoDevolver: 0,
    montoDeudar: 0,
  };

  constructor(
    public dialogRef: MatDialogRef<OperacionesLiquidacionCuentaComponent>,
    @Inject(MAT_DIALOG_DATA) public incomingData: any // Por si pasas ID de conductor, etc.
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
    console.log('Abriendo detalle de otros gastos...');
    // Aquí abrirías otro dialog o mostrarías un tooltip extendido
    // si el backend te enviara un array de "otros gastos".
  }

  // Acción de Imprimir
  imprimir(): void {
    console.log('Imprimiendo liquidación...');
    window.print(); // Funcionalidad nativa básica del navegador
  }

  // Acción de Confirmar/Aceptar
  aceptar(): void {
    console.log('Liquidación aceptada');
    // Retornamos true o la data para indicar que se cerró con éxito
    this.dialogRef.close(true);
  }
}
