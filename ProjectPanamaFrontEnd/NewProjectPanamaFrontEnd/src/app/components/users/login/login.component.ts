import { Component } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  constructor(private apiService: ApiService, private jwtService: JwtService) {}
  user: string = "";     
  password: string = "";
  eyeIconPath: string = '../../../../assets/icons/eye.svg'; // Ruta local del icono
  eyeIconVisiblePath: string = '../../../../assets/icons/no-eye.svg'; // Ruta local del icono cuando la contraseña está visible
  showPassword: boolean = false;
  eyeIcon: string = this.eyeIconPath;

  onSubmit(form: any) {
    const userLogin = {
      user: this.user,
      password: this.password
    };

    this.apiService.postData('login', userLogin).subscribe(
      (response) => {
        this.jwtService.setToken(response.token);
      },
      (error) => {
        console.log(error);
      }
    );

  }

  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
    const passwordInput = document.getElementById('password') as HTMLInputElement;
    passwordInput.type = this.showPassword ? 'text' : 'password';
    this.eyeIcon = this.showPassword ? this.eyeIconVisiblePath : this.eyeIconPath;
  }
}
