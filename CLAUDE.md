# CLAUDE.md - Guía de Arquitectura del Sistema ADMON-VEHICULOS

## 📋 Descripción General

Sistema de administración de vehículos desarrollado como aplicación full-stack con backend en Python (FastAPI) y frontend en Angular 16. El sistema gestiona vehículos, conductores, propietarios, inspecciones, documentación y reportes financieros para una empresa de transporte.

---

## 🏗️ Arquitectura del Sistema

### Estructura General
```
ADMON-VEHICULOS/
├── ProjectPanamaBackend/     # Backend API (FastAPI)
└── ProjectPanamaFrontEnd/    # Frontend Web (Angular 16)
    └── NewProjectPanamaFrontEnd/
```

---

## 🔧 BACKEND (ProjectPanamaBackend)

### Tecnologías Principales
- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0.29
- **Base de datos**: MySQL (PyMySQL)
- **Autenticación**: JWT (PyJWT 2.8.0)
- **Generación de documentos**: 
  - PDF: pdfkit 1.0.0
  - DOCX: python-docx, docxtpl
  - Excel: openpyxl, pandas
- **Servidor**: Uvicorn

### Estructura de Carpetas

#### `/config` - Configuración
- `dbconnection.py`: Conexión a base de datos usando SQLAlchemy
  - Engine con pool_recycle=3600 y pool_pre_ping=True
  - Variables de entorno: DB_TYPE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

#### `/models` - Modelos de Base de Datos (SQLAlchemy ORM)
Entidades principales:
- `vehiculos.py`: VEHICULOS (placa, marca, modelo, propietario, etc.)
- `conductores.py`: Conductores
- `propietarios.py`: Propietarios
- `centrales.py`: Centrales de operación
- `ciudades.py`: Ciudades
- `marcas.py`: Marcas de vehículos
- `inspecciones.py`: Inspecciones vehiculares
- `movienca.py`: Movimientos de cuenta
- `movimien.py`: Movimientos generales
- `cartera.py`: Cartera
- `cuentagastos.py`: Cuenta de gastos
- `cajarecaudos.py`: Caja de recaudos
- `infoempresas.py`: Información de empresas
- `patios.py`: Patios de vehículos
- `permisosusuario.py`: Permisos de usuario
- `estados.py`: Estados
- `modalidades.py`: Modalidades

#### `/schemas` - Esquemas Pydantic (Validación)
- `users.py`: userLogin, validaciones de usuario
- `owners.py`: Esquemas de propietarios
- `drivers.py`: Esquemas de conductores
- `vehicles.py`: Esquemas de vehículos
- `operations.py`: Esquemas de operaciones
- `inspections.py`: Esquemas de inspecciones
- `documents.py`: Esquemas de documentos
- `reports.py`: Esquemas de reportes

#### `/controller` - Lógica de Negocio
Controladores principales:
- `users.py`: get_user, process_login, process_logout
- `brands.py`: Gestión de marcas
- `central.py`: Gestión de centrales
- `cities.py`: Gestión de ciudades
- `collection_account.py`: Cuenta de recaudos
- `company.py`: Información de empresas
- `documents.py`: Gestión de documentos
- `drivers.py`: Gestión de conductores
- `expense_account.py`: Cuenta de gastos
- `extras.py`: Funcionalidades extras
- `inspections.py`: Gestión de inspecciones
- `operations.py`: Operaciones
- `states.py`: Estados
- `yards.py`: Patios

#### `/routes` - Endpoints API
Routers FastAPI:
- `users.py`: /users/, /login/, /logout
- `owners.py`: Endpoints de propietarios
- `drivers.py`: Endpoints de conductores
- `vehicles.py`: Endpoints de vehículos
- `states.py`: Endpoints de estados
- `cities.py`: Endpoints de ciudades
- `central.py`: Endpoints de centrales
- `operations.py`: Endpoints de operaciones
- `brands.py`: Endpoints de marcas
- `expense_account.py`: Endpoints de cuenta de gastos
- `modalities.py`: Endpoints de modalidades
- `extras.py`: Endpoints extras
- `collection_account.py`: Endpoints de cuenta de recaudos
- `inspections.py`: Endpoints de inspecciones
- `documents.py`: Endpoints de documentos
- `yards.py`: Endpoints de patios

**Subrutas de Reportes** (`/routes/reports/`):
- `feespaid.py`: Reportes de cuotas pagadas
- `owners.py`: Reportes de propietarios
- `statevehiclefleet.py`: Estado de flota vehicular
- `partsrelationship.py`: Relación de partes
- `relationshiprevenues.py`: Relación de ingresos
- `pandgstatus.py`: Estado de pérdidas y ganancias

