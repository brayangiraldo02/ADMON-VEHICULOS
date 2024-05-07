import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { ErrorHandlerService } from './error-handler.service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseURL: string = 'http://localhost:8000'; // MOVER A VARIABLES DE ENTORNO

  constructor(private http: HttpClient, private errorHandlerService: ErrorHandlerService) {}

  /**
   * Fetch data from a specified endpoint.
   * @param {string} endpoint - The endpoint to fetch data from.
   * @returns {Observable<any>} An Observable of the HTTP response.
   */
  getData(endpoint: string): Observable<any> {
    return this.http.get<any>(`${this.baseURL}/${endpoint}/`).pipe(
      catchError(this.errorHandlerService.handleError)
    );
  }
}