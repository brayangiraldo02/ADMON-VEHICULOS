import { computed, Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class InfoCompanyStateService {

  private infoCompanyState = signal<boolean>(false);

  public displayInfoCompany = computed(() => this.infoCompanyState());

  showInfoCompany(): void {
    this.infoCompanyState.set(true);
  }

  hideInfoCompany(): void {
    this.infoCompanyState.set(false);
  }
}