#### `/middlewares` - Middlewares
- `JWTBearer.py`: Middleware de autenticación JWT

#### `/security` - Seguridad
- `jwt_handler.py`: Manejo de tokens JWT

#### `/utils` - Utilidades
- `pdf.py`: Generación de PDFs
- `docx.py`: Generación de documentos Word
- `reports.py`: Generación de reportes
- `inspections.py`: Utilidades de inspecciones
- `panapass.py`: Utilidades de Panapass
- `text.py`: Utilidades de texto

#### `/templates` - Plantillas HTML para PDFs
- `renderDirectorioVehiculos.html`
- `renderDirectorioConductores.html`
- `renderDirectorioPropietarios.html`
- `renderInformeCuotas.html`
- `ReporteInspecciones.html`
- `ResumenEstadoPyG.html`
- Y más plantillas para generación de reportes

#### `/assets` - Recursos Estáticos
- `/img`: Imágenes
- `/logo`: Logotipos

#### `/documents` - Documentos Generados
Almacena documentos generados por el sistema

### Archivo Principal
**`main.py`**: 
- Inicializa la aplicación FastAPI
- Configura CORS para http://localhost:4200
- Crea tablas de BD con `Base.metadata.create_all(bind=engine)`
- Registra todos los routers
- Monta directorios estáticos (/assets, /uploads)
- Endpoint raíz: GET / retorna {"Hello": "World"}

### Variables de Entorno (`.env`)
```
SECRET_KEY_JWT=''
ROUTE_API=''
DB_TYPE=mysql+pymysql
DB_USER=
DB_PASSWORD=''
DB_HOST=
DB_PORT=
DB_NAME=
USER_ADMIN=''
PASSWORD_ADMIN=''
DIRECTORY_IMG=''
VEHICLE_DOCS_PATH=''
DRIVER_DOCS_PATH=''
DEBUG=True
```

### Flujo de Autenticación
1. Frontend envía credenciales a POST /login/
2. `routes/users.py` llama a `controller/users.py:process_login()`
3. Se valida usuario y genera token JWT con `security/jwt_handler.py`
4. Token se establece en cookie httponly
5. Rutas protegidas usan `middlewares/JWTBearer.py` para validar token

---

## 🎨 FRONTEND (ProjectPanamaFrontEnd/NewProjectPanamaFrontEnd)

### Tecnologías Principales
- **Framework**: Angular 16.2.0
- **UI Components**: Angular Material 16.2.14
- **Autenticación**: JWT (jwt-decode 4.0.0)
- **PDF Viewer**: pdfjs-dist 3.11.174
- **Lenguaje**: TypeScript 5.1.3

### Estructura de Carpetas

#### `/src/app`

##### `/guards` - Guardias de Ruta
- `auth.guard.ts`: Protege rutas que requieren autenticación
- `no-auth.guard.ts`: Redirige usuarios autenticados fuera del login
- `owners.guard.ts`: Protección específica para propietarios
- `users.guard.ts`: Protección específica para usuarios

##### `/interfaces` - Interfaces TypeScript
Definiciones de tipos para entidades del sistema

##### `/services` - Servicios Angular
- `api.service.ts`: Servicio principal para comunicación con backend
- `jwt.service.ts`: Manejo de tokens JWT
- `localstorage.service.ts`: Gestión de almacenamiento local
- `documents.service.ts`: Servicio para documentos
- `error-handler.service.ts`: Manejo de errores

##### `/states` - Gestión de Estado
Manejo de estado de la aplicación

##### `/modules` - Módulos Funcionales

**`/home`**
- `home-owners.component`: Página principal para propietarios
- `home-users.component`: Página principal para usuarios

**`/navigation`**
- `layout.component`: Layout principal de la aplicación
- `sidenav.component`: Menú lateral de navegación
- `toolbar.component`: Barra de herramientas superior
- `footer.component`: Pie de página

**`/users`**
- `login.component`: Componente de inicio de sesión

**`/tasks`** - Módulo de Tareas Principales
Submódulos:
- `/owners`: Gestión de propietarios
  - `owners-table.component`: Tabla de propietarios
  - `owners-resume.component`: Resumen de propietario
  - `owners-addnew.component`: Agregar nuevo propietario
