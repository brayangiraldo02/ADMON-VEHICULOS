import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-vehicles-resume',
  templateUrl: './vehicles-resume.component.html',
  styleUrls: ['./vehicles-resume.component.css']
})
export class VehiclesResumeComponent {
  selectedButton: string = "propiedad";
  imageVehicle: string = "https://cdn5.dibujos.net/dibujos/pintados/202013/coche-urbano-vehiculos-coches-11735143.jpg";

  isEditable = false;
  centralFound = false;
  usersFound = false;
  cityFound = false;
  isModalVisible: boolean = false;
  stateEdited = false;
  isLoading = false;

  // drivers: any = '';

  data: any = null;
  dataOriginal: any = null;
  cities: any = null;
  central: any = null;
  users: any = null;
  vehicles: any = null;

  code: string | null = null;

  createDate: string = '';
  

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
    // this.delay(500);
    // this.getCities();
    this.getVehicles();
  }

  async delay(ms: number) {
    await new Promise(resolve => setTimeout(resolve, ms));
  }

  fetchData() {
    this.apiService.getData(`vehicle/`+this.code).subscribe(
      (response) => {
        this.data = response;
        this.dataOriginal = { ...this.data };
        this.stateEdited = false;
        this.formatDate(this.data.vehiculo_fec_creacion)
        console.log(this.data);
        this.isLoading = false;
        this.checkCity();
      },
      (error) => {
        console.log(error);
        
      }
    );
  }

  formatDate(fecha: string) {
    const date = new Date(fecha);
    const options: Intl.DateTimeFormatOptions = {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    };
    this.createDate = date.toLocaleString('es-ES', options).replace(',', '');
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

    console.log('Data to save:', this.data);
    this.disableInputs();
  
    // this.apiService.updateData(`driver/${this.code}`, this.data).subscribe(
    //   (response) => {
    //     window.alert('Datos actualizados correctamente');
    //     this.disableInputs();
    //     // console.log(response);
    //     location.reload();
    //   },
    //   (error) => {
    //     console.log(error);
    //   }
    // );
  }

  getVehicles() {
    this.apiService.getData('vehicle-codes').subscribe(
      (response) => {
        this.vehicles = response
          .filter((vehicles: any) => vehicles.vehiculo_numero)  // Filtramos los drivers con código
          .sort((a: any, b: any) => a.vehiculo_consecutivo - b.vehiculo_consecutivo);  // Ordenamos los drivers por código
        
        console.log(this.vehicles); 
      },
      (error) => {
        console.log(error);
      }
    );
  }
  

  nextVehicle() {
    // console.log(this.data.vehiculo_consecutivo)
    const currentIndex = this.vehicles.findIndex((vehicle: any) => vehicle.vehiculo_consecutivo === this.data.vehiculo_consecutivo);
    // console.log(currentIndex)
    if (currentIndex !== -1 && currentIndex < this.vehicles.length - 1) {
      const nextVehicleId = this.vehicles[currentIndex + 1].vehiculo_numero;
      // console.log(nextVehicleId)
      this.router.navigate(['/vehicle/' + nextVehicleId]).then(() => {
        window.location.reload();
      });
    }

    if(currentIndex === this.vehicles.length - 1){
      this.firstVehicle()
    }
  }
  
  backVehicle() {
    const currentIndex = this.vehicles.findIndex((vehicle: any) => vehicle.vehiculo_consecutivo === this.data.vehiculo_consecutivo);
    if (currentIndex !== -1 && currentIndex > 0) {
      const previousVehicleId = this.vehicles[currentIndex - 1].vehiculo_numero;
      this.router.navigate(['/vehicle/' + previousVehicleId]).then(() => {
        window.location.reload();
      });
    }

    if (currentIndex === 0) {
      this.lastVehicle()
    }
  }
  

  firstVehicle() {
    this.router.navigate(['/vehicle/' + this.vehicles[0].vehiculo_numero]).then(() => {
      window.location.reload();
    });
  }
  
  lastVehicle() {
    this.router.navigate(['/vehicle/' + this.vehicles[this.vehicles.length - 1].vehiculo_numero]).then(() => {
      window.location.reload();
    });
  }

  goToVehicleOwnership() {
    this.selectButton('propiedad')
  }

  goToVehicleDocuments() {
    this.selectButton('documentos')
  }

  goToVehicleDrivers() {
    this.selectButton('conductores')
  }

  goToVehicleIncome() {
    this.selectButton('ingresos')
  }

  goToVehicleOrders() {
    this.selectButton('ordenes')
  }

  goToVehicleTools() {
    this.selectButton('herramientas')
  }

  goToVehiclePhotos() {
    this.selectButton('fotos')
  }

  goToVehicleDocumentation() {
    this.selectButton('documentacion')
  }

  goToVehiclePyG() {
    this.selectButton('pyg')
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
