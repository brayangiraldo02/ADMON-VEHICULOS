import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs/internal/Observable';
import { map } from 'rxjs/internal/operators/map';
import { startWith } from 'rxjs/internal/operators/startWith';
import { SignaturePadComponent } from 'src/app/modules/shared/components/signature-pad/signature-pad.component';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

interface vehicle {
  unidad: string;
  placa: string;
}

interface vehicleSignatureInfo {
  numero: string;
  marca: string;
  placa: string;
  cupo: string;
  central: string;
  propietario_nombre: string;
  nro_entrega: string;
  cuota_diaria: number;
  valor_deposito: number;
  estado: string;
  con_cupo: string;
  conductor_codigo: string;
  conductor_nombre: string;
  conductor_cedula: string;
  conductor_celular: string;
  conductor_direccion: string;
  fecha_contrato: string;
  permitido: number | null | undefined;
  mensaje: string;
}

@Component({
  selector: 'app-take-photo',
  templateUrl: './take-photo.component.html',
  styleUrls: ['./take-photo.component.css'],
})
export class TakePhotoComponent implements OnInit {
  @ViewChild(SignaturePadComponent)
  signaturePadComponent!: SignaturePadComponent;

  vehicles = new FormControl('');
  drivers = new FormControl({ value: '', disabled: true });
  options: vehicle[] = [];
  filteredOptions!: Observable<vehicle[]>;

  isLoadingVehicles = true;
  isLoadingvehicleSignatureInfo = false;
  signatureDriver = false;

  vehicleSignatureInfo: vehicleSignatureInfo = {
    numero: '',
    marca: '',
    placa: '',
    cupo: '',
    central: '',
    propietario_nombre: '',
    nro_entrega: '',
    cuota_diaria: 0,
    valor_deposito: 0,
    estado: '',
    con_cupo: '',
    conductor_codigo: '',
    conductor_nombre: '',
    conductor_cedula: '',
    conductor_celular: '',
    conductor_direccion: '',
    fecha_contrato: '',
    permitido: null,
    mensaje: '',
  };

  constructor(
    private apiService: ApiService,
    private jwtService: JwtService,
    private snackBar: MatSnackBar,
    private dialogRef: MatDialogRef<TakePhotoComponent>
  ) {}

  ngOnInit() {
    this.getVehicles();
  }

  getCompany() {
    const userData = this.jwtService.getUserData();
    return userData ? userData.empresa : '';
  }

  getVehicles() {
    const company = this.getCompany();
    this.apiService.getData('vehicles/' + company).subscribe(
      (response: vehicle[]) => {
        this.options = response;
        this.filteredOptions = this.vehicles.valueChanges.pipe(
          startWith(''),
          map((value) => this._filter(value || ''))
        );
        this.isLoadingVehicles = false;
      },
      (error) => {
        console.error('Error fetching vehicles:', error);
        this.openSnackbar(
          'Error al obtener las unidades. Inténtalo de nuevo más tarde.'
        );
        this.closeDialog();
      }
    );
  }

  openSnackbar(message: string) {
    this.snackBar.open(message, 'Cerrar', {
      duration: 3500,
      horizontalPosition: 'center',
      verticalPosition: 'top',
    });
  }

  resetInfo() {
    this.vehicleSignatureInfo = {
      numero: '',
      marca: '',
      placa: '',
      cupo: '',
      central: '',
      propietario_nombre: '',
      nro_entrega: '',
      cuota_diaria: 0,
      valor_deposito: 0,
      estado: '',
      con_cupo: '',
      conductor_codigo: '',
      conductor_nombre: '',
      conductor_cedula: '',
      conductor_celular: '',
      conductor_direccion: '',
      fecha_contrato: '',
      permitido: null,
      mensaje: '',
    };
    this.drivers.setValue('');
  }

  resetVehicleAutocomplete() {
    // Resetear el autocomplete completamente
    this.vehicles.setValue('');
    this.vehicles.updateValueAndValidity();

    // Opcional: Forzar la actualización del filtro
    this.filteredOptions = this.vehicles.valueChanges.pipe(
      startWith(''),
      map((value) => this._filter(value || ''))
    );
  }

  getContractInfo(event: any) {
    if (event.option.value === undefined) {
      this.resetInfo();
      this.resetVehicleAutocomplete();
      return;
    }

    if (event && event.option.value !== undefined) {
      const selectedVehicle = event.option.value;
      console.log('Selected Vehicle:', selectedVehicle);
      this.isLoadingvehicleSignatureInfo = true;
      this.resetInfo();

      this.apiService
        .getData('operations/generate-contract/info/' + selectedVehicle)
        .subscribe(
          (response: vehicleSignatureInfo) => {
            console.log('Contract Info:', response);

            this.isLoadingvehicleSignatureInfo = false;
            this.vehicleSignatureInfo = response;
            this.drivers.setValue(response.conductor_codigo);
          },
          (error) => {
            console.error('Error fetching contract info:', error);
            this.openSnackbar(
              'Error al obtener la información. Inténtalo de nuevo con otra unidad.'
            );
            this.isLoadingvehicleSignatureInfo = false;
            this.resetInfo();
            this.resetVehicleAutocomplete();
          }
        );
    }
  }

  private _filter(value: string): vehicle[] {
    const filterValue = value.toLowerCase();

    return this.options.filter(
      (option) =>
        option.placa.toLowerCase().includes(filterValue) ||
        option.unidad.toLowerCase().includes(filterValue)
    );
  }

  saveSignature() {
    if (this.signaturePadComponent) {
      this.signaturePadComponent.saveSignature();
    }
  }

  closeDialog() {
    this.dialogRef.close();
  }
}
