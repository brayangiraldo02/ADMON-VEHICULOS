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
  isLoading = true;

  constructor(private route: ActivatedRoute, private apiService: ApiService) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.code = params.get('code');
    });
    this.fetchData();
  }

  fetchData() {
    this.apiService.getData(`owner/${this.code}`).subscribe(
      (response) => {
        this.data = response;
        console.log(this.data);
        this.isLoading = false;
      },
      (error) => {
        console.log(error);
        this.isLoading = false;
      }
    );
  }

  enableInputs() {
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
      'correo', 'correo1'
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

    this.disableInputs();
    console.log('Data to save:', dataToSave);
    // Here you can send the dataToSave object to your API or handle it as needed
  }
}
