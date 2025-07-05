import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OwnersFeespaidComponent } from './owners-feespaid.component';

describe('OwnersFeespaidComponent', () => {
  let component: OwnersFeespaidComponent;
  let fixture: ComponentFixture<OwnersFeespaidComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OwnersFeespaidComponent]
    });
    fixture = TestBed.createComponent(OwnersFeespaidComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
