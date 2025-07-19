import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { map, Observable, startWith } from 'rxjs';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

interface Vehicles {
  placa_vehiculo: string;
  numero_unidad: string;
  marca: string;
  linea: string;
  modelo: string;
  nro_cupo: string;
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
  styleUrls: ['./inspections-add-dialog.component.css']
})
export class InspectionsAddDialogComponent implements OnInit {
  vehiclesForm!: FormGroup;

  isLoading: boolean = true;

  vehicles: Vehicles[] = [];
  optionsVehicles!: Observable<Vehicles[]>;

  constructor(
    private apiService: ApiService,
    private jwtService: JwtService,
    private formBuilder: FormBuilder,
  ) {}

  ngOnInit(): void {
    this.getDataVehicles();
    this.initForm();
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
      (data: Vehicles[]) => {
        this.vehicles = [...data];
        this.optionsVehicles = this.vehiclesForm.get('vehiculo')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterVehicles(value || '')),
        );
        this.isLoading = false;
      }
    );
  }

  private _filterVehicles(value: string | Vehicles): Vehicles[] {
    const filterValue = typeof value === 'string' ? value.toLowerCase() : value.placa_vehiculo.toLowerCase();
    return this.vehicles.filter(option => 
      option.placa_vehiculo.toLowerCase().includes(filterValue) || 
      option.numero_unidad.toLowerCase().includes(filterValue) ||
      option.nro_cupo.toLowerCase().includes(filterValue)
    );
  }

  displayVehicleData(vehicle: Vehicles): string {
    return vehicle ? `${vehicle.numero_unidad} ${vehicle.placa_vehiculo} - ${vehicle.marca} ${vehicle.linea} ${vehicle.modelo}` : '';
  }

  selectedOptionVehicle(event: MatAutocompleteSelectedEvent): void {
    const selectedVehicle = event.option.value;
    // this.documentsInfo = []; // Limpiamos al cambiar de vehículo

    if (selectedVehicle) {
      console.log('Vehículo seleccionado:', selectedVehicle);
    } else {
      this.vehiclesForm.get('vehiculo')?.reset('');
    }
  }
}
