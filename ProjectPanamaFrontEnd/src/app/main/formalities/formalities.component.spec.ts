import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormalitiesComponent } from './formalities.component';

describe('FormalitiesComponent', () => {
  let component: FormalitiesComponent;
  let fixture: ComponentFixture<FormalitiesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FormalitiesComponent]
    });
    fixture = TestBed.createComponent(FormalitiesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
