import { Component } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {

  isNavbarOpen: boolean = false;
  isProfileDropdownOpen: boolean = false;
  username: string = "Usuario"; // Aquí asigna el nombre del usuario dinámicamente

  logoUrl: string | null = 'https://media.licdn.com/dms/image/C4E0BAQFN9RPjAJAIdA/company-logo_200_200/0/1631324563752?e=2147483647&v=beta&t=wArf89ExUKjZh0xk-BOPfnLhlvSw5F-fHyf4wC8uK4Y';

  toggleNavbar(): void {
    this.isNavbarOpen = !this.isNavbarOpen;
  }

  toggleProfileDropdown(): void {
    this.isProfileDropdownOpen = !this.isProfileDropdownOpen;
  }

  logout(): void {
    // Aquí iría la lógica para cerrar sesión
  }
}
