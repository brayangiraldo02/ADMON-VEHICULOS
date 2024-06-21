import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-vehicles',
  templateUrl: './vehicles.component.html',
  styleUrls: ['./vehicles.component.css']
})
export class VehiclesComponent implements OnInit {
  data: any[] = [];
  filteredData: any[] = [];
  searchTerm: string = '';
  isLoading: boolean = true;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchData();
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

}
