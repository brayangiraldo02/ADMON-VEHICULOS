import { Component } from '@angular/core';
import { Router } from '@angular/router'
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {

  constructor(private apiService: ApiService, private jwtService: JwtService, private router: Router) { }

  logout(): void {
    this.jwtService.removeToken();
    this.apiService.postData('logout', {}).subscribe(
      (response) => {
        console.log(response);
        this.router.navigate(['/login']);
      },
      (error) => {
        console.log(error);
      }
    );
  }
}
