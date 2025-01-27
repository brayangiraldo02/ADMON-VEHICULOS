import { Component, Input, Output, EventEmitter } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

interface Owner {
  id: string;
  name: string;
}

@Component({
  selector: 'app-owners-statusfleetsummary',
  templateUrl: './owners-statusfleetsummary.component.html',
  styleUrls: ['./owners-statusfleetsummary.component.css']
})
export class OwnersStatusfleetsummaryComponent {
  @Output() close = new EventEmitter<void>();
  
    isLoading: boolean = false;
  
    selectedCompany: string = '';
  
    owners: Owner[] = [];
  
    user: any;
  
    constructor(
      private apiService: ApiService,
      private jwtService: JwtService
    ) { }
  
    ngOnInit(): void {
      this.listOwners();
      this.getUser();
    }
  
    listOwners(): void {
      console.log(this.jwtService.obtainId());
      const owner = {
        propietario: this.jwtService.obtainId()
      }
  
      console.log(owner);
  
      this.apiService.postData("companies_owners", owner).subscribe(
        (response) => {
          this.owners = response.filter((owner: any) => owner.id);
          this.owners.sort((a, b) => a.name.localeCompare(b.name));
          console.log(this.owners);
        },
        (error) => {
          console.log(error);
        }
      );
    }
  
    getUser() {
      this.user = this.jwtService.decodeToken();
      this.user = this.user.user_data.nombre;
    }
  
    onCompanyChange(event: Event): void {
      const selectElement = event.target as HTMLSelectElement;
      this.selectedCompany = selectElement.value;
      console.log(this.selectedCompany)
      this.openExternalLink()
    }
  
    resetValues(): void {
      this.selectedCompany = '';
    }
  
    openExternalLink(): void {
      let endpoint = 'estado-vehiculos-resumen-empresa/';
      endpoint += this.selectedCompany;
      if (endpoint) {
        const data = { user: this.user };
        console.log(data);
        localStorage.setItem('pdfEndpoint', endpoint);
        localStorage.setItem('pdfData', JSON.stringify(data));
        window.open(`/pdf`, '_blank')
        this.resetValues()
        this.closeModal();
      } else {
        console.error('URL no encontrada para la opción seleccionada.');
      }
    }
  
    closeModal() {
      this.close.emit();
    }
}
