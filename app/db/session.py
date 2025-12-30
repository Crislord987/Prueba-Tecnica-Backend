import os

# CRÍTICO: Limpiar variables ANTES de importar SQLAlchemy
PROBLEMATIC_VARS = [
    'PGCLIENTENCODING', 'PGSSLMODE', 'PGSSLCERT', 'PGSSLKEY',
    'PGSSLROOTCERT', 'PGPASSFILE', 'PGSERVICEFILE', 'PGOPTIONS',
    'PGAPPNAME', 'CURL_CA_BUNDLE', 'SSL_CERT_FILE', 'REQUESTS_CA_BUNDLE'
]

for var in PROBLEMATIC_VARS:
    os.environ.pop(var, None)

os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'

# Ahora sí importar SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()

# Motor/Config/Conexion DB
engine = create_engine(
    settings.DATABASE_URL,
    # Opciones de pool de conexiones
    #Like tps
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Crea sesiones 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea base de datos declarativas desde clases
# Meta de tablas
Base = declarative_base()


def get_db():
    #Dependency para obtener la sesion con DB.
    #Genera sesion y la cierra
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
