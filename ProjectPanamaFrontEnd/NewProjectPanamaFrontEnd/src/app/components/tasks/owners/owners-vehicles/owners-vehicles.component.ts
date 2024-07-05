import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-owners-vehicles',
  templateUrl: './owners-vehicles.component.html',
  styleUrls: ['./owners-vehicles.component.css']
})
export class OwnersVehiclesComponent implements OnInit {
  code: string | null = null;
  isLoading = true;
  vehicles: any = null;
  infoOwner: any = null;
  
  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.code = params.get('code');
    });
    this.getInfoOwner();
    this.getData();
  }

  getData() {
    this.apiService.getData(`owner-vehicles/${this.code}`).subscribe(
      (response) => {
        this.vehicles = response;
        this.vehicles.sort((a: any, b: any) => {
          const aStartsWithSpecialChar = a.estado.startsWith('»');
          const bStartsWithSpecialChar = b.estado.startsWith('»');

          if (aStartsWithSpecialChar && !bStartsWithSpecialChar) {
            return 1;
          }
          if (!aStartsWithSpecialChar && bStartsWithSpecialChar) {
            return -1;
          }

          return a.estado.localeCompare(b.estado);
          }
        );
        this.isLoading = false;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  getInfoOwner(){
    this.apiService.getData(`owner/${this.code}`).subscribe(
      (response) => {
        this.infoOwner = response;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  goToOwnerResume(code: string | null) {
    this.router.navigate(['/owner', code]);
  }

  goToOwnerContract(code: string | null) {
    this.router.navigate(['/owner-contract', code]);
  }
}
