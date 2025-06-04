import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeOwnersComponent } from './home-owners.component';

describe('HomeOwnersComponent', () => {
  let component: HomeOwnersComponent;
  let fixture: ComponentFixture<HomeOwnersComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [HomeOwnersComponent]
    });
    fixture = TestBed.createComponent(HomeOwnersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
