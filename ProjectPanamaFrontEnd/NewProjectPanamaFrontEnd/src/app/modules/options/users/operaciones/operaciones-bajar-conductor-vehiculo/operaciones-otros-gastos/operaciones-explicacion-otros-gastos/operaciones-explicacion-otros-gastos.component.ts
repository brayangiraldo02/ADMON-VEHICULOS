import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

export interface ExplicacionDialogData {
  codigo: string;
  nombre: string;
  explicacion: string;
  valor: number;
}

export interface ExplicacionDialogResult {
  explicacion: string;
  valor: number;
}

@Component({
  selector: 'app-operaciones-explicacion-otros-gastos',
  templateUrl: './operaciones-explicacion-otros-gastos.component.html',
  styleUrls: ['./operaciones-explicacion-otros-gastos.component.css'],
})
export class OperacionesExplicacionOtrosGastosComponent implements OnInit {
  explicacion: string = '';
  valorDisplay: string = ''; // Para mostrar con formato
  valor: number = 0; // Valor numérico real

  constructor(
    public dialogRef: MatDialogRef<OperacionesExplicacionOtrosGastosComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ExplicacionDialogData
  ) {}

  ngOnInit(): void {
    // Inicializar con los valores recibidos
    this.explicacion = this.data.explicacion || '';
    this.valor = this.data.valor || 0;

    // Si ya hay un valor, mostrarlo formateado
    if (this.valor > 0) {
      this.valorDisplay = this.formatNumber(this.valor);
    }
  }

  // Formatea un número a string con separadores de miles
  formatNumber(num: number): string {
    return num.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  }

  // Parsea un string formateado a número
  parseFormattedNumber(formatted: string): number {
    // Remover comas y convertir a número
    const cleaned = formatted.replace(/,/g, '');
    const num = parseFloat(cleaned);
    return isNaN(num) ? 0 : num;
  }

  // Maneja el input del valor
  onValorInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    let value = input.value;

    // Remover caracteres no válidos (solo permitir números, punto y coma)
    value = value.replace(/[^0-9.,]/g, '');

    // Guardar el valor numérico
    this.valor = this.parseFormattedNumber(value);
    this.valorDisplay = value;
  }

  // Formatea el valor cuando el input pierde el foco
  onValorBlur(): void {
    if (this.valor > 0) {
      this.valorDisplay = this.formatNumber(this.valor);
    } else {
      this.valorDisplay = '';
    }
  }

  // Limpia el cero inicial cuando el usuario hace foco
  onValorFocus(): void {
    if (this.valor === 0) {
      this.valorDisplay = '';
    }
  }

  // Aceptar y retornar los datos ingresados
  aceptar(): void {
    const result: ExplicacionDialogResult = {
      explicacion: this.explicacion.trim(),
      valor: this.valor,
    };
    this.dialogRef.close(result);
  }

  // Limpia el valor del input
  limpiarValor(): void {
    this.valor = 0;
    this.valorDisplay = '';
  }

  // Cancelar y cerrar sin guardar
  cancelar(): void {
    this.dialogRef.close(null);
  }
}
