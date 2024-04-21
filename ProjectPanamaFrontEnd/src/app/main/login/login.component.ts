// import { Component, OnInit } from '@angular/core';
// import { FormBuilder, FormGroup, Validators } from '@angular/forms';
// import { Router } from '@angular/router';
// import { AuthService } from 'src/app/services/auth.service';

// import { ApiService } from '../../services/api.service';

// @Component({
//   selector: 'app-login',
//   templateUrl: './login.component.html',
//   styleUrls: ['./login.component.css']
// })
// export class LoginComponent implements OnInit {
//   form!: FormGroup
//   constructor(
//     private _api: ApiService,
//     private _auth: AuthService,
//     private router: Router,
//     public fb: FormBuilder
//   ) { }

//   ngOnInit(): void {
//     this.form = this.fb.group({
//       username: ['', Validators.required],
//       password: ['', Validators.required]
//     });

//   }

//   login() {
//     let b = this.form.value
//     console.log(b)
//     this._api.postTypeRequest('login', b).subscribe((res: any) => {
//       console.log(res)
//       if (res.access_token) {

//         this._auth.setDataInLocalStorage('token', res.access_token)
//         this.router.navigate(['profile'])
//       }
//     }, err => {
//       console.log(err)
//     });
//   }

// }

// import { Component, OnInit } from '@angular/core';
// import { FormBuilder, FormGroup, Validators } from '@angular/forms';
// import { Router } from '@angular/router';
// import { AuthService } from 'src/app/services/auth.service';
// import { ApiService } from '../../services/api.service';
// import { catchError } from 'rxjs/operators';
// import { of } from 'rxjs';

// @Component({
//   selector: 'app-login',
//   templateUrl: './login.component.html',
//   styleUrls: ['./login.component.css']
// })
// export class LoginComponent implements OnInit {
//   form!: FormGroup;


//   constructor(
//     private _api: ApiService,
//     private _auth: AuthService,
//     private router: Router,
//     public fb: FormBuilder
//   ) { }

//   ngOnInit(): void {
//     this.form = this.fb.group({
//       username: ['', Validators.required],
//       password: ['', Validators.required]
//     });
//   }

//   login() {
//     let b = this.form.value;
//     console.log(b);
//     this._api.postTypeRequest('login', b)
//       .pipe(
//         catchError(error => {
//           // Manejar el error aquí, por ejemplo, imprimirlo en la consola
//           console.error('Error en la solicitud:', error);

//           //alert('¡Credenciales erróneas, inténtalo de nuevo!');
//           // Retornar un observable vacío para evitar que se propague el error
//           return of(null);
//         })
//       )
//       .subscribe((res: any) => {
//         if (res && res.access_token) {
//           this._auth.setDataInLocalStorage('token', res.access_token);
//           this.router.navigate(['profile']);
//         }
//       });
//   }
// }

import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { ApiService } from '../../services/api.service';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  form!: FormGroup;
  showAlert: boolean = false; // Variable para controlar la visibilidad de la alerta
  showPassword: boolean = false;
  constructor(
    private _api: ApiService,
    private _auth: AuthService,
    private router: Router,
    public fb: FormBuilder
  ) { }

  ngOnInit(): void {
    this.form = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  login() {
    let b = this.form.value;
    console.log(b);
    this._api.postTypeRequest('login', b)
      .pipe(
        catchError(error => {
          // Manejar el error aquí, por ejemplo, imprimirlo en la consola
          console.error('Error en la solicitud:', error);

          // Mostrar alerta de credenciales incorrectas
          this.showAlert = true;

          // Establecer un temporizador para ocultar la alerta después de 5 segundos
          setTimeout(() => {
            this.showAlert = false;
            this.form.controls['username'].setValue('');
            this.form.controls['password'].setValue('');
          }, 3000);

          // Retornar un observable vacío para evitar que se propague el error
          return of(null);
        })
      )
      .subscribe((res: any) => {
        if (res && res.access_token) {
          this._auth.setDataInLocalStorage('token', res.access_token);
          this.router.navigate(['profile']);
        }
      });
  }
  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }
}
