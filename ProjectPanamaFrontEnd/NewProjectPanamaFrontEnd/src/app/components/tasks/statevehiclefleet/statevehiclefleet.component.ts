import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-statevehiclefleet',
  templateUrl: './statevehiclefleet.component.html',
  styleUrls: ['./statevehiclefleet.component.css']
})
export class StatevehiclefleetComponent {
  selectedOption: string | null = null;
  titles: { [key: string]: string } = {
    'summary': 'Informe resumen de vehículos',
    'detail': 'Informe detalle de vehículos',
    'company-units': 'Informe unidades por empresa'
  };

  // URLs para las opciones generales y por empresa
  externalLinks: { [key: string]: { [key: string]: string } } = {
    'summary': {
      'general': 'http://localhost:8000/estado-vehiculos-resumen',
      'company': 'http://localhost:8000/estado-vehiculos-resumen-empresa'
    },
    'detail': {
      'general': 'http://example.com/detail-general',
      'company': 'http://example.com/detail-company'
    },
    'company-units': {
      'general': 'http://example.com/company-units-general',
      'company': 'http://example.com/company-units-company'
    }
  };

  constructor(private router: Router) { }

  selectOption(option: string): void {
    if (this.selectedOption === option || option === 'return') {
      this.selectedOption = null;
    } else {
      this.selectedOption = option;
    }
  }

  openExternalLink(option: string, type: string): void {
    const url = this.externalLinks[option][type];
    if (url) {
      window.open(url, '_blank');
    } else {
      console.error('URL no encontrada para la opción seleccionada.');
    }
  }
}