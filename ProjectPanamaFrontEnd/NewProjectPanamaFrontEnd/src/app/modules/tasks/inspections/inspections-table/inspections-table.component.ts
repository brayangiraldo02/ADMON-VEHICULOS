import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { MatPaginator } from '@angular/material/paginator';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { map, Observable, startWith } from 'rxjs';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';
import { InspectionsAddDialogComponent } from '../inspections-add-dialog/inspections-add-dialog.component';
import { InspectionFinishImagesDialogComponent } from '../inspection-finish-images-dialog/inspection-finish-images-dialog.component';
import { TakePhotosVehicleComponent } from '../take-photos-vehicle/take-photos-vehicle.component';

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
  Id_Tipo: string;
  Descripcion: string;
  Unidad: string;
  Placa: string;
  Usuario: string;
  Estado: string;
  Fotos: string[];
}

export interface apiResponse {
  id: string;
  fecha_hora: string;
  tipo_inspeccion: string;
  id_tipo_inspeccion: string;
  descripcion: string;
  unidad: string;
  placa: string;
  nombre_usuario: string;
  estado_inspeccion: string;
  fotos: string[];
}

@Component({
  selector: 'app-inspections',
  templateUrl: './inspections-table.component.html',
  styleUrls: ['./inspections-table.component.css'],
})
export class InspectionsTableComponent implements OnInit, AfterViewInit {
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
  isLoadingData = false;

  displayedColumns: string[] = [
    'Fecha',
    'Tipo',
    'Descripcion',
    'Unidad',
    'Placa',
    'Usuario',
    'Estado',
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
    private dialog: MatDialog,
    private breakpointObserver: BreakpointObserver
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
    if (this.paginator && this.sort) {
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    }
  }

