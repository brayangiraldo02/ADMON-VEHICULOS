import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  options = [
    { name: 'Caja', icon: '../../../../assets/icons/10.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'Operaciones', icon: '../../../../assets/icons/8.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'Cobros', icon: '../../../../assets/icons/9.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'Trámites', icon: '../../../../assets/icons/11.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'Almacén', icon: '../../../../assets/icons/12.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'Taller', icon: '../../../../assets/icons/14.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'Chapistería', icon: '../../../../assets/icons/15.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'Llavero', icon: '../../../../assets/icons/17.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'Reclamos', icon: '../../../../assets/icons/19.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'Cartera', icon: '../../../../assets/icons/18.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'Gerencia', icon: '../../../../assets/icons/21.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'Gastos', icon: '../../../../assets/icons/21.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'CNT', icon: '../../../../assets/icons/21.svg', url: 'hoalalalal', enabled: 1 },
    { name: 'Cerrar sesión', icon: '../../../../assets/icons/logout.svg', url: 'hoalalalal', enabled: 1 },
  ];

  images: string[] = [
    '../../../assets/img/taxi1.jpg',
    '../../../assets/img/taxi2.jpg',
    '../../../assets/img/taxi3.jpg'
  ];
  currentImageIndex: number = 0;
  showImage: boolean = true;

  ngOnInit() {
    this.changeImagesPeriodically();
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
