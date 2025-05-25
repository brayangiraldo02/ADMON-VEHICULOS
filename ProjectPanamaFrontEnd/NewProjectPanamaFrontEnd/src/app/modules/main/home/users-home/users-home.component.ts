import { Component, OnInit, ViewChild, ElementRef, inject, effect } from '@angular/core';
import { JwtService } from 'src/app/services/jwt.service';
import { ApiService } from 'src/app/services/api.service';
import { Router } from '@angular/router';
import { GlobalStatesService } from 'src/app/states/global-states.service';

@Component({
  selector: 'app-users-home',
  templateUrl: './users-home.component.html',
  styleUrls: ['./users-home.component.css']
})
export class UsersHomeComponent implements OnInit {
  @ViewChild('videoPlayer') videoPlayer!: ElementRef<HTMLVideoElement>;

  options: any[] = []

  isAdmin: boolean = false;

  logoutIcon: string = '../../../../assets/icons/logout.svg';
  rightIcon: string = '../../../../assets/icons/rightArrow.svg';

  images: string[] = [
    '../../../../assets/img/taxi1.jpg',
    '../../../../assets/img/taxi2.jpg',
    '../../../../assets/img/taxi3.jpg'
  ];

  videos: string[] = [
    '../../../../assets/video/calle.mp4',
    '../../../../assets/video/conduccion.mp4',
  ]

  currentImageIndex: number = 0;
  showImage: boolean = true;
  currentVideoIndex: number = 0;
  currentVideo: string = '';
  changeVideo: boolean = true;
  permisos: any;

  infoCompanyVisible: boolean = false;

  constructor(
    private jwtService: JwtService, 
    private apiService: ApiService, 
    private router: Router,
    private globalStatesService: GlobalStatesService
  ) { 
    effect(() => {
      this.infoCompanyVisible = this.globalStatesService.displayInfoCompany();
    });
  }

  ngOnInit() {
    this.changeImagesPeriodically();
    this.obtenerUsuario();
    this.currentVideo = this.videos[this.currentVideoIndex];
  }

  obtenerUsuario() {
    this.permisos = this.jwtService.decodeToken();
    this.isAdmin = this.jwtService.isAdmin();
    // console.log(this.permisos.user_data);

    this.convertirValoresBooleanos(this.permisos.user_data);

    this.options = [
      { name: 'Caja', icon: '../../../../assets/icons/caja.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion01, disabled: true },
      { name: 'Operaciones', icon: '../../../../assets/icons/operaciones.svg', url: '/operations', enabled: this.permisos.user_data.opcion02, disabled: false },
      { name: 'Cobros', icon: '../../../../assets/icons/cobros.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion03, disabled: true },
      { name: 'Trámites', icon: '../../../../assets/icons/tramites.svg', url: '/procedures', enabled: this.permisos.user_data.opcion04, disabled: false },
      { name: 'Almacén', icon: '../../../../assets/icons/almacen.svg', url: '/warehouse', enabled: this.permisos.user_data.opcion05, disabled: false },
      { name: 'Sucursal', icon: '../../../../assets/icons/taller.svg', url: '/workshop', enabled: this.permisos.user_data.opcion06, disabled: false },
      { name: 'Chapistería', icon: '../../../../assets/icons/chapisteria.svg', url: '/sheet-metal-work', enabled: this.permisos.user_data.opcion07, disabled: false },
      { name: 'Llavero', icon: '../../../../assets/icons/llavero.svg', url: '/keychain', enabled: this.permisos.user_data.opcion08, disabled: false },
      { name: 'Reclamos', icon: '../../../../assets/icons/reclamos.svg', url: '/claims', enabled: this.permisos.user_data.opcion09, disabled: false },
      { name: 'Cartera', icon: '../../../../assets/icons/cartera.svg', url: '/wallet', enabled: this.permisos.user_data.opcion10, disabled: false },
      { name: 'Gerencia', icon: '../../../../assets/icons/gerencia.svg', url: '/management', enabled: this.permisos.user_data.opcion11, disabled: false },
      { name: 'Gastos', icon: '../../../../assets/icons/gastos.svg', url: '/expenses', enabled: this.permisos.user_data.opcion12, disabled: false },
      { name: 'CNT', icon: '../../../../assets/icons/cnt.svg', url: '/cnt', enabled: this.permisos.user_data.opcion13, disabled: false },
      { name: 'Contado', icon: '../../../../assets/icons/contado.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion14, disabled: true },
      { name: 'Utilidades', icon: '../../../../assets/icons/utilidades1.svg', url: '/utilities', enabled: this.permisos.user_data.opcion15, disabled: false }
    ];
  }

  changeVideoState() {
    this.changeVideo = !this.changeVideo;
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

  ngAfterViewInit() {
    this.videoPlayer.nativeElement.muted = true;
  }

  onVideoEnded() {
    this.currentVideoIndex = (this.currentVideoIndex + 1) % this.videos.length;
    this.currentVideo = this.videos[this.currentVideoIndex];
    this.videoPlayer.nativeElement.load(); // Cargar el nuevo video
    // this.videoPlayer.nativeElement.muted = true;
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
