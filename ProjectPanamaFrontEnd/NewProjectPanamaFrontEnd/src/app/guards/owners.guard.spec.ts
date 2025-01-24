import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';

import { ownersGuard } from './owners.guard';

describe('ownersGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) => 
      TestBed.runInInjectionContext(() => ownersGuard(...guardParameters));

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(executeGuard).toBeTruthy();
  });
});
