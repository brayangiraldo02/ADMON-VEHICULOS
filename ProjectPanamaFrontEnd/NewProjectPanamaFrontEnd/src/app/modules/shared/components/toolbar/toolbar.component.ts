import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import { JwtService } from 'src/app/services/jwt.service';
import { ApiService } from 'src/app/services/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.css']
})
export class ToolbarComponent implements OnInit {
  @Output() menuClick = new EventEmitter<void>();

  permisos: any;
  ownerView: boolean = false;

  constructor(private jwtService: JwtService, private apiService: ApiService, private router: Router) {}

  ngOnInit() {
    this.obtenerUsuario();
  }

  obtenerUsuario() {
    this.permisos = this.jwtService.decodeToken();
    // this.imgUser = this.permisos.user_data.foto; // Cuando se tengan las rutas de las imágenes
    this.convertirValoresBooleanos(this.permisos.user_data);
    // this.subscribirEventosDeRuta();
    // console.log(this.permisos.user_data);
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

    if (
      this.permisos.user_data.opcion16 === true &&
      !this.jwtService.isAdmin()
    ) {
      this.ownerView = true;
    }
  }

  onMenuClick() {
    this.menuClick.emit();
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
}
