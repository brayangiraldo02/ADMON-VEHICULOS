import { Injectable } from '@angular/core';
import { jwtDecode, JwtPayload } from 'jwt-decode';

// Definimos una interfaz para la estructura de nuestro payload personalizado
interface AppJwtPayload extends JwtPayload {
  user_data: {
    id: string;
    nombre: string;
    empresa: string;
    foto: string;
    opcion01: string;
    opcion02: string;
    opcion03: string;
    opcion04: string;
    opcion05: string;
    opcion06: string;
    opcion07: string;
    opcion08: string;
    opcion09: string;
    opcion10: string;
    opcion11: string;
    opcion12: string;
    opcion13: string;
    opcion14: string;
    opcion15: string;
    opcion16: string;
    tarea01: string;
    tarea02: string;
    tarea03: string;
    tarea04: string;
    tarea05: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class JwtService {

  private readonly TOKEN_KEY = 'info_token';
  private decodedToken: AppJwtPayload | null = null;

  constructor() {
    // Al iniciar el servicio, intentamos decodificar el token existente
    this.decodeAndValidateToken();
  }

  // --- Métodos Públicos Principales ---

  setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
    this.decodeAndValidateToken(); // Actualizamos el token decodificado en memoria
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    this.decodedToken = null; // Limpiamos el token de la memoria
  }

  isAuthenticated(): boolean {
    // La autenticación depende de si tenemos un token válido en memoria
    return this.decodedToken !== null;
  }

  isOwner(): boolean {
    if (!this.isAuthenticated()) return false;
    const userData = this.decodedToken!.user_data;
    // La lógica para ser "Owner" está centralizada aquí
    return userData.opcion16 === 'T' || userData.nombre === 'Administrador';
  }

  isRegularUser(): boolean {
    // Un "usuario regular" es alguien autenticado pero que no es "Owner"
    return this.isAuthenticated() && !this.isOwner();
  }

  isAdmin(): boolean {
    if (!this.isAuthenticated()) return false;
    return this.decodedToken!.user_data.nombre === 'Administrador';
  }

  getUserData() {
    return this.isAuthenticated() ? this.decodedToken!.user_data : null;
  }

  // --- Métodos Privados de Ayuda ---

  private getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  private decodeAndValidateToken(): void {
    const token = this.getToken();
    if (!token) {
      this.decodedToken = null;
      return;
    }

    try {
      const decoded: AppJwtPayload = jwtDecode(token);
      const isExpired = decoded.exp! * 1000 < Date.now(); // se multiplica por 1000 para comparar milisegundos

      if (isExpired) {
        this.decodedToken = null;
        // Opcional: Proactivamente borramos el token expirado
        // localStorage.removeItem(this.TOKEN_KEY); 
      } else {
        this.decodedToken = decoded;
      }
    } catch (error) {
      console.error("Error al decodificar el token, es posible que esté malformado.", error);
      this.decodedToken = null;
    }
  }
}