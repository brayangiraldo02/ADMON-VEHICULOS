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
  isLoading = true;

  // drivers: any = '';

  data: any = null;
  dataOriginal: any = null;
  central: any = null;
  brands: any = null;
  owners: any = null;
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
    this.delay(500);
    this.getVehicles();
    this.getBrands();
    this.getOwners();
    this.getCentral();
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
        this.checkBrand();
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

  getBrands() {
    this.apiService.getData('brands').subscribe(
      (response) => {
        this.brands = response;
        this.checkBrand();
      },
      (error) => {
        console.log(error);
      }
    );
  }

  checkBrand() {
    if (this.data && this.brands) {
      const brandFound = this.brands.some((brand: any) => brand.codigo === this.data.vehiculo_marca);
      if (!brandFound) {
        this.brands.push({
          codigo: this.data.vehiculo_marca,
          nombre: "Marca no encontrada"
        });
      }
    }
  }

  getOwners() {
    this.apiService.getData('owners').subscribe(
      (response) => {
        this.owners = response;
        this.checkOwner();
      },
      (error) => {
        console.log(error);
      }
    );
  }

  checkOwner() {
    if (this.data && this.owners) {
      const ownerFound = this.owners.some((owner: any) => owner.id === this.data.vehiculo_propietario);
      if (!ownerFound) {
        this.owners.push({
          id: this.data.vehiculo_propietario,
          name: "Propietario no encontrado"
        });
      }
    }
  }

  getCentral() {
    this.apiService.getData('central').subscribe(
      (response) => {
        this.central = response;
        this.checkCentral();
      },
      (error) => {
        console.log(error);
      }
    );
  }

  checkCentral() {
    if (this.data && this.central) {
      const centralFound = this.central.some((central: any) => central.codigo === this.data.vehiculo_central);
      if (!centralFound) {
        this.central.push({
          codigo: this.data.vehiculo_propietario,
          nombre: "Propietario no encontrado"
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
