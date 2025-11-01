import { Component, ViewChild } from '@angular/core';
import { TakeSignatureComponent } from '../take-signature/take-signature.component';

@Component({
  selector: 'app-take-signature-photo',
  templateUrl: './options-take-signature-photo-dialog.component.html',
  styleUrls: ['./options-take-signature-photo-dialog.component.css'],
})
export class TakeSignaturePhotoComponent {
  @ViewChild(TakeSignatureComponent)
  takeSignatureComponent!: TakeSignatureComponent;

  takeSignature: boolean = false;
  takePhoto: boolean = false;
  isSignaturePadVisible: boolean = false;

  constructor() {}

  openDocuments(option: string) {
    if (option === 'signature') {
      this.takeSignature = true;
      this.takePhoto = false;
    } else if (option === 'photo') {
      this.takeSignature = false;
      this.takePhoto = true;
    } else if (option === 'close') {
      this.takeSignature = false;
      this.takePhoto = false;
    }
  }

  nextStepSignature() {
    if (this.takeSignatureComponent) {
      if (!this.isSignaturePadVisible) {
        this.takeSignatureComponent.viewSignaturePad();
        this.isSignaturePadVisible = true;
      } else {
        this.takeSignatureComponent.triggerSaveSignature();
      }
    }
  }

  isButtonDisabled(): boolean {
    if (!this.takeSignatureComponent) {
      return true;
    }

    const info = this.takeSignatureComponent.vehicleSignatureInfo;

    return (
      info.driver_code === '' ||
      info.has_signature === 1 ||
      !this.takeSignatureComponent.selectedVehicle
    );
  }
}
