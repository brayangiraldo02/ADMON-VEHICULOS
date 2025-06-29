// src/app/guards/owners.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';
import { JwtService } from 'src/app/services/jwt.service';

@Injectable({
  providedIn: 'root'
})
export class OwnersGuard implements CanActivate {
  constructor(private jwtService: JwtService, private router: Router) {}

  canActivate(): boolean | UrlTree {
    if (this.jwtService.isOwner()) {
      return true; // Es un owner, puede ver esta página.
    }
    
    // Si no es un owner, lo redirigimos a la página principal de usuarios (o a donde decidas).
    // No lo mandamos a login porque YA sabemos que está autenticado gracias al AuthGuard.
    return this.router.createUrlTree(['/home/users']); 
  }
}