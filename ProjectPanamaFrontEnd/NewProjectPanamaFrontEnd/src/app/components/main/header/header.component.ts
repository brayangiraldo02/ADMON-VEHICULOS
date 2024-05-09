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

  permisos: any;

  ngOnInit() {
    this.obtenerUsuario();
    console.log(this.permisos);
  }

  obtenerUsuario() {
    this.permisos = this.jwtService.decodeToken();

    this.convertirValoresBooleanos(this.permisos.user_data);

    console.log(this.permisos.user_data);
  }

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

  convertirValoresBooleanos(obj: any) {
    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        const value = obj[key];
        if (value === 'T') {
          obj[key] = true;
        } else if (value === 'F' || value === null) {
          obj[key] = false;
        }
      }
    }
  }
}
