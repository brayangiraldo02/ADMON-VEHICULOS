import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { JwtService } from 'src/app/services/jwt.service';  // Asegúrate de actualizar esta importación según la ruta real del archivo

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private jwtService: JwtService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (this.jwtService.tokenExistsAndValidForUsers()) {
      return true;
    } else {
      this.jwtService.verifyOwner() ? this.router.navigate(['/home/owners']) : this.router.navigate(['/login']);
      return false;
    }
  }
}