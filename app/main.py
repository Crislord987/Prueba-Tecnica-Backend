import os
import sys

# Lista de variables problemáticas en Windows
PROBLEMATIC_VARS = [
    'PGCLIENTENCODING', 'PGSSLMODE', 'PGSSLCERT', 'PGSSLKEY',
    'PGSSLROOTCERT', 'PGPASSFILE', 'PGSERVICEFILE', 'PGOPTIONS',
    'PGAPPNAME', 'CURL_CA_BUNDLE', 'SSL_CERT_FILE', 'REQUESTS_CA_BUNDLE'
]

# Limpiar ANTES de importar cualquier cosa
for var in PROBLEMATIC_VARS:
    os.environ.pop(var, None)

# Configurar encoding UTF-8
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, tasks

# Crear app
app = FastAPI(
    title="Task Management API",
    description="API REST para gestión de tareas con autenticación JWT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])

# Health check
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Task Management API"
    }

@app.get("/")
def root():
    """Root endpoint - redirect to docs"""
    return {
        "message": "Task Management API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
