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

  tokenExistsAndValidForUsers(): boolean {
    const token = this.getToken();
    if (!token) return false;

    const decoded: any = jwtDecode(token);
    const expiration = decoded.exp; // Tiempo de expiración como Unix timestamp (segundos)
    const now = Date.now() / 1000; // Fecha/hora actual como Unix timestamp (segundos)
    
    // Verificar si el token aún no ha expirado
    return expiration > now && (decoded.user_data.opcion16 !== 'T' || decoded.user_data.nombre === 'Administrador');
  }

  tokenExistsAndValidForOwner(): boolean {
    const token = this.getToken();
    if (!token) return false;

    const decoded: any = jwtDecode(token);
    const expiration = decoded.exp; // Tiempo de expiración como Unix timestamp (segundos)
    const now = Date.now() / 1000; // Fecha/hora actual como Unix timestamp (segundos)

    // Verificar si el token aún no ha expirado y si el usuario es dueño
    return expiration > now && (decoded.user_data.opcion16 === 'T' || decoded.user_data.nombre === 'Administrador');
  }

  verifyOwner(): boolean {
    const token = this.getToken();
    if (!token) return false;

    const decoded: any = jwtDecode(token);

    // Verificar si el usuario es dueño
    return decoded.user_data.opcion16 === 'T' || decoded.user_data.nombre === 'Administrador';
  }

  isAdmin(): boolean {
    const token = this.getToken();
    if (!token) return false;

    const decoded: any = jwtDecode(token);

    // Verificar si el usuario es administrador
    return decoded.user_data.nombre === 'Administrador';
  }

  obtainId(): string {
    const token = this.getToken();
    if (!token) return '';

    const decoded: any = jwtDecode(token);

    // Obtener el ID del usuario
    return decoded.user_data.id;
  }

  decodeToken(): any {
    const token = this.getToken();
    return token ? jwtDecode(token) : null;
  }
}
