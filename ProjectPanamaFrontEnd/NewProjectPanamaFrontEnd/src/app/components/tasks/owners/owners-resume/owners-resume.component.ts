import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-owners-resume',
  templateUrl: './owners-resume.component.html',
  styleUrls: ['./owners-resume.component.css']
})
export class OwnersResumeComponent implements OnInit {
  code: string | null = null;
  data: any = null;
  isLoading = true;

  constructor(private route: ActivatedRoute, private apiService: ApiService) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.code = params.get('code');
    });
    this.fetchData();
  }

  fetchData() {
    this.apiService.getData(`owner/${this.code}`).subscribe(
      (response) => {
        this.data = response;
        console.log(this.data);
        this.isLoading = false;
      },
      (error) => {
        console.log(error);
        this.isLoading = false;
      }
    );
  }

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
