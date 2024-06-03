import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
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
  @ViewChild('videoPlayer') videoPlayer!: ElementRef<HTMLVideoElement>;

  options: any[] = []

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
  changeVideo: boolean = false;
  permisos: any;

  ngOnInit() {
    this.changeImagesPeriodically();
    this.obtenerUsuario();
    this.currentVideo = this.videos[this.currentVideoIndex];
    this.ngAfterViewInit()
  }

  obtenerUsuario() {
    this.permisos = this.jwtService.decodeToken();
    // console.log(this.permisos.user_data);

    this.convertirValoresBooleanos(this.permisos.user_data);

    this.options = [
      { name: 'Caja', icon: '../../../../assets/icons/caja.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion01 },
      { name: 'Operaciones', icon: '../../../../assets/icons/operaciones.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion02 },
      { name: 'Cobros', icon: '../../../../assets/icons/cobros.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion03 },
      { name: 'Trámites', icon: '../../../../assets/icons/tramites.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion04 },
      { name: 'Almacén', icon: '../../../../assets/icons/almacen.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion05 },
      { name: 'Taller', icon: '../../../../assets/icons/taller.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion06 },
      { name: 'Chapistería', icon: '../../../../assets/icons/chapisteria.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion07 },
      { name: 'Llavero', icon: '../../../../assets/icons/llavero.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion08 },
      { name: 'Reclamos', icon: '../../../../assets/icons/reclamos.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion09 },
      { name: 'Cartera', icon: '../../../../assets/icons/cartera.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion10 },
      { name: 'Gerencia', icon: '../../../../assets/icons/gerencia.svg', url: 'management', enabled: this.permisos.user_data.opcion11 },
      { name: 'Gastos', icon: '../../../../assets/icons/gastos.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion12 },
      { name: 'CNT', icon: '../../../../assets/icons/cnt.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion13 },
      { name: 'Contado', icon: '../../../../assets/icons/contado.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion14 },
      { name: 'Utilidades', icon: '../../../../assets/icons/utilidades1.svg', url: 'hoalalalal', enabled: this.permisos.user_data.opcion15 }
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
    this.videoPlayer.nativeElement.muted = true;
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
