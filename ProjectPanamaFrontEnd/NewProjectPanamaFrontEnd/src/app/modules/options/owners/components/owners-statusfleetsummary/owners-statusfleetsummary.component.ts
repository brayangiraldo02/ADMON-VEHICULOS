import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

interface Owner {
  id: string;
  name: string;
}

@Component({
  selector: 'app-owners-statusfleetsummary',
  templateUrl: './owners-statusfleetsummary.component.html',
  styleUrls: ['./owners-statusfleetsummary.component.css'],
})
export class OwnersStatusfleetsummaryComponent implements OnInit {
  @Output() close = new EventEmitter<void>();

  isLoading: boolean = true;

  owners: Owner[] = [];

  user: any;

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
    this.listOwners();
    this.getUser();
  }

  listOwners(): void {
    console.log(this.jwtService.obtainId());
    const owner = {
      propietario: this.jwtService.obtainId(),
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
    this.user = this.jwtService.decodeToken();
    this.user = this.user.user_data.nombre;
  }

  resetValues(): void {
    this.infoForm.reset();
  }

  onSubmit(): void {
    if (this.infoForm.valid) {
      console.log(this.infoForm.value);
      this.openExternalLink();
    }
  }

  openExternalLink(): void {
    let endpoint = 'estado-vehiculos-resumen-empresa/';
    endpoint += this.infoForm.value.companie;
    if (endpoint) {
      const data = { user: this.user };
      console.log(data);
      localStorage.setItem('pdfEndpoint', endpoint);
      localStorage.setItem('pdfData', JSON.stringify(data));
      window.open(`/pdf`, '_blank');
      this.resetValues();
      this.closeModal();
    } else {
      console.error('URL no encontrada para la opción seleccionada.');
    }
  }

  closeModal() {
    this.close.emit();
  }
}
