import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-drivers-resume',
  templateUrl: './drivers-resume.component.html',
  styleUrls: ['./drivers-resume.component.css']
})
export class DriversResumeComponent implements OnInit {
  selectedButton: string = "personal";
  imageDriver: string = "https://www.w3schools.com/howto/img_avatar.png";
  signatureDriver: string = "https://www.w3schools.com/howto/img_avatar.png";

  isEditable = false;
  centralFound = false;
  usersFound = false;
  cityFound = false;
  isModalVisible: boolean = false;
  stateEdited = false;
  isLoading = true;

  drivers: any = '';

  data: any = null;
  dataOriginal: any = null;
  cities: any = null;
  central: any = null;
  users: any = null;

  code: string | null = null;
  

  constructor(
    private route: ActivatedRoute,
    private router: Router, 
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.code = params.get('code');
    });
    this.fetchData();
    this.delay(500);
    this.getCities();
    this.getDrivers();
  }

  async delay(ms: number) {
    await new Promise(resolve => setTimeout(resolve, ms));
  }

  fetchData() {
    this.apiService.getData(`driver/${this.code}`).subscribe(
      (response) => {
        this.data = response;
        this.dataOriginal = { ...this.data };
        this.stateEdited = false;
        // console.log(this.data);
        this.isLoading = false;
        this.checkCity();
      },
      (error) => {
        console.log(error);
        
      }
    );
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
      'nombre', 'ciudad', 'telefono', 'celular', 'correo', 'sexo', 'direccion', 'representa', 'estado_civil', 'contacto', 'contacto1', 'contacto2', 'tel_contacto', 'tel_contacto1', 'tel_contacto2', 'par_contacto', 'par_contacto1', 'par_contacto2', 'estado', 'cruce_ahorros', 'licencia_numero', 'licencia_categoria', 'licencia_vencimiento', 'detalle', 'observaciones'
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

  checkModifiedData(): boolean {
    for (const key in this.data) {
      // if(key == 'fec_nacimiento' || key == 'fec_ingreso') {
      //   if(this.data[key] == '') {
      //     this.data[key] = '0000-00-00';
      //   }
      // }
      if (this.data[key] !== this.dataOriginal[key]) {
        if(key == 'estado'){
          this.stateEdited = true;
        }
        // console.log(`Difference found at key: ${key}, data: ${this.data[key]}, dataOriginal: ${this.dataOriginal[key]}`);
        return true;
      }
    }
    return false;
  }

  saveData() {

    const modifiedData = this.checkModifiedData();

    // console.log(modifiedData)

    if (!modifiedData) {
      window.alert('No se ha modificado ningún dato.');
      this.disableInputs();
      return;
    }

    this.data['stateEdited'] = this.stateEdited;

    // console.log('Data to save:', this.data);
  
    this.apiService.updateData(`driver/${this.code}`, this.data).subscribe(
      (response) => {
        window.alert('Datos actualizados correctamente');
        this.disableInputs();
        // console.log(response);
        location.reload();
      },
      (error) => {
        console.log(error);
      }
    );
  }

  getDrivers() {
    this.apiService.getData('drivers').subscribe(
      (response) => {
        this.drivers = response
          .filter((drivers: any) => drivers.codigo)  // Filtramos los drivers con código
          .sort((a: any, b: any) => a.codigo - b.codigo); // Ordenamos ascendente por código
        
        // console.log(this.drivers); 
      },
      (error) => {
        console.log(error);
      }
    );
  }
  

  nextDriver() {
    const currentIndex = this.drivers.findIndex((driver: any) => driver.codigo === this.code);
    if (currentIndex !== -1 && currentIndex < this.drivers.length - 1) {
      const nextDriverId = this.drivers[currentIndex + 1].codigo;
      this.router.navigate(['/driver/' + nextDriverId]).then(() => {
        window.location.reload();
      });
    }

    if(currentIndex === this.drivers.length - 1){
      this.firstDriver()
    }
  }
  
  backDriver() {
    const currentIndex = this.drivers.findIndex((driver: any) => driver.codigo === this.code);
    if (currentIndex !== -1 && currentIndex > 0) {
      const previousDriverId = this.drivers[currentIndex - 1].codigo;
      this.router.navigate(['/driver/' + previousDriverId]).then(() => {
        window.location.reload();
      });
    }

    if (currentIndex === 0) {
      this.lastDriver()
    }
  }
  

  firstDriver() {
    this.router.navigate(['/driver/' + this.drivers[0].codigo]).then(() => {
      window.location.reload();
    });
  }
  
  lastDriver() {
    this.router.navigate(['/driver/' + this.drivers[this.drivers.length - 1].codigo]).then(() => {
      window.location.reload();
    });
  }

  goToDriverInfo() {
    this.selectButton('personal')
  }

  goToDriverGeneral() {
    this.selectButton('general')
  }

  goToDriverVehicles() {
    this.selectButton('vehiculos')
  }

  goToDriverIncome() {
    this.selectButton('ingresos')
  }

  goToDriverDocuments() {
    this.selectButton('documentacion')
  }

  showModal() {
    this.isModalVisible = true;
    document.documentElement.style.overflow = 'hidden';
    document.body.style.overflow = 'hidden';
  }

  hideModal() {
    this.isModalVisible = false;
    document.documentElement.style.overflow = '';
    document.body.style.overflow = '';
  }

}
