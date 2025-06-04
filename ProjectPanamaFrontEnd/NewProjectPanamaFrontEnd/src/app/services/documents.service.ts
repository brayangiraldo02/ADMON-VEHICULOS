import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class DocumentsService {

  constructor(private apiService: ApiService) { }

  /**
   * Download any type of document (PDF, Excel, etc.) from a POST endpoint
   * @param {string} endpoint - The endpoint to download the document from
   * @param {any} data - The data to send in the request body
   * @param {string} filename - Optional filename for the download (will be auto-detected if not provided)
   * @returns {Observable<void>} An Observable that completes when download starts
   */
  downloadDocument(endpoint: string, data: any, filename?: string): Observable<void> {
    return this.apiService.postDocuments(endpoint, data).pipe(
      map((blob: Blob) => {
        // Create blob URL
        const url = window.URL.createObjectURL(blob);
        
        // Create temporary link element
        const link = document.createElement('a');
        link.href = url;
        
        // Set filename
        if (filename) {
          link.download = filename;
        } else {
          // Try to extract filename from blob type or use default
          const fileExtension = this.getFileExtensionFromBlob(blob);
          link.download = `document_${new Date().getTime()}${fileExtension}`;
        }
        
        // Trigger download
        document.body.appendChild(link);
        link.click();
        
        // Cleanup
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      })
    );
  }

  /**
   * Get file extension based on blob MIME type
   * @param {Blob} blob - The blob to analyze
   * @returns {string} File extension with dot
   */
  private getFileExtensionFromBlob(blob: Blob): string {
    const mimeType = blob.type;
    
    switch (mimeType) {
      case 'application/pdf':
        return '.pdf';
      case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return '.xlsx';
      case 'application/vnd.ms-excel':
        return '.xls';
      case 'text/csv':
        return '.csv';
      case 'application/msword':
        return '.doc';
      case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return '.docx';
      default:
        return '.bin'; // Default binary extension
    }
  }
}