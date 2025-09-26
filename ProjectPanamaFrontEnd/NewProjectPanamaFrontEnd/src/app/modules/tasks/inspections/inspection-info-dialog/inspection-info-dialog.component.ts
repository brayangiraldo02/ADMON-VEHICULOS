import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

// Interfaz para los datos que recibirá el diálogo
export interface InspectionDialogData {
  id: number;
  empresa: string;
  fecha: string;
  hora: string;
  propietario: string;
  nombre_propietario: string;
  conductor: string;
  nombre_conductor: string;
  cedula_conductor: string;
  tipo_inspeccion: string;
  descripcion: string;
  unidad: string;
  placa: string;
  kilometraje: string;
  observaciones: string;
  estado_inspeccion: string;
  usuario: string;
  fotos: string[];
}

@Component({
  selector: 'app-inspection-info-dialog',
  templateUrl: './inspection-info-dialog.component.html',
  styleUrls: ['./inspection-info-dialog.component.css'],
})
export class InspectionInfoDialogComponent {
  // Inyectamos MatDialogRef para controlar el diálogo y MAT_DIALOG_DATA para recibir datos
  constructor(
    public dialogRef: MatDialogRef<InspectionInfoDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: InspectionDialogData
  ) {}

  // ngOnInit(): void {
  //   // Aquí podrías realizar alguna inicialización si es necesario
  //   this.data = {
  //     id: 10,
  //     empresa: '10',
  //     fecha: '26-09-2025',
  //     hora: '12:06',
  //     propietario: '1',
  //     nombre_propietario: 'FUSION GAMES',
  //     conductor: '',
  //     nombre_conductor: '',
  //     cedula_conductor: '',
  //     tipo_inspeccion: '02',
  //     descripcion: 'a',
  //     unidad: '1029',
  //     placa: 'AR3822',
  //     kilometraje: '',
  //     observaciones: 'a',
  //     estado_inspeccion: 'FIN',
  //     usuario: 'HFVG10',
  //     fotos: [
  //       'http://localhost:8000/uploads/10/1029/inspecciones/10/foto01.jpg',
  //       'http://localhost:8000/uploads/10/1029/inspecciones/10/foto02.jpg',
  //     ],
  //   };
  // }

  // Método para obtener el texto del estado (sin funcionalidad, solo para el diseño)
  getStatusText(status: string): string {
    switch (status) {
      case 'PEN':
        return 'Pendiente';
      case 'FIN':
        return 'Finalizada';
      case 'SUS':
        return 'Suspendida';
      default:
        return status;
    }
  }
}
