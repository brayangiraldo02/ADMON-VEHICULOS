import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-owners-resume',
  templateUrl: './owners-resume.component.html',
  styleUrls: ['./owners-resume.component.css']
})
export class OwnersResumeComponent implements OnInit {
  selectedButton: string = "hoja";
  code: string | null = null;
  data: any = null;
  dataOriginal: any = null;
  cities: any = null;
  central: any = null;
  users: any = null;
  vehicles: any = null;
  isLoading = true;
  isEditable = false;
  cityFound = false;
  centralFound = false;
  usersFound = false;
  stateEdited = false;
  OwnersVehiclesView = false;
  OwnersContractView = false;

  constructor(
    private route: ActivatedRoute, 
    private apiService: ApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.code = params.get('code');
    });
    this.fetchData();
    this.delay(500);
    this.getUsers();
    this.getCities();
    this.getCentral();
    this.getVehicles();
  }

  async delay(ms: number) {
    await new Promise(resolve => setTimeout(resolve, ms));
  }

  fetchData() {
    this.apiService.getData(`owner/${this.code}`).subscribe(
      (response) => {
        this.data = response;
        this.dataOriginal = { ...this.data };
        this.stateEdited = false;
        this.checkDate();
        console.log('Fetch Data:', this.data);
        this.checkCity();
      },
      (error) => {
        console.log(error);
        
      }
    );
  }

  checkDate() {
    this.data.fec_nacimiento = this.validateDate(this.data.fec_nacimiento);
    this.data.fec_ingreso = this.validateDate(this.data.fec_ingreso);
  }

  validateDate(date: string): string {
    return date === "0000-00-00" ? "" : date;
  }

  getCities() {
    this.apiService.getData('cities').subscribe(
      (response) => {
        this.cities = response;
        this.checkCity();
      },
      (error) => {
        console.log(error);
      }
    );
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
        this.isLoading = false;
      },
      (error) => {
        console.log(error);
        this.isLoading = false;
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
      },
      (error) => {
        console.log(error);
      }
    );
  }

  checkUsers() {
    var varCodigo;
    var varNombre  = "Sin Auditor";
    if(this.data.auditor == null) {
      this.data.auditor = '';
      varCodigo = this.data.auditor;
    }
    else {
      varCodigo = '';
    }
    if (this.data && this.users) {
      this.usersFound = this.users.some((users: any) => users.codigo === this.data.auditor);
      if (!this.usersFound) {
        varCodigo = this.data.auditor;
        if(varCodigo !== '') {
          varNombre = "Auditor no encontrado";
        }
      }
      this.users.push({
        codigo: varCodigo,
        nombre: varNombre
      });
    }
  }

  getVehicles() {
    this.apiService.getData(`owner-vehicles/${this.code}`).subscribe(
      (response) => {
        this.vehicles = response;
        this.vehicles.sort((a: any, b: any) => {
          const aStartsWithSpecialChar = a.estado.startsWith('»');
          const bStartsWithSpecialChar = b.estado.startsWith('»');

          if (aStartsWithSpecialChar && !bStartsWithSpecialChar) {
            return 1;
          }
          if (!aStartsWithSpecialChar && bStartsWithSpecialChar) {
            return -1;
          }

          return a.estado.localeCompare(b.estado);
          }
        );
      },
      (error) => {
        console.log(error);
      }
    );
  }

  selectButton(button: string) {
    this.selectedButton = button;
  }

  enableInputs() {
    if (this.isEditable) {
      this.disableInputs();
      window.alert('No se ha modificado ningún dato.');
      location.reload();
    }

    this.isEditable = true;
  }

  disableInputs() {
    this.isEditable = false;
  }

  newData() {
    const fields = [
      'nombre', 'abreviado', 'cc', 'ruc', 'ciudad', 'direccion', 
      'telefono', 'celular', 'celular1', 'representante', 'contacto', 
      'correo', 'correo1', 'estado', 'auditor', 'central', 'grupo', 
      'impuesto', 'admon_parado', 'descuento', 'fec_nacimiento', 'fec_ingreso', 'razon_social', 'tipo_documento', 'numero_documento', 'sexo', 'estado_civil', 'nacionalidad', 'ficha', 'documento'
    ]
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

    return dataToSave;
  }

  // checkModifiedData(dataToSave:any) {
  //   const fields = [
  //     'nombre', 'abreviado', 'cc', 'ruc', 'ciudad', 'direccion', 
  //     'telefono', 'celular', 'celular1', 'representante', 'contacto', 
  //     'correo', 'correo1', 'estado', 'auditor', 'central', 'grupo', 
  //     'impuesto', 'admon_parado', 'descuento', 'fec_nacimiento', 'fec_ingreso', 'razon_social', 'tipo_documento', 'numero_documento', 'sexo', 'estado_civil', 'nacionalidad', 'ficha', 'documento'
  //   ];

  //   let modified = false;
  //   fields.forEach(field => {
  //     if (field == 'nombre') {
  //       if(this.data['nombre_propietario'] !== dataToSave[field]) {
  //         modified = true;
  //         console.log('Modified field:', field, dataToSave[field], this.data['nombre_propietario'])
  //       }
  //     }
  //     else if (field == 'abreviado') {
  //       if(this.data['nombre_abreviado'] !== dataToSave[field]) {
  //         modified = true;
  //         console.log('Modified field:', field, dataToSave[field], this.data['nombre_abreviado'])
  //       }
  //     }
  //     else if (field == 'cc') {
  //       if(this.data['nit'] != dataToSave[field]) {
  //         modified = true;
  //         console.log('Modified field:', field, dataToSave[field], this.data['nit'])
  //       }
  //     }
  //     else if (dataToSave[field] != this.data[field]) {
  //       console.log('Modified field:', field, dataToSave[field], this.data[field])
  //       modified = true;
  //     }
  //   });

  //   return modified;
  // }

  // checkModifiedCity() {
  //   const estadoElement = document.getElementById('estado') as HTMLSelectElement;
  //   if (estadoElement && estadoElement.value !== this.data.estado) {
  //     this.stateEdited = true;
  //   }
  // }

  checkModifiedData(): boolean {
    for (const key in this.data) {
      if(key == 'fec_nacimiento' || key == 'fec_ingreso') {
        if(this.data[key] == '') {
          this.data[key] = '0000-00-00';
        }
      }
      if (this.data[key] !== this.dataOriginal[key]) {
        if(key == 'estado'){
          this.stateEdited = true;
        }
        console.log(`Difference found at key: ${key}, data: ${this.data[key]}, dataOriginal: ${this.dataOriginal[key]}`);
        return true;
      }
    }
    return false;
  }

  saveData() {

    const modifiedData = this.checkModifiedData();

    console.log(modifiedData)

    if (!modifiedData) {
      window.alert('No se ha modificado ningún dato.');
      this.disableInputs();
      return;
    }

    this.data['stateEdited'] = this.stateEdited;

    console.log('Data to save:', this.data);
  
    this.apiService.updateData(`owner/${this.code}`, this.data).subscribe(
      (response) => {
        window.alert('Datos actualizados correctamente');
        this.disableInputs();
        location.reload();
      },
      (error) => {
        console.log(error);
      }
    );
  }

  goToOwnerResume() {
    this.selectButton('hoja')
    this.OwnersContractView = false;
    this.OwnersVehiclesView = false;
  }

  goToOwnerContract() {
    this.selectButton('contrato')
    this.OwnersVehiclesView = false
    this.OwnersContractView = true;
  }

  goToOwnerVehicles() {
    this.selectButton('vehiculos')
    this.OwnersContractView = false;
    this.OwnersVehiclesView = true;
  }
}
