import { Injectable, signal, computed, inject } from '@angular/core';
import { InfoCompanyStateService } from '../modules/shared/services/info-company-state.service';
import { InfoCompany } from '../interfaces/info-company.interface';
import { SelectedOwnersStateService } from '../modules/home/services/selected-owners-state.service';

@Injectable({
  providedIn: 'root'
})
export class GlobalStatesService {

  private infoCompanyStateService = inject(InfoCompanyStateService);

  public setInfoCompany(infoCompany: InfoCompany): void {
    this.infoCompanyStateService.setInfoCompany(infoCompany);
  }
  
  public displayInfoCompany = this.infoCompanyStateService.displayInfoCompany;

  private selectedOwnersCobrosStateService = inject(SelectedOwnersStateService)

  public getSelectedOwners = this.selectedOwnersCobrosStateService.getSelectedOwners;

  public clearSelectedOwners(): void {
    this.selectedOwnersCobrosStateService.clearSelectedOwners();
  }
}
