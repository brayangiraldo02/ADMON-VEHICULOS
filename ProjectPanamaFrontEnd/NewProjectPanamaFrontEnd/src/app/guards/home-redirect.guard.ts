import { Injectable } from '@angular/core';
import {
  CanActivate,
  Router,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  UrlTree
} from '@angular/router';
import { JwtService } from 'src/app/services/jwt.service';

@Injectable({ providedIn: 'root' })
export class HomeRedirectGuard implements CanActivate {
  constructor(private jwtService: JwtService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): UrlTree {
    // Decide a dónde redirigir basado en el rol.
    if (this.jwtService.isOwner()) {
      return this.router.createUrlTree(['/home/owners']);
    }
    
    if (this.jwtService.isRegularUser()) {
      return this.router.createUrlTree(['/home/users']);
    }

    // Si llega aquí, no está autenticado de ninguna forma válida.
    this.jwtService.logout();
    return this.router.createUrlTree(['/login']);
  }
}