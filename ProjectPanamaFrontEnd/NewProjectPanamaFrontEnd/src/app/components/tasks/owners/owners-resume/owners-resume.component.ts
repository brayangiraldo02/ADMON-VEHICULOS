import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-owners-resume',
  templateUrl: './owners-resume.component.html',
  styleUrls: ['./owners-resume.component.css']
})
export class OwnersResumeComponent implements OnInit {
  code: string | null = null;
  data: any = null;
  cities: any = null;
  central: any = null;
  users: any = null;
  isLoading = true;
  isEditable = false;
  cityFound = false;
  centralFound = false;
  usersFound = false;
  stateEdited = false;

  constructor(private route: ActivatedRoute, private apiService: ApiService) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.code = params.get('code');
    });
    this.getUsers();
    this.getCities();
    this.getCentral();
    this.fetchData();
  }

  fetchData() {
    this.apiService.getData(`owner/${this.code}`).subscribe(
      (response) => {
        this.data = response;
        console.log(this.data);
        this.isLoading = false;
        this.checkCity();
      },
      (error) => {
        console.log(error);
        this.isLoading = false;
      }
    );
  }

  getCities() {
    this.apiService.getData('cities').subscribe(
      (response) => {
        this.cities = response.map((city: any) => ({
          ...city,
          codigo: this.removeLeadingZero(city.codigo)
        }));
        this.checkCity();
        console.log(this.cities);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  removeLeadingZero(code: string): string {
    return code.replace(/^0+/, '');
  }

  checkCity() {
    if (this.data && this.cities) {
      this.cityFound = this.cities.some((city: any) => city.codigo === this.data.ciudad);
      if (!this.cityFound) {
        this.cities.push({
          codigo: this.data.ciudad,
          nombre: "Ciudad no encontrada"
        });
      }
    }
  }

  getCentral() {
    this.apiService.getData('central').subscribe(
      (response) => {
        this.central = response.filter((central: any) => central.codigo);
        this.checkCentral();
        console.log(this.central);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  checkCentral() {
    if (this.data && this.central) {
      this.centralFound = this.central.some((central: any) => central.codigo === this.data.central);
      if (!this.centralFound) {
        this.central.push({
          codigo: this.data.central,
          nombre: "Central no encontrada"
        });
      }
    }
  }

  getUsers() {
    this.apiService.getData('users').subscribe(
      (response) => {
        this.users = response.filter((users: any) => users.codigo);
        this.checkUsers();
        console.log(this.users);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  checkUsers() {
    if (this.data && this.users) {
      this.usersFound = this.users.some((users: any) => users.codigo === this.data.auditor);
      if (!this.usersFound) {
        this.users.push({
          codigo: this.data.auditor,
          nombre: "Auditor no encontrado"
        });
      }
    }
  }

  enableInputs() {
    if (this.isEditable) {
      this.disableInputs();
      return;
    }

    this.isEditable = true;
    const fields = [
      'nombre', 'abreviado', 'cc', 'nit', 'ruc', 'ciudad', 'direccion', 
      'telefono', 'celular', 'celular1', 'representante', 'contacto', 
      'correo', 'correo1'
    ];
    fields.forEach(field => {
      const element = document.getElementById(field) as HTMLInputElement;
      if (element) {
        element.disabled = false;
      }
    });
  }

  disableInputs() {
    this.isEditable = false;
    const fields = [
      'nombre', 'abreviado', 'cc', 'nit', 'ruc', 'ciudad', 'direccion', 
      'telefono', 'celular', 'celular1', 'representante', 'contacto', 
      'correo', 'correo1'
    ];
    fields.forEach(field => {
      const element = document.getElementById(field) as HTMLInputElement;
      if (element) {
        element.disabled = true;
      }
    });
  }

  saveData() {
    const fields = [
      'nombre', 'abreviado', 'cc', 'nit', 'ruc', 'ciudad', 'direccion', 
      'telefono', 'celular', 'celular1', 'representante', 'contacto', 
      'correo', 'correo1', 'estado', 'auditora', 'central'
    ];
    
    const dataToSave: any = {};
    fields.forEach(field => {
      const element = document.getElementById(field) as HTMLInputElement;
      if (element) {
        dataToSave[field] = element.value;
      }
    });
    
    // Add the 'codigo' field which should be read-only
    const codigoElement = document.getElementById('codigo') as HTMLInputElement;
    if (codigoElement) {
      dataToSave['codigo'] = codigoElement.value;
    }

     // Check if the city field was edited
    const estadoElement = document.getElementById('estado') as HTMLSelectElement;
    if (estadoElement && estadoElement.value !== this.data.estado) {
      this.stateEdited = true;
    }

    dataToSave['stateEdited'] = this.stateEdited;

    this.disableInputs();
    console.log('Data to save:', dataToSave);
    // Here you can send the dataToSave object to your API or handle it as needed
  }
}
