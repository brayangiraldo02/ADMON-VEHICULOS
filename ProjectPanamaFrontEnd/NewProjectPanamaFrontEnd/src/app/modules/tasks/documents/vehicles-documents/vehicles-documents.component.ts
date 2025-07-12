import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { map, Observable, startWith } from 'rxjs';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

export interface vehicles {
  placa_vehiculo: string;
  numero_unidad: string;
  codigo_conductor: string;
  codigo_propietario: string;
  marca: string;
  linea: string;
  modelo: string;
}

@Component({
  selector: 'app-vehicles-documents',
  templateUrl: './vehicles-documents.component.html',
  styleUrls: ['./vehicles-documents.component.css']
})
export class VehiclesDocumentsComponent implements OnInit {
  vehiclesForm!: FormGroup;

  isLoading: boolean = true;

  vehicles: vehicles[] = [];

  optionsVehicles!: Observable<vehicles[]>;

  constructor(
    private apiService: ApiService,
    private jwtService: JwtService,
    private formBuilder: FormBuilder
  ){}

  ngOnInit(): void {
    this.initForm();
    this.getDataVehicles();
  }

  initForm(): void {
    this.vehiclesForm = this.formBuilder.group({
      vehiculo: ['']
    });
  }

  getCompany() {
    const userData = this.jwtService.getUserData();
    return userData ? userData.empresa : '';
  }

  getDataVehicles(){
    const company = this.getCompany();
    this.apiService.getData('inspections/vehicles_data/'+company).subscribe(
      (data: vehicles[]) => {
        this.vehicles = [...data]; // Inicializar con todos los datos
        this.optionsVehicles = this.vehiclesForm.get('vehiculo')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterVehicles(value || '')),
        );
        this.isLoading = false;
      }
    );
  }

  private _filterVehicles(value: string | vehicles): vehicles[] {
    const filterValue = typeof value === 'string' ? value.toLowerCase() : value.placa_vehiculo.toLowerCase();
    return this.vehicles.filter(option => 
      option.placa_vehiculo.toLowerCase().includes(filterValue) || 
      option.numero_unidad.toLowerCase().includes(filterValue)
    );
  }

  displayVehiclePlate(vehicle: vehicles): string {
    return vehicle ? `${vehicle.numero_unidad} ${vehicle.placa_vehiculo} - ${vehicle.marca} ${vehicle.linea} ${vehicle.modelo}` : '';
  }
}
