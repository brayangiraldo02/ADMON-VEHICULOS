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

  permissions: any;
  ownerView: boolean = false;

  constructor(private jwtService: JwtService, private apiService: ApiService, private router: Router) {}

  ngOnInit() {
    this.getUser();
  }

  getInfoCompany(): void {
    const userData = this.jwtService.getUserData();
    const idCompany = userData ? userData.empresa : null;
    this.apiService.getData('info-company/'+idCompany).subscribe(
      (response) => {
        console.log('getInfoCompany: ', response);
      }
    );
  }

  getUser() {
    this.permissions = this.jwtService.getUserData(); // getUserData() ahora es la fuente de verdad.
    // this.imgUser = this.permissions.foto; // Cuando se tengan las rutas de las imágenes
    this.convertBooleanValues(this.permissions);
    // this.getInfoCompany();
    // this.subscribirEventosDeRuta();
    // console.log(this.permissions);
  }

  convertBooleanValues(obj: any) {
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
      this.permissions.opcion16 === true &&
      !this.jwtService.isAdmin()
    ) {
      this.ownerView = true;
    }
  }

  onMenuClick() {
    this.menuClick.emit();
  }

  logout(): void {
    this.jwtService.logout(); 
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
