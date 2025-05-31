import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { ApiService } from 'src/app/services/api.service';

export interface VehicleInfoData {
  Unidad: string;
  Condu: string;
  Nombre: string;
  'Vlr.Cta': string; 
  Celular: string;
  Ingreso: string;
  'Sin Pagar': string;
  'Sdo.Renta': string;
  Deposito: string;
  PanaPass: string;
  Siniestro: string;
  Mantenimien: string; 
  'Otra Deu': string;
  Empresa: string;
  Central: string;
  Estado: string;
}

interface apiResponse {
  vehiculo_numero?: string;
  conductor?: string;
  conductores_nombre?: string;
  conductores_cuodiaria?: number;
  conductores_celular?: string;
  conductores_fecingres?: string;
  diferencia?: number; 
  deu_renta?: number; 
  fon_inscri?: number; 
  deu_sinies?: number; 
  deu_otras?: number; 
  nombre?: string; 
  centrales_nombre?: string;
  estado?: string;
}

interface DebtOption {
  text: string;
  color: string;
}

@Component({
  selector: 'app-info-table',
  templateUrl: './info-table.component.html',
  styleUrls: ['./info-table.component.css']
})
export class InfoTableComponent implements AfterViewInit {
  debts = new FormControl<string[]>([]);

  debtList: DebtOption[] = [
    { text: 'Más de 3 Días', color: '#FFCDD2' }, // Light Red
    { text: 'Menor o Igual a 2 Días', color: '#FFE0B2' }, // Light Orange
    { text: 'Menor o Igual a 1 Día', color: '#FFF9C4' }, // Light Yellow
    { text: 'Sin Deuda', color: '#C8E6C9' }, // Light Green
    { text: 'Todos', color: '#ADD8E6' } // Light Grey
  ];

  displayedColumns: string[] = ['Unidad', 'Condu', 'Nombre', 'Vlr.Cta', 'Celular', 'Ingreso', 'Sin Pagar', 'Sdo.Renta', 'Deposito', 'PanaPass', 'Siniestro', 'Mantenimien', 'Otra Deu', 'Empresa', 'Central', 'Estado'];
  dataSource: MatTableDataSource<VehicleInfoData>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(private apiService: ApiService) {
    this.dataSource = new MatTableDataSource<VehicleInfoData>([]);
  }

  ngAfterViewInit() {
    this.getTableData();
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  getTableData(){

    const data = {
      'owners': [
        '26', '27'
      ]
    }

    this.apiService.postData('collection-accounts', data).subscribe({
      next: (response) => {
        console.log('Data fetched successfully:', response);
        const mappedData: VehicleInfoData[] = response.map((item: apiResponse) => {
          return {
            Unidad: item.vehiculo_numero || '',
            Condu: item.conductor || '', 
            Nombre: item.conductores_nombre || '',
            'Vlr.Cta': item.conductores_cuodiaria !== undefined ? item.conductores_cuodiaria.toString() : '0',
            Celular: item.conductores_celular || '',
            Ingreso: item.conductores_fecingres || 'N/A',
            'Sin Pagar': '', 
            'Sdo.Renta': item.deu_renta !== undefined ? item.deu_renta.toString() : '0',
            Deposito: item.fon_inscri !== undefined ? item.fon_inscri.toString() : '0',
            PanaPass: '', 
            Siniestro: item.deu_sinies !== undefined ? item.deu_sinies.toString() : '0',
            Mantenimien: '', 
            'Otra Deu': item.deu_otras !== undefined ? item.deu_otras.toString() : '0',
            Empresa: item.nombre || '', 
            Central: item.centrales_nombre || '',
            Estado: item.estado || '',
          };
        });

        this.dataSource.data = mappedData;
        if (this.paginator) {
          this.dataSource.paginator = this.paginator;
        }
        if (this.sort) {
          this.dataSource.sort = this.sort;
        }
      },
      error: (error) => {
        console.error('Error fetching data:', error);
      }
    });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }
}