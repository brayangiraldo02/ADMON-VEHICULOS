import {
  AfterViewInit,
  Component,
  Inject,
  OnInit,
  ViewChild,
} from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { map, Observable, startWith } from 'rxjs';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';
import { VehicleStatesFormComponent } from '../inspections-forms/vehicle-states-form/vehicle-states-form.component';
import { TakePhotosVehicleComponent } from '../take-photos-vehicle/take-photos-vehicle.component';

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

interface ChecklistItem {
  id: string;
  label: string;
  value: boolean | null;
}

interface InspectionCreateResponse {
  id: string;
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
        this.mainInspectionForm.addControl(
          'vehicleState',
          component.vehicleForm
        );
      }, 0);
    }
  }

  @ViewChild(TakePhotosVehicleComponent) takePhotosVehicleComponent!: TakePhotosVehicleComponent;

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

  inspectionCreateID: string = '';

  constructor(
    private apiService: ApiService,
    private jwtService: JwtService,
    private formBuilder: FormBuilder,
    private snackBar: MatSnackBar,
    private dialogRef: MatDialogRef<InspectionsAddDialogComponent>
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

    console.log(this.mainInspectionForm.value.vehicleState);
    const checklistItems: ChecklistItem[] =
      this.mainInspectionForm.value.vehicleState.checklistItems;

    const newInspectionData = {
      user: this.jwtService.getUserData()?.id,
      company_code: this.getCompany(),
      vehicle_number: this.vehicleInfo.numero,
      mileage: this.mainInspectionForm.value.vehicleState.kilometraje || 0,
      inspection_type:
        this.mainInspectionForm.value.inspectionInfo.tipo_inspeccion.id,
      inspection_date: this.vehicleInfo.fecha_inspeccion,
      inspection_time: this.vehicleInfo.hora_inspeccion,
      alfombra: checklistItems.find((item) => item.id === 'alfombra')?.value
        ? 1
        : 0,
      copas_rines: checklistItems.find((item) => item.id === 'copas_rines')
        ?.value
        ? 1
        : 0,
      extinguidor: checklistItems.find((item) => item.id === 'extinguidor')
        ?.value
        ? 1
        : 0,
      antena: checklistItems.find((item) => item.id === 'antena')?.value
        ? 1
        : 0,
      lamparas: checklistItems.find((item) => item.id === 'lamparas')?.value
        ? 1
        : 0,
      triangulo: checklistItems.find((item) => item.id === 'triangulo')?.value
        ? 1
        : 0,
      gato: checklistItems.find((item) => item.id === 'gato')?.value ? 1 : 0,
      pipa: checklistItems.find((item) => item.id === 'pipa')?.value ? 1 : 0,
      copas: checklistItems.find((item) => item.id === 'copas')?.value ? 1 : 0,
      llanta_repuesto: checklistItems.find(
        (item) => item.id === 'llanta_repuesto'
      )?.value
        ? 1
        : 0,
      placa_municipal: checklistItems.find(
        (item) => item.id === 'placa_municipal'
      )?.value
        ? 1
        : 0,
      caratula_radio: checklistItems.find(
        (item) => item.id === 'caratula_radio'
      )?.value
        ? 1
        : 0,
      registro_vehiculo: checklistItems.find(
        (item) => item.id === 'registro_vehiculo'
      )?.value
        ? 1
        : 0,
      revisado: checklistItems.find((item) => item.id === 'revisado')?.value
        ? 1
        : 0,
      pago_municipio: checklistItems.find(
        (item) => item.id === 'pago_municipio'
      )?.value
        ? 1
        : 0,
      formato_colisiones_menores: checklistItems.find(
        (item) => item.id === 'formato_colisiones_menores'
      )?.value
        ? 1
        : 0,
      poliza_seguros: checklistItems.find((item) => item.id === 'poliza_seguro')
        ?.value
        ? 1
        : 0, // Nota: En el array es 'poliza_seguro', ajustado aquí
      luces_delanteras: checklistItems.find(
        (item) => item.id === 'luces_delanteras'
      )?.value
        ? 1
        : 0,
      luces_traseras: checklistItems.find(
        (item) => item.id === 'luces_traseras'
      )?.value
        ? 1
        : 0,
      vidrios: checklistItems.find((item) => item.id === 'vidrios')?.value
        ? 1
        : 0,
      retrovisor: checklistItems.find((item) => item.id === 'retrovisor')?.value
        ? 1
        : 0,
      tapiceria: checklistItems.find((item) => item.id === 'tapiceria')?.value
        ? 1
        : 0, 
      gps: checklistItems.find((item) => item.id === 'gps')?.value ? 1 : 0,
      combustible: this.mainInspectionForm.value.vehicleState.combustible || '',
      // panapass: this.mainInspectionForm.value.vehicleState.panapass || '',
      panapass: 1, // TODO: CORREGIR
      description: this.mainInspectionForm.value.vehicleState.descripcion || '',
    };

    console.log('Datos a enviar:', newInspectionData);

    this.apiService
      .postData('inspections/create_inspection', newInspectionData)
      .subscribe(
        (response: InspectionCreateResponse) => {
          console.log('Inspección creada con éxito:', response);
          this.inspectionCreateID = response.id;   
          this.openSnackbar('Inspección creada con éxito.');
        },
        (error) => {
          console.error('Error al crear la inspección:', error);
        }
      );
  }

  uploadImages() {
    if(this.takePhotosVehicleComponent) {
      this.takePhotosVehicleComponent.sendAllPhotos();
    }
  }
}
