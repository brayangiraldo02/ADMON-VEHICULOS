import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

interface Owner {
  id: string;
  name: string;
}

@Component({
  selector: 'app-owners-purchasevalueandpiquera',
  templateUrl: './owners-purchasevalueandpiquera.component.html',
  styleUrls: ['./owners-purchasevalueandpiquera.component.css'],
})
export class OwnersPurchasevalueandpiqueraComponent implements OnInit {
  @Output() close = new EventEmitter<void>();

  isLoading: boolean = true;

  user: any;
  owners: Owner[] = [];

  infoForm: FormGroup;

  constructor(
    private apiService: ApiService,
    private jwtService: JwtService,
    private fb: FormBuilder
  ) {
    this.infoForm = this.fb.group({
      companie: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.getUser();
    this.listOwners();
  }

  listOwners(): void {
    const userData = this.jwtService.getUserData();
    console.log(userData);
    const owner = {
      propietario: userData ? userData.id : null,
    };

    console.log(owner);

    this.apiService.postData('companies_owners', owner).subscribe(
      (response) => {
        this.owners = response.filter((owner: any) => owner.id);
        this.owners.sort((a, b) => a.name.localeCompare(b.name));
        console.log(this.owners);
        this.isLoading = false;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  getUser() {
    this.user = this.jwtService.getUserData();
    this.user = this.user.nombre;
  }

  onSubmit(): void {
    if (this.infoForm.valid) {
      console.log(this.infoForm.value);
      this.openExternalLink();
    }
  }

  openExternalLink(): void {
    let endpoint = 'valor-compra-vehiculos';
    if (endpoint) {
      const data = {
        usuario: this.user,
        empresas: [this.infoForm.value.companie],
        estados: [],
      };
      console.log(data);
      localStorage.setItem('pdfEndpoint', endpoint);
      localStorage.setItem('pdfData', JSON.stringify(data));
      window.open(`/pdf`, '_blank');
      this.closeModal();
    } else {
      console.error('URL no encontrada para la opción seleccionada.');
    }
  }

  closeModal() {
    this.close.emit();
  }
}
