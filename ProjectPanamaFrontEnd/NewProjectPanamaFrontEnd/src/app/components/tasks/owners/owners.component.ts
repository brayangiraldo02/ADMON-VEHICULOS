import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-owners',
  templateUrl: './owners.component.html',
  styleUrls: ['./owners.component.css']
})
export class OwnersComponent implements OnInit {
  data: any[] = [];
  filteredData: any[] = [];
  searchTerm: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData() {
    this.apiService.getData('owners/all').subscribe(
      (response) => {
        this.data = response.filter((data: any) => data.codigo);
        this.data.sort((a, b) => a.nombre_propietario.localeCompare(b.nombre_propietario));
        this.filteredData = [...this.data]; 
        console.log(response);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  filterData() {
    const term = this.searchTerm.toLowerCase();
    this.filteredData = this.data.filter(item => 
      item.codigo.toString().toLowerCase().includes(term) ||
      item.nombre_propietario.toLowerCase().includes(term)
      // item.ruc.toLowerCase().includes(term) ||
      // (item.telefono + ' ' + item.celular).toLowerCase().includes(term) ||
      // item.representante.toLowerCase().includes(term) ||
      // item.central.toLowerCase().includes(term) ||
      // item.auditor.toLowerCase().includes(term) ||
      // item.cnt.toString().toLowerCase().includes(term) ||
      // item.dcto.toString().toLowerCase().includes(term) ||
      // item.estado.toLowerCase().includes(term)
    );
  }
}