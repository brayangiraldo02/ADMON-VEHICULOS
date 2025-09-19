import { Component, Input } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-vehicle-states-form',
  templateUrl: './vehicle-states-form.component.html',
  styleUrls: ['./vehicle-states-form.component.css'],
})
export class VehicleStatesFormComponent {
  @Input() vehicleNumber: string = '';

  checklistItems = [
    { id: 'alfombra', label: 'Alfombra' },
    { id: 'antena', label: 'Antena' },
    { id: 'caratula_radio', label: 'Carátula de Radio' },
    { id: 'copas', label: 'Copas' },
    { id: 'copas_rines', label: 'Copas/Rines' },
    { id: 'extinguidor', label: 'Extinguidor' },
    {
      id: 'formato_colisiones_menores',
      label: 'Formato de Colisiones Menores',
    },
    { id: 'gato', label: 'Gato' },
    { id: 'gps', label: 'GPS' },
    { id: 'lamparas', label: 'Lámparas' },
    { id: 'llanta_repuesto', label: 'Llanta de Repuestos' },
    { id: 'luces_delanteras', label: 'Luces Delanteras' },
    { id: 'luces_traseras', label: 'Luces Traseras' },
    { id: 'pago_municipio', label: 'Pago Municipio' },
    { id: 'pipa', label: 'Pipa' },
    { id: 'placa_municipal', label: 'Placa Municipal' },
    { id: 'poliza_seguro', label: 'Póliza de Seguros' },
    { id: 'registro_vehiculo', label: 'Registro Vehículo' },
    { id: 'retrovisor', label: 'Retrovisor' },
    { id: 'revisado', label: 'Revisado' },
    { id: 'tapiceria', label: 'Tapicería' },
    { id: 'triangulo', label: 'Triángulo' },
    { id: 'vidrios', label: 'Vidrios' },
  ];

  vehicleForm!: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.vehicleForm = this.fb.group({
      combustible: ['', Validators.required],
      kilometraje: ['', Validators.required],
      panapass: ['', Validators.required],
      descripcion: ['', Validators.required],
      nota: [''],

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
