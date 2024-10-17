import { Component } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-drivers-addnew',
  templateUrl: './drivers-addnew.component.html',
  styleUrls: ['./drivers-addnew.component.css']
})
export class DriversAddnewComponent {
  selectedButton: string = "personal";
  imageDriver: string = "https://www.w3schools.com/howto/img_avatar.png";
  signatureDriver: string = "https://www.w3schools.com/howto/img_avatar.png";

  isEditable = true;
  centralFound = false;
  usersFound = false;
  cityFound = false;
  isModalVisible: boolean = false;

  drivers: any = '';

  data: any = null;
  cities: any = null;
  central: any = null;
  users: any = null;

  code: string | null = null;

  driverForm: FormGroup;
  
  isLoading = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router, 
    private apiService: ApiService,
    private fb: FormBuilder
  ) {
    this.driverForm = this.fb.group({
      codigo: ['', [Validators.required, Validators.pattern(/^\d{1,12}$/)]], 
      nombre: ['', [Validators.required, Validators.maxLength(50)]],
      cedula: ['', [Validators.required, Validators.pattern(/^\d{1,12}$/)]],
      ciudad: [''],
      telefono: ['', Validators.pattern(/^\d{1,30}$/)],
      celular: ['', Validators.pattern(/^\d{1,30}$/)],
      correo: ['', Validators.maxLength(40)],
      sexo: [''],
      fecha_ingreso: [''],
      direccion: ['', Validators.maxLength(120)],
      fecha_nacimiento: [''],
      representa: ['', Validators.maxLength(30)],
      estado_civil: [''],
      fecha_retiro: [''],
      contacto: ['', Validators.maxLength(40)],
      contacto1: ['', Validators.maxLength(20)],
      contacto2: ['', Validators.maxLength(20)],
      tel_contacto: ['', Validators.pattern(/^\d{1,40}$/)],
      tel_contacto1: ['', Validators.pattern(/^\d{1,40}$/)],
      tel_contacto2: ['', Validators.pattern(/^\d{1,40}$/)],
      par_contacto: ['', Validators.maxLength(20)],
      par_contacto1: ['', Validators.maxLength(20)],
      par_contacto2: ['', Validators.maxLength(20)],
      estado: [''],
      contrato_auto: [''],
      cruce_ahorros: [''],
      licencia_numero: ['', Validators.maxLength(12)],
      licencia_categoria: ['', Validators.maxLength(2)],
      licencia_vencimiento: [''],
      detalle: ['', Validators.maxLength(50)],
      observaciones: ['', Validators.maxLength(50)],
    });
  }

  ngOnInit(): void {
    this.fetchData();
    this.delay(500);
    this.getCities();
    this.getDrivers();
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

  getDrivers() {
    this.apiService.getData('driver-codes').subscribe(
      (response) => {
        this.drivers = response.filter((drivers: any) => drivers);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  checkCode(): boolean {
    const code = this.driverForm.get('codigo')?.value;
    this.code = code;
    if (code !== null && code !== undefined && code !== '') {
      const owner = this.drivers.find((owner: any) => owner === code.toString());
      if (owner) {
        window.alert('El código ya existe.');
        this.driverForm.get('codigo')?.setValue('');
        return false;
      }
      return true;
    }
    return false;
  }

  onSubmit() {
    if (this.driverForm.valid) {
      if (this.checkCode()){
        this.isLoading = false;
        const formData = this.driverForm.value;
        console.log(formData);
        this.apiService.postData('drivers', formData).subscribe(
          (response) => {
            window.alert('Propietario creado exitosamente.');
            this.driverForm.reset();
            this.router.navigate(['/driver/'+this.code]);
          },
          (error) => {
            console.log(error);
          }
        );
      }
    }
    else {
      window.alert('Por favor, llene los campos correctamente.');
    }
  }

}
