import { Component } from '@angular/core';

@Component({
  selector: 'app-owners-resume',
  templateUrl: './owners-resume.component.html',
  styleUrls: ['./owners-resume.component.css']
})
export class OwnersResumeComponent {
  enableInputs() {
    const nameElement = document.getElementById('nombre') as HTMLInputElement;
    if (nameElement) {
      nameElement.disabled = false;
    }
  }

  disableInputs() {
    const nameElement = document.getElementById('nombre') as HTMLInputElement;
    if (nameElement) {
      nameElement.disabled = true;
    }
  }
}


