import { Injectable } from '@angular/core';
import {
  CanActivate,
  Router,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  UrlTree
} from '@angular/router';
import { JwtService } from 'src/app/services/jwt.service';

@Injectable({
  providedIn: 'root'
})
export class HomeRedirectGuard implements CanActivate {
  constructor(
    private jwtService: JwtService,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot, // Esta es la ruta '' del HomeModule
    state: RouterStateSnapshot
  ): boolean | UrlTree {
    // Primero, verificar si el usuario califica como "owner"
    // Usamos la misma lógica que OwnersGuard para la decisión principal
    if (this.jwtService.tokenExistsAndValidForOwner()) {
      // Redirigir a la sub-ruta 'owners' del HomeModule.
      // Dado que HomeModule se carga bajo una ruta (ej. '/home'),
      // usamos state.url para construir la ruta correcta (ej. '/home/owners').
      return this.router.createUrlTree([state.url, 'owners']);
    }

    // Si no es owner, verificar si califica como "user" general
    // Usamos la misma lógica que AuthGuard para la decisión principal
    if (this.jwtService.tokenExistsAndValidForUsers()) {
      // Redirigir a la sub-ruta 'users' del HomeModule.
      // Esto redirigirá a, por ejemplo, '/home/users'.
      return this.router.createUrlTree([state.url, 'users']);
    }

    // Si no califica para ninguna de las anteriores (no es owner ni user autenticado
    // según las lógicas de sus respectivas guardas), redirigir a la página de login.
    // La ruta '/login' es una ruta raíz definida en AppRoutingModule.
    return this.router.createUrlTree(['/login']);
  }
}