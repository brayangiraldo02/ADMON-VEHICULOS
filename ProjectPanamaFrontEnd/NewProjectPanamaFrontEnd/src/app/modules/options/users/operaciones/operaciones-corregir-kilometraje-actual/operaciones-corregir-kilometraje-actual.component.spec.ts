import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacionesCorregirKilometrajeActualComponent } from './operaciones-corregir-kilometraje-actual.component';

describe('OperacionesCorregirKilometrajeActualComponent', () => {
  let component: OperacionesCorregirKilometrajeActualComponent;
  let fixture: ComponentFixture<OperacionesCorregirKilometrajeActualComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacionesCorregirKilometrajeActualComponent]
    });
    fixture = TestBed.createComponent(OperacionesCorregirKilometrajeActualComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
