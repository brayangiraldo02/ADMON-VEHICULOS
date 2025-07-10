import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { map, Observable, startWith } from 'rxjs';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

export interface owners {
  id: string;
  name: string;
}

export interface drivers {
  codigo_conductor: string;
  numero_unidad: string;
  nombre_conductor: string;
  cedula: string;
  codigo_propietario: string;
}

export interface vehicles {
  placa_vehiculo: string;
  numero_unidad: string;
  codigo_conductor: string;
  codigo_propietario: string;
  marca: string;
  linea: string;
  modelo: string;
}

export interface InspectionsInfoData {
  id: string;
  Fecha: string;
  Tipo: string;
  Descripcion: string;
  Unidad: string;
  Placa: string;
  Usuario: string;
  acciones: string;
}

export interface apiResponse {
  id: string;
  fecha_hora: string;
  tipo_inspeccion: string;
  descripcion: string;
  unidad: string;
  placa: string;
  nombre_usuario: string;
  acciones: string;
}

@Component({
  selector: 'app-inspections',
  templateUrl: './inspections.component.html',
  styleUrls: ['./inspections.component.css']
})
export class InspectionsComponent implements OnInit {
  inspectionForm!: FormGroup;
  owners: owners[] = [];
  drivers: drivers[] = [];
  vehicles: vehicles[] = [];

  allDrivers: drivers[] = [];
  allVehicles: vehicles[] = [];

  optionsOwners!: Observable<owners[]>;
  optionsDrivers!: Observable<drivers[]>;
  optionsVehicles!: Observable<vehicles[]>;

  maxDate: Date = new Date();

  isLoading = true;

