import { Component, OnInit, AfterViewInit  } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';

import { ApiService } from '../../services/api.service';


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit{

  constructor(
    private _api: ApiService,
    private _auth: AuthService,
  ) { }

  ngOnInit(): void {
    this.test_jwt();
  }

  // ngAfterViewInit(): void {
  //   // Inicializar todos los elementos dropdown
  //   const dropdownElems = document.querySelectorAll('.dropdown-trigger');
  //   M.Dropdown.init(dropdownElems, {});
  // }


  test_jwt() {
    this._api.getTypeRequest('test-jwt').subscribe((res: any) => {
      console.log(res);
    }, err => {
      console.log(err);
    });
  }
}

// export class ProfileComponent {


// //Sidebar toggle show hide function
// status = false;
// addToggle()
// {
//   this.status = !this.status;
// }

// }


// import { Component } from '@angular/core';
// import {
// faPen,
// faPlus,
// faMoneyBill,
// faUsers,
// faClock,
// faBriefcase,
// } from '@fortawesome/free-solid-svg-icons';
// @Component({
// selector: 'app-profile',
// templateUrl: './profile.component.html',
// styleUrls: ['./profile.component.css'],
// })
// export class DashboardComponent {
// edit = faPen;
// create = faPlus;
// budget = faMoneyBill;
// project = faUsers;
// time = faClock;
// work = faBriefcase;
// }