  getDataAutoCompletes() {
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

  getDataOwners() {
    const company = this.getCompany();
    this.apiService.getData('owners/' + company).subscribe((data: owners[]) => {
      // Filtrar elementos con id vacío antes de almacenarlos
      this.owners = data.filter((owner) => owner.id);
      this.optionsOwners = this.inspectionForm
        .get('propietario')!
        .valueChanges.pipe(
          startWith(''),
          map((value) => this._filterOwners(value || ''))
        );
      this.isLoading = false;
    });
  }

  setupOwnerListener() {
    this.inspectionForm
      .get('propietario')
      ?.valueChanges.subscribe((selectedOwner) => {
        // Limpiar selecciones de conductor y vehículo cuando cambie el propietario
        this.inspectionForm.patchValue({
          conductor: '',
          vehiculo: '',
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
    // Configurar listener para vehículo (ahora el vehículo filtra los conductores)
    this.inspectionForm
      .get('vehiculo')
      ?.valueChanges.subscribe((selectedVehicle) => {
        // Limpiar selección de conductor cuando cambie el vehículo
        this.inspectionForm.patchValue({
          conductor: '',
        });

        if (selectedVehicle && selectedVehicle.numero_unidad) {
          // Filtrar conductores por vehículo seleccionado
          this.filterDriversByVehicle(selectedVehicle.numero_unidad);
        } else {
          // Si no hay vehículo seleccionado, filtrar por propietario (si hay uno seleccionado)
          const selectedOwner = this.inspectionForm.get('propietario')?.value;
          if (selectedOwner && selectedOwner.id) {
            this.filterDriversByOwner(selectedOwner.id);
          } else {
            this.resetDriverFilter();
          }
        }
      });
  }

  filterDriversByOwner(ownerId: string) {
    this.drivers = this.allDrivers.filter(
      (driver) => driver.codigo_propietario === ownerId
    );
    this.optionsDrivers = this.inspectionForm
      .get('conductor')!
      .valueChanges.pipe(
        startWith(''),
        map((value) => this._filterDrivers(value || ''))
      );
  }

  filterVehiclesByOwner(ownerId: string) {
    this.vehicles = this.allVehicles.filter(
      (vehicle) => vehicle.codigo_propietario === ownerId
    );
    this.optionsVehicles = this.inspectionForm
      .get('vehiculo')!
      .valueChanges.pipe(
        startWith(''),
        map((value) => this._filterVehicles(value || ''))
      );
  }

  filterDriversByVehicle(numeroUnidad: string) {
    // Encontrar el vehículo seleccionado para obtener su código de conductor
    const selectedVehicle = this.allVehicles.find(
      (vehicle) => vehicle.numero_unidad === numeroUnidad
    );
    if (selectedVehicle) {
      // Filtrar conductores que puedan manejar este vehículo (mismo numero_unidad)
      this.drivers = this.allDrivers.filter(
        (driver) => driver.numero_unidad === numeroUnidad
      );
    } else {
      this.drivers = [];
    }
    this.optionsDrivers = this.inspectionForm
      .get('conductor')!
      .valueChanges.pipe(
        startWith(''),
        map((value) => this._filterDrivers(value || ''))
      );
  }

  resetDriverFilter() {
    this.drivers = [...this.allDrivers];
    this.optionsDrivers = this.inspectionForm
      .get('conductor')!
      .valueChanges.pipe(
        startWith(''),
        map((value) => this._filterDrivers(value || ''))
      );
  }

  resetVehicleFilter() {
    this.vehicles = [...this.allVehicles];
    this.optionsVehicles = this.inspectionForm
      .get('vehiculo')!
      .valueChanges.pipe(
        startWith(''),
        map((value) => this._filterVehicles(value || ''))
      );
  }

  resetFilters() {
    this.drivers = [...this.allDrivers];
    this.vehicles = [...this.allVehicles];

    this.optionsDrivers = this.inspectionForm
      .get('conductor')!
      .valueChanges.pipe(
        startWith(''),
        map((value) => this._filterDrivers(value || ''))
      );

    this.optionsVehicles = this.inspectionForm
      .get('vehiculo')!
      .valueChanges.pipe(
        startWith(''),
        map((value) => this._filterVehicles(value || ''))
      );
  }

  getDataDrivers() {
    const company = this.getCompany();
    this.apiService
      .getData('inspections/drivers_data/' + company)
      .subscribe((data: drivers[]) => {
        this.allDrivers = data; // Guardar todos los conductores
        this.drivers = [...data]; // Inicializar con todos los datos
        this.optionsDrivers = this.inspectionForm
          .get('conductor')!
          .valueChanges.pipe(
            startWith(''),
            map((value) => this._filterDrivers(value || ''))
          );
      });
  }

  getDataVehicles() {
    const company = this.getCompany();
    this.apiService
      .getData('inspections/vehicles_data/' + company)
      .subscribe((data: vehicles[]) => {
        this.allVehicles = data; // Guardar todos los vehículos
        this.vehicles = [...data]; // Inicializar con todos los datos
        this.optionsVehicles = this.inspectionForm
          .get('vehiculo')!
          .valueChanges.pipe(
            startWith(''),
            map((value) => this._filterVehicles(value || ''))
          );
      });
  }

  private _filterOwners(value: string | owners): owners[] {
    const filterValue =
      typeof value === 'string'
        ? value.toLowerCase()
        : value.name.toLowerCase();
    return this.owners.filter(
      (option) =>
        option.name.toLowerCase().includes(filterValue) ||
        option.id.toLowerCase().includes(filterValue)
    );
  }

  private _filterDrivers(value: string | drivers): drivers[] {
    const filterValue =
      typeof value === 'string'
        ? value.toLowerCase()
        : value.nombre_conductor.toLowerCase();
    return this.drivers.filter(
      (option) =>
        option.nombre_conductor.toLowerCase().includes(filterValue) ||
        option.cedula.toLowerCase().includes(filterValue)
    );
  }

  private _filterVehicles(value: string | vehicles): vehicles[] {
    const filterValue =
      typeof value === 'string'
        ? value.toLowerCase()
        : value.placa_vehiculo.toLowerCase();
    return this.vehicles.filter(
      (option) =>
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
    return vehicle
      ? `${vehicle.numero_unidad} ${vehicle.placa_vehiculo} - ${vehicle.marca} ${vehicle.linea} ${vehicle.modelo}`
      : '';
  }

  private initializePaginator() {
    setTimeout(() => {
      if (this.paginator && this.sort) {
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
      }
    }, 0);
  }

  clearTableData() {
    if (this.dataSource.data.length > 0) {
      this.dataSource.data = [];
      // Reinicializar el paginator y sort
      this.initializePaginator();
    }
  }

  getTableData() {
    if (this.inspectionForm.invalid) {
      this.inspectionForm.markAllAsTouched();
      return;
    }

    // Limpiar datos existentes de la tabla
    this.clearTableData();

    this.isLoadingData = true;

    const formValues = this.inspectionForm.value;

    // Formatear las fechas para enviar solo YYYY-MM-DD
    const formattedValues = {
      conductor:
        formValues.conductor && formValues.conductor.codigo_conductor
          ? formValues.conductor.codigo_conductor
          : '',
      propietario:
        formValues.propietario && formValues.propietario.id
          ? formValues.propietario.id
          : '',
      vehiculo:
        formValues.vehiculo && formValues.vehiculo.numero_unidad
          ? formValues.vehiculo.numero_unidad
          : '',
      fechaInicial: formValues.fechaInicial
        ? new Date(formValues.fechaInicial).toISOString().split('T')[0]
        : '',
      fechaFinal: formValues.fechaFinal
        ? new Date(formValues.fechaFinal).toISOString().split('T')[0]
        : '',
    };

    const company = this.getCompany();

    console.log('Form Values:', formattedValues);

    this.apiService
      .postData('inspections/inspections_info/' + company, formattedValues)
      .subscribe({
        next: (data: apiResponse[]) => {
          this.dataSource.data = data.map((item) => ({
            id: item.id,
            Fecha: item.fecha_hora,
            Tipo: item.tipo_inspeccion,
            Id_Tipo: item.id_tipo_inspeccion,
            Descripcion: item.descripcion,
            Unidad: item.unidad,
            Placa: item.placa,
            Usuario: item.nombre_usuario,
            Estado: item.estado_inspeccion,
            Fotos: item.fotos || [],
          }));
          
          // Reinicializar paginator y sort después de cargar los datos
          this.initializePaginator();

          if (data.length === 0) {
            this.openSnackbar(
              'No se encontraron inspecciones para los criterios seleccionados.'
            );
          } else {
            this.openSnackbar('Inspecciones cargadas correctamente.');
          }

          this.isLoadingData = false;
        },
        error: (error) => {
          console.error('Error fetching inspections:', error);

          if (error.status === 404) {
            this.openSnackbar(
              'No se encontraron inspecciones para los criterios seleccionados.'
            );
          } else {
            this.openSnackbar(
              'Error al cargar las inspecciones. Por favor, inténtelo de nuevo más tarde.'
            );
          }
          this.isLoadingData = false;
        },
      });
  }

  getPdfData() {
    if (this.inspectionForm.invalid) {
      this.inspectionForm.markAllAsTouched();
      return;
    }

    const formValues = this.inspectionForm.value;
    const user = this.getUser();

    // Formatear las fechas para enviar solo YYYY-MM-DD
    const formattedValues = {
      usuario: user,
      conductor:
        formValues.conductor && formValues.conductor.codigo_conductor
          ? formValues.conductor.codigo_conductor
          : '',
      propietario:
        formValues.propietario && formValues.propietario.id
          ? formValues.propietario.id
          : '',
      vehiculo:
        formValues.vehiculo && formValues.vehiculo.numero_unidad
          ? formValues.vehiculo.numero_unidad
          : '',
      fechaInicial: formValues.fechaInicial
        ? new Date(formValues.fechaInicial).toISOString().split('T')[0]
        : '',
      fechaFinal: formValues.fechaFinal
        ? new Date(formValues.fechaFinal).toISOString().split('T')[0]
        : '',
    };

    const company = this.getCompany();

    const endpoint = 'inspections/report_inspections/' + company;

    if (endpoint) {
      localStorage.setItem('pdfEndpoint', endpoint);
      localStorage.setItem('pdfData', JSON.stringify(formattedValues));
      window.open(`/pdf`, '_blank');
    }
  }

  openDialogInspectionAdd() {
    const isSmallScreen = this.breakpointObserver.isMatched(Breakpoints.XSmall);
    const dialogWidth = isSmallScreen ? '90vw' : '60%';

    const dialogRef = this.dialog.open(InspectionsAddDialogComponent, {
      width: dialogWidth,
      disableClose: true,
    });

    dialogRef.afterClosed().subscribe((result) => {
      console.log('Result from dialog:', result);
      if (result === 'refresh') {
        const formValues = this.inspectionForm.value;
        const hasFilter =
          formValues.propietario ||
          formValues.conductor ||
          formValues.vehiculo ||
          formValues.fechaInicial ||
          formValues.fechaFinal;
        console.log('Has filter:', hasFilter);
        if (hasFilter) {
          console.log('Refreshing table data...');
          this.getTableData();
        }
      }
    });
  }

  openSnackbar(message: string) {
    this.snackBar.open(message, 'Cerrar', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'top',
    });
  }

  getEstadoText(estado: string): string {
    switch (estado) {
      case 'PEN':
        return '<strong>PENDIENTE</strong>';
      case 'SUS':
        return '<strong>SUSPENDIDO</strong>';
      case 'FIN':
        return 'FINALIZADO';
      default:
        return 'DESCONOCIDO';
    }
  }

  openImgDialog(inspection: InspectionsInfoData) {
    const isSmallScreen = this.breakpointObserver.isMatched(Breakpoints.XSmall);
    const dialogWidth = isSmallScreen ? '90vw' : '60%';

    this.dialog.open(InspectionFinishImagesDialogComponent, {
      width: dialogWidth,
      data: {
        vehicleNumber: inspection.Unidad,
        images: inspection.Fotos,
      },
    });
  }

  openUploadImagesDialog(inspection: InspectionsInfoData) {
    if (inspection.Estado !== 'PEN') {
      this.openSnackbar(
        'Solo se pueden subir fotos a inspecciones PENDIENTES.'
      );
      return;
    }

    const isSmallScreen = this.breakpointObserver.isMatched(Breakpoints.XSmall);
    const dialogWidth = isSmallScreen ? '90vw' : '60%';

    console.log(inspection);

    const dialogRef = this.dialog.open(InspectionsAddDialogComponent, {
      width: dialogWidth,
      data: {
        idInspection: inspection.id,
        idTypeInspection: inspection.Id_Tipo,
      },
      disableClose: true,
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result === 'refresh') {
        const formValues = this.inspectionForm.value;
        const hasFilter =
          formValues.propietario ||
          formValues.conductor ||
          formValues.vehiculo ||
          formValues.fechaInicial ||
          formValues.fechaFinal;
        if (hasFilter) {
          this.getTableData();
        }
      }
    });
  }
}
