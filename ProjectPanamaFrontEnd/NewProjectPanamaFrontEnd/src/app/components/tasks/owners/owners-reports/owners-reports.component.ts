import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-owners-reports',
  templateUrl: './owners-reports.component.html',
  styleUrls: ['./owners-reports.component.css']
})
export class OwnersReportsComponent {
  @Input() isVisible: boolean = false;
  @Output() close = new EventEmitter<void>();

  closeModal() {
    this.close.emit();
  }
}