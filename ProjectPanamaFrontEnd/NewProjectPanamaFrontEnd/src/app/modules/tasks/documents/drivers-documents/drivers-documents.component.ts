import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { map, Observable, startWith } from 'rxjs';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

export interface drivers {
  codigo_conductor: string;
  numero_unidad: string;
  nombre_conductor: string;
  cedula: string;
  codigo_propietario: string;
}

@Component({
  selector: 'app-drivers-documents',
  templateUrl: './drivers-documents.component.html',
  styleUrls: ['./drivers-documents.component.css']
})
export class DriversDocumentsComponent implements OnInit{
  driversForm!: FormGroup;

  isLoading: boolean = true;

  drivers: drivers[] = [];

  optionsDrivers!: Observable<drivers[]>;

  constructor(
    private apiService: ApiService,
    private jwtService: JwtService,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.getDataDrivers();
  }

  initForm(): void {
    this.driversForm = this.formBuilder.group({
      conductor: ['']
    });
  }

  getCompany() {
    const userData = this.jwtService.getUserData();
    return userData ? userData.empresa : '';
  }

  getDataDrivers(){
    const company = this.getCompany();
    this.apiService.getData('inspections/drivers_data/'+company).subscribe(
      (data: drivers[]) => {
        this.drivers = [...data]; // Inicializar con todos los datos
        this.optionsDrivers = this.driversForm.get('conductor')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterDrivers(value || '')),
        );
        this.isLoading = false;
      }
    );
  }

  private _filterDrivers(value: string | drivers): drivers[] {
    const filterValue = typeof value === 'string' ? value.toLowerCase() : value.nombre_conductor.toLowerCase();
    return this.drivers.filter(option => 
      option.nombre_conductor.toLowerCase().includes(filterValue) ||
      option.cedula.toLowerCase().includes(filterValue)
    );
  }

  displayDriverName(driver: drivers): string {
    return driver ? `${driver.nombre_conductor} - ${driver.cedula}` : '';
  }
}
