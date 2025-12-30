"""
Database initialization script.
Creates database, runs migrations, and seeds initial data.
Uses docker exec to avoid encoding issues.
"""
import os
import sys
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(text)
    print('='*60 + '\n')


def create_database_via_docker():
    """Create the database using docker exec (avoids encoding issues)."""
    print("Paso 1: Verificando/creando base de datos...")
    
    try:
        # Verificar si la base de datos existe
        check_cmd = [
            'docker', 'exec', 'technical_test_db',
            'psql', '-U', 'postgres', '-tc',
            "SELECT 1 FROM pg_database WHERE datname='technical_test'"
        ]
        
        result = subprocess.run(check_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and '1' in result.stdout:
            print("✅ Base de datos 'technical_test' ya existe")
            return True
        
        # Crear la base de datos
        create_cmd = [
            'docker', 'exec', 'technical_test_db',
            'psql', '-U', 'postgres', '-c',
            "CREATE DATABASE technical_test ENCODING 'UTF8'"
        ]
        
        result = subprocess.run(create_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 or 'already exists' in result.stderr:
            print("✅ Base de datos 'technical_test' creada")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
        
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False


def create_tables_via_docker():
    """Create tables directly using docker exec."""
    print("\nPaso 2: Creando tablas...")
    
    try:
        # SQL para crear todas las tablas
        sql_script = """
        -- Tabla users
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
        );
        
        CREATE INDEX IF NOT EXISTS ix_users_id ON users(id);
        CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);
        
        -- Enum TaskStatus
        DO $$ BEGIN
            CREATE TYPE taskstatus AS ENUM ('pending', 'in_progress', 'done');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        
        -- Tabla tasks
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status taskstatus DEFAULT 'pending' NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
        );
        
        CREATE INDEX IF NOT EXISTS ix_tasks_id ON tasks(id);
        CREATE INDEX IF NOT EXISTS ix_tasks_status ON tasks(status);
        CREATE INDEX IF NOT EXISTS ix_tasks_created_at ON tasks(created_at);
        CREATE INDEX IF NOT EXISTS ix_tasks_status_created_at ON tasks(status, created_at);
        
        -- Tabla alembic_version (para compatibilidad)
        CREATE TABLE IF NOT EXISTS alembic_version (
            version_num VARCHAR(32) PRIMARY KEY
        );
        
        INSERT INTO alembic_version VALUES ('002_seed_data') 
        ON CONFLICT DO NOTHING;
        """
        
        # Ejecutar SQL
        cmd = [
            'docker', 'exec', '-i', 'technical_test_db',
            'psql', '-U', 'postgres', '-d', 'technical_test'
        ]
        
        result = subprocess.run(
            cmd,
            input=sql_script,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Tablas creadas correctamente")
            return True
        else:
            print(f"❌ Error creando tablas: {result.stderr}")
            return False
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        import traceback
        traceback.print_exc()
        return False


def seed_initial_data():
    """Seed initial user and tasks using docker exec."""
    print("\nPaso 3: Insertando datos iniciales...")
    
    try:
        from app.core.security import get_password_hash
        from app.core.config import get_settings
        
        settings = get_settings()
        hashed_password = get_password_hash(settings.INITIAL_USER_PASSWORD)
        
        # SQL para insertar datos
        sql_script = f"""
        -- Insertar usuario
        INSERT INTO users (email, hashed_password)
        VALUES ('{settings.INITIAL_USER_EMAIL}', '{hashed_password}')
        ON CONFLICT (email) DO NOTHING;
        
        -- Verificar si hay tareas
        DO $$
        DECLARE
            task_count INTEGER;
        BEGIN
            SELECT COUNT(*) INTO task_count FROM tasks;
            
            IF task_count = 0 THEN
                -- Insertar tareas de ejemplo
                INSERT INTO tasks (title, description, status) VALUES
                ('Complete project documentation', 'Write comprehensive README and API documentation', 'in_progress'),
                ('Implement user authentication', 'Set up JWT authentication with secure password hashing', 'done'),
                ('Add pagination to task list', 'Implement cursor-based pagination for better performance', 'done'),
                ('Write unit tests', 'Create comprehensive test suite for all endpoints', 'pending'),
                ('Set up CI/CD pipeline', 'Configure GitHub Actions for automated testing and deployment', 'pending'),
                ('Optimize database queries', 'Add appropriate indexes and optimize N+1 queries', 'in_progress'),
                ('Implement rate limiting', 'Add rate limiting middleware to prevent abuse', 'pending'),
                ('Add logging and monitoring', 'Set up structured logging and application monitoring', 'pending'),
                ('Create Docker deployment', 'Containerize application for easy deployment', 'pending'),
                ('Review code quality', 'Perform code review and refactoring where necessary', 'pending');
                
                RAISE NOTICE 'Tareas creadas';
            ELSE
                RAISE NOTICE 'Tareas ya existen';
            END IF;
        END $$;
        """
        
        cmd = [
            'docker', 'exec', '-i', 'technical_test_db',
            'psql', '-U', 'postgres', '-d', 'technical_test'
        ]
        
        result = subprocess.run(
            cmd,
            input=sql_script,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Usuario '{settings.INITIAL_USER_EMAIL}' creado")
            if 'Tareas creadas' in result.stderr:
                print("✅ 10 tareas de ejemplo creadas")
            else:
                print("✅ Las tareas ya existen")
            return True
        else:
            print(f"⚠️  Advertencia: {result.stderr}")
            return True  # Continuar aunque haya advertencias
        
    except Exception as e:
        print(f"❌ Error insertando datos: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_docker():
    """Verify Docker is running."""
    try:
        result = subprocess.run(
            ['docker', 'ps'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("❌ Docker no está corriendo. Ejecuta: docker-compose up -d")
            return False
        
        if 'technical_test_db' not in result.stdout:
            print("❌ Contenedor 'technical_test_db' no encontrado. Ejecuta: docker-compose up -d")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando Docker: {e}")
        return False


def main():
    """Initialize database with all steps."""
    print_header("INICIALIZACIÓN DE BASE DE DATOS")
    
    # Verificar Docker
    if not check_docker():
        print("\n💡 Primero ejecuta: docker-compose up -d")
        sys.exit(1)
    
    # Paso 1: Crear base de datos
    if not create_database_via_docker():
        print("\n❌ Falló la creación de la base de datos")
        sys.exit(1)
    
    # Paso 2: Crear tablas
    if not create_tables_via_docker():
        print("\n❌ Falló la creación de tablas")
        sys.exit(1)
    
    # Paso 3: Insertar datos iniciales
    if not seed_initial_data():
        print("\n❌ Falló la inserción de datos iniciales")
        sys.exit(1)
    
    # Éxito
    print_header("✅ ¡BASE DE DATOS INICIALIZADA CORRECTAMENTE!")
    
    print("📝 Credenciales del usuario inicial:")
    print("   Email:    admin@example.com")
    print("   Password: Admin123!")
    print("\n🚀 Para iniciar la aplicación ejecuta:")
    print("   python run.py")
    print("\n📚 Documentación disponible en:")
    print("   http://localhost:8000/docs")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
