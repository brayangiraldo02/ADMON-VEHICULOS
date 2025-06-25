import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree } from '@angular/router';
import { JwtService } from 'src/app/services/jwt.service'; 

@Injectable({ providedIn: 'root' })
export class NoAuthGuard implements CanActivate {
  constructor(private jwtService: JwtService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean | UrlTree {
    if (!this.jwtService.isAuthenticated()) {
      return true; // No está autenticado, puede ver el login.
    } else {
      // Está autenticado, no debe ver el login. Lo mandamos a su home correspondiente.
      const targetUrl = this.jwtService.isOwner() ? '/home/owners' : '/home/users';
      return this.router.createUrlTree([targetUrl]);
    }
  }
}