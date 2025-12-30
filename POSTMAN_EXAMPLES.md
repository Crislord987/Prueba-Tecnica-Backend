# Colección Postman - Task Management API

## Variables de Entorno Sugeridas

Crea estas variables en Postman para facilitar el testing:

```
base_url: http://localhost:8000
api_version: /api/v1
token: (se actualizará automáticamente después del login)
```

## 1. Authentication

### Login (POST)
```
URL: {{base_url}}{{api_version}}/auth/login
Method: POST
Headers:
  Content-Type: application/json

Body (JSON):
{
  "email": "admin@example.com",
  "password": "Admin123!"
}

Expected Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}

Script (Tests) - Guardar token automáticamente:
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Save access token", function () {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.access_token);
});
```

## 2. Health Check

### Get Health Status (GET)
```
URL: {{base_url}}/health
Method: GET

Expected Response (200):
{
  "status": "healthy",
  "service": "Task Management API"
}
```

## 3. Tasks CRUD

**Nota**: Todos los endpoints de tasks requieren el header de autorización:
```
Authorization: Bearer {{token}}
```

### Create Task (POST)
```
URL: {{base_url}}{{api_version}}/tasks
Method: POST
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body (JSON) - Ejemplo 1 (Completo):
{
  "title": "Implementar nueva funcionalidad",
  "description": "Desarrollar el módulo de reportes avanzados",
  "status": "pending"
}

Body (JSON) - Ejemplo 2 (Mínimo):
{
  "title": "Tarea rápida"
}

Expected Response (201):
{
  "id": 11,
  "title": "Implementar nueva funcionalidad",
  "description": "Desarrollar el módulo de reportes avanzados",
  "status": "pending",
  "created_at": "2024-01-15T12:30:00.123456Z",
  "updated_at": "2024-01-15T12:30:00.123456Z"
}
```

### Get All Tasks (GET)
```
URL: {{base_url}}{{api_version}}/tasks
Method: GET
Headers:
  Authorization: Bearer {{token}}

Query Parameters (todos opcionales):
  page: 1
  page_size: 10
  status: pending

Examples:
- Basic: {{base_url}}{{api_version}}/tasks
- Paginated: {{base_url}}{{api_version}}/tasks?page=1&page_size=5
- Filtered: {{base_url}}{{api_version}}/tasks?status=in_progress
- Combined: {{base_url}}{{api_version}}/tasks?page=2&page_size=10&status=done

Expected Response (200):
{
  "items": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "description": "Write comprehensive README and API documentation",
      "status": "in_progress",
      "created_at": "2024-01-15T10:00:00.000000Z",
      "updated_at": "2024-01-15T10:00:00.000000Z"
    }
  ],
  "total": 10,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

### Get Task by ID (GET)
```
URL: {{base_url}}{{api_version}}/tasks/1
Method: GET
Headers:
  Authorization: Bearer {{token}}

Expected Response (200):
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API documentation",
  "status": "in_progress",
  "created_at": "2024-01-15T10:00:00.000000Z",
  "updated_at": "2024-01-15T10:00:00.000000Z"
}

Error Response (404):
{
  "detail": "Task with id 999 not found",
  "status_code": 404
}
```

### Update Task (PUT)
```
URL: {{base_url}}{{api_version}}/tasks/1
Method: PUT
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body (JSON) - Actualizar solo status:
{
  "status": "done"
}

Body (JSON) - Actualizar múltiples campos:
{
  "title": "Documentación completada",
  "description": "README y docs API finalizados",
  "status": "done"
}

Expected Response (200):
{
  "id": 1,
  "title": "Documentación completada",
  "description": "README y docs API finalizados",
  "status": "done",
  "created_at": "2024-01-15T10:00:00.000000Z",
  "updated_at": "2024-01-15T13:00:00.000000Z"
}

Error Response (400):
{
  "detail": "No fields provided for update",
  "status_code": 400
}
```

### Delete Task (DELETE)
```
URL: {{base_url}}{{api_version}}/tasks/1
Method: DELETE
Headers:
  Authorization: Bearer {{token}}

Expected Response: 204 No Content (sin body)

Error Response (404):
{
  "detail": "Task with id 999 not found",
  "status_code": 404
}
```

## 4. Error Cases Testing

### Unauthorized Request (Sin token)
```
URL: {{base_url}}{{api_version}}/tasks
Method: GET

Expected Response (401):
{
  "detail": "Not authenticated"
}
```

### Invalid Token
```
URL: {{base_url}}{{api_version}}/tasks
Method: GET
Headers:
  Authorization: Bearer invalid_token_here

Expected Response (401):
{
  "detail": "Could not validate credentials",
  "status_code": 401
}
```

### Invalid Login Credentials
```
URL: {{base_url}}{{api_version}}/auth/login
Method: POST
Headers:
  Content-Type: application/json

Body:
{
  "email": "wrong@example.com",
  "password": "wrongpassword"
}

Expected Response (401):
{
  "detail": "Incorrect email or password",
  "status_code": 401
}
```

### Validation Error (Campo requerido faltante)
```
URL: {{base_url}}{{api_version}}/tasks
Method: POST
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body:
{
  "description": "Sin título"
}

Expected Response (422):
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "title"],
      "msg": "Field required",
      "input": {"description": "Sin título"}
    }
  ],
  "status_code": 422
}
```

### Invalid Status Value
```
URL: {{base_url}}{{api_version}}/tasks
Method: POST
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body:
{
  "title": "Test task",
  "status": "invalid_status"
}

Expected Response (422):
{
  "detail": [
    {
      "type": "enum",
      "loc": ["body", "status"],
      "msg": "Input should be 'pending', 'in_progress' or 'done'",
      "ctx": {
        "expected": "'pending', 'in_progress' or 'done'"
      }
    }
  ],
  "status_code": 422
}
```

## 5. Flujo Completo de Prueba

### Secuencia recomendada:

1. **Health Check** - Verificar que la API está corriendo
2. **Login** - Obtener token (se guarda automáticamente)
3. **Get All Tasks** - Ver tareas iniciales (deberían haber 10)
4. **Create Task** - Crear nueva tarea
5. **Get Task by ID** - Obtener la tarea recién creada
6. **Update Task** - Cambiar status a "in_progress"
7. **Get All Tasks con filtro** - Filtrar por status "in_progress"
8. **Update Task** - Cambiar status a "done"
9. **Get All Tasks paginadas** - Probar paginación (page=1, page_size=5)
10. **Delete Task** - Eliminar la tarea de prueba

## 6. Tips para Postman

### Auto-refresh del token
Agrega este script en el Pre-request Script de la colección:

```javascript
// Verificar si el token existe
if (!pm.environment.get("token")) {
    console.log("No token found. Please login first.");
}
```

### Test común para todos los endpoints autenticados
```javascript
pm.test("Status code is successful", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 201, 204]);
});

pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

### Limpiar token
```javascript
pm.environment.unset("token");
```

## 7. Archivo JSON para importar

Puedes importar esta configuración creando un archivo JSON con esta estructura:

```json
{
  "info": {
    "name": "Task Management API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"admin@example.com\",\n  \"password\": \"Admin123!\"\n}"
            },
            "url": {
              "raw": "{{base_url}}{{api_version}}/auth/login",
              "host": ["{{base_url}}"],
              "path": ["{{api_version}}", "auth", "login"]
            }
          }
        }
      ]
    }
  ]
}
```

---

**Documentación completa disponible en:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
