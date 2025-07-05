import { computed, Injectable, signal } from '@angular/core';
import { Owners } from '../interfaces/owners.interface';

const DEFAFULT_OWNERS: Owners = {
  owners: []
};

@Injectable({
  providedIn: 'root',
})
export class SelectedOwnersStateService {
  private selectedOwners = signal<Owners>({
    owners: [],
  });

  public getSelectedOwners = computed(() => this.selectedOwners());

  setSelectedOwners(owners: Owners): void {
    this.selectedOwners.set(owners);
  }

  clearSelectedOwners(): void {
    this.selectedOwners.set(DEFAFULT_OWNERS);
  }
}
