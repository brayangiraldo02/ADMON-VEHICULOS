import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { map, Observable, startWith } from 'rxjs';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

interface vehicle {
  unidad: string;
  placa: string;
}

interface vehicleInfo {
  numero: string;
  marca: string;
  placa: string;
  cupo: string;
  nro_entrega: string;
  cuota_diaria: string;
  estado: string;
  propietario: string;
  conductor: string;
  con_cupo: number; //1 ES SÍ, 2 ES NO
  fecha_estado: string;
}

interface driverInfo {
  codigo: string;
  nombre: string;
  cedula: string;
  telefono: string;
  direccion: string;
  licencia_numero: string;
  licencia_vencimiento: string;
  vehiculo: string;
  estado: string;
}

@Component({
  selector: 'app-operaciones-cambiar-patio-vehiculo',
  templateUrl: './operaciones-cambiar-patio-vehiculo.component.html',
  styleUrls: ['./operaciones-cambiar-patio-vehiculo.component.css'],
})
export class OperacionesCambiarPatioVehiculoComponent {
  vehicles = new FormControl('');
  drivers = new FormControl({ value: '', disabled: true });
  options: vehicle[] = [];
  filteredOptions!: Observable<vehicle[]>;

  isLoadingVehicles: boolean = true;
  isLoadingVehicleInfo: boolean = false;
  selectedVehicle: boolean = false;

  vehicleData: vehicleInfo = {
    numero: '',
    marca: '',
    placa: '',
    cupo: '',
    nro_entrega: '',
    cuota_diaria: '',
    estado: '',
    propietario: '',
    conductor: '',
    con_cupo: 0, //1 ES SÍ, 2 ES NO
    fecha_estado: '',
  };

  driverData: driverInfo = {
    codigo: '',
    nombre: '',
    cedula: '',
    telefono: '',
    direccion: '',
    licencia_numero: '',
    licencia_vencimiento: '',
    vehiculo: '',
    estado: '',
  };

  constructor(
    private jwtService: JwtService,
    private apiService: ApiService,
    private snackBar: MatSnackBar,
    private dialogRef: MatDialogRef<OperacionesCambiarPatioVehiculoComponent>
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

  private _filter(value: string): vehicle[] {
    const filterValue = value.toLowerCase();

    return this.options.filter(
      (option) =>
        option.placa.toLowerCase().includes(filterValue) ||
        option.unidad.toLowerCase().includes(filterValue)
    );
  }

  vehicleSearch(vehicleValue: string) {
    this.resetInfo();
    this.selectedVehicle = false;
    console.log('Vehicle selected:', vehicleValue);
    if (vehicleValue !== '') {
      this.isLoadingVehicleInfo = true;
      this.apiService
        .getData(`operations/deliveryvehicledriver/vehicle/${vehicleValue}`)
        .subscribe({
          next: (data: vehicleInfo) => {
            this.vehicleData = data;
            console.log(this.vehicleData);
            this.drivers.setValue(this.vehicleData.conductor);
            this.driverSearch(this.vehicleData.conductor);
          },
          error: (error: HttpErrorResponse) => {
            this.isLoadingVehicleInfo = false;
            this.selectedVehicle = false;
            if (error.status === 404) {
              this.openSnackbar('Vehículo no encontrado. Intenta con otro.');
            } else {
              this.openSnackbar(
                'Error al obtener la información del vehículo. Inténtalo de nuevo más tarde.'
              );
            }
          },
        });
    }
  }

  driverSearch(driverValue: string) {
    if (driverValue !== '') {
      this.apiService
        .getData(`operations/deliveryvehicledriver/driver/${driverValue}`)
        .subscribe({
          next: (data: driverInfo) => {
            this.driverData = data;
            console.log(this.driverData);
            this.isLoadingVehicleInfo = false;
            this.selectedVehicle = true;
          },
          error: (error: HttpErrorResponse) => {
            this.isLoadingVehicleInfo = false;
            this.selectedVehicle = true;
            if (error.status === 404) {
              this.openSnackbar(
                'No se encontró el conductor para esta unidad.'
              );
            } else {
              this.openSnackbar(
                'Error al obtener la información del conductor. Inténtalo de nuevo más tarde.'
              );
            }
          },
        });
      return;
    }
    this.isLoadingVehicleInfo = false;
    this.selectedVehicle = true;
  }

  resetInfo() {
    this.selectedVehicle = false;
    this.vehicleData = {
      numero: '',
      marca: '',
      placa: '',
      cupo: '',
      nro_entrega: '',
      cuota_diaria: '',
      estado: '',
      propietario: '',
      conductor: '',
      con_cupo: 0, //1 ES SÍ, 2 ES NO
      fecha_estado: '',
    };
    this.driverData = {
      codigo: '',
      nombre: '',
      cedula: '',
      telefono: '',
      direccion: '',
      licencia_numero: '',
      licencia_vencimiento: '',
      vehiculo: '',
      estado: '',
    };
  }

  resetAutocomplete() {
    this.vehicles.setValue('');
  }

  openSnackbar(message: string) {
    this.snackBar.open(message, 'Cerrar', {
      duration: 3500,
      horizontalPosition: 'center',
      verticalPosition: 'top',
    });
  }

  closeDialog() {
    this.dialogRef.close();
  }
}
