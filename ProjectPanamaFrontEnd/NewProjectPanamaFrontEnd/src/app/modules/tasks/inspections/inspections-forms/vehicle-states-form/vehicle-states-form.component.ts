import { Component } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-vehicle-states-form',
  templateUrl: './vehicle-states-form.component.html',
  styleUrls: ['./vehicle-states-form.component.css'],
})
export class VehicleStatesFormComponent {
  checklistItems = [
    { id: 'alfombra', label: 'Alfombra' },
    { id: 'copas_rines', label: 'Copas/Rines' },
    { id: 'extinguidor', label: 'Extinguidor' },
    { id: 'antena', label: 'Antena' },
    { id: 'lamparas', label: 'Lámparas' },
    { id: 'triangulo', label: 'Triángulo' },
    { id: 'gato', label: 'Gato' },
    { id: 'pipa', label: 'Pipa' },
    { id: 'copas', label: 'Copas' },
    { id: 'llanta_repuesto', label: 'Llanta de Repuestos' },
    { id: 'placa_municipal', label: 'Placa Municipal' },
    { id: 'caratula_radio', label: 'Carátula de Radio' },
    { id: 'registro_vehiculo', label: 'Registro Vehículo' },
    { id: 'revisado', label: 'Revisado' },
    { id: 'pago_municipio', label: 'Pago Municipio' },
    {
      id: 'formato_colisiones_menores',
      label: 'Formato de Colisiones Menores',
    },
    { id: 'poliza_seguro', label: 'Póliza de Seguros' },
    { id: 'luces_delanteras', label: 'Luces Delanteras' },
    { id: 'luces_traseras', label: 'Luces Traseras' },
    { id: 'vidrios', label: 'Vidrios' },
    { id: 'retrovisor', label: 'Retrovisor' },
    { id: 'tapiceria', label: 'Tapicería' },
    { id: 'gps', label: 'GPS' },
  ];

  vehicleForm!: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.vehicleForm = this.fb.group({
      combustible: ['', Validators.required],
      kilometraje: ['', Validators.required],
      panapass: ['', Validators.required],
      descripcion: ['', Validators.required],

      checklistItems: this.fb.array(
        this.checklistItems.map((item) =>
          this.fb.group({
            id: [item.id],
            label: [item.label],
            value: [null, Validators.required],
          })
        )
      ),
    });
  }

  get checklistItemsArray(): FormArray {
    return this.vehicleForm.get('checklistItems') as FormArray;
  }
}
