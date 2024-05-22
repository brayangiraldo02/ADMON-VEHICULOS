import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-statevehiclefleet',
  templateUrl: './statevehiclefleet.component.html',
  styleUrls: ['./statevehiclefleet.component.css']
})
export class StatevehiclefleetComponent implements OnInit {
  constructor(private router: Router, private apiService: ApiService) { }

  selectedOption: string | null = null;
  showCompanySelect: boolean = false;
  owners: any[] = [];
  selectedCompany: string = '';

  titles: { [key: string]: string } = {
    'summary': 'Informe resumen de vehículos',
    'detail': 'Informe detalle de vehículos',
    'company-units': 'Informe unidades por empresa'
  };

  externalLinks: { [key: string]: { [key: string]: string } } = {
    'summary': {
      'general': `${environment.url}/estado-vehiculos-resumen`,
      'company': `${environment.url}/estado-vehiculos-resumen-empresa/`
    },
    'detail': {
      'general': 'http://example.com/detail-general',
      'company': 'http://example.com/detail-company/'
    },
    'company-units': {
      'general': 'http://example.com/company-units-general',
      'company': 'http://example.com/company-units-company/'
    }
  };

  ngOnInit(): void {
    this.listOwners();
  }

  listOwners(): void {
    this.apiService.getData("owners").subscribe(
      (response) => {
        this.owners = response;
        console.log(this.owners);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  selectOption(option: string): void {
    this.showCompanySelect = false;
    if (this.selectedOption === option || option === 'return') {
      this.selectedOption = null;
    } else {
      this.selectedOption = option;
    }
  }

  selectCompanyOption(): void {
    this.showCompanySelect = true;
  }

  onCompanyChange(event: Event): void {
    const selectElement = event.target as HTMLSelectElement;
    this.selectedCompany = selectElement.value;
    this.openExternalLink(this.selectedOption!, 'company');
  }

  openExternalLink(option: string, type: string): void {
    let url = this.externalLinks[option][type];
    if (type === 'company' && this.selectedCompany) {
      url += this.selectedCompany;
    }
    if (url) {
      window.open(url, '_blank');
    } else {
      console.error('URL no encontrada para la opción seleccionada.');
    }
  }
}
