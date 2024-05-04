import { Component } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  eyeIconPath: string = '../../../../assets/icons/eye.svg'; // Ruta local del icono
  eyeIconVisiblePath: string = '../../../../assets/icons/no-eye.svg'; // Ruta local del icono cuando la contraseña está visible
  showPassword: boolean = false;
  eyeIcon: string = this.eyeIconPath;

  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
    const passwordInput = document.getElementById('password') as HTMLInputElement;
    passwordInput.type = this.showPassword ? 'text' : 'password';
    this.eyeIcon = this.showPassword ? this.eyeIconVisiblePath : this.eyeIconPath;
  }
}
