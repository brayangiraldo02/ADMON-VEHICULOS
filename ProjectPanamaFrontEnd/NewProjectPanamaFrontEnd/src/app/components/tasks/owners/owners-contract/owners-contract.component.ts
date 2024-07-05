import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-owners-contract',
  templateUrl: './owners-contract.component.html',
  styleUrls: ['./owners-contract.component.css']
})
export class OwnersContractComponent implements OnInit {
  code: string | null = null;
  isLoading = true;
  data: any;
  infoOwner: any;
  isEditable = false;
  fields = [
    'razon_social', 'representante', 'sexo', 'estado_civil', 'tipo_documento', 'numero_documento', 'nacionalidad', 'ficha', 'documento'
  ];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService
  ) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.code = params.get('code');
    });
    this.fetchData();
    this.getInfoOwner();
  }

  fetchData() {
    this.apiService.getData(`owner-representative/${this.code}`).subscribe(
      (response) => {
        this.data = response;
        console.log('Fetch Data:', this.data);
        this.isLoading = false;
      },
      (error) => {
        console.log(error);
        this.isLoading = false;
      }
    );
  }

  getInfoOwner(){
    this.apiService.getData(`owner/${this.code}`).subscribe(
      (response) => {
        this.infoOwner = response;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  enableInputs() {
    if (this.isEditable) {
      this.disableInputs();
      window.alert('No se ha modificado ningún dato.');
      location.reload();
    }

    this.isEditable = true;
    this.fields.forEach(field => {
      const element = document.getElementById(field) as HTMLInputElement;
      if (element) {
        element.disabled = false;
      }
    });
  }

  disableInputs() {
    this.isEditable = false;
    this.fields.forEach(field => {
      const element = document.getElementById(field) as HTMLInputElement;
      if (element) {
        element.disabled = true;
      }
    });
  }

  newData() {
    const dataToSave: any = {};
    this.fields.forEach(field => {
      const element = document.getElementById(field) as HTMLInputElement;
      if (element) {
        dataToSave[field] = element.value;
      }
    });

    return dataToSave;
  }

  checkModifiedData(dataToSave:any) {

    let modified = false;
    this.fields.forEach(field => {
      if (dataToSave[field] != this.data[field]) {
        console.log('Modified field:', field, dataToSave[field], this.data[field])
        modified = true;
      }
    });

    return modified;
  }

  saveData() {

    const dataToSave = this.newData();

    const modifiedData = this.checkModifiedData(dataToSave);

    console.log(modifiedData)

    if (!modifiedData) {
      window.alert('No se ha modificado ningún dato.');
      this.disableInputs();
      return;
    }

    console.log('Data to save:', dataToSave);
    this.disableInputs();
  
    this.apiService.updateData(`owner-representative/${this.code}`, dataToSave).subscribe(
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

  goToOwnerVehicles(code: string | null) {
    this.router.navigate(['/owner-vehicles', code]);
  }

  goToOwnerResume(code: string | null) {
    this.router.navigate(['/owner', code]);
  }
}
