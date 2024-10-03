import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';

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

  data: any = null;
  cities: any = null;
  central: any = null;
  users: any = null;
  

  constructor(
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    this.fetchData();
    this.delay(500);
    this.getUsers();
    this.getCities();
    this.getCentral();
  }

  async delay(ms: number) {
    await new Promise(resolve => setTimeout(resolve, ms));
  }

  fetchData() {
    this.apiService.getData(`owner/26`).subscribe(
      (response) => {
        this.data = response;
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

  getCentral() {
    this.apiService.getData('central').subscribe(
      (response) => {
        this.central = response.filter((central: any) => central.codigo);
        this.checkCentral();
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

  selectButton(button: string) {
    this.selectedButton = button;
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

}
