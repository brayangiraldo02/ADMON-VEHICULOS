import { Component, Inject, OnInit} from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ApiService } from 'src/app/services/api.service';
import { Clipboard } from '@angular/cdk/clipboard';

interface DialogData {
  vehicleNumber: string;
}

interface VehicleInfo {
  numero_unidad: string;
  placa_vehiculo: string;
  nro_cupo: string;
  propietario: string;
  codigo_conductor: string;
  nombre_conductor: string;
  telefono_conductor: string;
  panapass: string;
  fecha_contrato: string;
}

@Component({
  selector: 'app-info-vehicle-dialog',
  templateUrl: './info-vehicle-dialog.component.html',
  styleUrls: ['./info-vehicle-dialog.component.css'],
})
export class InfoVehicleDialogComponent implements OnInit {
  isLoading: boolean = true;

  vehicle!: VehicleInfo;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
    private dialogRef: MatDialogRef<InfoVehicleDialogComponent>,
    private apiService: ApiService,
    private snackBar: MatSnackBar,
    private clipboard: Clipboard
  ) {}

  ngOnInit(): void {
    this.getVehicleInfo();
  }

  getVehicleInfo(): void {
    this.apiService
      .getData('documents/vehicle-info/' + this.data.vehicleNumber)
      .subscribe((data: VehicleInfo) => {
        this.vehicle = data;
        console.log('Vehicle Info:', this.vehicle);
        this.isLoading = false;
      },
      (error) => {
        console.error('Error fetching vehicle info:', error);
        this.openSnackbar('Error al obtener la información del vehículo, vuelve a intentarlo más tarde.');
        this.isLoading = false;
        this.closeModal();
      });
  }

  openSnackbar(message: string) {
    this.snackBar.open(message, 'Cerrar', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'top',
    })
  }

  copyToClipboard(text: string) {
    this.clipboard.copy(text);
    this.openSnackbar('Copiado al portapapeles');
  }

  closeModal() {
    this.dialogRef.close();
  }
}
