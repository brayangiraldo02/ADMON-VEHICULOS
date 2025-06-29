// src/app/guards/auth.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';
import { JwtService } from 'src/app/services/jwt.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private jwtService: JwtService, private router: Router) {}

  canActivate(): boolean | UrlTree {
    if (this.jwtService.isAuthenticated()) {
      return true; // Usuario autenticado (cualquier rol), puede pasar al layout principal.
    }

    // Si no está autenticado, lo limpiamos por si hay un token inválido y lo mandamos a login.
    this.jwtService.logout();
    return this.router.createUrlTree(['/login']);
  }
}