- `/drivers`: Gestión de conductores
  - `drivers-table.component`: Tabla de conductores
  - `drivers-resume.component`: Resumen de conductor
  - `drivers-addnew.component`: Agregar nuevo conductor
  - `drivers-documentation.component`: Documentación de conductor
- `/vehicles`: Gestión de vehículos
  - `vehicles-table.component`: Tabla de vehículos
  - `vehicles-resume.component`: Resumen de vehículo
  - `vehicles-addnew.component`: Agregar nuevo vehículo
  - `vehicles-documentation.component`: Documentación de vehículo
- `/feespaid`: Cuotas pagadas
- `/statevehiclefleet`: Estado de flota vehicular

**`/options`** - Módulos de Opciones por Departamento
- `/users/gerencia`: opciones-gerencia.component
- `/users/tramites`: opciones-tramites.component
- `/users/chapisteria`: opciones-chapisteria.component
- `/users/gastos`: opciones-gastos.component
- `/users/taller`: opciones-taller.component
- `/users/operaciones`: opciones-operaciones.component
- `/users/llavero`: opciones-llavero.component
- `/users/reclamos`: opciones-reclamos.component
- `/users/cnt`: opciones-cnt.component
- `/users/utilidades`: opciones-utilidades.component
- `/users/cartera`: opciones-cartera.component
- `/users/almacen`: opciones-almacen.component
- `/users/cobros`: Módulo de cobros (lazy-loaded)

**`/options/owners`** - Reportes para Propietarios
- `owners-feespaid.component`: Reporte de cuotas pagadas
- `owners-pandgstatus.component`: Estado de pérdidas y ganancias
- `owners-partsrelationship.component`: Relación de partes
- `owners-purchasevalueandpiquera.component`: Valor de compra y piquera
- `owners-relationshiprevenues.component`: Relación de ingresos
- `owners-relationshiprevenuesgeneral.component`: Relación de ingresos general
- `owners-statusfleetdetail.component`: Detalle estado de flota
- `owners-statusfleetsummary.component`: Resumen estado de flota

**`/shared`** - Componentes Compartidos
Componentes reutilizables en toda la aplicación

**`/others`**
- `pdf-viewer.component`: Visor de PDFs
- `dev-preview.component`: Vista previa de desarrollo
- `info-company.component`: Información de empresa

#### `/environments` - Configuración de Entornos
- `environment.development.ts`: 
  ```typescript
  { production: false, url: 'http://localhost:8000' }
  ```
- `environment.production.ts`: Configuración de producción

#### `/assets` - Recursos Estáticos
- `/icons`: Iconos
- `/img`: Imágenes
- `/video`: Videos

### Enrutamiento

**App Routing** (`app-routing.module.ts`):
- `/login` → LoginComponent (NoAuthGuard)
- `/pdf` → PdfViewerComponent
- `''` → Carga NavigationModule (lazy loading)

**Navigation Module** contiene rutas protegidas:
- Rutas de gestión (vehicles, owners, drivers)
- Rutas de opciones departamentales
- Rutas de reportes

### Flujo de Autenticación Frontend
1. Usuario ingresa credenciales en LoginComponent
2. api.service.ts envía POST a `/login/`
3. Token JWT se almacena en localStorage vía localstorage.service.ts
4. jwt.service.ts decodifica y valida tokens
5. Guards verifican autenticación antes de acceder a rutas
6. Token se envía en headers de peticiones HTTP

---

## 🔄 Flujo de Comunicación Frontend-Backend

### Peticiones HTTP
```
Frontend (Angular)
    ↓
api.service.ts (HTTP Client)
    ↓
http://localhost:8000/[endpoint]
    ↓
Backend (FastAPI) main.py
    ↓
CORS Middleware (valida origen)
    ↓
Router específico (/routes)
    ↓
Controller (lógica de negocio)
    ↓
Model (SQLAlchemy ORM)
    ↓
MySQL Database
    ↓
Respuesta JSON
    ↓
Frontend procesa respuesta
```

### Ejemplo: Obtener Lista de Vehículos
1. **Frontend**: `vehicles-table.component.ts` llama a `api.service.getVehicles()`
2. **HTTP**: GET request a `http://localhost:8000/vehicles/`
3. **Backend**: Router en `routes/vehicles.py` recibe petición
4. **Controller**: `controller/vehicles.py` obtiene datos con SQLAlchemy
5. **Model**: Query a tabla `VEHICULOS` via `models/vehiculos.py`
6. **Database**: MySQL ejecuta SELECT
7. **Response**: JSON con lista de vehículos
8. **Frontend**: Componente renderiza tabla con Angular Material

