import { Component, ViewChild } from '@angular/core';
import { TakeSignatureComponent } from '../take-signature/take-signature.component';
import { TakePhotoComponent } from '../take-photo/take-photo.component';

@Component({
  selector: 'app-take-signature-photo',
  templateUrl: './options-take-signature-photo-dialog.component.html',
  styleUrls: ['./options-take-signature-photo-dialog.component.css'],
})
export class TakeSignaturePhotoComponent {
  @ViewChild(TakeSignatureComponent)
  takeSignatureComponent!: TakeSignatureComponent;

  @ViewChild(TakePhotoComponent)
  takePhotoComponent!: TakePhotoComponent;

  takeSignature: boolean = false;
  takePhoto: boolean = false;
  isSignaturePadVisible: boolean = false;
  isCameraVisible: boolean = false;

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

  nextStepPhoto() {
    if (this.takePhotoComponent) {
      if (!this.isCameraVisible) {
        this.takePhotoComponent.viewCamera();
        this.isCameraVisible = true;
      } else {
        this.takePhotoComponent.triggerSavePhoto();
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

  isPhotoButtonDisabled(): boolean {
    if (!this.takePhotoComponent) {
      return true;
    }

    const info = this.takePhotoComponent.vehiclePhotoInfo;

    return (
      info.driver_code === '' ||
      info.has_picture === 1 ||
      !this.takePhotoComponent.selectedVehicle
    );
  }
}
