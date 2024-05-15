import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-statevehiclefleet',
  templateUrl: './statevehiclefleet.component.html',
  styleUrls: ['./statevehiclefleet.component.css']
})
export class StatevehiclefleetComponent {

  constructor(private router: Router) { }

  home(): void {
    this.router.navigate(['/home']);
  }
}
