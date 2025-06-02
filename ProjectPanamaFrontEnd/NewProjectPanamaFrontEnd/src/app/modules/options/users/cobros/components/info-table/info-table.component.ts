import {
  AfterViewInit,
  Component,
  ViewChild,
  Renderer2,
  Inject,
  effect,
  OnDestroy,
} from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { FormControl } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { ApiService } from 'src/app/services/api.service';
import {
  trigger,
  state,
  style,
  transition,
  animate,
  query,
  stagger,
} from '@angular/animations';
import { GlobalStatesService } from 'src/app/states/global-states.service';
import { Owners } from '../../interfaces/owners.interface';
import { Router } from '@angular/router';
import { DocumentsService } from 'src/app/services/documents.service';
import { MatSnackBar } from '@angular/material/snack-bar';

export interface VehicleInfoData {
  Unidad: string;
  Condu: string;
  Nombre: string;
  'Vlr.Cta': string;
  Celular: string;
  Ingreso: string;
  'Sin Pagar': string;
  'Sdo.Renta': string;
  Deposito: string;
  PanaPass: string;
  Siniestro: string;
  Mantenimien: string;
  'Otra Deu': string;
  Empresa: string;
  Central: string;
  Estado: string;
}

interface apiResponse {
  vehiculo_numero?: string;
  conductor?: string;
  conductores_nombre?: string;
  conductores_cuodiaria?: number;
  conductores_celular?: string;
  conductores_fecingres?: string;
  diferencia?: number;
  deu_renta?: number;
  fon_inscri?: number;
  deu_sinies?: number;
  deu_otras?: number;
  nombre?: string;
  centrales_nombre?: string;
  estado?: string;
}

interface DebtOption {
  text: string;
  color: string;
  hoverColor: string;
}

@Component({
  selector: 'app-info-table',
  templateUrl: './info-table.component.html',
  styleUrls: ['./info-table.component.css'],
  animations: [
    trigger('fadeInOut', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(-10px)' }),
        animate(
          '300ms ease-in',
          style({ opacity: 1, transform: 'translateY(0)' })
        ),
      ]),
      transition(':leave', [
        animate(
          '200ms ease-out',
          style({ opacity: 0, transform: 'translateY(-10px)' })
        ),
      ]),
    ]),
    // Animación para los elementos de la lista/tabla
    trigger('listAnimation', [
      transition('* => *', [
        query(
          ':enter',
          [
            style({ opacity: 0, transform: 'translateY(20px)' }),
            stagger(50, [
              animate(
                '300ms ease-out',
                style({ opacity: 1, transform: 'translateY(0)' })
              ),
            ]),
          ],
          { optional: true }
        ),
      ]),
    ]),
  ],
})
export class InfoTableComponent implements AfterViewInit, OnDestroy {
  debts = new FormControl<string>('Todos');

  debtList: DebtOption[] = [
    {
      text: 'Más de 3 Días',
      color: '#FFCDD2',
      hoverColor: '#FFAAAA',
    },
    {
      text: 'Menor o Igual a 2 Días',
      color: '#FFE0B2',
      hoverColor: '#FFCC80',
    },
    {
      text: 'Menor o Igual a 1 Día',
      color: '#FFF9C4',
      hoverColor: '#FFF176',
    },
    {
      text: 'Sin Deuda',
      color: '#C8E6C9',
      hoverColor: '#A5D6A7',
    },
    {
      text: 'Todos',
      color: '#ADD8E6',
      hoverColor: '#90CAF9',
    },
  ];

  selectedDebtLevel: string = 'Todos'; 

