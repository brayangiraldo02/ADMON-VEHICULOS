import { Component, EventEmitter, inject, OnDestroy, OnInit, Output } from '@angular/core';
import { InfoCompanyStateService } from 'src/app/states/info-company-state.service';

@Component({
  selector: 'app-info-company',
  templateUrl: './info-company.component.html',
  styleUrls: ['./info-company.component.css']
})
export class InfoCompanyComponent {
  @Output() close = new EventEmitter<void>();

  isLoading: boolean = false;

  constructor(private stateInfoCompany: InfoCompanyStateService) {}

  closeModal() {
    this.stateInfoCompany.hideInfoCompany();
    this.close.emit();
  }
}
