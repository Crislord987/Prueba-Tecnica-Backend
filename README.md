# Task Management API - Prueba Técnica Backend Python

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)](https://www.docker.com/)

API REST completa y robusta para gestión de tareas con autenticación JWT, desarrollada con FastAPI, SQLAlchemy y PostgreSQL.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Arquitectura](#-arquitectura)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso de la API](#-uso-de-la-api)
- [Endpoints](#-endpoints)
- [Decisiones Técnicas](#-decisiones-técnicas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Troubleshooting](#-troubleshooting)

## ✨ Características

- ✅ **Autenticación JWT**: Sistema completo con tokens seguros y expiración configurable
- ✅ **CRUD Completo**: Operaciones Create, Read, Update, Delete para tareas
- ✅ **Paginación**: Sistema de paginación eficiente con metadata completa
- ✅ **Seguridad**: Hash de contraseñas con bcrypt, endpoints protegidos
- ✅ **Migraciones**: Base de datos versionada con Alembic
- ✅ **Seed Data**: Usuario inicial y datos de ejemplo automáticos
- ✅ **Validación**: Validación de datos con Pydantic (incluyendo emails)
- ✅ **Manejo de Errores**: Respuestas HTTP consistentes (400/401/404/422)
- ✅ **Documentación**: Swagger UI y ReDoc automáticos
- ✅ **Filtros**: Filtrado de tareas por estado
- ✅ **Índices Optimizados**: Consultas rápidas con índices estratégicos
- ✅ **Docker Ready**: PostgreSQL en contenedor Docker

## 🛠 Tecnologías

- **Python 3.11+**: Lenguaje de programación
- **FastAPI 0.109.0**: Framework web moderno y de alto rendimiento
- **SQLAlchemy 2.0.25**: ORM para interacción con base de datos
- **PostgreSQL 15**: Base de datos relacional
- **Alembic 1.13.1**: Herramienta de migraciones de base de datos
- **Pydantic 2.5.3**: Validación de datos y settings
- **python-jose 3.3.0**: Implementación JWT
- **passlib 1.7.4 + bcrypt 4.0.1**: Hash seguro de contraseñas
- **Docker & Docker Compose**: Orquestación de contenedores
- **email-validator 2.1.0**: Validación de direcciones de email

## 🏗 Arquitectura

El proyecto sigue una arquitectura limpia y modular con separación de responsabilidades:

```
app/
├── api/           # Endpoints y routers (capa de presentación)
├── core/          # Configuración, seguridad, autenticación
├── db/            # Conexión a base de datos y sesiones
├── models/        # Modelos SQLAlchemy (entidades)
├── schemas/       # Schemas Pydantic (DTOs)
└── services/      # Lógica de negocio
```

### Principios aplicados:

- **Separación de capas**: API → Services → Models
- **Inyección de dependencias**: Para sesiones DB y autenticación
- **Single Responsibility**: Cada módulo tiene una responsabilidad clara
- **DRY (Don't Repeat Yourself)**: Código reutilizable y mantenible

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

### 1. **Python 3.11 o superior**
```bash
# Verificar versión
python --version
```
Descargar desde: https://www.python.org/downloads/

### 2. **Docker Desktop**
**Docker es REQUERIDO** para ejecutar PostgreSQL.

#### Windows:
1. Descargar Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Instalar y reiniciar el sistema si es necesario
3. Abrir Docker Desktop y esperar a que inicie completamente
4. Verificar instalación:
```powershell
docker --version
docker-compose --version
```

#### Linux:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Fedora
sudo dnf install docker docker-compose

# Verificar
docker --version
docker-compose --version
```

#### macOS:
1. Descargar Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Instalar y abrir Docker Desktop
3. Verificar:
```bash
docker --version
docker-compose --version
```

### 3. **Git** (opcional, para clonar el repositorio)
```bash
git --version
```

## 🚀 Instalación y Configuración

Sigue estos pasos cuidadosamente para configurar el proyecto:

### Paso 1: Clonar el repositorio

```bash
git clone <repository-url>
cd Pruebatecnica
```

### Paso 2: Crear entorno virtual e instalar dependencias

#### Windows (PowerShell):
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\activate

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

#### Linux/Mac:
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

**Nota**: Si hay errores de instalación, asegúrate de tener las herramientas de compilación necesarias instaladas.

### Paso 3: Verificar archivo .env

El archivo `.env` ya está incluido con valores por defecto funcionales:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=technical_test
DB_USER=postgres
DB_PASSWORD=postgres

# JWT
SECRET_KEY=clave-secreta-juas-juas
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Usuario inicial
INITIAL_USER_EMAIL=admin@example.com
INITIAL_USER_PASSWORD=Admin123!
```

**⚠️ IMPORTANTE**: En producción, cambia `SECRET_KEY` por un valor criptográficamente seguro.

### Paso 4: Verificar PostgreSQL local (IMPORTANTE)

**⚠️ CRÍTICO**: Si tienes PostgreSQL instalado localmente en tu máquina Windows, **DEBES detenerlo** antes de continuar, ya que ocupará el puerto 5432 e impedirá que el contenedor Docker funcione correctamente.

#### 4.1 Verificar si PostgreSQL local está corriendo

```powershell
# Verificar servicios PostgreSQL
Get-Service | Where-Object {$_.Name -like "*postgres*"}
```

Si ves algo como:
```
Status   Name               DisplayName
------   ----               -----------
Running  postgresql-x64-18  postgresql-x64-18 - PostgreSQL Server...
```

Significa que tienes PostgreSQL local corriendo y **DEBES detenerlo**.

#### 4.2 Detener PostgreSQL local (si está corriendo)

**IMPORTANTE**: Necesitas ejecutar PowerShell como **Administrador** para detener servicios.

1. Cierra tu PowerShell actual
2. Busca "PowerShell" en el menú de Windows
3. Click derecho → "Ejecutar como administrador"
4. Navega a tu proyecto: `cd D:\Pruebatecnica`
5. Activa el entorno virtual: `.\venv\Scripts\activate`
6. Detén el servicio PostgreSQL:

```powershell
# Reemplaza 'postgresql-x64-18' con el nombre exacto que viste en el paso 4.1
Stop-Service postgresql-x64-18

# Verificar que se detuvo
Get-Service postgresql-x64-18
# Debe mostrar Status: Stopped
```

**Alternativa (sin permisos de admin)**: Si no puedes obtener permisos de administrador, cambia el puerto del contenedor Docker:

1. Edita `docker-compose.yml` y cambia `"5432:5432"` por `"5433:5432"`
2. Edita `.env` y cambia `DB_PORT=5432` por `DB_PORT=5433`
3. Reinicia: `docker-compose down && docker-compose up -d`

#### 4.3 Asegúrate de que Docker Desktop está ejecutándose

**Windows**: Docker Desktop debe estar abierto y el ícono debe estar verde en la bandeja del sistema.

**Linux/Mac**: Inicia el servicio Docker:
```bash
sudo systemctl start docker  # Linux
```

#### 4.4 Iniciar el contenedor de PostgreSQL

```bash
# Levantar PostgreSQL en background
docker-compose up -d

# Verificar que el contenedor está corriendo
docker-compose ps
```

Deberías ver algo como:
```
NAME                IMAGE                COMMAND                  STATUS
technical_test_db   postgres:15-alpine   "docker-entrypoint.s…"   Up (healthy)
```

#### 4.5 Verificar logs (opcional)

```bash
# Ver logs del contenedor
docker-compose logs -f

# Salir con Ctrl+C
```

### Paso 5: Inicializar la base de datos

**Este paso es CRÍTICO** - ejecuta el script de inicialización:

```bash
python init_db.py
```

Este script automáticamente:
1. ✅ Verifica que Docker está corriendo
2. ✅ Crea la base de datos `technical_test`
3. ✅ Crea todas las tablas necesarias (`users`, `tasks`)
4. ✅ Crea índices optimizados
5. ✅ Inserta el usuario administrador
6. ✅ Inserta 10 tareas de ejemplo

**Salida esperada:**
```
============================================================
INICIALIZACIÓN DE BASE DE DATOS
============================================================

Paso 1: Verificando/creando base de datos...
✅ Base de datos 'technical_test' creada

Paso 2: Creando tablas...
✅ Tablas creadas correctamente

Paso 3: Insertando datos iniciales...
✅ Usuario 'admin@example.com' creado
✅ 10 tareas de ejemplo creadas

============================================================
✅ ¡BASE DE DATOS INICIALIZADA CORRECTAMENTE!
============================================================
```

### Paso 6: Ejecutar la aplicación

```bash
# Opción 1: Usando el script run.py (recomendado)
python run.py

# Opción 2: Directamente con uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Salida esperada:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

### Paso 7: Verificar que funciona

Abre tu navegador en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔐 Uso de la API

### Credenciales del Usuario Inicial

El sistema crea automáticamente un usuario administrador:

- **Email**: `admin@example.com`
- **Password**: `Admin123!`

### Flujo de autenticación

1. **Obtener token JWT** → `POST /api/v1/auth/login`
2. **Usar token en headers** → `Authorization: Bearer <token>`
3. **Acceder a endpoints protegidos** → Todos los endpoints de tareas

### Ejemplo rápido con Swagger UI

1. Ve a http://localhost:8000/docs
2. Click en **POST /api/v1/auth/login**
3. Click en **"Try it out"**
4. Usa las credenciales:
   ```json
   {
     "email": "admin@example.com",
     "password": "Admin123!"
   }
   ```
5. Click en **"Execute"**
6. Copia el `access_token` de la respuesta
7. Click en el botón **"Authorize"** (🔒 arriba a la derecha)
8. Pega el token y click en **"Authorize"**
9. ¡Ahora puedes usar todos los endpoints!

## 📚 Endpoints

### Autenticación

#### POST /api/v1/auth/login

Autenticar usuario y obtener token JWT.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "Admin123!"
  }'
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errores:**
- `401 Unauthorized`: Credenciales incorrectas
- `422 Unprocessable Entity`: Email inválido

### Tareas

**Nota**: Todos los endpoints de tareas requieren autenticación (header Authorization).

#### POST /api/v1/tasks

Crear una nueva tarea.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nueva tarea",
    "description": "Descripción de la tarea",
    "status": "pending"
  }'
```

**Response (201):**
```json
{
  "id": 1,
  "title": "Nueva tarea",
  "description": "Descripción de la tarea",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### GET /api/v1/tasks

Obtener lista paginada de tareas con filtros opcionales.

**Parámetros query:**
- `page` (optional): Número de página (default: 1, min: 1)
- `page_size` (optional): Tamaño de página (default: 10, min: 1, max: 100)
- `status` (optional): Filtrar por estado (pending, in_progress, done)

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks?page=1&page_size=10&status=pending" \
  -H "Authorization: Bearer <token>"
```

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Tarea 1",
      "description": "Descripción",
      "status": "pending",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 25,
  "page": 1,
  "page_size": 10,
  "total_pages": 3
}
```

#### GET /api/v1/tasks/{task_id}

Obtener una tarea específica por ID.

**Response (200):** Objeto Task  
**Errores:** `404 Not Found` - Tarea no existe

#### PUT /api/v1/tasks/{task_id}

Actualizar una tarea (actualización parcial permitida).

**Request:**
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }'
```

**Errores:**
- `400 Bad Request`: No se envió ningún campo
- `404 Not Found`: Tarea no existe

#### DELETE /api/v1/tasks/{task_id}

Eliminar una tarea.

**Response (204 No Content)**  
**Errores:** `404 Not Found` - Tarea no existe

### Health Check

#### GET /health

Verificar estado de la API (no requiere autenticación).

**Response (200):**
```json
{
  "status": "healthy",
  "service": "Task Management API"
}
```

## 🎯 Decisiones Técnicas

### 1. Docker para PostgreSQL

**Decisión**: Usar Docker Compose para ejecutar PostgreSQL en contenedor.

**Ventajas:**
- ✅ **Portabilidad**: Funciona igual en Windows, Linux y macOS
- ✅ **Aislamiento**: DB en contenedor separado, sin conflictos
- ✅ **Configuración simple**: Un solo comando para levantar la DB
- ✅ **Reproducibilidad**: Misma versión de PostgreSQL en todos los entornos
- ✅ **Fácil limpieza**: `docker-compose down -v` elimina todo

**Configuración** (`docker-compose.yml`):
```yaml
services:
  db:
    image: postgres:15-alpine
    container_name: technical_test_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### 2. Inicialización con SQL directo (sin Alembic inicial)

**Problema encontrado**: En Windows, `psycopg2` tiene problemas con encoding UTF-8 en variables de entorno del sistema.

**Solución implementada**: `init_db.py` ejecuta SQL directamente en el contenedor Docker usando `docker exec`, evitando completamente los problemas de encoding.

**Ventajas:**
- ✅ **Confiable**: No depende de configuración del sistema Windows
- ✅ **Rápido**: Una sola ejecución crea todo
- ✅ **Compatible**: Funciona en todos los sistemas operativos
- ✅ **Automático**: Usuario y datos de ejemplo incluidos

### 3. Validación de Email con Pydantic

**Implementación**: Uso de `EmailStr` de Pydantic para validación automática.

**Requiere**: `email-validator` instalado (incluido en `requirements.txt`)

**Ventajas:**
- ✅ **Validación automática**: Rechaza emails mal formados
- ✅ **Documentación clara**: Swagger UI muestra formato esperado
- ✅ **RFC compliant**: Sigue estándares de email

### 4. bcrypt 4.0.1 específico

**Decisión**: Fijar versión de bcrypt en 4.0.1

**Razón**: bcrypt 5.x tiene cambios en API que causan incompatibilidades con passlib 1.7.4

**Solución en código**: `security.py` trunca contraseñas a 72 bytes (límite de bcrypt) automáticamente.

### 5. Índices de Base de Datos

Se definieron índices estratégicos en la tabla `tasks`:

- **`status` (individual)**: Optimiza filtrados por estado
- **`created_at` (individual)**: Mejora ordenamiento por fecha
- **`status + created_at` (compuesto)**: Optimiza la query más común

**Justificación**: Estos índices cubren los patrones de consulta más frecuentes y mejoran significativamente el rendimiento en listas grandes de tareas.

### 6. Paginación Offset-based

```json
{
  "items": [...],
  "total": 100,
  "page": 2,
  "page_size": 10,
  "total_pages": 10
}
```

**Por qué offset pagination:**
- ✅ Simple de implementar y entender
- ✅ Permite saltar a cualquier página
- ✅ Metadata útil para UI (total de páginas, items)
- ⚠️ Menos eficiente en tablas muy grandes (alternativa: cursor pagination)

### 7. JWT Stateless

**Implementación:**
- Token JWT con algoritmo HS256
- Expiración configurable (default: 30 minutos)
- No requiere almacenamiento de sesiones

**Trade-offs:**
- ✅ **Escalable**: Perfecto para microservicios
- ✅ **Simple**: No necesita Redis/cache de sesiones
- ⚠️ **No revocación instantánea**: Token válido hasta expiración

## 📁 Estructura del Proyecto

```
.
├── alembic/                    # Migraciones (compatibilidad futura)
│   ├── versions/               # Archivos de migración
│   └── env.py                  # Configuración Alembic
├── app/
│   ├── api/                    # Endpoints
│   │   ├── auth.py            # Login
│   │   └── tasks.py           # CRUD tareas
│   ├── core/                   # Configuración
│   │   ├── config.py          # Settings
│   │   └── security.py        # JWT, bcrypt, auth
│   ├── db/                     # Base de datos
│   │   └── session.py         # SQLAlchemy setup
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   └── task.py
│   ├── services/               # Lógica de negocio
│   │   ├── user_service.py
│   │   └── task_service.py
│   └── main.py                 # FastAPI app
├── .env                        # Variables de entorno
├── .gitignore
├── docker-compose.yml          # PostgreSQL container
├── init_db.py                  # Script de inicialización ⚡
├── requirements.txt            # Dependencias Python
├── run.py                      # Ejecutar servidor
└── README.md
```

## 🐛 Troubleshooting

### Error: "Docker no está corriendo"

**Síntoma:**
```
❌ Docker no está corriendo. Ejecuta: docker-compose up -d
```

**Solución:**
1. Abre Docker Desktop (Windows/Mac)
2. Espera a que el ícono esté verde
3. Ejecuta: `docker-compose up -d`

### Error: "Module 'email_validator' not found"

**Síntoma:**
```
ImportError: email-validator is not installed
```

**Solución:**
```bash
pip install email-validator==2.1.0
```

### Error: "UnicodeDecodeError" al inicializar DB

**Síntoma:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf3
```

**Solución:** El script `init_db.py` está diseñado para evitar este problema. Si persiste:

```powershell
# Windows PowerShell
$env:PGCLIENTENCODING = $null
$env:PGSSLMODE = $null
python init_db.py
```

### Error: "UndefinedTable: no existe la relación «users»" PERO las tablas sí existen

**Síntoma:** 
- `init_db.py` reporta que las tablas se crearon correctamente
- Al verificar con `docker exec -it technical_test_db psql -U postgres -d technical_test` y ejecutar `\dt`, las tablas **SÍ existen**
- Sin embargo, la aplicación dice `UndefinedTable: no existe la relación «users»`

**Causa:** Tienes PostgreSQL instalado localmente en Windows ocupando el puerto 5432. La aplicación se conecta a tu PostgreSQL local (que está vacío) en lugar del contenedor Docker (que tiene las tablas).

**Solución:**

**Paso 1:** Verificar si PostgreSQL local está corriendo:
```powershell
Get-Service | Where-Object {$_.Name -like "*postgres*"}
```

**Paso 2:** Si ves un servicio corriendo, deténlo. **DEBES usar PowerShell como Administrador**:

1. Cierra tu PowerShell actual
2. Busca "PowerShell" en el menú de Windows
3. Click derecho → "Ejecutar como administrador"
4. Navega al proyecto: `cd D:\Pruebatecnica`
5. Activa el entorno: `.\venv\Scripts\activate`
6. Detén el servicio:
```powershell
# Reemplaza con el nombre exacto que viste
Stop-Service postgresql-x64-18

# Verificar que se detuvo
Get-Service postgresql-x64-18
# Debe mostrar: Status: Stopped
```

**Paso 3:** Reinicia la aplicación:
```powershell
python run.py
```

**Alternativa (sin permisos admin):** Cambiar el puerto del Docker:
1. Edita `docker-compose.yml`: cambia `"5432:5432"` por `"5433:5432"`
2. Edita `.env`: cambia `DB_PORT=5432` por `DB_PORT=5433`
3. Reinicia: `docker-compose down && docker-compose up -d`

### Error: "Port 5432 already in use" al levantar Docker

**Síntoma:** El contenedor Docker no puede iniciar porque el puerto 5432 está ocupado.

**Solución:** Sigue los mismos pasos de la sección anterior para detener PostgreSQL local.

### Error: "Connection refused to localhost:5432"

**Síntoma:** La aplicación no puede conectar a PostgreSQL.

**Verificación:**
```bash
# Ver si el contenedor está corriendo
docker-compose ps

# Ver logs del contenedor
docker-compose logs db

# Reiniciar contenedor
docker-compose restart
```

### Base de datos no se inicializa correctamente

**Solución:** Reiniciar desde cero
```bash
# Detener y eliminar todo (incluyendo datos)
docker-compose down -v

# Levantar de nuevo
docker-compose up -d

# Reinicializar
python init_db.py
```

### Error: "passlib.handlers.bcrypt: password cannot be longer than 72 bytes"

**Causa:** bcrypt tiene límite de 72 bytes para contraseñas.

**Solución:** El código en `security.py` trunca automáticamente. Si ves este error, asegúrate de tener bcrypt 4.0.1:
```bash
pip install bcrypt==4.0.1 --force-reinstall
```

## 🧪 Testing

### Testing manual con datos de ejemplo

El sistema incluye 10 tareas de ejemplo creadas automáticamente:

1. Complete project documentation (in_progress)
2. Implement user authentication (done)
3. Add pagination to task list (done)
4. Write unit tests (pending)
5. Set up CI/CD pipeline (pending)
6. Optimize database queries (in_progress)
7. Implement rate limiting (pending)
8. Add logging and monitoring (pending)
9. Create Docker deployment (pending)
10. Review code quality (pending)

### Ejemplo de flujo completo con cURL

```bash
# 1. Login y obtener token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"Admin123!"}' \
  | jq -r '.access_token')

# 2. Listar tareas pendientes
curl -X GET "http://localhost:8000/api/v1/tasks?status=pending&page=1&page_size=5" \
  -H "Authorization: Bearer $TOKEN"

# 3. Crear nueva tarea
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"Testing API","status":"pending"}'

# 4. Actualizar tarea #1 a completada
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}'

# 5. Eliminar tarea #1
curl -X DELETE "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer $TOKEN"
```

## 🔒 Seguridad

### Implementaciones actuales:

1. ✅ **Password Hashing**: bcrypt con 12 rounds
2. ✅ **JWT**: Tokens firmados con secret key
3. ✅ **SQL Injection Protection**: SQLAlchemy ORM
4. ✅ **Input Validation**: Pydantic valida todos los inputs
5. ✅ **Email Validation**: RFC compliant con email-validator

### ⚠️ Recomendaciones para producción:

- [ ] Cambiar `SECRET_KEY` a valor criptográficamente seguro (usar `openssl rand -hex 32`)
- [ ] Usar HTTPS en producción
- [ ] Configurar CORS apropiadamente
- [ ] Implementar rate limiting
- [ ] Agregar logging estructurado y monitoring
- [ ] Usar secrets manager para variables sensibles (no .env en repo)
- [ ] Agregar 2FA para usuarios críticos
- [ ] Implementar refresh tokens
- [ ] Agregar audit logs

## 🚢 Despliegue en Producción

### Dockerfile para producción

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Puerto
EXPOSE 8000

# Comando
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Stack recomendado para producción:

- **Aplicación**: Gunicorn + Uvicorn workers en contenedor Docker
- **Base de datos**: PostgreSQL gestionado (AWS RDS, Google Cloud SQL, Azure Database)
- **Proxy inverso**: Nginx para SSL/TLS y load balancing
- **Orquestación**: Kubernetes o Docker Swarm
- **CI/CD**: GitHub Actions, GitLab CI, o Jenkins
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack o CloudWatch

## 🎓 Notas de Implementación

### Desafíos resueltos:

1. ✅ **Encoding UTF-8 en Windows**: Solucionado usando `docker exec` para inicialización
2. ✅ **Compatibilidad bcrypt**: Fijada versión 4.0.1 con truncamiento automático
3. ✅ **Email validation**: Agregado `email-validator` para validación RFC compliant
4. ✅ **Docker en diferentes OS**: Configuración universal que funciona en Windows/Linux/Mac

### Mejoras implementadas:

- ✅ Seed data automático con 10 tareas
- ✅ Filtrado por estado
- ✅ Documentación con ejemplos cURL
- ✅ Health check endpoint
- ✅ Scripts de inicialización robustos
- ✅ Troubleshooting guide completo
- ✅ Docker-ready con un comando

