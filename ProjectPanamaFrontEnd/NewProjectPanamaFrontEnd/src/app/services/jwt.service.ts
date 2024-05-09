import { Injectable } from '@angular/core';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})

export class JwtService {

  private readonly TOKEN_KEY = 'info_token';

  constructor() { }

  setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  removeToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  tokenExistsAndValid(): boolean {
    const token = this.getToken();
    if (!token) return false;

    const decoded: any = jwtDecode(token);
    const expiration = decoded.exp; // Tiempo de expiración como Unix timestamp (segundos)
    const now = Date.now() / 1000; // Fecha/hora actual como Unix timestamp (segundos)
    
    // Verificar si el token aún no ha expirado
    return expiration > now;
  }

  decodeToken(): any {
    const token = this.getToken();
    return token ? jwtDecode(token) : null;
  }
}
