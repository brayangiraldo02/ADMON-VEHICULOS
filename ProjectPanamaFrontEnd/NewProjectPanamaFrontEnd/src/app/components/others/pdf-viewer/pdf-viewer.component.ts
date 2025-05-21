import { Component, OnInit, ElementRef, ViewChild, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ApiService } from 'src/app/services/api.service';
import * as pdfjsLib from 'pdfjs-dist'; // Importar pdfjs-dist

@Component({
  selector: 'app-pdf-viewer',
  templateUrl: './pdf-viewer.component.html',
  styleUrls: ['./pdf-viewer.component.css']
})
export class PdfViewerComponent implements OnInit, OnDestroy {
  @ViewChild('pdfPagesContainer', { static: false }) pdfPagesContainer!: ElementRef<HTMLDivElement>;

  isLoading: boolean = true;
  pdfLoadError: string | null = null;
  private pdfDocument: pdfjsLib.PDFDocumentProxy | null = null;
  private activeBlobUrls: string[] = [];

  isDesktop: boolean = false;
  isIOS: boolean = false;
  isAndroid: boolean = false;
  safePdfUrl: SafeResourceUrl | null = null;
  pdfBlob: Blob | null = null; // Para almacenar el Blob original del PDF

  constructor(
    private apiService: ApiService,
    private cdr: ChangeDetectorRef,
    private sanitizer: DomSanitizer
  ) {
    console.log('PdfViewerComponent constructor: Setting workerSrc');
    // Asegúrate que la ruta coincida con tu configuración en angular.json
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'assets/pdfjs-worker/pdf.worker.min.js';
  }

  ngOnInit(): void {
    const userAgent = navigator.userAgent;
    this.isDesktop = !/Mobi|Android|iPhone|iPad|iPod/i.test(userAgent);
    this.isIOS = /iPhone|iPad|iPod/i.test(userAgent);
    this.isAndroid = /Android/i.test(userAgent);

    console.log(`PdfViewerComponent ngOnInit: Starting PDF load process. Is Desktop: ${this.isDesktop}, Is iOS: ${this.isIOS}, Is Android: ${this.isAndroid}`);

    // Lógica para iPad que se identifica como Mac (se maneja en loadPdf si isDesktop es true)
    const isMacintosh = /Macintosh/i.test(userAgent);
    const hasTouch = 'ontouchend' in document || navigator.maxTouchPoints > 0;
    if (isMacintosh && hasTouch && this.isDesktop) {
      console.log('ngOnInit: Detected iPad masquerading as Mac. Will be handled by desktop logic + auto-download.');
      // No necesitamos cambiar isIOS o isAndroid aquí, ya que isDesktop será true.
    }

    this.isLoading = true;
    this.pdfLoadError = null;
    this.pdfBlob = null;
    const endpoint = localStorage.getItem('pdfEndpoint');
    const dataParam = localStorage.getItem('pdfData') || '0';
    console.log(`ngOnInit: Endpoint: ${endpoint}, DataParam: ${dataParam}`);

    if (endpoint) {
      if (dataParam !== '0') {
        let data = {};
        try {
          data = JSON.parse(dataParam);
        } catch (e) {
          this.pdfLoadError = 'Error: Invalid PDF parameters.';
          this.isLoading = false;
          this.cleanupLocalStorage();
          this.cdr.detectChanges();
          return;
        }
        this.loadPdf(endpoint, data);
      } else {
        this.loadPdf(endpoint);
      }
    } else {
      this.pdfLoadError = 'Error: PDF endpoint not found.';
      this.isLoading = false;
      this.cleanupLocalStorage();
      this.cdr.detectChanges();
    }
  }

