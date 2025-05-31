import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { JwtService } from 'src/app/services/jwt.service'; 

@Injectable({
  providedIn: 'root'
})
export class NoAuthGuard implements CanActivate {
  constructor(private jwtService: JwtService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (!this.jwtService.tokenExistsAndValid()) {
      return true;  
    } else {
      this.jwtService.verifyOwner() ? this.router.navigate(['/home/owners']) : this.router.navigate(['/home/users']);
      return false;
    }
  }
}