import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';
import { OwnersGuard } from 'src/app/guards/owners.guard';
import { MatDialog } from '@angular/material/dialog';
import { InfoCompanyComponent } from '../info-company/info-company.component';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { OptionsDocumentsDialogComponent } from 'src/app/modules/tasks/documents/options-documents-dialog/options-documents-dialog.component';

@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrls: ['./sidenav.component.css']
})
export class SidenavComponent implements OnInit {
  @Input() isOpen = false;
  @Output() backdropClick = new EventEmitter<void>();
  @Output() itemClick = new EventEmitter<void>();

  permisos: any;
  imgUser: string = '../../../../../assets/img/taxi.jpg';
  ownerView: boolean = false;
  menuItems: any[] = [];
  infoCompanyName: string = '';

  constructor(
    private apiService: ApiService,
    private jwtService: JwtService,
    private router: Router,
    private ownersGuard: OwnersGuard,
    private dialog: MatDialog,
    private breakpointObserver: BreakpointObserver
  ) {}

  ngOnInit() {
    this.obtenerUsuario();
  }

  obtenerUsuario() {
    this.permisos = this.jwtService.getUserData();
    // this.imgUser = this.permisos.foto; // Cuando se tengan las rutas de las imágenes
    this.convertirValoresBooleanos(this.permisos);
    this.getInfoCompany();
    // this.subscribirEventosDeRuta();
    // console.log(this.permisos);
  }

  logout(): void {
    this.jwtService.logout(); 
    this.apiService.postData('logout', {}).subscribe(
      (response) => {
        this.onItemClick();
        this.router.navigate(['/login']);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  initMenuItems() {
    this.menuItems = [
      {
        icon: 'apartment', 
        label: 'Propietarios', 
        route: '/owners',
        conditions: this.permisos.tarea01
      },
      {
        icon: 'badge', 
        label: 'Conductores', 
        route: '/drivers',
        conditions: this.permisos.tarea02
      },
      {
        icon: 'local_taxi', 
        label: 'Vehículos', 
        route: '/vehicles',
        conditions: this.permisos.tarea03
      },
      {
        icon: 'garage', 
        label: 'Estado de Flota', 
        route: '/statevehiclefleet',
        conditions: this.permisos.tarea04
      },
      {
        icon: 'payments', 
        label: 'Cuotas Pagas', 
        route: '/feespaid',
        conditions: this.permisos.tarea05
      },
      {
        icon: 'card_travel',
        label: 'Inspecciones',
        route: '/inspections',
        conditions: this.permisos.opcion17
      },
      {
        icon: 'insert_drive_file',
        label: 'Documentos',
        action: () => this.openDialogDocuments(),
        conditions: true
      }
    ];
  }

  getInfoCompany(): void {
    const userData = this.jwtService.getUserData();
    const idCompany = userData ? userData.empresa : null;
    this.apiService.getData('info-company/'+idCompany).subscribe(
      (response) => {
        console.log('getInfoCompany: ', response);
        this.infoCompanyName = response.name;
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

    if (
      this.permisos.opcion16 === true &&
      !this.jwtService.isAdmin()
    ) {
      this.ownerView = true;
    }

    this.initMenuItems();
  }

  onBackdropClick(): void {
    this.backdropClick.emit();
  }

  openDialogDocuments(): void {
    const isSmallScreen = this.breakpointObserver.isMatched(Breakpoints.XSmall);
    const dialogWidth = isSmallScreen ? '90vw' : '60%';

    const dialogRef = this.dialog.open(OptionsDocumentsDialogComponent,
      {
        width: dialogWidth,
      }
    );
  }

  openDialogInfoCompany(): void {
    const isSmallScreen = this.breakpointObserver.isMatched(Breakpoints.XSmall);
    const dialogWidth = isSmallScreen ? '90vw' : '60%';

    console.log(isSmallScreen ? 'Pantalla pequeña' : 'Pantalla grande');

    const dialogRef = this.dialog.open(InfoCompanyComponent,
      {
        width: dialogWidth,
      }
    );
  }

  onItemClick(): void {
    this.itemClick.emit();
  }
}
