# Comandos Útiles - Task Management API

## 🐳 Docker Commands

```bash
# Iniciar PostgreSQL
docker-compose up -d

# Ver logs de PostgreSQL
docker-compose logs -f postgres

# Detener PostgreSQL
docker-compose down

# Detener y eliminar datos
docker-compose down -v

# Ver estado del contenedor
docker-compose ps

# Ejecutar comandos en PostgreSQL
docker-compose exec postgres psql -U postgres -d technical_test

# Backup de base de datos
docker-compose exec postgres pg_dump -U postgres technical_test > backup.sql

# Restaurar backup
docker-compose exec -T postgres psql -U postgres technical_test < backup.sql
```

## 📊 Database Commands

```bash
# Crear nueva migración (automática)
alembic revision --autogenerate -m "descripción del cambio"

# Aplicar todas las migraciones
alembic upgrade head

# Aplicar hasta una migración específica
alembic upgrade 001_initial

# Revertir última migración
alembic downgrade -1

# Revertir a migración específica
alembic downgrade 001_initial

# Ver historial de migraciones
alembic history

# Ver migración actual
alembic current

# Ver SQL que se ejecutará (sin aplicar)
alembic upgrade head --sql
```

## 🚀 Application Commands

```bash
# Iniciar servidor con reload automático
uvicorn app.main:app --reload

# Iniciar en puerto específico
uvicorn app.main:app --reload --port 8080

# Iniciar con más workers (producción)
uvicorn app.main:app --workers 4

# Iniciar accesible desde red local
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Usando el script run.py
python run.py

# Usando el script de inicio rápido (Windows)
start.bat

# Usando el script de inicio rápido (Linux/Mac)
./start.sh
```

## 🔍 Testing Commands (cURL)

### Authentication

```bash
# Login y obtener token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"Admin123!"}'

# Guardar token en variable (Bash)
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"Admin123!"}' \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# Guardar token en variable (PowerShell)
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" -Method POST -Body (@{email="admin@example.com";password="Admin123!"} | ConvertTo-Json) -ContentType "application/json"
$TOKEN = $response.access_token
```

### Tasks CRUD

```bash
# Crear tarea
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Nueva tarea","description":"Descripción","status":"pending"}'

# Listar todas las tareas
curl -X GET "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer $TOKEN"

# Listar con paginación
curl -X GET "http://localhost:8000/api/v1/tasks?page=1&page_size=5" \
  -H "Authorization: Bearer $TOKEN"

# Listar con filtro por estado
curl -X GET "http://localhost:8000/api/v1/tasks?status=pending" \
  -H "Authorization: Bearer $TOKEN"

# Obtener tarea por ID
curl -X GET "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer $TOKEN"

# Actualizar tarea
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}'

# Eliminar tarea
curl -X DELETE "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer $TOKEN"

# Pretty print JSON (con jq)
curl -X GET "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer $TOKEN" | jq
```

## 🐍 Python Commands

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Generar requirements.txt
pip freeze > requirements.txt

# Ver paquetes instalados
pip list

# Desactivar entorno virtual
deactivate

# Ejecutar shell interactivo con contexto de app
python -i -c "from app.db.session import SessionLocal; from app.models.task import Task; db = SessionLocal()"
```

## 🔧 Development Commands

```bash
# Formatear código con black
black app/

# Lint con flake8
flake8 app/

# Type checking con mypy
mypy app/

# Ver estructura del proyecto
tree /F  # Windows
tree -L 3  # Linux/Mac

# Contar líneas de código
find app/ -name '*.py' -exec wc -l {} + | tail -1  # Linux/Mac

# Buscar TODOs
grep -r "TODO" app/  # Linux/Mac
findstr /s "TODO" app\*.py  # Windows
```

## 📊 Monitoring Commands

```bash
# Ver uso de CPU/memoria del contenedor
docker stats technical_test_db

# Ver conexiones activas a PostgreSQL
docker-compose exec postgres psql -U postgres -d technical_test -c "SELECT count(*) FROM pg_stat_activity;"

# Ver tamaño de la base de datos
docker-compose exec postgres psql -U postgres -d technical_test -c "SELECT pg_size_pretty(pg_database_size('technical_test'));"

# Ver tamaño de cada tabla
docker-compose exec postgres psql -U postgres -d technical_test -c "SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) FROM pg_stat_user_tables ORDER BY pg_total_relation_size(relid) DESC;"

