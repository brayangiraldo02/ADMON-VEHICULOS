import { Component, Input } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { PanapassDialogComponent } from '../../panapass-dialog/panapass-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';

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

  constructor(
    private fb: FormBuilder,
    private dialog: MatDialog,
    private breakpointObserver: BreakpointObserver
  ) {}

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

  openGetPanapassDialog() {
    const isSmallScreen = this.breakpointObserver.isMatched(Breakpoints.XSmall);
    const dialogWidth = isSmallScreen ? '90vw' : '60%';

    const dialogRef = this.dialog.open(PanapassDialogComponent, {
      width: dialogWidth,
    });
  }

  // Función para validar que solo se ingresen números
  onlyNumbers(event: KeyboardEvent): boolean {
    const charCode = event.which ? event.which : event.keyCode;
    
    // Permitir teclas especiales: backspace, delete, tab, escape, enter, home, end, flechas
    if (charCode === 8 || charCode === 9 || charCode === 27 || charCode === 13 ||
        charCode === 35 || charCode === 36 ||
        (charCode >= 37 && charCode <= 40) || charCode === 46) {
      return true;
    }
    
    // Permitir Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X, Ctrl+Z
    if (event.ctrlKey && (charCode === 65 || charCode === 67 || charCode === 86 || charCode === 88 || charCode === 90)) {
      return true;
    }
    
    // Solo permitir números (0-9)
    if (charCode < 48 || charCode > 57) {
      event.preventDefault();
      return false;
    }
    
    return true;
  }
}
