import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  permisos: any;
  isHome: boolean = true;

  constructor(
    private apiService: ApiService,
    private jwtService: JwtService,
    private router: Router,
    private cdr: ChangeDetectorRef // Importante para detectar cambios
  ) { }

  ngOnInit() {
    this.obtenerUsuario();
  }

  private subscribirEventosDeRuta() {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.isHome = this.router.url === '/home';
        if (this.router.url === '/home') {
          this.isHome = true;
        }
        else {
          this.isHome = false;
        }
        console.log('NavigationEnd event detected');
        console.log(`URL changed: ${this.router.url}`);
        console.log(`isHome: ${this.isHome}`);
        this.cdr.detectChanges(); 
      }
    });
  }

  obtenerUsuario() {
    this.permisos = this.jwtService.decodeToken();
    this.convertirValoresBooleanos(this.permisos.user_data);
    this.subscribirEventosDeRuta();
    console.log(this.permisos.user_data);
  }

  logout(): void {
    this.jwtService.removeToken();
    this.apiService.postData('logout', {}).subscribe(
      (response) => {
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