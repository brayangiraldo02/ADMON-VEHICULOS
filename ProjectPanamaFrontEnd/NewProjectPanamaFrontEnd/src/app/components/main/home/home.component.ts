import { Component, OnInit } from '@angular/core';
import { JwtService } from 'src/app/services/jwt.service';
import { ApiService } from 'src/app/services/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  constructor(private jwtService: JwtService, private apiService: ApiService, private router: Router) { }

  options: any[] = []

  logoutIcon: string = '../../../../assets/icons/logout.svg';

  images: string[] = [
    '../../../assets/img/taxi1.jpg',
    '../../../assets/img/taxi2.jpg',
    '../../../assets/img/taxi3.jpg'
  ];
  currentImageIndex: number = 0;
  showImage: boolean = true;
  permisos: any;

  ngOnInit() {
    this.changeImagesPeriodically();
    this.obtenerUsuario();
  }

  obtenerUsuario() {
    this.permisos = this.jwtService.decodeToken();
    console.log(this.permisos.user_data);

    this.convertirValoresBooleanos(this.permisos.user_data);

    this.options = [
      { name: 'Caja', icon: '../../../../assets/icons/10.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion01 },
      { name: 'Operaciones', icon: '../../../../assets/icons/8.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion02 },
      { name: 'Cobros', icon: '../../../../assets/icons/9.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion03 },
      { name: 'Trámites', icon: '../../../../assets/icons/11.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion04 },
      { name: 'Almacén', icon: '../../../../assets/icons/12.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion5 },
      { name: 'Taller', icon: '../../../../assets/icons/14.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion06 },
      { name: 'Chapistería', icon: '../../../../assets/icons/15.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion07 },
      { name: 'Llavero', icon: '../../../../assets/icons/17.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion08 },
      { name: 'Reclamos', icon: '../../../../assets/icons/19.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion09 },
      { name: 'Cartera', icon: '../../../../assets/icons/18.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion10 },
      { name: 'Gerencia', icon: '../../../../assets/icons/21.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion11 },
      { name: 'Gastos', icon: '../../../../assets/icons/21.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion12 },
      { name: 'CNT', icon: '../../../../assets/icons/21.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion13 }
    ];
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

  changeImagesPeriodically() {
    setInterval(() => {
      this.showImage = false; // Oculta la imagen actual
      setTimeout(() => {
        this.currentImageIndex = (this.currentImageIndex + 1) % this.images.length;
        this.showImage = true; // Muestra la siguiente imagen
      }, 1000); // Espera 1 segundo para comenzar a mostrar la siguiente imagen
    }, 5000); // Intervalo total entre cambios de imagen
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

// ------------------------------------------------------

// import { Component } from '@angular/core';

// @Component({
//   selector: 'app-home',
//   templateUrl: './home.component.html',
//   styleUrls: ['./home.component.css']
// })
// export class HomeComponent {

// }
