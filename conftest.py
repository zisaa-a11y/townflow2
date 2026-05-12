"""
Pytest configuration for TownFlow backend.

This file configures pytest for the entire project.
"""

import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Pytest markers for organizing tests
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


# Create test database using SQLite for faster tests
def pytest_db_configure(config):
    """Configure test database."""
    # This can be overridden in pytest.ini or environment variables
    pass
