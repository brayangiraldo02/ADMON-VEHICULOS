import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { map, Observable, startWith } from 'rxjs';

@Component({
  selector: 'app-inspections',
  templateUrl: './inspections.component.html',
  styleUrls: ['./inspections.component.css']
})
export class InspectionsComponent implements OnInit {
  inspectionForm!: FormGroup;
  opcionesPropietarios: string[] = ['One', 'Two', 'Three'];
  opcionesConductor: string[] = ['One', 'Two', 'Three'];
  opcionesVehiculo: string[] = ['One', 'Two', 'Three'];
  opcionesFiltradas1!: Observable<string[]>;
  opcionesFiltradas2!: Observable<string[]>;
  opcionesFiltradas3!: Observable<string[]>;

  constructor(private fb: FormBuilder) {}

  ngOnInit() {
    this.inspectionForm = this.fb.group({
      propietario: [''],
      conductor: [''],
      vehiculo: [''],
      fechaInicial: [''],
      fechaFinal: ['']
    });

    this.opcionesFiltradas1 = this.inspectionForm.get('propietario')!.valueChanges.pipe(
      startWith(''),
      map(value => this._filter(value || '', this.opcionesPropietarios)),
    );

    this.opcionesFiltradas2 = this.inspectionForm.get('conductor')!.valueChanges.pipe(
      startWith(''),
      map(value => this._filter(value || '', this.opcionesConductor)),
    );

    this.opcionesFiltradas2 = this.inspectionForm.get('vehiculo')!.valueChanges.pipe(
      startWith(''),
      map(value => this._filter(value || '', this.opcionesVehiculo)),
    );
  }

  private _filter(value: string, options: string[]): string[] {
    const filterValue = value.toLowerCase();

    return options.filter(option => option.toLowerCase().includes(filterValue));
  }
}