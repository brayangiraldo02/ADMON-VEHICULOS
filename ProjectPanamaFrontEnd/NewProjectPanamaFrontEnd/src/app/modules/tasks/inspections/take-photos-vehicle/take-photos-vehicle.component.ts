import { Component, ElementRef, ViewChild, OnDestroy, OnInit, Input } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { forkJoin, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { ApiService } from 'src/app/services/api.service';
import { ImagePreviewDialogComponent } from '../image-preview-dialog/image-preview-dialog.component';

// Definimos una interfaz para el objeto de foto
interface Photo {
  previewUrl: SafeUrl;
  blob: Blob;
}

@Component({
  selector: 'app-take-photos-vehicle',
  templateUrl: './take-photos-vehicle.component.html',
  styleUrls: ['./take-photos-vehicle.component.css']
})
export class TakePhotosVehicleComponent implements OnInit, OnDestroy {
  // Entradas para hacer el componente reutilizable
  @Input() companyCode!: string;
  @Input() vehicleNumber!: string;

  // Referencias al DOM
  @ViewChild('videoElement') videoElement!: ElementRef<HTMLVideoElement>;
  @ViewChild('canvasElement') canvasElement!: ElementRef<HTMLCanvasElement>;

  // Constantes y estado
  readonly MAX_PHOTOS = 16;
  photos: Photo[] = [];
  isUploading = false;
  uploadStatus = '';
  private stream: MediaStream | null = null;

  constructor(
    private sanitizer: DomSanitizer,
    private apiService: ApiService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.startCamera();
  }

  ngOnDestroy(): void {
    this.stopCamera();
  }

  async startCamera(): Promise<void> {
    if (this.stream) return;
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' }
      });
      this.videoElement.nativeElement.srcObject = this.stream;
    } catch (err) {
      console.error('Error al acceder a la cámara:', err);
      // Aquí podrías mostrar un mensaje al usuario
    }
  }

  takePhoto(): void {
    if (this.photos.length >= this.MAX_PHOTOS || !this.stream) return;

    const video = this.videoElement.nativeElement;
    const canvas = this.canvasElement.nativeElement;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d')?.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      if (blob) {
        const newPhoto: Photo = {
          blob: blob,
          previewUrl: this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(blob))
        };
        this.photos.push(newPhoto);
        if (this.photos.length >= this.MAX_PHOTOS) {
          this.stopCamera();
        }
      }
    }, 'image/jpeg', 0.9);
  }
  
  openPreview(index: number): void {
    const dialogRef = this.dialog.open(ImagePreviewDialogComponent, {
      data: { imageUrl: this.photos[index].previewUrl },
      width: 'auto',
      panelClass: 'custom-dialog-container' // Clase opcional para más estilos
    });

    // Nos suscribimos para saber qué pasó cuando se cerró el diálogo
    dialogRef.afterClosed().subscribe(result => {
      // Si el resultado tiene la propiedad 'delete' en true, eliminamos la foto
      if (result && result.delete) {
        this.deletePhoto(index);
      }
    });
  }
  
  // El método deletePhoto se mantiene igual, no necesita cambios
  deletePhoto(index: number): void {
    this.photos.splice(index, 1);
    if (this.photos.length < this.MAX_PHOTOS && !this.stream) {
      this.startCamera();
    }
  }

  sendAllPhotos(): void {
    if (this.photos.length === 0 || !this.companyCode || !this.vehicleNumber) {
        console.error('Faltan datos para la subida (companyCode, vehicleNumber).');
        return;
    }

    this.isUploading = true;
    this.uploadStatus = `Subiendo ${this.photos.length} fotos...`;

    // Creamos un array de observables, uno por cada petición de subida
    const uploadObservables = this.photos.map((photo, index) => {
      const formData = new FormData();
      formData.append('image', photo.blob, `vehicle-${this.vehicleNumber}-${index + 1}.jpg`);
      // El endpoint de FastAPI buscará estos campos en el FormData
      formData.append('company_code', this.companyCode);
      formData.append('vehicle_number', this.vehicleNumber);
      
      return this.apiService.uploadPhoto('prueba', formData).pipe(
        catchError(error => {
          console.error(`Error subiendo la foto ${index + 1}:`, error);
          // Devolvemos un observable con el error para que forkJoin no se cancele
          return of({ error: true, photoIndex: index + 1 });
        })
      );
    });

    // forkJoin ejecuta todos los observables en paralelo y emite cuando todos han completado
    forkJoin(uploadObservables).subscribe({
      next: (results) => {
        const errors = results.filter(r => r?.error);
        if (errors.length > 0) {
          this.uploadStatus = `Proceso completado con ${errors.length} errores.`;
        } else {
          this.uploadStatus = '¡Todas las fotos se han subido con éxito!';
          this.photos = []; // Limpiamos la galería al terminar
        }
      },
      error: () => {
        // Este bloque es por si forkJoin falla de forma inesperada, aunque catchError lo previene.
        this.uploadStatus = 'Ocurrió un error inesperado durante la subida.';
      },
      complete: () => {
        this.isUploading = false;
        this.startCamera(); // Reactivamos la cámara si es necesario
      }
    });
  }

  private stopCamera(): void {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
  }
}