  private loadPdf(endpoint: string, data?: any): void {
    console.log(`loadPdf: Attempting to load PDF from endpoint: ${endpoint}`, data ? 'with POST data' : 'with GET request');
    const observable = data
      ? this.apiService.postPdf(endpoint, data)
      : this.apiService.getPdf(endpoint);

    observable.subscribe(
      async (responseBlob: Blob) => {
        console.log('loadPdf success: Received responseBlob', responseBlob);
        if (!responseBlob || responseBlob.size === 0) {
          this.pdfLoadError = 'Error: Received empty PDF data from server.';
          this.isLoading = false;
          this.cleanupLocalStorage();
          this.cdr.detectChanges();
          return;
        }
        this.cleanupLocalStorage();
        this.pdfBlob = responseBlob; // Guardar el Blob original

        if (this.isDesktop) {
          console.log('loadPdf: Desktop detected. Creating blob URL for iframe.');
          const blobUrl = URL.createObjectURL(this.pdfBlob);
          this.activeBlobUrls.push(blobUrl);
          this.safePdfUrl = this.sanitizer.bypassSecurityTrustResourceUrl(blobUrl);
          this.isLoading = false;
          this.pdfLoadError = null;
          this.cdr.detectChanges();

          // Nueva lógica: si es un Mac (que podría ser un iPad), también descargar.
          const isMacintosh = /Macintosh/i.test(navigator.userAgent);
          if (isMacintosh) {
            console.log('loadPdf: Macintosh detected (could be iPad). Triggering download as well.');
            // Pequeña demora para asegurar que el iframe comience a cargar antes de la descarga
            setTimeout(() => {
              if (this.pdfBlob) { // Re-verificar por si acaso
                 this.downloadPdf();
              }
            }, 500); // 500ms de demora, ajustar si es necesario
          }
        } else { // No es Desktop, entonces es Móvil
          if (this.isIOS) {
            // Para iOS (iPhone/iPad no Mac): Intentar descarga/apertura directa
            console.log('loadPdf: iOS Mobile detected. Triggering direct OS handling.');
            this.isLoading = false; // Indicar que la carga de datos ha terminado
            this.pdfLoadError = null;
            this.cdr.detectChanges(); // Actualizar UI antes de la acción
            this.downloadPdf(); // iOS maneja esto para "Abrir con..." o descargar
          } else if (this.isAndroid) {
            // Para Android: Renderizar con PDF.js en canvas
            console.log('loadPdf: Android Mobile detected. Processing with PDF.js.');
            try {
              const arrayBuffer = await this.pdfBlob.arrayBuffer();
              if (arrayBuffer.byteLength === 0) {
                this.pdfLoadError = 'Error: PDF data is empty after conversion for Android.';
                this.isLoading = false;
                this.cdr.detectChanges();
                return;
              }
              this.pdfDocument = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
              if (this.pdfDocument) {
                this.isLoading = false;
                this.pdfLoadError = null;
                this.cdr.detectChanges(); // Actualizar UI para que #pdfPagesContainer aparezca

                Promise.resolve().then(() => { // Esperar a que el DOM se actualice
                  if (this.pdfPagesContainer && this.pdfPagesContainer.nativeElement) {
                    console.log('loadPdf Android: pdfPagesContainer is now available. Calling renderAllPages.');
                    this.renderAllPages();
                  } else {
                    console.error('loadPdf Android: pdfPagesContainer still not available after DOM update.');
                    this.pdfLoadError = 'Error: PDF display area could not be initialized for Android.';
                    this.cdr.detectChanges();
                  }
                });
              } else {
                this.pdfLoadError = 'Error: Failed to parse PDF document structure for Android.';
                this.isLoading = false;
                this.cdr.detectChanges();
              }
            } catch (error) {
              console.error('loadPdf Android: Error loading or rendering PDF with PDF.js:', error);
              this.pdfLoadError = 'Error: Could not load or render PDF for Android.';
              this.isLoading = false;
              this.cdr.detectChanges();
            }
          } else {
            // Fallback para otros móviles no identificados específicamente (raro)
            // Renderizar en canvas como un default seguro.
            console.log('loadPdf: Other Mobile detected. Defaulting to PDF.js rendering.');
            try {
              const arrayBuffer = await this.pdfBlob.arrayBuffer();
              if (arrayBuffer.byteLength === 0) {
                this.pdfLoadError = 'Error: PDF data is empty after conversion for Other Mobile.';
                this.isLoading = false;
                this.cdr.detectChanges();
                return;
              }
              this.pdfDocument = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
              if (this.pdfDocument) {
                this.isLoading = false;
                this.pdfLoadError = null;
                this.cdr.detectChanges();
                Promise.resolve().then(() => {
                  if (this.pdfPagesContainer && this.pdfPagesContainer.nativeElement) {
                    this.renderAllPages();
                  } else {
                    this.pdfLoadError = 'Error: PDF display area not ready for Other Mobile.';
                    this.cdr.detectChanges();
                  }
                });
              } else {
                this.pdfLoadError = 'Error: Failed to parse PDF document structure for Other Mobile.';
                this.isLoading = false;
                this.cdr.detectChanges();
              }
            } catch (error) {
              console.error('loadPdf Other Mobile: Error loading or rendering PDF with PDF.js:', error);
              this.pdfLoadError = 'Error: Could not load or render PDF for Other Mobile.';
              this.isLoading = false;
              this.cdr.detectChanges();
            }
          }
        }
      },
      (error) => {
        console.error('loadPdf error: Error fetching PDF from API:', error);
        this.pdfLoadError = 'Error: Could not fetch PDF from server.';
        this.isLoading = false;
        this.cleanupLocalStorage();
        this.cdr.detectChanges();
      }
    );
  }

