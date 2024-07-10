// pdf-viewer.component.ts
import { Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-pdf-viewer',
  templateUrl: './pdf-viewer.component.html',
  styleUrls: ['./pdf-viewer.component.css']
})
export class PdfViewerComponent implements OnInit {
  pdfBlobUrl: SafeResourceUrl | null = null;

  constructor(
    private apiService: ApiService,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    const endpoint = localStorage.getItem('pdfEndpoint');
    const dataParam = localStorage.getItem('pdfData') || '0';

    if (endpoint) {
      if (dataParam != '0') {
        let data = {};
        try {
          data = JSON.parse(dataParam);
        } catch (e) {
          console.error('Error parsing data param:', e);
        }
        this.loadPostPdf(endpoint, data);
      } else {
        this.loadGetPdf(endpoint);
      }
    } else {
      console.log('Missing endpoint');
    }
  }

  loadPostPdf(endpoint: string, data: any) {
    this.apiService.postPdf(endpoint, data).subscribe(
      response => {
        // Limpiar LocalStorage
        localStorage.removeItem('pdfEndpoint');
        localStorage.removeItem('pdfData');
        const blob = new Blob([response], { type: 'application/pdf' });
        this.pdfBlobUrl = this.sanitizer.bypassSecurityTrustResourceUrl(URL.createObjectURL(blob));
      },
      error => {
        console.error('Error al cargar el PDF:', error);
      }
    );
  }

  loadGetPdf(endpoint: string) {
    this.apiService.getPdf(endpoint).subscribe(
      response => {
        // Limpiar LocalStorage
        localStorage.removeItem('pdfEndpoint');
        localStorage.removeItem('pdfData');
        const blob = new Blob([response], { type: 'application/pdf' });
        this.pdfBlobUrl = this.sanitizer.bypassSecurityTrustResourceUrl(URL.createObjectURL(blob));
      },
      error => {
        console.error('Error al cargar el PDF:', error);
      }
    );
  }
}
