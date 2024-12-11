import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-vehicles-addnew',
  templateUrl: './vehicles-addnew.component.html',
  styleUrls: ['./vehicles-addnew.component.css']
})
export class VehiclesAddnewComponent {
  vehicleForm: FormGroup;

  selectedButton: string = "propiedad";
  imageVehicle: string = "https://cdn5.dibujos.net/dibujos/pintados/202013/coche-urbano-vehiculos-coches-11735143.jpg";

  isEditable = false;
  centralFound = false;
  usersFound = false;
  cityFound = false;
  isModalVisible: boolean = false;
  hasPermission: boolean = false;
  grantedPermission: string = '';
  stateEdited = false;

  // drivers: any = '';

  data: any = null;
  dataOriginal: any = null;
  central: any = null;
  brands: any = null;
  owners: any = null;
  users: any = null;
  vehicles: any = null;
  expenseAccounts: any = null;
  modalities: any = null;

  code: string | null = null;

  createDate: string = '';

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router, 
    private apiService: ApiService
  ) {
    this.vehicleForm = this.fb.group({
      vehiculo_placa: [''],
      vehiculo_numero: [''],
      vehiculo_marca: [''],
      vehiculo_modelo: [''],
      vehiculo_fec_modelo: [''],
      vehiculo_cilindraje: [''],
      vehiculo_nro_puertas: [''],
      vehiculo_licencia_nro: [''],
      vehiculo_licencia_fec: [''],
      vehiculo_color: [''],
      vehiculo_servicio: [''],
      vehiculo_fec_matricula: [''],
      vehiculo_clase: [''],
      vehiculo_capacidad: [''],
      vehiculo_fec_vencimiento_matricula: [''],
      vehiculo_tipo: [''],
      vehiculo_ne: [''],
      vehiculo_fec_importacion: [''],
      vehiculo_combustible: [''],
      vehiculo_vin: [''],
      vehiculo_motor: [''],
      vehiculo_serie: [''],
      vehiculo_chasis: [''],
      vehiculo_motor_reg: [''],
      vehiculo_serie_reg: [''],
      vehiculo_chasis_reg: [''],
      vehiculo_propietario: [''],
      vehiculo_cta_gasto: [''],
      vehiculo_central: [''],
      vehiculo_nro_cupo: [''],
      vehiculo_permiso_nro: [''],
      vehiculo_fec_vencimiento_permiso: [''],
      vehiculo_blindaje: [''],
      vehiculo_potencia: [''],
      vehiculo_dec_importacion: [''],
      vehiculo_restriccion_movilidad: [''],
      vehiculo_limit_propiedad: [''],
      vehiculo_organismo_transito: [''],
      vehiculo_codigo_barras: [''],
      vehiculo_lateral: [''],
      vehiculo_kilometraje: [''],
      vehiculo_modalidad: [''],
      vehiculo_consulta_panapass: [''],
      vehiculo_panapass: [''],
      vehiculo_panapass_pwd: [''],
    });
  }

  ngOnInit(): void {
    this.getBrands();
    this.getOwners();
    this.getCentral();
    this.getExpenseAccounts();
    this.getModalities();
    this.getVehicles();
  }

  getBrands() {
    this.apiService.getData('brands').subscribe(
      (response) => {
        this.brands = response;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  getModalities() {
    this.apiService.getData('modalities').subscribe(
      (response) => {
        this.modalities = response;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  getOwners() {
    this.apiService.getData('owners').subscribe(
      (response) => {
        this.owners = response;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  getCentral() {
    this.apiService.getData('central').subscribe(
      (response) => {
        this.central = response;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  getExpenseAccounts() {
    this.apiService.getData('expense-accounts').subscribe(
      (response) => {
        this.expenseAccounts = response;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  selectButton(button: string) {
    this.selectedButton = button;
  }

  finalDate(fecha: string): string {
    if (fecha) {
      return `${fecha} 00:00:00`; // Añade la hora "00:00:00" al final de la fecha
    }
    return '0000-00-00 00:00:00'; // Si la fecha no es válida, devuelve una fecha nula
  }

  getVehicles() {
    this.apiService.getData('vehicle-codes').subscribe(
      (response) => {
        this.vehicles = response
          .sort((a: any, b: any) => a.vehiculo_consecutivo - b.vehiculo_consecutivo);  // Ordenamos los drivers por código
        
        console.log(this.vehicles); 
      },
      (error) => {
        console.log(error);
      }
    );
  }

  saveData() {

    const formValues = this.vehicleForm.value;

    // console.log(modifiedData)

    // this.data['stateEdited'] = this.stateEdited;

    formValues.vehiculo_licencia_fec = this.finalDate(formValues.vehiculo_licencia_fec);
    formValues.vehiculo_fec_importacion = this.finalDate(formValues.vehiculo_fec_importacion);
    formValues.vehiculo_fec_vencimiento_matricula = this.finalDate(formValues.vehiculo_fec_vencimiento_matricula);
    formValues.vehiculo_fec_matricula = this.finalDate(formValues.vehiculo_fec_matricula);

    formValues.vehiculo_consecutivo = Number(this.vehicles[this.vehicles.length - 1].vehiculo_consecutivo) + 1;

    console.log('Data to save:', formValues);
  
    this.apiService.postData(`vehicles`, formValues).subscribe(
      (response) => {
        window.alert('Vehículo creado correctamente');
        // console.log(response);
        this.router.navigate(['/vehicle/'+formValues.vehiculo_consecutivo]);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  goToVehicleOwnership() {
    this.selectButton('propiedad')
  }

  goToVehicleDocuments() {
    this.selectButton('documentos')
  }

  goToVehicleDrivers() {
    this.selectButton('conductores')
  }

  goToVehicleIncome() {
    this.selectButton('ingresos')
  }

  goToVehicleOrders() {
    this.selectButton('ordenes')
  }

  goToVehicleTools() {
    this.selectButton('herramientas')
  }

  goToVehiclePhotos() {
    this.selectButton('fotos')
  }

  goToVehicleDocumentation() {
    this.selectButton('documentacion')
  }

  goToVehiclePyG() {
    this.selectButton('pyg')
  }

}
