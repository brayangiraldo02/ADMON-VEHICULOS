// src/app/guards/users.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';
import { JwtService } from 'src/app/services/jwt.service';

@Injectable({
  providedIn: 'root'
})
export class UsersGuard implements CanActivate {
  constructor(private jwtService: JwtService, private router: Router) {}

  canActivate(): boolean | UrlTree {
    // Usamos el método que creamos para verificar si es un usuario regular
    if (this.jwtService.isRegularUser()) {
      return true; // Es un usuario regular, puede ver esta página.
    }

    // Si no es un usuario regular, debe ser un owner. Lo mandamos a su página.
    return this.router.createUrlTree(['/home/owners']);
  }
}