import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { ErrorHandlerService } from './error-handler.service';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseURL: string = environment.url;

  constructor(private http: HttpClient, private errorHandlerService: ErrorHandlerService) {}

  /**
   * Fetch data from a specified endpoint.
   * @param {string} endpoint - The endpoint to fetch data from.
   * @returns {Observable<any>} An Observable of the HTTP response.
   */
  getData(endpoint: string): Observable<any> {
    return this.http.get<any>(`${this.baseURL}/${endpoint}/`, { withCredentials: true }).pipe(
      catchError(this.errorHandlerService.handleError)
    );
  }

  /**
   * Fetch data from a specified endpoint.
   * @param {string} endpoint - The endpoint to fetch data from.
   * @returns {Observable<any>} An Observable of the HTTP response.
   */
  getPdf(endpoint: string): Observable<any> {
    return this.http.get<any>(`${this.baseURL}/${endpoint}/`, { responseType: 'blob' as 'json', withCredentials: true }).pipe(
      catchError(this.errorHandlerService.handleError)
    );
  }

  /**
   * Post data to a specified endpoint.
   * @param {string} endpoint - The endpoint to post data to.
   * @param {any} data - The data to post.
   * @returns {Observable<any>} An Observable of the HTTP response.
   */
  postPdf(endpoint: string, data: any): Observable<any> {
    return this.http.post<any>(`${this.baseURL}/${endpoint}/`, data, { responseType: 'blob' as 'json', withCredentials: true }).pipe(
      catchError(this.errorHandlerService.handleError)
    );
  }

  /**
   * Post data to a specified endpoint.
   * @param {string} endpoint - The endpoint to post data to.
   * @param {any} data - The data to post.
   * @returns {Observable<any>} An Observable of the HTTP response.
   */
  postData(endpoint: string, data: any): Observable<any> {
    return this.http.post<any>(`${this.baseURL}/${endpoint}/`, data, { withCredentials: true }).pipe(
      catchError(this.errorHandlerService.handleError)
    );
  }

  /**
   * Update data at a specified endpoint.
   * @param {string} endpoint - The endpoint to put data to.
   * @param {any} data - The data to update.
   * @returns {Observable<any>} An Observable of the HTTP response.
   */
  updateData(endpoint: string, data: any): Observable<any> {
    return this.http.put<any>(`${this.baseURL}/${endpoint}/`, data, { withCredentials: true }).pipe(
      catchError(this.errorHandlerService.handleError)
    );
  }
}