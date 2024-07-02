import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { Router } from '@angular/router';
import { JwtService } from 'src/app/services/jwt.service';

@Component({
  selector: 'app-vehicles',
  templateUrl: './vehicles.component.html',
  styleUrls: ['./vehicles.component.css']
})
export class VehiclesComponent implements OnInit {
  data: any[] = [];
  user: any;
  filteredData: any[] = [];
  searchTerm: string = '';
  isLoading: boolean = true;

  constructor(
    private apiService: ApiService,
    private router: Router,
    private jwtService: JwtService
  ) {}

  ngOnInit(): void {
    this.fetchData();
    this.getUser();
  }

  fetchData() {
    this.apiService.getData('vehicles').subscribe(
      (response) => {
        this.data = response.filter((data: any) => data.unidad);
        this.data.sort((a, b) => a.unidad.localeCompare(b.unidad));
        this.filteredData = [...this.data];
        this.isLoading = false;
      },
      (error) => {
        console.log(error);
        this.isLoading = false;
      }
    );
  }

  filterData() {
    const term = this.searchTerm.toLowerCase();
    this.filteredData = this.data.filter(item => 
      item.unidad.toString().toLowerCase().includes(term) ||
      item.placa.toLowerCase().includes(term) ||
      item.nro_cupo.toLowerCase().includes(term) ||
      item.permiso.toLowerCase().includes(term) ||
      item.empresa.toLowerCase().includes(term) ||
      item.conductor.toLowerCase().includes(term) ||
      item.estado.toLowerCase().includes(term)
    );
  }

  formatDate(dateString: string): string {
    if (dateString == "0000-00-00 00:00:00") {
      return "-";
    }
    return dateString.split('T')[0];
  }

  getUser() {
    this.user = this.jwtService.decodeToken();
    this.user = this.user.user_data.nombre;
  }

  openExternalLink(): void {
    this.isLoading = true;
    const data = { user: this.user };
    this.apiService.getPdf("directorio-vehiculos").subscribe(
      response => {
        const blob = new Blob([response], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        const viewerUrl = this.router.serializeUrl(
          this.router.createUrlTree(['/pdf', { url }])
        );
        window.open(viewerUrl, '_blank'); // Abrir en una nueva pestaña
        this.router.navigate(['/home']);
      },
      error => {
        console.error('Error al generar el informe:', error);
      }
    );
  }
}
