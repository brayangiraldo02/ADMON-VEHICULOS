import { computed, Injectable, signal } from '@angular/core';
import { InfoCompany } from '../interfaces/info-company.interface';

const INFOCOMPANY_DEFAULT: InfoCompany = {
  name: '',
  nit: '',
  direction: '',
  city: '',
  phone: '',
  email: '',
  logo: ''
};


@Injectable({
  providedIn: 'root'
})
export class InfoCompanyStateService {

  private infoCompanyState = signal<boolean>(false);
  private infoCompany = signal<InfoCompany>(INFOCOMPANY_DEFAULT);

  public displayInfoCompany = computed(() => this.infoCompanyState());
  public getInfoCompany = computed(() => this.infoCompany());

  showInfoCompany(): void {
    this.infoCompanyState.set(true);
  }

  hideInfoCompany(): void {
    this.infoCompanyState.set(false);
  }

  setInfoCompany(infoCompany: InfoCompany): void {
    this.infoCompany.set(infoCompany);
  }
}