---

## 📊 Módulos Principales del Sistema

### 1. Gestión de Vehículos
- **Backend**: routes/vehicles.py, controller/vehicles.py, models/vehiculos.py
- **Frontend**: modules/tasks/vehicles/*
- **Funciones**: CRUD, documentación, inspecciones, reportes

### 2. Gestión de Conductores
- **Backend**: routes/drivers.py, controller/drivers.py, models/conductores.py
- **Frontend**: modules/tasks/drivers/*
- **Funciones**: CRUD, documentación, asignación a vehículos

### 3. Gestión de Propietarios
- **Backend**: routes/owners.py, models/propietarios.py
- **Frontend**: modules/tasks/owners/*
- **Funciones**: CRUD, reportes financieros, estado de flota

### 4. Inspecciones
- **Backend**: routes/inspections.py, controller/inspections.py, models/inspecciones.py
- **Frontend**: Integrado en módulos de vehículos
- **Funciones**: Registro de inspecciones, reportes

### 5. Operaciones
- **Backend**: routes/operations.py, controller/operations.py
- **Frontend**: modules/options/users/operaciones/*
- **Funciones**: Contratos, declaraciones juradas, documentos operativos

### 6. Reportes
- **Backend**: routes/reports/*, utils/reports.py, utils/pdf.py
- **Frontend**: modules/options/owners/* (reportes para propietarios)
- **Tipos**: 
  - Cuotas pagadas
  - Estado de flota
  - Pérdidas y ganancias
  - Relación de ingresos
  - Relación de partes

### 7. Documentación
- **Backend**: routes/documents.py, controller/documents.py, utils/docx.py
- **Frontend**: modules/tasks/*/documentation.component
- **Funciones**: Generación de PDFs, DOCX, gestión de archivos

### 8. Finanzas
- **Backend**: 
  - routes/collection_account.py (recaudos)
  - routes/expense_account.py (gastos)
  - models/cartera.py, models/cuentagastos.py
