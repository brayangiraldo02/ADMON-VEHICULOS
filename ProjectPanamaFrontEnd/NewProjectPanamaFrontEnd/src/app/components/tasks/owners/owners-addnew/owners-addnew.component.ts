import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-owners-addnew',
  templateUrl: './owners-addnew.component.html',
  styleUrls: ['./owners-addnew.component.css']
})
export class OwnersAddnewComponent implements OnInit {
  selectedButton: string = "hoja";
  OwnersContractView = false;
  ownerForm: FormGroup;
  cities: any = null;
  users: any = null;
  central: any = null;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) {
    this.ownerForm = this.fb.group({
      codigo: ['', Validators.required],
      nombre_propietario: ['', Validators.required],
      nombre_abreviado: [''],
      nit: [''],
      ruc: [''],
      ciudad: [''],
      direccion: [''],
      telefono: [''],
      celular: [''],
      celular1: [''],
      representante: [''],
      contacto: [''],
      correo: [''],
      correo1: [''],
      estado: [''],
      auditor: [''],
      central: [''],
      grupo: [''],
      impuesto: [''],
      admon_parado: [''],
      descuento: [''],
      fec_nacimiento: [''],
      fec_ingreso: [''],
      razon_social: [''],
      tipo_documento: [''],
      numero_documento: [''],
      sexo: [''],
      estado_civil: [''],
      nacionalidad: [''],
      ficha: [''],
      documento: ['']
    });
  }

  ngOnInit(): void {
    this.getCities();
    this.getUsers();
    this.getCentral();
  }

  getCities() {
    this.apiService.getData('cities').subscribe(
      (response) => {
        this.cities = response;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  getUsers() {
    this.apiService.getData('users').subscribe(
      (response) => {
        this.users = response.filter((users: any) => users.codigo);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  getCentral() {
    this.apiService.getData('central').subscribe(
      (response) => {
        this.central = response.filter((central: any) => central.codigo);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  selectButton(button: string) {
    this.selectedButton = button;
  }

  goToOwnerResume() {
    this.selectButton('hoja')
    this.OwnersContractView = false;
  }

  goToOwnerContract() {
    this.selectButton('contrato')
    this.OwnersContractView = true;
  }

  checkCode() {
    const code = this.ownerForm.get('codigo')?.value;
    if (code) {
      
    }
  
  }

  onSubmit() {
    if (this.ownerForm.valid) {
      const formData = this.ownerForm.value;
      console.log(formData);
    }
    else {
      window.alert('Por favor, llene los campos requeridos.');
    }
  }

}
