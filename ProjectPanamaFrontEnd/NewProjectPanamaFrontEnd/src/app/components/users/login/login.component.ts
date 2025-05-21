import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';
import { InfoCompanyStateService } from 'src/app/states/info-company-state.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  eyeIconPath: string = '../../../../assets/icons/eye.svg';
  eyeIconVisiblePath: string = '../../../../assets/icons/no-eye.svg';
  showPassword: boolean = false;
  showUser: boolean = false;
  eyeIconUsername: string = this.eyeIconPath;
  eyeIconPassword: string = this.eyeIconPath;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private jwtService: JwtService,
    private router: Router,
    private stateInfoCompany: InfoCompanyStateService
  ) {
    this.loginForm = this.fb.group({
      user: ['', [Validators.required, Validators.minLength(6), Validators.maxLength(10)]],
      password: ['', [Validators.required, Validators.minLength(4), Validators.maxLength(10)]]
    });
  }

  ngOnInit(): void {}

  onSubmit(): void {
    if (this.loginForm.valid) {
      const userLogin = this.loginForm.value;

      this.apiService.postData('login', userLogin).subscribe(
        (response) => {
          this.jwtService.setToken(response.token);
          this.getInfoCompany();
          this.jwtService.isAdmin() ? this.router.navigate(['/users-home']) : (this.jwtService.verifyOwner() ? this.router.navigate(['/owners-home']) : this.router.navigate(['/users-home']));
        },
        (error) => {
          if (error.status === 404) {
            window.alert("Usuario o contraseña incorrectos.");
          } else {
            window.alert("Ha ocurrido un error inesperado, por favor intenta de nuevo.");
          }
          console.log(error);
        }
      );
    } else {
      this.loginForm.markAllAsTouched();
    }
  }

  togglePasswordVisibility(option: string): void {
    if(option === 'password') {
      this.showPassword = !this.showPassword;
      this.eyeIconPassword = this.showPassword ? this.eyeIconVisiblePath : this.eyeIconPath;
      const input = document.getElementById(option) as HTMLInputElement;
      input.type = this.showPassword ? 'text' : 'password';
    }
    else if(option === 'user') {
      this.showUser = !this.showUser;
      this.eyeIconUsername = this.showUser ? this.eyeIconVisiblePath : this.eyeIconPath;
      const input = document.getElementById(option) as HTMLInputElement;
      input.type = this.showUser ? 'text' : 'password';
    }
  }

  getInfoCompany(): void {
    const idCompany = this.jwtService.getIdCompany();
    this.apiService.getData('info-company/'+idCompany).subscribe(
      (response) => {
        this.stateInfoCompany.setInfoCompany(response);
      }
    );
  }
}