  displayedColumns: string[] = [
    'Fecha',
    'Tipo',
    'Descripcion',
    'Unidad',
    'Placa',
    'Usuario',
    'Acciones',
  ];
  dataSource: MatTableDataSource<InspectionsInfoData>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private jwtService: JwtService,
    private snackBar: MatSnackBar,
  ) {
    this.dataSource = new MatTableDataSource<InspectionsInfoData>([]);
  }

  ngOnInit() {
    this.inspectionForm = this.fb.group({
      propietario: [''],
      conductor: [''],
      vehiculo: [''],
      fechaInicial: ['', Validators.required],
      fechaFinal: ['', Validators.required],
    });

    this.getDataAutoCompletes();
    this.getMaxDate();
    this.setupOwnerListener();
    this.setupDriverListener();
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  getDataAutoCompletes(){
    this.getDataOwners();
    this.getDataDrivers();
    this.getDataVehicles();
  }

  getMaxDate() {
    this.apiService.getData('extras/time').subscribe(
      (response: any) => {
        const dateParts = response.time.split('-');
        this.maxDate = new Date(
          parseInt(dateParts[0]), 
          parseInt(dateParts[1]) - 1, 
          parseInt(dateParts[2])
        );
      },
      (error) => {
        this.maxDate = new Date();
      }
    );
  }

  getUser() {
    const userData = this.jwtService.getUserData();
    return userData ? userData.nombre : '';
  }

  getCompany() {
    const userData = this.jwtService.getUserData();
    return userData ? userData.empresa : '';
  }

  getDataOwners(){
    const company = this.getCompany();
    this.apiService.getData('owners/'+company).subscribe(
      (data: owners[]) => {
        // Filtrar elementos con id vacío antes de almacenarlos
        this.owners = data.filter(owner => owner.id);
        this.optionsOwners = this.inspectionForm.get('propietario')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterOwners(value || '')),
        );
        this.isLoading = false; 
      }
    );
  }

  setupOwnerListener() {
    this.inspectionForm.get('propietario')?.valueChanges.subscribe(selectedOwner => {
      // Limpiar selecciones de conductor y vehículo cuando cambie el propietario
      this.inspectionForm.patchValue({
        conductor: '',
        vehiculo: ''
      });

      if (selectedOwner && selectedOwner.id) {
        // Filtrar conductores y vehículos por propietario seleccionado
        this.filterDriversByOwner(selectedOwner.id);
        this.filterVehiclesByOwner(selectedOwner.id);
      } else {
        // Si no hay propietario seleccionado, mostrar todos
        this.resetFilters();
      }
    });
  }

  setupDriverListener() {
    this.inspectionForm.get('conductor')?.valueChanges.subscribe(selectedDriver => {
      // Limpiar selección de vehículo cuando cambie el conductor
      this.inspectionForm.patchValue({
        vehiculo: ''
      });

      if (selectedDriver && selectedDriver.numero_unidad) {
        // Filtrar vehículos por conductor seleccionado
        this.filterVehiclesByDriver(selectedDriver.numero_unidad);
      } else {
        // Si no hay conductor seleccionado, filtrar por propietario (si hay uno seleccionado)
        const selectedOwner = this.inspectionForm.get('propietario')?.value;
        if (selectedOwner && selectedOwner.id) {
          this.filterVehiclesByOwner(selectedOwner.id);
        } else {
          this.resetVehicleFilter();
        }
      }
    });
  }

  filterDriversByOwner(ownerId: string) {
    this.drivers = this.allDrivers.filter(driver => driver.codigo_propietario === ownerId);
    this.optionsDrivers = this.inspectionForm.get('conductor')!.valueChanges.pipe(
      startWith(''),
      map(value => this._filterDrivers(value || '')),
    );
  }

  filterVehiclesByOwner(ownerId: string) {
    this.vehicles = this.allVehicles.filter(vehicle => vehicle.codigo_propietario === ownerId);
    this.optionsVehicles = this.inspectionForm.get('vehiculo')!.valueChanges.pipe(
      startWith(''),
      map(value => this._filterVehicles(value || '')),
    );
  }

  filterVehiclesByDriver(numeroUnidad: string) {
    this.vehicles = this.allVehicles.filter(vehicle => vehicle.numero_unidad === numeroUnidad);
    this.optionsVehicles = this.inspectionForm.get('vehiculo')!.valueChanges.pipe(
      startWith(''),
      map(value => this._filterVehicles(value || '')),
    );
  }

  resetVehicleFilter() {
    this.vehicles = [...this.allVehicles];
    this.optionsVehicles = this.inspectionForm.get('vehiculo')!.valueChanges.pipe(
      startWith(''),
      map(value => this._filterVehicles(value || '')),
    );
  }

  resetFilters() {
    this.drivers = [...this.allDrivers];
    this.vehicles = [...this.allVehicles];
    
    this.optionsDrivers = this.inspectionForm.get('conductor')!.valueChanges.pipe(
      startWith(''),
      map(value => this._filterDrivers(value || '')),
    );
    
    this.optionsVehicles = this.inspectionForm.get('vehiculo')!.valueChanges.pipe(
      startWith(''),
      map(value => this._filterVehicles(value || '')),
    );
  }

  getDataDrivers(){
    const company = this.getCompany();
    this.apiService.getData('inspections/drivers_data/'+company).subscribe(
      (data: drivers[]) => {
        this.allDrivers = data; // Guardar todos los conductores
        this.drivers = [...data]; // Inicializar con todos los datos
        this.optionsDrivers = this.inspectionForm.get('conductor')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterDrivers(value || '')),
        );
      }
    );
  }

  getDataVehicles(){
    const company = this.getCompany();
    this.apiService.getData('inspections/vehicles_data/'+company).subscribe(
      (data: vehicles[]) => {
        this.allVehicles = data; // Guardar todos los vehículos
        this.vehicles = [...data]; // Inicializar con todos los datos
        this.optionsVehicles = this.inspectionForm.get('vehiculo')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterVehicles(value || '')),
        );
      }
    );
  }

  private _filterOwners(value: string | owners): owners[] {
    const filterValue = typeof value === 'string' ? value.toLowerCase() : value.name.toLowerCase();
    return this.owners.filter(option => 
      option.name.toLowerCase().includes(filterValue) ||
      option.id.toLowerCase().includes(filterValue)
    );
  }
  
  private _filterDrivers(value: string | drivers): drivers[] {
    const filterValue = typeof value === 'string' ? value.toLowerCase() : value.nombre_conductor.toLowerCase();
    return this.drivers.filter(option => 
      option.nombre_conductor.toLowerCase().includes(filterValue) ||
      option.cedula.toLowerCase().includes(filterValue)
    );
  }
  
  private _filterVehicles(value: string | vehicles): vehicles[] {
    const filterValue = typeof value === 'string' ? value.toLowerCase() : value.placa_vehiculo.toLowerCase();
    return this.vehicles.filter(option => 
      option.placa_vehiculo.toLowerCase().includes(filterValue) || 
      option.numero_unidad.toLowerCase().includes(filterValue)
    );
  }

  displayOwnerName(owner: owners): string {
    return owner ? `${owner.name} - ${owner.id}` : '';
  }

  displayDriverName(driver: drivers): string {
    return driver ? `${driver.nombre_conductor} - ${driver.cedula}` : '';
  }

  displayVehiclePlate(vehicle: vehicles): string {
    return vehicle ? `${vehicle.numero_unidad} ${vehicle.placa_vehiculo} - ${vehicle.marca} ${vehicle.linea} ${vehicle.modelo}` : '';
  }

  clearTableData() {
    if (this.dataSource.data.length > 0) {
      this.dataSource.data = [];
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    }
  }

  getTableData() {
    if (this.inspectionForm.invalid) {
      this.inspectionForm.markAllAsTouched();
      return;
    }

    // Limpiar datos existentes de la tabla
    this.clearTableData();

    const formValues = this.inspectionForm.value;
  
    // Formatear las fechas para enviar solo YYYY-MM-DD
    const formattedValues = {
      conductor: formValues.conductor && formValues.conductor.codigo_conductor ? formValues.conductor.codigo_conductor : '',
      propietario: formValues.propietario && formValues.propietario.id ? formValues.propietario.id : '',
      vehiculo: formValues.vehiculo && formValues.vehiculo.numero_unidad ? formValues.vehiculo.numero_unidad : '',
      fechaInicial: formValues.fechaInicial ? new Date(formValues.fechaInicial).toISOString().split('T')[0] : '',
      fechaFinal: formValues.fechaFinal ? new Date(formValues.fechaFinal).toISOString().split('T')[0] : ''
    };

    const company = this.getCompany();
    
    console.log('Form Values:', formattedValues);

    this.apiService.postData('inspections/inspections_info/'+company, formattedValues).subscribe({
      next: (data: apiResponse[]) => {
        this.dataSource.data = data.map(item => ({
          id: item.id,
          Fecha: item.fecha_hora,
          Tipo: item.tipo_inspeccion,
          Descripcion: item.descripcion,
          Unidad: item.unidad,
          Placa: item.placa,
          Usuario: item.nombre_usuario,
          acciones: 'Edit',
        }));
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
        
        if (data.length === 0) {
          this.openSnackbar('No se encontraron inspecciones para los criterios seleccionados.');
        } else {
          this.openSnackbar('Inspecciones cargadas correctamente.');
        }
      },
      error: (error) => {
        console.error('Error fetching inspections:', error);
        
        if (error.status === 404) {
          this.openSnackbar('No se encontraron inspecciones para los criterios seleccionados.');
        } else {
          this.openSnackbar('Error al cargar las inspecciones. Por favor, inténtelo de nuevo más tarde.');
        }
      }
    });
  }

  getPdfData(){
    if (this.inspectionForm.invalid) {
      this.inspectionForm.markAllAsTouched();
      return;
    }

    const formValues = this.inspectionForm.value;
    const user = this.getUser();
  
    // Formatear las fechas para enviar solo YYYY-MM-DD
    const formattedValues = {
      usuario: user,
      conductor: formValues.conductor && formValues.conductor.codigo_conductor ? formValues.conductor.codigo_conductor : '',
      propietario: formValues.propietario && formValues.propietario.id ? formValues.propietario.id : '',
      vehiculo: formValues.vehiculo && formValues.vehiculo.numero_unidad ? formValues.vehiculo.numero_unidad : '',
      fechaInicial: formValues.fechaInicial ? new Date(formValues.fechaInicial).toISOString().split('T')[0] : '',
      fechaFinal: formValues.fechaFinal ? new Date(formValues.fechaFinal).toISOString().split('T')[0] : ''
    };

    const company = this.getCompany();

    const endpoint = 'inspections/report_inspections/'+company;

    if (endpoint) {
      localStorage.setItem('pdfEndpoint', endpoint);
      localStorage.setItem('pdfData', JSON.stringify(formattedValues));
      window.open(`/pdf`, '_blank');
    }
  }

  openSnackbar(message: string) {
    this.snackBar.open(message, 'Cerrar', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'top',
    })
  }
}