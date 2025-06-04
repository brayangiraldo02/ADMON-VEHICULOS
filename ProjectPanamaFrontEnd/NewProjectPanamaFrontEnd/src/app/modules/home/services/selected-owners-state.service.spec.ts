import { TestBed } from '@angular/core/testing';

import { SelectedOwnersStateService } from './selected-owners-state.service';

describe('SelectedOwnersStateService', () => {
  let service: SelectedOwnersStateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SelectedOwnersStateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
