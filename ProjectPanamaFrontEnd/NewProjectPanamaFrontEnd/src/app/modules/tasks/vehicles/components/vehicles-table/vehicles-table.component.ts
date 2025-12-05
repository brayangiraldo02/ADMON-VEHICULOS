import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

export interface VehicleData {
  unidad: string;
  placa: string;
  modelo: string;
  nro_cupo: string;
  motor: string;
  chasis: string;
  matricula: string;
  central: string;
  empresa: string;
  conductor: string;
  nombre_estado: string;
  vlr_cta: string;
  nro_ctas: string;
  panapass: string;
  nro_llaves: string;
  consecutivo: string;
  // added fields based on usage in old component, though not all might be displayed
  estado?: string;
  saldo?: number;
  clave?: string;
  permiso?: string;
}

@Component({
  selector: 'app-vehicles-table',
  templateUrl: './vehicles-table.component.html',
  styleUrls: ['./vehicles-table.component.css'],
})
export class VehiclesTableComponent implements OnInit, AfterViewInit {
  displayedColumns: string[] = [
    'Unidad',
    'Placa',
    'Año',
    'Cupo',
    'Motor',
    'Chasis',
    'Matricula',
    'Central',
    'Empresa',
    'Conductor',
    'Estado',
    'Vlr.Cta',
    'N° Ctas',
    'Panapass',
    'Llavero',
  ];

  dataSource: MatTableDataSource<VehicleData>;
  isLoading: boolean = true;
  originalData: VehicleData[] = [];
  user: any;

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private apiService: ApiService,
    private router: Router,
    private jwtService: JwtService
  ) {
    this.dataSource = new MatTableDataSource<VehicleData>([]);
  }

  ngOnInit(): void {
    this.fetchData();
    this.getUser();
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  getUser() {
    this.user = this.jwtService.getUserData();
    // In old component it was re-assigning user to user.nombre, but keeping object is safer for now
    // logic: this.user = this.user.nombre;
  }

  getCompany() {
    const userData = this.jwtService.getUserData();
    return userData ? userData.empresa : '';
  }

  fetchData() {
    this.isLoading = true;
    const company = this.getCompany();
    this.apiService.getData('vehicles/all/' + company).subscribe(
      (response) => {
        // Old logic: this.data = response.filter((data: any) => data.unidad);
        // Old logic: this.data.sort((a, b) => a.unidad.localeCompare(b.unidad));

        const filteredResponse = response.filter((data: any) => data.unidad);
        this.originalData = filteredResponse;
        this.dataSource.data = filteredResponse;
        this.isLoading = false;
        console.log(this.dataSource.data);
      },
      (error) => {
        console.log(error);
        this.isLoading = false;
      }
    );
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  // Filter for 'Manera de Listar' (Todos/Activos/Retirados)
  listData(event: any) {
    const selectedValue = event.value; // MatSelect change event

    // Logic from old component:
    // item.estado.toString().toLowerCase().includes(selectedValue)

    // If selectedValue is empty, show all.
    if (!selectedValue) {
      this.dataSource.data = this.originalData;
    } else {
      this.dataSource.data = this.originalData.filter((item) =>
        item.estado
          ? item.estado.toString().toLowerCase().includes(selectedValue)
          : false
      );
    }

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  formatDate(dateString: string): string {
    if (!dateString || dateString == '0000-00-00 00:00:00') {
      return '-';
    }
    return dateString.split('T')[0];
  }

  goToVehicleResume(codigo: string) {
    this.router.navigate(['/vehicle', codigo]);
  }

  openExternalLink(): void {
    this.isLoading = true;

    const data = { user: this.user.nombre }; 

    localStorage.setItem(
      'pdfEndpoint',
      'directorio-vehiculos/' + this.getCompany()
    );
    localStorage.setItem('pdfData', '0');
    window.open(`/pdf`, '_blank');
    this.isLoading = false;
  }
}
