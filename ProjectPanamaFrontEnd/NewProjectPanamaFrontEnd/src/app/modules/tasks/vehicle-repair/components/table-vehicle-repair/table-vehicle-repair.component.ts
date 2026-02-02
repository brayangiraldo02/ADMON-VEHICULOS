import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';

export interface VehicleRepairData {
  Fecha: string;
  Descripcion: string;
  Unidad: string;
  Placa: string;
  Cupo: string;
  Usuario: string;
  Propietario: string;
  Estado: string;
  PuedeEditar: number;
}

// Datos mockup para la tabla
const MOCK_DATA: VehicleRepairData[] = [
  {
    Fecha: '26-01-2026 18:05',
    Descripcion: 'a',
    Unidad: 'TT232',
    Placa: 'EE9910',
    Cupo: '8RIO487',
    Usuario: 'HECTOR F. VANECAS G.',
    Propietario: 'TOTAL TAXI PANAMA S.A.',
    Estado: 'SUS',
    PuedeEditar: 0,
  },
  {
    Fecha: '21-01-2026 16:43',
    Descripcion: 'A',
    Unidad: 'TT232',
    Placa: 'EE9910',
    Cupo: '8RIO487',
    Usuario: 'HECTOR F. VANECAS G.',
    Propietario: 'TOTAL TAXI PANAMA S.A.',
    Estado: 'PEN',
    PuedeEditar: 1,
  },
  {
    Fecha: '20-01-2026 15:44',
    Descripcion: 'a',
    Unidad: 'TT232',
    Placa: 'EE9910',
    Cupo: '8RIO487',
    Usuario: 'HECTOR F. VANECAS G.',
    Propietario: 'TOTAL TAXI PANAMA S.A.',
    Estado: 'SUS',
    PuedeEditar: 0,
  },
  {
    Fecha: '19-01-2026 19:47',
    Descripcion: 'A',
    Unidad: 'TT232',
    Placa: 'EE9910',
    Cupo: '8RIO487',
    Usuario: 'HECTOR F. VANECAS G.',
    Propietario: 'TOTAL TAXI PANAMA S.A.',
    Estado: 'SUS',
    PuedeEditar: 0,
  },
  {
    Fecha: '19-01-2026 18:32',
    Descripcion: 'PRUEBA',
    Unidad: 'TT232',
    Placa: 'EE9910',
    Cupo: '8RIO487',
    Usuario: 'HECTOR F. VANECAS G.',
    Propietario: 'TOTAL TAXI PANAMA S.A.',
    Estado: 'SUS',
    PuedeEditar: 0,
  },
  {
    Fecha: '26-11-2025 21:26',
    Descripcion: 'PRUEBA',
    Unidad: '0340',
    Placa: 'EQ8196',
    Cupo: '13TI716',
    Usuario: 'HECTOR F. VANECAS G.',
    Propietario: 'TOTAL TAXI 2',
    Estado: 'FIN',
    PuedeEditar: 0,
  },
  {
    Fecha: '26-11-2025 21:25',
    Descripcion: 'PRUEBA',
    Unidad: 'TT232',
    Placa: 'EE9910',
    Cupo: '8RIO487',
    Usuario: 'HECTOR F. VANECAS G.',
    Propietario: 'TOTAL TAXI PANAMA S.A.',
    Estado: 'FIN',
    PuedeEditar: 0,
  },
  {
    Fecha: '08-11-2025 11:37',
    Descripcion: 'prueba desarrollo',
    Unidad: 'TT232',
    Placa: 'EE9910',
    Cupo: '8RIO487',
    Usuario: 'HECTOR F. VANECAS G.',
    Propietario: 'TOTAL TAXI PANAMA S.A.',
    Estado: 'FIN',
    PuedeEditar: 0,
  },
];

// Opciones mockup para los autocompletes
const MOCK_OWNERS = [
  { id: '001', name: 'TOTAL TAXI PANAMA S.A.' },
  { id: '002', name: 'TOTAL TAXI 2' },
  { id: '003', name: 'TAXI EXPRESS S.A.' },
];

const MOCK_VEHICLES = [
  {
    numero_unidad: 'TT232',
    placa_vehiculo: 'EE9910',
    marca: 'TOYOTA',
    linea: 'COROLLA',
    modelo: '2022',
  },
  {
    numero_unidad: '0340',
    placa_vehiculo: 'EQ8196',
    marca: 'HYUNDAI',
    linea: 'ACCENT',
    modelo: '2021',
  },
  {
    numero_unidad: 'TT100',
    placa_vehiculo: 'AB1234',
    marca: 'KIA',
    linea: 'RIO',
    modelo: '2023',
  },
];

const MOCK_DRIVERS = [
  { nombre_conductor: 'HECTOR F. VANECAS G.', cedula: '8-123-456' },
  { nombre_conductor: 'JUAN PEREZ', cedula: '8-789-012' },
  { nombre_conductor: 'MARIA GONZALEZ', cedula: '8-345-678' },
];

@Component({
  selector: 'app-table-vehicle-repair',
  templateUrl: './table-vehicle-repair.component.html',
  styleUrls: ['./table-vehicle-repair.component.css'],
})
export class TableVehicleRepairComponent implements OnInit, AfterViewInit {
  displayedColumns: string[] = [
    'Fecha',
    'Unidad',
    'Placa',
    'Cupo',
    'Descripcion',
    'Propietario',
    'Usuario',
    'Estado',
    'Acciones',
  ];
  dataSource = new MatTableDataSource<VehicleRepairData>(MOCK_DATA);
  isLoadingData = false;
  maxDate = new Date();

  // Opciones para los autocompletes
  optionsOwners = MOCK_OWNERS;
  optionsVehicles = MOCK_VEHICLES;
  optionsDrivers = MOCK_DRIVERS;

  vehicleRepairForm: FormGroup;

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(private fb: FormBuilder) {
    this.vehicleRepairForm = this.fb.group({
      propietario: [''],
      vehiculo: [''],
      conductor: [''],
      fechaInicial: [''],
      fechaFinal: [''],
    });
  }

  ngOnInit(): void {
    // Simular carga de datos
    this.isLoadingData = true;
    setTimeout(() => {
      this.isLoadingData = false;
    }, 500);
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
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
}
