import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

@Component({
  selector: 'app-drivers',
  templateUrl: './drivers.component.html',
  styleUrls: ['./drivers.component.css']
})
export class DriversComponent implements OnInit {
  data: any[] = [];
  filteredData: any[] = [];
  searchTerm: string = '';
  user: any;
  isLoading: boolean = true;

  constructor(
    private apiService: ApiService, 
    private router: Router,
    private jwtService: JwtService) {}

  ngOnInit(): void {
    this.fetchData();
    this.getUser();
  }

  fetchData() {
    this.apiService.getData('drivers').subscribe(
      (response) => {
        this.data = response.filter((data: any) => data.codigo);
        this.data.sort((a, b) => a.nombre.localeCompare(b.nombre));
        this.filteredData = [...this.data];
        this.isLoading = false;
      },
      (error) => {
        console.log(error);
        this.isLoading = false;
      }
    );
  }

  getUser() {
    this.user = this.jwtService.decodeToken();
    this.user = this.user.user_data.nombre;
  }

  filterData() {
    const term = this.searchTerm.toLowerCase();
    this.filteredData = this.data.filter(item => 
      item.codigo.toString().toLowerCase().includes(term) ||
      item.unidad.toLowerCase().includes(term) ||
      item.nombre.toLowerCase().includes(term) ||
      item.cedula.toLowerCase().includes(term)
    );
  }

  openExternalLink(): void {
    this.isLoading = true;
    const data = { user: this.user };
    this.apiService.getPdf("directorio-conductores").subscribe(
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
