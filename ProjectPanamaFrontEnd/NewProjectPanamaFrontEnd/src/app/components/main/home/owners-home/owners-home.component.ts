import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { JwtService } from 'src/app/services/jwt.service';
import { ApiService } from 'src/app/services/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-owners-home',
  templateUrl: './owners-home.component.html',
  styleUrls: ['./owners-home.component.css']
})
export class OwnersHomeComponent {
  constructor(private jwtService: JwtService, private apiService: ApiService, private router: Router) { }
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
  changeVideo: boolean = false;
  permisos: any;

  ownersFeespaidVisible: boolean = false;

  ngOnInit() {
    this.changeImagesPeriodically();
    this.obtenerUsuario();
    this.currentVideo = this.videos[this.currentVideoIndex];
  }

  obtenerUsuario() {
    this.permisos = this.jwtService.decodeToken();
    // console.log(this.permisos.user_data);

    this.isAdmin = this.jwtService.isAdmin();

    this.convertirValoresBooleanos(this.permisos.user_data);

    this.options = [
      { name: 'Estado de Flota Resumen', url: 'hoalalalal', enabled: this.permisos.user_data.opcion01, disabled: true, click: null },
      { name: 'Estado de Flota Detalle', url: 'hoalalalal', enabled: this.permisos.user_data.opcion01, disabled: true, click: null },
      { name: 'Relación Ingresos', url: 'hoalalalal', enabled: this.permisos.user_data.opcion02, disabled: true, click: null },
      { name: 'Relación Piezas', url: 'hoalalalal', enabled: this.permisos.user_data.opcion03, disabled: true, click: null },
      { name: 'Estado de P y G', url: 'hoalalalal', enabled: this.permisos.user_data.opcion04, disabled: true, click: null },
      { name: 'Cuotas Pagas por Conductor', url: 'hoalalalal', enabled: this.permisos.user_data.opcion05, disabled: false, click: () => this.showModalOwnersFeespaid()}
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

  showModalOwnersFeespaid() {
    this.ownersFeespaidVisible = !this.ownersFeespaidVisible;
    document.documentElement.style.overflow = 'hidden';
    document.body.style.overflow = 'hidden';
  }

  hideModal() {
    this.ownersFeespaidVisible = !this.ownersFeespaidVisible;
    document.documentElement.style.overflow = '';
    document.body.style.overflow = '';
  }
}
