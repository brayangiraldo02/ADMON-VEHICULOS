import { Component, Input, Output, EventEmitter } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ApiService } from 'src/app/services/api.service';

interface vehicleInfo {
  marca: string;
  placa: string;
  cupo: string;
  nro_entrega: string;
  cuota_diaria: string;
  estado: string;
  propietario: string;
  conductor: string;
}

interface driverInfo {
  nombre: string;
  cedula: string;
  telefono: string;
  direccion: string;
  licencia_numero: string;
  licencia_vencimiento: string;
  estado: string;
}

@Component({
  selector: 'app-operaciones-entrega-vehiculo-conductor',
  templateUrl: './operaciones-entrega-vehiculo-conductor.component.html',
  styleUrls: ['./operaciones-entrega-vehiculo-conductor.component.css']
})
export class OperacionesEntregaVehiculoConductorComponent {
  @Output() close = new EventEmitter<void>();

  vehicleData: vehicleInfo = {
    marca: '',
    placa: '',
    cupo: '',
    nro_entrega: '',
    cuota_diaria: '',
    estado: '',
    propietario: '',
    conductor: ''
  }

  driverData: driverInfo = {
    nombre: '',
    cedula: '',
    telefono: '',
    direccion: '',
    licencia_numero: '',
    licencia_vencimiento: '',
    estado: ''
  }

  constructor(
    private apiService: ApiService
  ) { }

  ngOnInit(): void {
  }

  vehicleSearch(event: any){
    const vehicleInputValue = (event.target as HTMLInputElement).value;
    if (vehicleInputValue.length > 0) {
      console.log(vehicleInputValue);
      this.apiService.getData(`operations/vehicle/${vehicleInputValue}`).subscribe({
        next: (data: vehicleInfo) => {
          this.vehicleData = data;
          console.log(this.vehicleData);
        },
        error: (error: HttpErrorResponse) => {
          if (error.status === 404) {
            window.alert('No se encontró el vehículo');
          }
          else {
            window.alert('Error al buscar el vehículo. Vuelva a intentarlo.');
          }
        }
      });
    }
  }

  driverSearch(event: any){
    const driverInputValue = (event.target as HTMLInputElement).value;
    if (driverInputValue.length > 0) {
      this.apiService.getData(`operations/driver/${driverInputValue}`).subscribe({
        next: (data: driverInfo) => {
          this.driverData = data;
          console.log(this.driverData);
        },
        error: (error: HttpErrorResponse) => {
          if (error.status === 404) {
            window.alert('No se encontró el conductor');
          }
          else {
            window.alert('Error al buscar el conducto. Vuelva a intentarlo.');
          }
        }
      });
      console.log(driverInputValue);
    }
  }

  closeModal() {
    this.close.emit();
  }
}
