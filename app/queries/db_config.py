#!/usr/bin/env python3
"""Module docstring"""

import configparser

class ConfigManager:
    """Classe qui stocke les attributs de configuration pour une utilisation externe."""
    def __init__(self, config_path, activities_path):
        """Initialisation config."""
        self.config_path = config_path
        config = configparser.ConfigParser()
        config.read(self.config_path)
        self.db_name = config['pg']['dbname']
        self.db_user = config['pg']['user']
        self.db_password = config['pg']['password']
        self.db_host = config['pg']['host']
        self.db_port = config['pg']['port']
        self.activities_path = activities_path

CONFIG = ConfigManager(
    '/app/config.ini',
    '/data/activities.csv'
)
