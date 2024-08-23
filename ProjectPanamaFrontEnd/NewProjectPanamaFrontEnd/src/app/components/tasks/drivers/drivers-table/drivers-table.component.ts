import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

@Component({
  selector: 'app-drivers-table',
  templateUrl: './drivers-table.component.html',
  styleUrls: ['./drivers-table.component.css']
})
export class DriversTableComponent implements OnInit{
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
        console.log(this.data)
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
    localStorage.setItem('pdfEndpoint', 'directorio-conductores');
    localStorage.setItem('pdfData', '0');
    window.open(`/pdf`, '_blank')
    this.router.navigate(['/home']);
  }
}
