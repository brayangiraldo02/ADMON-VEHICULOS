import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { JwtService } from 'src/app/services/jwt.service';  // Asegúrate de actualizar esta importación según la ruta real del archivo

@Injectable({
  providedIn: 'root'
})
export class OwnersGuard implements CanActivate {
  constructor(private jwtService: JwtService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (this.jwtService.tokenExistsAndValidForOwner()) {
      return true;
    } else {
      this.jwtService.verifyOwner() ? this.router.navigate(['/login']) : this.router.navigate(['/home/users']);
      return false;
    }
  }
}