import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { map, Observable, startWith } from 'rxjs';
import { ApiService } from 'src/app/services/api.service';

export interface owners {
  codigo_propietario: string;
  nombre_propietario: string;
  conductores: drivers[];
  vehiculos: vehicles[];
}

export interface drivers {
  codigo_conductor: string;
  numero_unidad: string;
  nombre_conductor: string;
  cedula: string;
}

export interface vehicles {
  placa_vehiculo: string;
  numero_unidad: string;
  codigo_conductor: string;
  marca: string;
  linea: string;
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
  optionsOwners!: Observable<owners[]>;
  optionsDrivers!: Observable<drivers[]>;
  optionsVehicles!: Observable<vehicles[]>;

  isLoading = true;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) {}

  ngOnInit() {
    this.inspectionForm = this.fb.group({
      propietario: [''],
      conductor: [''],
      vehiculo: [''],
      fechaInicial: [''],
      fechaFinal: ['']
    });

    this.getDataAutoCompletes();
  }

  getDataAutoCompletes(){
    this.getDataOwners();
    this.getDataDrivers();
    this.getDataVehicles();
  }

  getDataOwners(){
    this.apiService.getData('owners_data/58').subscribe(
      (data: owners[]) => {
        this.owners = data;
        this.optionsOwners = this.inspectionForm.get('propietario')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterOwners(value || '')),
        );
        this.isLoading = false; 
      }
    );
  }

  getDataDrivers(){
    this.apiService.getData('drivers_data/58').subscribe(
      (data: drivers[]) => {
        this.drivers = data;
        this.optionsDrivers = this.inspectionForm.get('conductor')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterDrivers(value || '')),
        );
      }
    );
  }

  getDataVehicles(){
    this.apiService.getData('vehicles_data/58').subscribe(
      (data: vehicles[]) => {
        this.vehicles = data;
        this.optionsVehicles = this.inspectionForm.get('vehiculo')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterVehicles(value || '')),
        );
      }
    );
  }

  private _filterOwners(value: string): owners[] {
    const filterValue = value.toLowerCase();
    return this.owners.filter(option => option.nombre_propietario.toLowerCase().includes(filterValue));
  }

  private _filterDrivers(value: string): drivers[] {
    const filterValue = value.toLowerCase();
    // Aquí asumimos que cuando se selecciona un propietario, this.opcionesConductor se llena.
    return this.drivers.filter(option => option.nombre_conductor.toLowerCase().includes(filterValue));
  }

  private _filterVehicles(value: string): vehicles[] {
    const filterValue = value.toLowerCase();
    // Aquí asumimos que cuando se selecciona un propietario, this.opcionesVehiculo se llena.
    return this.vehicles.filter(option => option.placa_vehiculo.toLowerCase().includes(filterValue));
  }

  displayOwnerName(owner: owners): string {
    return owner ? `${owner.nombre_propietario} - ${owner.codigo_propietario}` : '';
  }

  displayDriverName(driver: drivers): string {
    return driver ? `${driver.nombre_conductor} - ${driver.cedula}` : '';
  }

  displayVehiclePlate(vehicle: vehicles): string {
    return vehicle ? `${vehicle.placa_vehiculo} - ${vehicle.marca} ${vehicle.linea}` : '';
  }
}