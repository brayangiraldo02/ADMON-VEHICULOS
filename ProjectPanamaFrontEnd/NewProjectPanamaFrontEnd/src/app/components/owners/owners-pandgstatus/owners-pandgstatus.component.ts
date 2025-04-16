import { Component, Input, Output, EventEmitter } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

interface Vehicle {
  placa: string;
  numero: string;
  marca: string;
  consecutivo: string;
}

interface DateCurrently {
  time: string;
}

interface CompaniesOwners {
  id: string;
  name: string;
}

@Component({
  selector: 'app-owners-pandgstatus',
  templateUrl: './owners-pandgstatus.component.html',
  styleUrls: ['./owners-pandgstatus.component.css']
})
export class OwnersPandgstatusComponent {

  @Output() close = new EventEmitter<void>();
      
      isLoading: boolean = false;
      isLoadingValues: boolean = true;
    
      vehicles: Vehicle[] = [];
    
      vehicles_per: any;
      companiesKeys: string[] = [];
      selectedCompany: string = '';
    
      user: any;
    
      infoForm: FormGroup;
    
      companiesOwners: CompaniesOwners[] = [];
    
      date!: DateCurrently;
    
      constructor(
        private apiService: ApiService,
        private jwtService: JwtService,
        private fb: FormBuilder
      ) {
        this.infoForm = this.fb.group({
          companie: ['', Validators.required],
          vehicle: [{ value: '', disabled: true }],
          firstDate: ['', Validators.required],
          lastDate: ['', Validators.required]
        });
      }
    
      ngOnInit(): void {
        this.listVehiclesPerOwners()
        this.listVehicles();
        this.getDate();
        this.getUser();
      }
    
      getDate(): void {
        this.apiService.getData('extras/time').subscribe(
          (response) => {
            this.date = response;
            this. isLoadingValues = false;
            console.log(this.date);
          },
          (error) => {
            error.log(error);
          }
        );
      }
    
      onCompanyChange(event: Event): void {
        const selectElement = event.target as HTMLSelectElement;
        const value = selectElement.value;
        this.selectedCompany = value;
        if (value) {
          this.infoForm.get('vehicle')?.enable();
        } else {
          this.infoForm.get('vehicle')?.disable();
        }
      }
    
      listVehiclesPerOwners(): void {
        console.log(this.jwtService.obtainId());
        const vehicle = {
          propietario: this.jwtService.obtainId()
        }
    
        console.log(vehicle);
    
        this.apiService.postData("vehicles_per_owners", vehicle).subscribe(
          (response) => {
            this.vehicles_per = response; // vehicles ahora es un objeto
            // Extraer las llaves (nombres de empresa)
            this.companiesKeys = Object.keys(response);
            console.log(response);
          },
          (error) => {
            error.log(error);
          }
        );
      }
    
      listVehicles(): void {
        console.log(this.jwtService.obtainId());
        const vehicle = {
          propietario: this.jwtService.obtainId()
        }
    
        console.log(vehicle);
    
        this.apiService.postData("vehicles_owners", vehicle).subscribe(
          (response) => {
            this.vehicles = response;
            // this.vehicles.sort((a, b) => a.numero.localeCompare(b.numero));
            if (!this.jwtService.isAdmin()) {
              const defaultVehicle = {
                placa: "",
                numero: "",
                marca: "",
                consecutivo: ""
              };
              this.vehicles = [defaultVehicle, ...this.vehicles];
            }
            console.log(this.vehicles);
          },
          (error) => {
            error.log(error);
          }
        );
      }
    
      getUser() {
        this.user = this.jwtService.decodeToken();
        this.user = this.user.user_data.nombre;
        this.getCompanies();
      }
    
      getCompanies() {
        const owner = {
          propietario: this.jwtService.obtainId()
        }
        this.apiService.postData('companies_owners', owner).subscribe(
          (response: any[]) => {
            this.companiesOwners = response.map(item => item.id);
            console.log(this.companiesOwners); // Will show: ['50', '51', '57', '60', '63']
          },
          (error) => {
            console.error(error);
          }
        );
    }
    
    onSubmit(): void {
      if (this.infoForm.valid) {
        console.log(this.infoForm.value);
        this.openExternalLink();
      }
    }
  
    openExternalLink(): void {
      let endpoint = 'pandgstatus';
      if (endpoint) {
        const companyValue = this.infoForm.value.companie;
        let companyName = companyValue; // Default to the full value
        if (companyValue && companyValue.includes(' - ')) {
          companyName = companyValue.split(' - ')[0].trim(); 
        }
        const data = {
          'usuario': this.user,
          'primeraFecha': this.infoForm.value.firstDate,
          'ultimaFecha': this.infoForm.value.lastDate,
          'unidad': this.infoForm.value.vehicle,
          'empresa': companyName
        };
        console.log(data);
        localStorage.setItem('pdfEndpoint', endpoint);
        localStorage.setItem('pdfData', JSON.stringify(data));
        window.open(`/pdf`, '_blank')
        this.closeModal();
      } else {
        console.error('URL no encontrada para la opción seleccionada.');
      }
    }
  
    closeModal() {
      this.close.emit();
    }

}
