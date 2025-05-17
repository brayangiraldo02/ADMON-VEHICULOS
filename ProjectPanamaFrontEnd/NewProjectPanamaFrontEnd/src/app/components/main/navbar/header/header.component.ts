import { Component, effect, inject, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';
import { OwnersGuard } from 'src/app/guards/owners.guard';
import { InfoCompanyStateService } from 'src/app/states/info-company-state.service';
import { InfoCompany } from 'src/app/interfaces/info-company.interface';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  permisos: any;
  isHome: boolean = true;
  imgUser: string = "../../../../assets/img/taxi.jpg";
  ownerView: boolean = false;
  infoCompanyVisible: boolean = false;

  infoCompany: InfoCompany = {
    name: '',
    nit: '',
    direction: '',
    city: '',
    phone: '',
    email: '',
    logo: ''
  }

  constructor(
    private apiService: ApiService,
    private jwtService: JwtService,
    private router: Router,
    private cdr: ChangeDetectorRef, // Importante para detectar cambios
    private ownersGuard: OwnersGuard,
    private stateInfoCompany: InfoCompanyStateService
  ) { 
    effect(() => {
      this.infoCompany = this.stateInfoCompany.getInfoCompany();
    });
  }

  ngOnInit() {
    this.obtenerUsuario();
  }

  // FUTURA FUNCIÓN, QUE CUANDO ESTÉ EN UNA RUTA DIFERENTE DEL HOME, NO MUESTRE LAS TAREAS.
  // private subscribirEventosDeRuta() {
  //   this.router.events.subscribe(event => {
  //     if (event instanceof NavigationEnd) {
  //       this.isHome = this.router.url === '/home';
  //       if (this.router.url === '/home') {
  //         this.isHome = true;
  //       }
  //       else {
  //         this.isHome = false;
  //       }
  //       console.log('NavigationEnd event detected');
  //       console.log(`URL changed: ${this.router.url}`);
  //       console.log(`isHome: ${this.isHome}`);
  //       this.cdr.detectChanges(); 
  //     }
  //   });
  // }

  obtenerUsuario() {
    this.permisos = this.jwtService.decodeToken();
    // this.imgUser = this.permisos.user_data.foto; // Cuando se tengan las rutas de las imágenes
    this.convertirValoresBooleanos(this.permisos.user_data);
    // this.subscribirEventosDeRuta();
    // console.log(this.permisos.user_data);
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

    if (this.permisos.user_data.opcion16 === true && !this.jwtService.isAdmin()) {
      this.ownerView = true;
    }
  }

  showModal() {
    this.infoCompanyVisible = !this.infoCompanyVisible;
    this.stateInfoCompany.showInfoCompany();

    document.documentElement.style.overflow = 'hidden';
    document.body.style.overflow = 'hidden';
  }

  hideModal() {
    this.infoCompanyVisible = !this.infoCompanyVisible;

    document.documentElement.style.overflow = '';
    document.body.style.overflow = '';
  }
}