# Ver queries lentas (requiere configuración)
docker-compose exec postgres psql -U postgres -d technical_test -c "SELECT query, mean_exec_time, calls FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
```

## 🧹 Cleanup Commands

```bash
# Limpiar caché de Python
find . -type d -name __pycache__ -exec rm -r {} +  # Linux/Mac
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"  # Windows

# Limpiar archivos .pyc
find . -name '*.pyc' -delete  # Linux/Mac
del /s /q *.pyc  # Windows

# Limpiar entorno virtual
rm -rf venv/  # Linux/Mac
rmdir /s /q venv  # Windows

# Limpiar contenedores y volúmenes Docker
docker-compose down -v --remove-orphans

# Limpiar todo Docker (CUIDADO: afecta todos los contenedores)
docker system prune -a --volumes
```

## 📝 Git Commands (para tu repo)

```bash
# Inicializar repositorio
git init

# Agregar archivos
git add .

# Commit inicial
git commit -m "Initial commit: Complete Task Management API implementation"

# Agregar remote
git remote add origin <tu-repo-url>

# Push
git push -u origin main

# Ver estado
git status

# Ver diferencias
git diff

# Ver log
git log --oneline
```

## 🔐 Security Commands

```bash
# Generar nuevo SECRET_KEY seguro (Python)
python -c "import secrets; print(secrets.token_hex(32))"

# Verificar fortaleza de password
python -c "from app.core.security import pwd_context; print(pwd_context.verify('test', pwd_context.hash('test')))"

# Hash un password manualmente
python -c "from app.core.security import get_password_hash; print(get_password_hash('mypassword'))"
```

## 📦 Production Deployment

```bash
# Build Docker image
docker build -t task-api:latest .

# Run container
docker run -d -p 8000:8000 --name task-api task-api:latest

# Push to registry
docker tag task-api:latest myregistry/task-api:latest
docker push myregistry/task-api:latest

# Deploy con docker-compose (producción)
docker-compose -f docker-compose.prod.yml up -d
```

## 🧪 Testing Scenarios

```bash
# Flujo completo de testing
# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"Admin123!"}' \
  | jq -r '.access_token')

# 2. Crear tarea
TASK_ID=$(curl -s -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","status":"pending"}' \
  | jq -r '.id')

# 3. Actualizar tarea
curl -X PUT "http://localhost:8000/api/v1/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}'

# 4. Eliminar tarea
curl -X DELETE "http://localhost:8000/api/v1/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN"

# Test de error 401
curl -X GET "http://localhost:8000/api/v1/tasks"
# Debe retornar: {"detail":"Not authenticated"}

# Test de error 404
curl -X GET "http://localhost:8000/api/v1/tasks/99999" \
  -H "Authorization: Bearer $TOKEN"
# Debe retornar: {"detail":"Task with id 99999 not found"}
```

## 📊 Performance Testing

```bash
# Instalar apache bench
# Linux: sudo apt-get install apache2-utils
# Mac: brew install httpd

# Test simple de carga (100 requests, 10 concurrent)
ab -n 100 -c 10 -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/tasks

# Test con Locust (requiere instalación)
pip install locust
locust -f locustfile.py

# Monitor performance en tiempo real
watch -n 1 'curl -s http://localhost:8000/health | jq'
```

## 💡 Tips

### Bash Aliases Útiles

Agregar a `~/.bashrc` o `~/.zshrc`:

```bash
# Task API aliases
alias task-start='cd /path/to/project && docker-compose up -d && python run.py'
alias task-stop='docker-compose down'
alias task-logs='docker-compose logs -f'
alias task-db='docker-compose exec postgres psql -U postgres -d technical_test'
alias task-migrate='alembic upgrade head'
alias task-test='curl -X GET http://localhost:8000/health'
```

### PowerShell Functions Útiles

Agregar a `$PROFILE`:

```powershell
function Task-Start {
    docker-compose up -d
    python run.py
}

function Task-Stop {
    docker-compose down
}

function Task-Login {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" `
        -Method POST `
        -Body (@{email="admin@example.com";password="Admin123!"} | ConvertTo-Json) `
        -ContentType "application/json"
    $global:TOKEN = $response.access_token
    Write-Host "Token saved to `$TOKEN variable"
}
```

---

**Pro tip**: Guarda estos comandos en un archivo para referencia rápida durante el desarrollo.
