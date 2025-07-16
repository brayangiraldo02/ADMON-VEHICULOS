import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { map, Observable, startWith } from 'rxjs';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';
import { FolioInfoDialogComponent } from '../folio-info-dialog/folio-info-dialog.component';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';

export interface vehicles {
  placa_vehiculo: string;
  numero_unidad: string;
  codigo_conductor: string;
  codigo_propietario: string;
  marca: string;
  linea: string;
  modelo: string;
}

export interface existDocumentsVehicles {
  nombre_documento: string;
  existe: boolean;
  folios: boolean;
  mensaje: string;
}

@Component({
  selector: 'app-vehicles-documents',
  templateUrl: './vehicles-documents.component.html',
  styleUrls: ['./vehicles-documents.component.css']
})
export class VehiclesDocumentsComponent implements OnInit {
  vehiclesForm!: FormGroup;

  isLoading: boolean = true;
  selectedVehicle: boolean = false;
  loadingDocumentsInfoVehicles: boolean = false;

  vehicles: vehicles[] = [];

  optionsVehicles!: Observable<vehicles[]>;
  // ✅ Renombrado para mayor simplicidad
  documentsInfo: existDocumentsVehicles[] = [];

  constructor(
    private apiService: ApiService,
    private jwtService: JwtService,
    private formBuilder: FormBuilder,
    private snackBar: MatSnackBar,
    private dialog: MatDialog,
    private breakpointObserver: BreakpointObserver
  ){}

  ngOnInit(): void {
    this.initForm();
    this.getDataVehicles();
  }

  initForm(): void {
    this.vehiclesForm = this.formBuilder.group({
      vehiculo: ['']
    });
  }

  getCompany() {
    const userData = this.jwtService.getUserData();
    return userData ? userData.empresa : '';
  }

  getDataVehicles(){
    const company = this.getCompany();
    this.apiService.getData('inspections/vehicles_data/'+company).subscribe(
      (data: vehicles[]) => {
        this.vehicles = [...data];
        this.optionsVehicles = this.vehiclesForm.get('vehiculo')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterVehicles(value || '')),
        );
        this.isLoading = false;
      }
    );
  }

  private _filterVehicles(value: string | vehicles): vehicles[] {
    const filterValue = typeof value === 'string' ? value.toLowerCase() : value.placa_vehiculo.toLowerCase();
    return this.vehicles.filter(option => 
      option.placa_vehiculo.toLowerCase().includes(filterValue) || 
      option.numero_unidad.toLowerCase().includes(filterValue)
    );
  }

  displayVehiclePlate(vehicle: vehicles): string {
    return vehicle ? `${vehicle.numero_unidad} ${vehicle.placa_vehiculo} - ${vehicle.marca} ${vehicle.linea} ${vehicle.modelo}` : '';
  }

  getDocumentsInfoVehicle(vehicle_number: string) {
    this.loadingDocumentsInfoVehicles = true;
    const company = this.getCompany();
    this.apiService.getData('documents/vehicle-documents/' + company + '/' + vehicle_number).subscribe({
      next: (data: existDocumentsVehicles[]) => {
        console.log('Información de documentos del vehículo:', data);
        this.loadingDocumentsInfoVehicles = false;
        this.selectedVehicle = true;
        this.documentsInfo = data; // Asignamos los datos a la propiedad
      },
      error: (err: HttpErrorResponse) => {
        console.error('Error HTTP:', err);
        let snackbarMessage = '';
  
        if (err.status === 404) {
          snackbarMessage = 'No se encontraron documentos para el vehículo seleccionado. Intenta con otro.';
        } else {
          snackbarMessage = 'Ocurrió un error inesperado. Por favor, intenta más tarde.';
        }
  
        this.openSnackbar(snackbarMessage);

        this.loadingDocumentsInfoVehicles = false;
        this.vehiclesForm.get('vehiculo')?.reset('');
        this.selectedVehicle = false;
        this.documentsInfo = []; // Limpiamos los datos en caso de error
      }
    });
  }

  selectedOptionVehicle(event: MatAutocompleteSelectedEvent): void {
    const selectedVehicle = event.option.value;
    this.selectedVehicle = false;
    this.documentsInfo = []; // Limpiamos al cambiar de vehículo

    if (selectedVehicle) {
      console.log('Vehículo seleccionado:', selectedVehicle);
      this.getDocumentsInfoVehicle(selectedVehicle.numero_unidad);
    } else {
      this.vehiclesForm.get('vehiculo')?.reset('');
    }
  }

  getDocumentVehicle(vehicle: string, document: string): void {
    if (!vehicle || !document) return;

    const company = this.getCompany();

    console.log('Solicitando documento del vehículo:', {
      empresa: company,
      vehiculo: vehicle,
      documento: document
    });
  }

  validateDocumentVehicle(document: existDocumentsVehicles, nombreHtml: string): void {
    if (!document) return;

    console.log('Documento solicitado:', {
      nombre: document.nombre_documento,
      folios: document.folios,
      mensaje: document.mensaje
    });

    if(!document.folios){
      this.getDocumentVehicle(this.vehiclesForm.get('vehiculo')?.value.numero_unidad, document.nombre_documento);
      return;
    }

    const isSmallScreen = this.breakpointObserver.isMatched(Breakpoints.XSmall);
    const dialogWidth = isSmallScreen ? '90vw' : '40%';

    const dialogRef = this.dialog.open(FolioInfoDialogComponent, {
      width: dialogWidth,
      disableClose: true,
      data: {
        documentName: nombreHtml,
        message: document.mensaje
      }
    })

    dialogRef.afterClosed().subscribe(result => {
      console.log('El diálogo se cerró con el resultado:', result);
  
      if (result === true) {
        this.getDocumentVehicle(this.vehiclesForm.get('vehiculo')?.value.numero_unidad, document.nombre_documento);
      }
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