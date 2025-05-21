import { Component, effect, EventEmitter, inject, OnDestroy, OnInit, Output } from '@angular/core';
import { InfoCompany } from 'src/app/interfaces/info-company.interface';
import { InfoCompanyStateService } from 'src/app/states/info-company-state.service';

@Component({
  selector: 'app-info-company',
  templateUrl: './info-company.component.html',
  styleUrls: ['./info-company.component.css']
})
export class InfoCompanyComponent {
  @Output() close = new EventEmitter<void>();

  isLoading: boolean = false;

  infoCompany: InfoCompany = {
    name: '',
    nit: '',
    direction: '',
    city: '',
    phone: '',
    email: '',
    logo: ''
  }

  constructor(private stateInfoCompany: InfoCompanyStateService) {
    effect(() => {
      this.infoCompany = this.stateInfoCompany.getInfoCompany();
    });
  }

  closeModal() {
    this.stateInfoCompany.hideInfoCompany();
    this.close.emit();
  }
}
