import { Component, ViewChild } from '@angular/core';
import { TakeSignatureComponent } from '../take-signature/take-signature.component';
import { TakePhotoComponent } from '../take-photo/take-photo.component';
import { TakeVehiclePhotoComponent } from '../take-vehicle-photo/take-vehicle-photo.component';

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

  @ViewChild(TakeVehiclePhotoComponent)
  takeVehiclePhotoComponent!: TakeVehiclePhotoComponent;

  takeSignature: boolean = false;
  takePhoto: boolean = false;
  takeVehicle: boolean = false;
  isSignaturePadVisible: boolean = false;
  isCameraVisible: boolean = false;

  constructor() {}

  openDocuments(option: string) {
    if (option === 'signature') {
      this.takeSignature = true;
      this.takePhoto = false;
      this.takeVehicle = false;
    } else if (option === 'photo') {
      this.takeSignature = false;
      this.takePhoto = true;
      this.takeVehicle = false;
    } else if (option === 'vehicle') {
      this.takeSignature = false;
      this.takePhoto = false;
      this.takeVehicle = true;
    }
     else if (option === 'close') {
      this.takeSignature = false;
      this.takePhoto = false;
      this.takeVehicle = false;
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

  nextStepVehiclePhoto() {
    if (this.takeVehiclePhotoComponent) {
      if (!this.isCameraVisible) {
        this.takeVehiclePhotoComponent.viewCamera();
        this.isCameraVisible = true;
      } else {
        this.takeVehiclePhotoComponent.triggerSavePhoto();
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
      !this.takePhotoComponent.selectedVehicle
    );
  }

  isVehiclePhotoButtonDisabled(): boolean {
    if (!this.takeVehiclePhotoComponent) {
      return true;
    }

    const info = this.takeVehiclePhotoComponent.vehiclePhotoInfo;

    return (
      info.driver_code === '' ||
      !this.takeVehiclePhotoComponent.selectedVehicle
    );
  }
}