- **Frontend**: modules/options/users/cartera/*, modules/options/users/gastos/*
- **Funciones**: Control de cuentas, reportes financieros

---

## 🔐 Seguridad

### Autenticación y Autorización
- **JWT**: Tokens con SECRET_KEY_JWT
- **Cookies HttpOnly**: Almacenamiento seguro de tokens
- **Guards**: Protección de rutas en frontend
- **JWTBearer Middleware**: Validación de tokens en backend
- **Permisos**: Sistema de permisos por usuario (permisosusuario.py)

### CORS
- Configurado en main.py
- Permite: http://localhost:4200
- Métodos: GET, POST, PUT, DELETE
- Credentials: True

---

## 💾 Base de Datos

### Motor
- **DBMS**: MySQL
- **Conector**: PyMySQL
- **ORM**: SQLAlchemy

### Tablas Principales
- VEHICULOS: Información de vehículos
- Conductores: Información de conductores
- Propietarios: Información de propietarios
- CENTRALES: Centrales de operación
- CIUDADES: Ciudades
- MARCAS: Marcas de vehículos
- INSPECCIONES: Inspecciones vehiculares
- MOVIENCA: Movimientos de cuenta
- MOVIMIEN: Movimientos generales
- CARTERA: Cartera
- CUENTAGASTOS: Cuenta de gastos
- CAJARECAUDOS: Caja de recaudos
- INFOEMPRESAS: Información de empresas
- PATIOS: Patios de vehículos
- PERMISOSUSUARIO: Permisos de usuario

### Conexión
- Pool recycle: 3600 segundos (1 hora)
- Pool pre-ping: Habilitado (evita "server has gone away")

---

## 🚀 Ejecución del Sistema

### Backend
```bash
cd ProjectPanamaBackend
# Activar entorno virtual
venv\Scripts\activate  # Windows
# Instalar dependencias
pip install -r requirements.txt
# Configurar .env
# Ejecutar servidor
uvicorn main:app --reload
# Disponible en: http://localhost:8000
# Documentación: http://localhost:8000/docs
```

### Frontend
```bash
cd ProjectPanamaFrontEnd/NewProjectPanamaFrontEnd
# Instalar dependencias
npm install
# Ejecutar desarrollo
npm run start:dev
# Disponible en: http://localhost:4200
# Build producción
npm run build:prod
```

---

## 📁 Archivos de Configuración Importantes

### Backend
- `main.py`: Punto de entrada, configuración de app
- `config/dbconnection.py`: Configuración de BD
- `requirements.txt`: Dependencias Python
- `.env`: Variables de entorno (NO commitear)
- `.env.example`: Plantilla de variables

### Frontend
- `angular.json`: Configuración de Angular
- `package.json`: Dependencias npm y scripts
- `tsconfig.json`: Configuración TypeScript
- `src/environments/`: Configuración de entornos

---

## 🛠️ Dependencias Clave

### Backend (Python)
- fastapi==0.110.2
- SQLAlchemy==2.0.29
- PyMySQL==1.1.0
- PyJWT==2.8.0
- uvicorn==0.29.0
- pdfkit==1.0.0
- python-docx==1.2.0
- pandas==2.2.3
- openpyxl==3.1.5

### Frontend (Node.js)
- @angular/core: ^16.2.0
- @angular/material: ^16.2.14
- jwt-decode: ^4.0.0
- pdfjs-dist: ~3.11.174
- rxjs: ~7.8.0

---

## 📝 Notas de Desarrollo

### Patrones de Arquitectura
- **Backend**: 
  - Arquitectura en capas (Routes → Controllers → Models)
  - Repository pattern con SQLAlchemy
  - Dependency Injection con FastAPI
- **Frontend**: 
  - Component-based architecture
  - Lazy loading de módulos
  - Servicios singleton para estado compartido

### Convenciones de Código
- **Backend**: Snake_case para Python
- **Frontend**: camelCase para TypeScript, kebab-case para selectores
- **API**: RESTful endpoints
- **Respuestas**: JSON

### Generación de Documentos
El sistema genera múltiples tipos de documentos:
- **PDFs**: Usando pdfkit y plantillas HTML en /templates
- **DOCX**: Usando python-docx y docxtpl
- **Excel**: Usando openpyxl y pandas
- Plantillas ubicadas en ProjectPanamaBackend/templates/

### Almacenamiento de Archivos
- **Imágenes**: DIRECTORY_IMG (configurado en .env)
- **Documentos de vehículos**: VEHICLE_DOCS_PATH
- **Documentos de conductores**: DRIVER_DOCS_PATH
- **Assets estáticos**: /assets en backend

---

## 🔍 Debugging y Desarrollo

### Backend
- FastAPI Docs: http://localhost:8000/docs
- Logs de Uvicorn en consola
- DEBUG=True en .env para modo desarrollo

### Frontend
- Angular DevTools (extensión Chrome)
- Console logs en navegador
- Source maps habilitados en desarrollo

---

## 📌 Endpoints API Principales

### Autenticación
- POST /login/ - Iniciar sesión
- POST /logout/ - Cerrar sesión
- GET /users/ - Obtener usuarios

### Entidades
- GET/POST/PUT/DELETE /vehicles/ - Vehículos
- GET/POST/PUT/DELETE /drivers/ - Conductores
- GET/POST/PUT/DELETE /owners/ - Propietarios
- GET /states/ - Estados
- GET /cities/ - Ciudades
- GET /brands/ - Marcas
- GET /central/ - Centrales

### Reportes
- GET /reports/feespaid/ - Reporte cuotas pagadas
- GET /reports/statevehiclefleet/ - Estado flota
- GET /reports/pandgstatus/ - Estado P&G

### Operaciones
- GET/POST /operations/ - Operaciones
- GET/POST /inspections/ - Inspecciones
- GET/POST /documents/ - Documentos

---

## 🎯 Flujo de Trabajo Típico

### Agregar Nueva Entidad
1. **Backend**:
   - Crear modelo en `/models`
   - Crear schema en `/schemas`
   - Crear controller en `/controller`
   - Crear router en `/routes`
   - Registrar router en `main.py`

2. **Frontend**:
   - Crear interface en `/interfaces`
   - Crear servicio en `/services`
   - Crear componentes en `/modules/tasks`
   - Agregar rutas en routing module
   - Implementar UI con Angular Material

### Agregar Nuevo Reporte
1. **Backend**:
   - Crear endpoint en `/routes/reports`
   - Implementar lógica en controller
   - Crear plantilla HTML en `/templates`
   - Usar `/utils/pdf.py` o `/utils/reports.py`

2. **Frontend**:
   - Crear componente en `/modules/options/owners`
   - Llamar endpoint desde servicio
   - Mostrar/descargar reporte

---

Este documento proporciona una visión completa de la arquitectura y conexiones del sistema ADMON-VEHICULOS. Para información específica sobre implementación de funcionalidades, consultar el código fuente en las carpetas correspondientes.
