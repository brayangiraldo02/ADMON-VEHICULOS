import { Component, Input, Output, EventEmitter } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';
import { Router } from '@angular/router';

interface State {
  id: string;
  name: string;
}

interface Owner {
  id: string;
  name: string;
}

@Component({
  selector: 'app-owners-feespaid',
  templateUrl: './owners-feespaid.component.html',
  styleUrls: ['./owners-feespaid.component.css']
})
export class OwnersFeespaidComponent {
  @Output() close = new EventEmitter<void>();

  isLoading: boolean = true;

  mostrarOpcionesEmpresas: boolean = true;
  mostrarOpcionesEstados: boolean = false;

  states: State[] = [];
  owners: Owner[] = [];

  estadosSeleccionados: string[] = [];
  empresasSeleccionadas: string[] = [];

  constructor(
    private apiService: ApiService,
    private jwtService: JwtService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.listStates();
    this.listOwners();
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
        console.log(this.states);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  listOwners(): void {
    console.log(this.jwtService.obtainId());
    const owner = {
      propietario: this.jwtService.obtainId()
    }

    console.log(owner);

    this.apiService.postData("companies_owners", owner).subscribe(
      (response) => {
        this.owners = response.filter((owner: any) => owner.id);
        this.owners.sort((a, b) => a.name.localeCompare(b.name));
        console.log(this.owners);
        this.isLoading = false;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  toggleOpcionesEstados(): void {
    this.mostrarOpcionesEstados = !this.mostrarOpcionesEstados;
  }

  toggleOpcionesEmpresas(): void {
    this.mostrarOpcionesEmpresas = !this.mostrarOpcionesEmpresas;
  }

  backOptions(): void {
    if (this.mostrarOpcionesEmpresas) {
      this.mostrarOpcionesEmpresas = !this.mostrarOpcionesEmpresas;
      this.empresasSeleccionadas = [];
    }
    if (this.mostrarOpcionesEstados) {
      this.mostrarOpcionesEstados = !this.mostrarOpcionesEstados;
      this.mostrarOpcionesEmpresas = true;
      this.estadosSeleccionados = [];
    }
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
    this.mostrarOpcionesEmpresas = false; // Cierra el cuadro después de la selección
    this.mostrarOpcionesEstados = true; // Abre el cuadro de selección de estados
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

  onEstadoSeleccionar() {
    this.estadosSeleccionados.sort((a, b) => parseInt(a) - parseInt(b));
    this.mostrarOpcionesEstados = false; 
  }

  obtenerUsuario() {
    let user = this.jwtService.decodeToken();
    return user.user_data.nombre;
  }

  obtenerIdsEmpresas(): string[] {
    return this.owners.map(owner => owner.id).filter(id => id);
  }

  obtenerIdsEstados(): string[] {
    return this.states.map(state => state.id).filter(id => id);
  }

  generarInforme() {
    this.isLoading = true;
    let user = this.obtenerUsuario();
    if (this.empresasSeleccionadas.length === 0) {
      this.empresasSeleccionadas = this.obtenerIdsEmpresas();
    }
    if (this.estadosSeleccionados.length === 0) {
      this.estadosSeleccionados = this.obtenerIdsEstados();
    }
    let info = {
      usuario: user,
      empresas: this.empresasSeleccionadas,
      estados: this.estadosSeleccionados
    };

    console.log(this.estadosSeleccionados);

    // Guardar endpoint y data en LocalStorage
    localStorage.setItem('pdfEndpoint', 'informe-cuotas-pagas');
    localStorage.setItem('pdfData', JSON.stringify(info));

    // Navegar al componente PdfViewerComponent
    window.open(`/pdf`, '_blank')
    this.closeModal();
  }

  closeModal() {
    this.close.emit();
  }
}
