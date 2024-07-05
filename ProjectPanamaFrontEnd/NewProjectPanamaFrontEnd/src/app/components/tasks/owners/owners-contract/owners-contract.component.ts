import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-owners-contract',
  templateUrl: './owners-contract.component.html',
  styleUrls: ['./owners-contract.component.css']
})
export class OwnersContractComponent implements OnInit {
  code: string | null = null;
  isLoading = true;
  data: any;
  infoOwner: any;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService
  ) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.code = params.get('code');
    });
    this.fetchData();
    this.getInfoOwner();
  }

  fetchData() {
    this.apiService.getData(`owner-representative/${this.code}`).subscribe(
      (response) => {
        this.data = response;
        console.log('Fetch Data:', this.data);
        this.isLoading = false;
      },
      (error) => {
        console.log(error);
        this.isLoading = false;
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

  goToOwnerVehicles(code: string | null) {
    this.router.navigate(['/owner-vehicles', code]);
  }

  goToOwnerResume(code: string | null) {
    this.router.navigate(['/owner', code]);
  }
}