  // Método para renderizar todas las páginas en canvas (para móviles)
  private async renderAllPages(): Promise<void> {
    console.log('renderAllPages (mobile): Starting page rendering process.');
    if (this.isDesktop || !this.pdfDocument) {
      console.log('renderAllPages (mobile): Skipped (desktop or no document).');
      return;
    }
    if (!this.pdfPagesContainer || !this.pdfPagesContainer.nativeElement) {
      this.pdfLoadError = 'Error: PDF display area not ready for mobile.';
      // isLoading ya debería ser false
      this.cdr.detectChanges();
      return;
    }

    const container = this.pdfPagesContainer.nativeElement;
    container.innerHTML = ''; // Limpiar páginas previas
    const containerWidth = container.clientWidth;
    console.log(`renderAllPages (mobile): Container width: ${containerWidth}px`);

    const numPages = this.pdfDocument.numPages;
    console.log(`renderAllPages (mobile): Document has ${numPages} pages.`);
    if (numPages === 0) {
      this.pdfLoadError = 'Info: The PDF document has no pages.';
      this.cdr.detectChanges();
      return;
    }

    for (let pageNum = 1; pageNum <= numPages; pageNum++) {
      console.log(`renderAllPages (mobile): Attempting to render page ${pageNum}.`);
      try {
        const page = await this.pdfDocument.getPage(pageNum);
        const originalViewport = page.getViewport({ scale: 1 });
        const scale = containerWidth / originalViewport.width;
        const viewport = page.getViewport({ scale: scale });

        const canvas = document.createElement('canvas');
        canvas.className = 'pdf-page-canvas';
        const context = canvas.getContext('2d');

        if (!context) {
          throw new Error('Could not get canvas context for page ' + pageNum);
        }

        const outputScale = window.devicePixelRatio || 1;
        canvas.width = Math.floor(viewport.width * outputScale);
        canvas.height = Math.floor(viewport.height * outputScale);
        canvas.style.width = Math.floor(viewport.width) + "px";
        canvas.style.height = Math.floor(viewport.height) + "px";

        const transform = outputScale !== 1 ? [outputScale, 0, 0, outputScale, 0, 0] : undefined;

        const renderContext = { canvasContext: context, viewport: viewport, transform: transform };
        await page.render(renderContext).promise;
        container.appendChild(canvas);
        console.log(`renderAllPages (mobile): Appended canvas for page ${pageNum}.`);
      } catch (pageError) {
        console.error(`renderAllPages (mobile): Error rendering page ${pageNum}:`, pageError);
        this.pdfLoadError = `Error rendering page ${pageNum}.`;
        this.cdr.detectChanges();
      }
    }
    console.log('renderAllPages (mobile): Finished rendering all pages.');
    this.cdr.detectChanges(); // Asegurar que la UI se actualice
  }

  // Método para el botón de descarga
  downloadPdf(): void {
    if (this.pdfBlob) {
      const url = URL.createObjectURL(this.pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      const endpointForName = localStorage.getItem('pdfEndpoint') || 'documento';
      const fileNameBase = endpointForName.split('/').pop()?.split('?')[0].replace(/[^a-z0-9]/gi, '_') || 'documento';
      a.download = `${fileNameBase}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      console.log('downloadPdf: PDF download initiated.');
    } else {
      console.error('downloadPdf: pdfBlob is null, cannot download.');
      this.pdfLoadError = 'Error: No hay PDF para descargar.';
      this.cdr.detectChanges();
    }
  }

  /*
  // MÉTODO DE DESCARGA/APERTURA AUTOMÁTICA (AHORA COMENTADO/DESACTIVADO)
  private triggerMobilePdfHandling(blobUrl: string): void {
    console.log('triggerMobilePdfHandling: Mobile detected. Triggering PDF handling via anchor.');
    const a = document.createElement('a');
    a.href = blobUrl;
    const endpointForName = localStorage.getItem('pdfEndpoint') || 'documento';
    const fileNameBase = endpointForName.split('/').pop()?.split('?')[0].replace(/[^a-z0-9]/gi, '_') || 'documento';
    a.download = `${fileNameBase}.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    console.log('triggerMobilePdfHandling: Mobile - PDF handling initiated via anchor click.');
  }
  */

  private cleanupLocalStorage(): void {
    console.log('cleanupLocalStorage: Removing PDF endpoint and data from localStorage.');
    localStorage.removeItem('pdfEndpoint');
    localStorage.removeItem('pdfData');
  }

  private revokeActiveBlobUrls(): void {
    if (this.activeBlobUrls.length > 0) {
      console.log('revokeActiveBlobUrls: Revoking active blob URLs.', this.activeBlobUrls);
      this.activeBlobUrls.forEach(url => URL.revokeObjectURL(url));
      this.activeBlobUrls = [];
    }
  }

  ngOnDestroy(): void {
    console.log('PdfViewerComponent ngOnDestroy: Cleaning up.');
    this.cleanupLocalStorage();
    this.revokeActiveBlobUrls();
    if (this.pdfDocument) {
      this.pdfDocument.destroy().catch(err => console.error("ngOnDestroy: Error destroying PDF document", err));
      this.pdfDocument = null;
    }
    if (this.pdfBlob) {
        this.pdfBlob = null;
    }
  }
}