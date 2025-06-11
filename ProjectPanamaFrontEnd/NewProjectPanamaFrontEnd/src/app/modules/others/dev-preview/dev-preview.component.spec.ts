import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DevPreviewComponent } from './dev-preview.component';

describe('DevPreviewComponent', () => {
  let component: DevPreviewComponent;
  let fixture: ComponentFixture<DevPreviewComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DevPreviewComponent]
    });
    fixture = TestBed.createComponent(DevPreviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
