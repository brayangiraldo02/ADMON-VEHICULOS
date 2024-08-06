import { Component, Input, Output, EventEmitter, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-owners-delete',
  templateUrl: './owners-delete.component.html',
  styleUrls: ['./owners-delete.component.css']
})
export class OwnersDeleteComponent implements OnInit, OnChanges {
  @Input() isVisible: boolean = false;
  @Input() owner: string | null = null;
  @Output() close = new EventEmitter<void>();

  doubleValidation: boolean = false;
  permissionsDelete: any;
  hasPermission: boolean = false;
  grantedPermission: string = '';

  constructor(
    private router: Router,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['isVisible'] && changes['isVisible'].currentValue === true) {
      this.resetState();
      this.verifyPermissions();
    }
  }

  acceptRemove() {
    if(this.doubleValidation){

    }
    else{

      this.doubleValidation = true;
    }
  }

  verifyPermissions() {
    this.apiService.getData("verify-owner-delete/"+this.owner).subscribe(
      (response) => {
        this.permissionsDelete = response;
        console.log(this.permissionsDelete)

        for (const [key, value] of Object.entries(response)) {
          if (value === true) {
            this.hasPermission = true;
            this.grantedPermission = key;
            break; 
          }
        }
        console.log('Has Permission:', this.hasPermission);
        console.log('Granted Permission:', this.grantedPermission);
      },
      (error) => {
      }
    );
  }

  resetState() {
    this.permissionsDelete = null;
  }

  closeModal() {
    this.resetState();
    this.close.emit();
  }
}
