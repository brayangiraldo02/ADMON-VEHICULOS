import { Component, Input, Output, EventEmitter } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ApiService } from 'src/app/services/api.service';

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

interface panamaTime {
  time: string;
}

@Component({
  selector: 'app-operaciones-entrega-vehiculo-conductor',
  templateUrl: './operaciones-entrega-vehiculo-conductor.component.html',
  styleUrls: ['./operaciones-entrega-vehiculo-conductor.component.css']
})
export class OperacionesEntregaVehiculoConductorComponent {
  @Output() close = new EventEmitter<void>();

  driverInputValue: string = '';
  vehicleInputValue: string = '';

  driverInputDisabled: boolean = true;
  deliveryVehicleDriverDisabled: boolean = true;

  confirmation: boolean = false;

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
    fecha_estado: ''
  }

  driverData: driverInfo = {
    codigo: '',
    nombre: '',
    cedula: '',
    telefono: '',
    direccion: '',
    licencia_numero: '',
    licencia_vencimiento: '',
    vehiculo: '',
    estado: ''
  }

  day: panamaTime = {
    time: ''
  }

  dayBackup: panamaTime = {
    time: ''
  }

  constructor(
    private apiService: ApiService
  ) { }

  ngOnInit(): void {
    this.getTodayDate();
  }

  getTodayDate() {
    this.apiService.getData('extras/time').subscribe({
      next: (data: panamaTime) => {
        this.day = JSON.parse(JSON.stringify(data));
        this.dayBackup = JSON.parse(JSON.stringify(data));
      },
      error: (error: HttpErrorResponse) => {
        console.log('Error al obtener el día de Panamá');
      }
    });
  }

  vehicleValidations(){
    if (this.vehicleData.estado.substring(0, 2) !== '06'){
      window.alert('Vehículo debe estar esperando operador.');

      if (this.vehicleData.estado.substring(0, 2) === '01' && this.vehicleData.conductor !== ''){
        this.driverInputValue = this.vehicleData.conductor;
        this.day.time = this.vehicleData.fecha_estado;
        this.driverSearch(this.vehicleData.conductor, false);
      }

      return;
    }

    if (this.vehicleData.con_cupo === 2) {
      window.alert('Vehículo sin cupo.');
      return;
    }

    this.driverInputDisabled = false;
  }

  vehicleSearch(vehicleValue: string){
    this.apiService.getData(`operations/deliveryvehicledriver/vehicle/${vehicleValue}`).subscribe({
      next: (data: vehicleInfo) => {
        this.vehicleData = data;
        console.log(this.vehicleData);
        this.vehicleValidations();
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

  vehicleInput(event: any){
    const vehicleInputValue = (event.target as HTMLInputElement).value;
    if (vehicleInputValue.length > 0) {
      this.deliveryVehicleDriverDisabled = true;
      this.driverInputDisabled = true;
      this.driverInputValue = '';
      this.day.time = this.dayBackup.time;
      this.driverData = {
        codigo: '',
        nombre: '',
        cedula: '',
        telefono: '',
        direccion: '',
        licencia_numero: '',
        licencia_vencimiento: '',
        vehiculo: '',
        estado: ''
      };
      this.vehicleSearch(vehicleInputValue);
    }
  }

  driverValidations() {
    if (this.driverData.estado !== '1') {
      window.alert('Conductor debe estar activo.');
    }

    if (this.driverData.vehiculo !== '') {
      window.alert('Conductor tiene el vehículo ' + this.driverData.vehiculo + ' asignado.');
    }
  }

  driverSearch(driverValue: string, validations?: boolean){
    this.deliveryVehicleDriverDisabled = true;
    this.apiService.getData(`operations/deliveryvehicledriver/driver/${driverValue}`).subscribe({
      next: (data: driverInfo) => {
        this.driverData = data;
        console.log(this.driverData);
        if (validations !== false) {
          this.driverValidations();
          this.deliveryVehicleDriverValidations();
        };
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
  }

  driverInput(event: any){
    const driverInputValue = (event.target as HTMLInputElement).value;
    if (driverInputValue.length > 0) {
      this.driverSearch(driverInputValue);
    }
  }

  deliveryVehicleDriverValidations() {
    if (this.driverData.estado === '1' && 
        this.driverData.vehiculo === '' &&
        this.vehicleData.estado.substring(0, 2) === '06' &&
        this.vehicleData.con_cupo === 1 &&
        this.vehicleData.conductor === '') {
      this.deliveryVehicleDriverDisabled = false;
    }
  }

  confirmationChange(){
    this.confirmation = !this.confirmation;
  }

  saveDeliveryVehicleDriver() {
    const data = {
      vehicle_number: this.vehicleData.numero,
      driver_number: this.driverData.codigo,
      delivery_date: this.day.time
    }

    this.apiService.postData('operations/deliveryvehicledriver', data).subscribe({
      next: () => {
        window.alert('Entrega de vehículo al conductor guardada exitosamente');
        this.closeModal();
      },
      error: (error: HttpErrorResponse) => {
        if (error.status === 400) {
          window.alert('Error al guardar la entrega de vehículo al conductor. Vuelva a intentarlo.');
        }
        if (error.status === 404) {
          window.alert('No se ha encontrado el conductor o el vehículo. Vuelva a intentarlo.');
        }
        else {
          window.alert('Error al guardar la entrega de vehículo al conductor.');
        }
      }
    });
  }

  closeModal() {
    this.close.emit();
  }
}
