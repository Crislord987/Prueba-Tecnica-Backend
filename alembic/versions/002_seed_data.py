"""Seed initial user and sample tasks

Revision ID: 002_seed_data
Revises: 001_initial

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Text
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.core.security import get_password_hash
from app.core.config import get_settings

# revision identifiers, used by Alembic.
revision = '002_seed_data'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    settings = get_settings()
    
    # Define tables for seeding
    users_table = table(
        'users',
        column('id', Integer),
        column('email', String),
        column('hashed_password', String),
    )
    
    tasks_table = table(
        'tasks',
        column('id', Integer),
        column('title', String),
        column('description', Text),
        column('status', String),
    )
    
    # Insert initial user
    op.bulk_insert(
        users_table,
        [
            {
                'email': settings.INITIAL_USER_EMAIL,
                'hashed_password': get_password_hash(settings.INITIAL_USER_PASSWORD),
            }
        ]
    )
    
    # Insert sample tasks
    op.bulk_insert(
        tasks_table,
        [
            {
                'title': 'Complete project documentation',
                'description': 'Write comprehensive README and API documentation',
                'status': 'in_progress',
            },
            {
                'title': 'Implement user authentication',
                'description': 'Set up JWT authentication with secure password hashing',
                'status': 'done',
            },
            {
                'title': 'Add pagination to task list',
                'description': 'Implement cursor-based pagination for better performance',
                'status': 'done',
            },
            {
                'title': 'Write unit tests',
                'description': 'Create comprehensive test suite for all endpoints',
                'status': 'pending',
            },
            {
                'title': 'Set up CI/CD pipeline',
                'description': 'Configure GitHub Actions for automated testing and deployment',
                'status': 'pending',
            },
            {
                'title': 'Optimize database queries',
                'description': 'Add appropriate indexes and optimize N+1 queries',
                'status': 'in_progress',
            },
            {
                'title': 'Implement rate limiting',
                'description': 'Add rate limiting middleware to prevent abuse',
                'status': 'pending',
            },
            {
                'title': 'Add logging and monitoring',
                'description': 'Set up structured logging and application monitoring',
                'status': 'pending',
            },
            {
                'title': 'Create Docker deployment',
                'description': 'Containerize application for easy deployment',
                'status': 'pending',
            },
            {
                'title': 'Review code quality',
                'description': 'Perform code review and refactoring where necessary',
                'status': 'pending',
            },
        ]
    )


def downgrade() -> None:
    # Delete sample data
    op.execute("DELETE FROM tasks WHERE id <= 10")
    op.execute("DELETE FROM users WHERE id = 1")
