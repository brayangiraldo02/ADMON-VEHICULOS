import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

@Component({
  selector: 'app-statevehiclefleet',
  templateUrl: './statevehiclefleet.component.html',
  styleUrls: ['./statevehiclefleet.component.css']
})
export class StatevehiclefleetComponent implements OnInit {
  constructor(private router: Router, private apiService: ApiService, private jwtService: JwtService) { }

  selectedOption: string | null = null;
  showCompanySelect: boolean = false;
  owners: any[] = [];
  selectedCompany: string = '';
  user: any;

  titles: { [key: string]: string } = {
    'summary': 'Informe resumen de vehículos',
    'detail': 'Informe detalle de vehículos',
    'company-units': 'Informe unidades por empresa'
  };

  externalLinks: { [key: string]: { [key: string]: string } } = {
    'summary': {
      'general': `estado-vehiculos-resumen`,
      'company': `estado-vehiculos-resumen-empresa/`
    },
    'detail': {
      'general': `conteo-vehiculos-estados-numeros`,
      'company': `conteo-propietarios-vehiculos-estados-numeros/`
    },
    'company-units': {
      'general': 'http://example.com/company-units-general',
      'company': 'http://example.com/company-units-company/'
    }
  };

  ngOnInit(): void {
    this.listOwners();
    this.obtenerUsuario();
  }

  obtenerUsuario() {
    this.user = this.jwtService.decodeToken();
    this.user = this.user.user_data.nombre;
    console.log(this.user);
  }

  listOwners(): void {
    this.apiService.getData("owners").subscribe(
      (response) => {
        this.owners = response;
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
    let endpoint = this.externalLinks[option][type];
    if (type === 'company' && this.selectedCompany) {
      endpoint += this.selectedCompany;
    }
    if (option === 'company-units') {
      window.alert("Informe no disponible.");
    } else {
      if (endpoint) {
        const data = { user: this.user };
        this.apiService.postPdf(endpoint, data).subscribe(
          response => {
            const blob = new Blob([response], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            const viewerUrl = this.router.serializeUrl(
              this.router.createUrlTree(['/pdf', { url }])
            );
            window.open(viewerUrl, '_blank'); // Abrir en una nueva pestaña
          },
          error => {
            console.error('Error al generar el informe:', error);
          }
        );
      } else {
        console.error('URL no encontrada para la opción seleccionada.');
      }
    }
  }
}
