import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';

import { inspectionsGuard } from './inspections.guard';

describe('inspectionsGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) => 
      TestBed.runInInjectionContext(() => inspectionsGuard(...guardParameters));

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(executeGuard).toBeTruthy();
  });
});