  displayedColumns: string[] = [
    'Unidad',
    'Condu',
    'Nombre',
    'Vlr.Cta',
    'Celular',
    'Ingreso',
    'Sin Pagar',
    'Sdo.Renta',
    'Deposito',
    'PanaPass',
    'Siniestro',
    'Mantenimien',
    'Otra Deu',
    'Empresa',
    'Central',
    'Estado',
  ];
  dataSource: MatTableDataSource<VehicleInfoData>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private apiService: ApiService,
    private globalStates: GlobalStatesService,
    private renderer: Renderer2,
    private router: Router,
    private documentsService: DocumentsService,
    private snackBar: MatSnackBar,
    @Inject(DOCUMENT) private document: Document
  ) {
    this.dataSource = new MatTableDataSource<VehicleInfoData>([]);

    effect(() => {
      const selectedOwners = this.globalStates.getSelectedOwners();

      if (selectedOwners.owners.length > 0) {
        console.log('Selected owners in info table components: ', selectedOwners);
        this.getTableData(selectedOwners);
        // TODO: Limpiar info guardada en los estados globales una vez se deja de utilizar
        // this.globalStates.clearSelectedOwners();
      }
    });
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
    this.generateHoverStyles();
    this.validatedOwnersList();
  }

  validatedOwnersList() {
    const selectedOwners = this.globalStates.getSelectedOwners();
    if (selectedOwners.owners.length === 0) {
      this.router.navigate(['/home/users']);
    }
  }

  generateHoverStyles() {
    // Eliminar estilos previos si existen
    const existingStyle = this.document.getElementById('debt-hover-styles');
    if (existingStyle) {
      existingStyle.remove();
    }

    // Crear nuevo elemento style
    const style = this.renderer.createElement('style');
    this.renderer.setAttribute(style, 'id', 'debt-hover-styles');

    let css = `
      .mat-mdc-option {
        transition: all 0.2s ease !important;
        margin: 1px !important;
        border-radius: 4px !important;
      }
    `;

    // Generar CSS dinámicamente desde el array debtList
    this.debtList.forEach((debt, index) => {
      css += `
        .debt-option-${index}:hover {
          background-color: ${debt.hoverColor} !important;
          transform: scale(1.02) !important;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
        }
      `;
    });

    this.renderer.setProperty(style, 'textContent', css);
    this.renderer.appendChild(this.document.head, style);
  }

  onDebtSelectionChange(event: any) {
    this.selectedDebtLevel = event.value;
    console.log('Selected debt level:', this.selectedDebtLevel);
    // TODO: Agregar lógica para filtrar la tabla según el nivel de deuda seleccionado
    this.nextFeatures();
    this.selectedDebtLevel = 'Todos';
    this.debts.setValue('Todos');
  }

  getTableData(selectedOwners: Owners) {

    this.apiService.postData('collection-accounts', selectedOwners).subscribe({
      next: (response) => {
        console.log('Data fetched successfully:', response);
        const mappedData: VehicleInfoData[] = response.map(
          (item: apiResponse) => {
            return {
              Unidad: item.vehiculo_numero || '',
              Condu: item.conductor || '',
              Nombre: item.conductores_nombre || '',
              'Vlr.Cta':
                item.conductores_cuodiaria !== undefined
                  ? item.conductores_cuodiaria.toString()
                  : '0',
              Celular: item.conductores_celular || '',
              Ingreso: item.conductores_fecingres || 'N/A',
              'Sin Pagar': '',
              'Sdo.Renta':
                item.deu_renta !== undefined ? item.deu_renta.toString() : '0',
              Deposito:
                item.fon_inscri !== undefined
                  ? item.fon_inscri.toString()
                  : '0',
              PanaPass: '',
              Siniestro:
                item.deu_sinies !== undefined
                  ? item.deu_sinies.toString()
                  : '0',
              Mantenimien: '',
              'Otra Deu':
                item.deu_otras !== undefined ? item.deu_otras.toString() : '0',
              Empresa: item.nombre || '',
              Central: item.centrales_nombre || '',
              Estado: item.estado || '',
            };
          }
        );

        this.dataSource.data = mappedData;
        if (this.paginator) {
          this.dataSource.paginator = this.paginator;
        }
        if (this.sort) {
          this.dataSource.sort = this.sort;
        }
      },
      error: (error) => {
        console.error('Error fetching data:', error);
      },
    });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  downloadCollectionAccountsXLS() {
    const selectedOwners = this.globalStates.getSelectedOwners();
    if (selectedOwners.owners.length === 0) {
      console.error('No owners selected for XLS download');
      this.openSnackbar('No hay propietarios seleccionados para descargar el reporte.');
      return;
    }

    this.openSnackbar('En un momento se descargará el reporte de cuentas de cobro.');

    this.documentsService.downloadDocument(
      'collection-accounts/download', 
      selectedOwners, 
      'collection_accounts_report.xlsx'
    ).subscribe({
      next: () => {
        console.log('Download started successfully');
      },
      error: (error) => {
        console.error('Download failed:', error);
        this.openSnackbar('Error al descargar el reporte de cuentas de cobro.');
      }
    });
  }

  nextFeatures() {
    this.openSnackbar('Esta funcionalidad está en desarrollo.');
  }

  openSnackbar(message: string) {
    this.snackBar.open(message, 'Cerrar', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'top',
    })
  }

  ngOnDestroy() {
    this.globalStates.clearSelectedOwners();
  }
}
