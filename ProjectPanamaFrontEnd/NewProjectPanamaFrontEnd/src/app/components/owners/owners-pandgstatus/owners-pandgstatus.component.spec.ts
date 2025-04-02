import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OwnersPandgstatusComponent } from './owners-pandgstatus.component';

describe('OwnersPandgstatusComponent', () => {
  let component: OwnersPandgstatusComponent;
  let fixture: ComponentFixture<OwnersPandgstatusComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OwnersPandgstatusComponent]
    });
    fixture = TestBed.createComponent(OwnersPandgstatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
