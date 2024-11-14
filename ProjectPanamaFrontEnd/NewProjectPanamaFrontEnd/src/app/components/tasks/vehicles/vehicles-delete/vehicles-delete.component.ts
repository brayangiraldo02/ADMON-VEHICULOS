import { Component, Input, Output, EventEmitter, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-vehicles-delete',
  templateUrl: './vehicles-delete.component.html',
  styleUrls: ['./vehicles-delete.component.css']
})
export class VehiclesDeleteComponent {
  @Input() isVisible: boolean = false;
  @Input() vehicle: string | null = null;
  @Input() number: string | null = null;
  @Output() close = new EventEmitter<void>();

  isLoading: boolean = true;
  doubleValidation: boolean = false;
  permissionsDelete: any;
  hasPermission: boolean = false;
  grantedPermission: string = '';
  deleteSuccesful: boolean = false;

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
      if(!this.hasPermission){
        this.apiService.deleteData("vehicle/"+this.vehicle).subscribe(
          (response) => {
            this.deleteSuccesful = true;
          },
          (error) => {
          }
        );
      }
    }
    else{
      this.doubleValidation = true;
    }
  }

  verifyPermissions() {
    this.apiService.getData("verify-vehicle-delete/"+this.vehicle).subscribe(
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
        this.isLoading = false;
      },
      (error) => {
      }
    );
  }

  resetState() {
    this.permissionsDelete = null;
    this.hasPermission = false;
    this.grantedPermission = '';
    this.isLoading = true;
    this.doubleValidation = false;
    this.deleteSuccesful = false;
  }

  returnOwners() {
    this.closeModal();
    this.router.navigate(['/vehicles']);
  }

  closeModal() {
    this.resetState();
    this.close.emit();
  }

}
