#!/usr/bin/env python3
"""Module docstring"""

import psycopg
from db_config import CONFIG

def db_connection():
    """Main function docstring."""
    return psycopg.connect(
        dbname=CONFIG.db_name,
        user=CONFIG.db_user,
        password=CONFIG.db_password,
        host=CONFIG.db_host,
        port=CONFIG.db_port
    )
