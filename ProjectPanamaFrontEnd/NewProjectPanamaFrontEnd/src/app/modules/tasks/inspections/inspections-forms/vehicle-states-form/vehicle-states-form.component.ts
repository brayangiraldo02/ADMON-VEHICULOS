import { Component } from '@angular/core';
import { FormArray, FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-vehicle-states-form',
  templateUrl: './vehicle-states-form.component.html',
  styleUrls: ['./vehicle-states-form.component.css'],
})
export class VehicleStatesFormComponent {
  checklistItems = [
    { id: 'alfombra', label: 'Alfombra' },
    { id: 'copas', label: 'Copas/Rines' },
    { id: 'extinguidor', label: 'Extinguidor' },
    { id: 'antena', label: 'Antena' },
    { id: 'lamparas', label: 'Lámparas' },
    { id: 'triangulo', label: 'Triángulo' },
    { id: 'gato', label: 'Gato' },
    { id: 'pipa', label: 'Pipa' },
    { id: 'copas', label: 'Copas' },
    { id: 'llanta-repuestos', label: 'Llanta de Repuestos' },
    { id: 'placa-municipal', label: 'Placa Municipal' },
    { id: 'caratula-radio', label: 'Carátula de Radio' },
    { id: 'registro-vehiculo', label: 'Registro Vehículo' },
    { id: 'revisado', label: 'Revisado' },
    { id: 'pago-municipio', label: 'Pago Municipio' },
    {
      id: 'formato-colisiones-menores',
      label: 'Formato de Colisiones Menores',
    },
    { id: 'poliza-seguros', label: 'Póliza de Seguros' },
    { id: 'luces-delanteras', label: 'Luces Delanteras' },
    { id: 'luces-traseras', label: 'Luces Traseras' },
    { id: 'vidrios', label: 'Vidrios' },
    { id: 'retrovisor', label: 'Retrovisor' },
    { id: 'gps', label: 'GPS' },
  ];

  vehicleForm!: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.vehicleForm = this.fb.group({
      // Controles para los textareas
      combustible: [''], // Valor inicial: string vacío
      kilometraje: [''],
      panapass: [''],
      descripcion: [''],

      // Un FormArray para la lista dinámica de checklist
      checklistItems: this.fb.array(
        this.checklistItems.map((item) =>
          this.fb.group({
            id: [item.id],
            label: [item.label],
            value: [null], // Valor inicial para cada radio button
          })
        )
      ),
    });
  }

  // Getter para acceder fácilmente al FormArray en la plantilla HTML
  get checklistItemsArray(): FormArray {
    return this.vehicleForm.get('checklistItems') as FormArray;
  }

  mostrarValores() {
    console.log('--- Objeto completo del FormGroup ---');
    console.log(this.vehicleForm.value);

    // Si necesitas el valor RAW (incluyendo controles deshabilitados, etc.)
    // console.log(this.vehicleForm.getRawValue());
  }
}
