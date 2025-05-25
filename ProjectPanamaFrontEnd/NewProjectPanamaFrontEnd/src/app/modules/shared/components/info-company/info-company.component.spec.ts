import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoCompanyComponent } from './info-company.component';

describe('InfoCompanyComponent', () => {
  let component: InfoCompanyComponent;
  let fixture: ComponentFixture<InfoCompanyComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InfoCompanyComponent]
    });
    fixture = TestBed.createComponent(InfoCompanyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
