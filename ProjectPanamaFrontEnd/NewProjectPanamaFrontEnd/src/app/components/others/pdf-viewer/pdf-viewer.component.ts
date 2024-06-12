// pdf-viewer.component.ts
import { Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { JwtService } from 'src/app/services/jwt.service';

@Component({
  selector: 'app-pdf-viewer',
  templateUrl: './pdf-viewer.component.html',
  styleUrls: ['./pdf-viewer.component.css']
})
export class PdfViewerComponent implements OnInit {
  pdfUrl: SafeResourceUrl | null = null;
  user: any;

  constructor(
    private apiService: ApiService,
    private sanitizer: DomSanitizer,
    private route: ActivatedRoute,
    private jwtService: JwtService
  ) {}

  ngOnInit(): void {
    this.obtenerUsuario();
    const pdfUrl = this.route.snapshot.paramMap.get('url');
    if (pdfUrl) {
      this.loadPdf(pdfUrl);
    } else {
      console.log('No pdfUrl');
    }
  }

  obtenerUsuario() {
    this.user = this.jwtService.decodeToken();
    this.user = this.user.user_data.nombre;
    console.log(this.user);
  }

  loadPdf(endpoint: string) {
    this.apiService.getPdf(endpoint).subscribe(response => {
      const blob = new Blob([response], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      this.pdfUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
    });
  }
}
