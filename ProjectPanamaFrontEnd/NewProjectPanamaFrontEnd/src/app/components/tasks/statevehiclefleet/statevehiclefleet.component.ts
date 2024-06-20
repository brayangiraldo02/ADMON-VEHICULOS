import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-statevehiclefleet',
  templateUrl: './statevehiclefleet.component.html',
  styleUrls: ['./statevehiclefleet.component.css']
})
export class StatevehiclefleetComponent implements OnInit {
  constructor(
    private router: Router, 
    private apiService: ApiService, 
    private jwtService: JwtService, 
    private snack:MatSnackBar) { }

  selectedOption: string | null = null;
  showCompanySelect: boolean = false;
  owners: any[] = [];
  states: any[] = [];
  empresasSeleccionadas: string[] = [];
  estadosSeleccionados: string[] = [];
  selectedCompany: string = '';
  user: any;
  mostrarOpcionesEmpresas: boolean = false;
  mostrarOpcionesEstados: boolean = false;
  selectedEmpresasOptions: { [key: string]: boolean } = {};
  selectedEstadosOptions: { [key: string]: boolean } = {};

  titles: { [key: string]: string } = {
    'summary': 'Informe Resumen de Vehículos',
    'detail': 'Informe Detalle de Vehículos',
    'company-units': 'Relación Unidad/Estado Empresa'
  };

  externalLinks: { [key: string]: { [key: string]: string } } = {
    'summary': {
      'general': `estado-vehiculos-resumen`,
      'company': `estado-vehiculos-resumen-empresa/`
    },
    'detail': {
      'general': `informe-estados-detallado`,
      'company': `informe-estados-detallado-empresa/`
    },
    'company-units': {
      'general': 'http://example.com/company-units-general',
      'company': 'http://example.com/company-units-company/'
    }
  };

  ngOnInit(): void {
    this.listOwners();
    this.listStates();
    this.obtenerUsuario();
  }

  backOptions() {
    if (this.mostrarOpcionesEmpresas) {
      this.mostrarOpcionesEmpresas = !this.mostrarOpcionesEmpresas;
      // this.toggleEmpresaSelect('empresas');
      this.empresasSeleccionadas = [];
      this.clearEmpresasSelections();
    }
    if (this.mostrarOpcionesEstados) {
      this.mostrarOpcionesEstados = !this.mostrarOpcionesEstados;
      // this.toggleEstadoSelect('estados');
      this.estadosSeleccionados = [];
      this.clearEstadosSelections();
    }
  }

  openSnack() {
    this.snack.open("Un momento...", "Aceptar"),{
      duration:3000
    }
  }

  obtenerUsuario() {
    this.user = this.jwtService.decodeToken();
    this.user = this.user.user_data.nombre;
    console.log(this.user);
  }

  listOwners(): void {
    this.apiService.getData("owners").subscribe(
      (response) => {
        this.owners = response.filter((owner: any) => owner.id);
        this.owners.sort((a, b) => a.name.localeCompare(b.name));
      },
      (error) => {
        console.log(error);
      }
    );
  }

  listStates(): void {
    this.apiService.getData("states").subscribe(
      (response) => {
        this.states = response.filter((state: any) => state.id);
        this.states.sort((a, b) => {
          const aStartsWithSpecialChar = a.name.startsWith('»');
          const bStartsWithSpecialChar = b.name.startsWith('»');
        
          if (aStartsWithSpecialChar && !bStartsWithSpecialChar) {
            return 1;
          }
          if (!aStartsWithSpecialChar && bStartsWithSpecialChar) {
            return -1;
          }
        
          return a.name.localeCompare(b.name);
        });
        console.log(response);
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

  isEmpresaSeleccionada(opcionId: string): boolean {
    return this.empresasSeleccionadas.includes(opcionId);
  }

  onCheckboxEmpresaChange(opcionId: string, event: any) {
    if (event.target.checked) {
      if (!this.empresasSeleccionadas.includes(opcionId)) {
        this.empresasSeleccionadas.push(opcionId);
      }
    } else {
      this.empresasSeleccionadas = this.empresasSeleccionadas.filter(id => id !== opcionId);
    }
  }

  onCheckboxEmpresaContainerClick(opcionId: string, event: any) {
    const checkbox = event.currentTarget.querySelector('input[type="checkbox"]');
    checkbox.checked = !checkbox.checked;
    this.onCheckboxEmpresaChange(opcionId, { target: checkbox });
    event.stopPropagation(); // Evita que el evento de clic se propague
  }

  onEmpresaSeleccionar() {
    this.empresasSeleccionadas.sort((a, b) => parseInt(a) - parseInt(b));
    console.log('Empresas seleccionadas:', this.empresasSeleccionadas);
    this.mostrarOpcionesEmpresas = false; // Cierra el cuadro después de la selección
    this.clearEmpresasSelections();
  }

  toggleEmpresaSelect(option: string) {
    this.selectedEmpresasOptions[option] = !this.selectedEmpresasOptions[option];
  }

  clearEmpresasSelections() {
    this.selectedEmpresasOptions = {};
  }

  onEstadoSeleccionar() {
    this.estadosSeleccionados.sort((a, b) => parseInt(a) - parseInt(b));
    console.log('Estados seleccionadas:', this.estadosSeleccionados);
    this.mostrarOpcionesEstados = false; 
    this.clearEstadosSelections();
  }

  clearEstadosSelections() {
    this.selectedEstadosOptions = {};
  }

  toggleOpcionesEmpresas() {
    this.mostrarOpcionesEmpresas = !this.mostrarOpcionesEmpresas;
    if (!this.mostrarOpcionesEmpresas) {
      this.clearEmpresasSelections();
      this.onEmpresaSeleccionar();
    }
  }
  
  toggleOpcionesEstados() {
    this.mostrarOpcionesEstados = !this.mostrarOpcionesEstados;
    if (!this.mostrarOpcionesEstados) {
      this.clearEstadosSelections();
      this.onEstadoSeleccionar();
    }
  }

  isEstadoSeleccionado(opcionId: string): boolean {
    return this.estadosSeleccionados.includes(opcionId);
  }

  onCheckboxEstadoChange(opcionId: string, event: any) {
    if (event.target.checked) {
      if (!this.estadosSeleccionados.includes(opcionId)) {
        this.estadosSeleccionados.push(opcionId);
      }
    } else {
      this.estadosSeleccionados = this.estadosSeleccionados.filter(id => id !== opcionId);
    }
  }

  onCheckboxEstadoContainerClick(opcionId: string, event: any) {
    const checkbox = event.currentTarget.querySelector('input[type="checkbox"]');
    checkbox.checked = !checkbox.checked;
    this.onCheckboxEstadoChange(opcionId, { target: checkbox });
    event.stopPropagation(); // Evita que el evento de clic se propague
  }

  openExternalLink(option: string, type: string): void {
    // this.openSnack();
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

  obtenerIdsEmpresas(): string[] {
    return this.owners.map(owner => owner.id).filter(id => id);
  }

  obtenerIdsEstados(): string[] {
    return this.states.map(state => state.id).filter(id => id);
  }

  generarInforme() {
    if(this.empresasSeleccionadas.length == 0) {
      this.empresasSeleccionadas = this.obtenerIdsEmpresas();
    }
    if(this.estadosSeleccionados.length == 0) {
      this.estadosSeleccionados = this.obtenerIdsEstados();
    }
    let info = {
      usuario: this.user,
      empresas: this.empresasSeleccionadas,
      estados: this.estadosSeleccionados
    }
    
    this.apiService.postPdf("relacion-vehiculos-propietario", info).subscribe(
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
  }
}
