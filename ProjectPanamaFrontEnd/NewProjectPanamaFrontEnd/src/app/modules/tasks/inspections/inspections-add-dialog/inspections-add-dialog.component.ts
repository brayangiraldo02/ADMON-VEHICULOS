import {
  AfterViewInit,
  Component,
  Inject,
  OnInit,
  ViewChild,
} from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { map, Observable, startWith } from 'rxjs';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';
import { VehicleStatesFormComponent } from '../inspections-forms/vehicle-states-form/vehicle-states-form.component';

interface Vehicles {
  placa_vehiculo: string;
  numero_unidad: string;
  marca: string;
  linea: string;
  modelo: string;
  nro_cupo: string;
  codigo_propietario: string;
  nombre_propietario: string;
}

interface InspectionTypes {
  id: string;
  nombre: string;
  tipo: string;
}

interface InspectionsVehicleData {
  numero: string;
  marca: string;
  modelo: string;
  placa: string;
  conductor_nombre: string;
  conductor_codigo: string;
  conductor_celular: string;
  kilometraje: number;
  fecha_inspeccion: string;
  hora_inspeccion: string;
  panapass: number;
}

@Component({
  selector: 'app-inspections-add-dialog',
  templateUrl: './inspections-add-dialog.component.html',
  styleUrls: ['./inspections-add-dialog.component.css'],
})
export class InspectionsAddDialogComponent implements OnInit {
  @ViewChild(VehicleStatesFormComponent)
  set vehicleStatesFormComponent(component: VehicleStatesFormComponent) {
    if (component) {
      setTimeout(() => {
        this.mainInspectionForm.addControl('vehicleState', component.vehicleForm);
      }, 0); 
    }
  }

  inspectionInfoForm!: FormGroup;

  mainInspectionForm!: FormGroup;

  isLoading: boolean = true;

  vehicles: Vehicles[] = [];
  optionsVehicles!: Observable<Vehicles[]>;

  inspectionTypes: InspectionTypes[] = [];

  loadingVehicleInfo: boolean = false;
  selectedVehicle: boolean = false;

  inspectionType: string = '';

  vehicleInfo!: InspectionsVehicleData;

  constructor(
    private apiService: ApiService,
    private jwtService: JwtService,
    private formBuilder: FormBuilder,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.getInputsData();
    this.resetVehicleInfo();
    this.initForms();
  }

  getInputsData() {
    this.getDataVehicles();
    this.getInspectionTypes();
  }

  initForms(): void {
    this.inspectionInfoForm = this.formBuilder.group({
      vehiculo: ['', Validators.required],
      tipo_inspeccion: ['', Validators.required],
    });

    this.mainInspectionForm = this.formBuilder.group({
      inspectionInfo: this.inspectionInfoForm,
    });
  }

  getCompany() {
    const userData = this.jwtService.getUserData();
    return userData ? userData.empresa : '';
  }

  getDataVehicles() {
    const company = this.getCompany();
    this.apiService
      .getData('inspections/vehicles_data/' + company)
      .subscribe((data: Vehicles[]) => {
        this.vehicles = [...data];
        this.optionsVehicles = this.inspectionInfoForm
          .get('vehiculo')!
          .valueChanges.pipe(
            startWith(''),
            map((value) => this._filterVehicles(value || ''))
          );
        this.isLoading = false;
      });
  }

  private _filterVehicles(value: string | Vehicles): Vehicles[] {
    const filterValue =
      typeof value === 'string'
        ? value.toLowerCase()
        : value.placa_vehiculo.toLowerCase();
    return this.vehicles.filter(
      (option) =>
        option.placa_vehiculo.toLowerCase().includes(filterValue) ||
        option.numero_unidad.toLowerCase().includes(filterValue) ||
        option.nro_cupo.toLowerCase().includes(filterValue) ||
        option.nombre_propietario.toLowerCase().includes(filterValue)
    );
  }

  displayVehicleData(vehicle: Vehicles): string {
    return vehicle
      ? `${vehicle.numero_unidad} - ${vehicle.marca} ${vehicle.linea} ${vehicle.modelo}`
      : '';
  }

  getInspectionTypes() {
    const company = this.getCompany();
    this.apiService
      .getData('inspections/inspection_types/' + company)
      .subscribe(
        (data: InspectionTypes[]) => {
          this.inspectionTypes = [...data];
        },
        (error) => {
          console.error('Error fetching inspection types:', error);
        }
      );
  }

  openSnackbar(message: string) {
    this.snackBar.open(message, 'Cerrar', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'top',
    });
  }

  resetVehicleInfo() {
    this.vehicleInfo = {
      numero: '',
      marca: '',
      modelo: '',
      placa: '',
      conductor_nombre: '',
      conductor_codigo: '',
      conductor_celular: '',
      kilometraje: 0,
      fecha_inspeccion: '',
      hora_inspeccion: '',
      panapass: 0,
    };

    this.inspectionType = '';
  }

  selectedOptionVehicle(event: MatAutocompleteSelectedEvent): void {
    this.resetVehicleInfo();
    this.selectedVehicle = false;

    const selectedVehicle = event.option.value.numero_unidad;

    if (selectedVehicle) {
      this.loadingVehicleInfo = true;
      this.getVehicleInfo(selectedVehicle);
    } else {
      this.inspectionInfoForm.get('vehiculo')?.reset('');
      this.inspectionType = '';
      this.openSnackbar(
        'No se ha encontrado información del vehículo seleccionado. Prueba con otro.'
      );
    }
  }

  getVehicleInfo(vehicle: string) {
    const company = this.getCompany();

    this.apiService
      .getData('inspections/new_inspection_data/' + company + '/' + vehicle)
      .subscribe(
        (data: InspectionsVehicleData) => {
          this.vehicleInfo = data;
          this.loadingVehicleInfo = false;
          this.selectedVehicle = true;
        },
        (error) => {
          console.error('Error fetching vehicle info:', error);
          this.openSnackbar(
            'error al obtener la información del vehículo seleccionado. Vuelve a intentarlo más tarde.'
          );
          this.loadingVehicleInfo = false;
          this.selectedVehicle = false;
        }
      );
  }

  startInspection() {
    if (this.inspectionInfoForm.invalid || !this.selectedVehicle) {
      this.openSnackbar('Por favor, completa los campos requeridos.');
      this.inspectionInfoForm.markAllAsTouched();
      return;
    }

    const InspectionsSelectedType =
      this.inspectionInfoForm.get('tipo_inspeccion')!.value;

    this.inspectionType = InspectionsSelectedType.tipo;
  }

  onSaveOrNext() {
    if (this.mainInspectionForm.invalid) {
      console.log('El formulario completo es inválido.');
      this.openSnackbar('Por favor, completa los campos requeridos.');

      this.mainInspectionForm.markAllAsTouched();
      return;
    }

    console.log('🚀 Formulario completo es válido!');
    console.log('Valores combinados:', this.mainInspectionForm.value);

    const inspectionInfoData = this.mainInspectionForm.value.inspectionInfo;
    const vehicleStateData = this.mainInspectionForm.value.vehicleState;
  }
}
