import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { ActivatedRoute, Router } from '@angular/router';

interface Driver {
  auditor: string;
  cedula: string;
  celular: string;
  ciudad: string;
  codigo: string;
  contacto: string;
  contacto1: string;
  contacto2: string;
  correo: string;
  cruce_ahorros: string;
  direccion: string;
  estado: string;
  estado_civil: string;
  fecha_estado: string;
  fecha_nacimiento: string;
  fecha_retiro: string;
  licencia_categoria: string;
  licencia_numero: string;
  licencia_vencimiento: string;
  nombre: string;
  observaciones: string;
  par_contacto: string;
  par_contacto1: string;
  par_contacto2: string;
  representa: string;
  tel_contacto: string;
  tel_contacto1: string;
  tel_contacto2: string;
  telefono: string;
}

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
        this.stateEdited = false;
        console.log(this.data);
        this.isLoading = false;
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
