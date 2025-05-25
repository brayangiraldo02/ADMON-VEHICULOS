import { TestBed } from '@angular/core/testing';

import { InfoCompanyStateService } from './info-company-state.service';

describe('InfoCompanyStateService', () => {
  let service: InfoCompanyStateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InfoCompanyStateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
