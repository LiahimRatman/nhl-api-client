"""
NHL API Client - A comprehensive Python client for accessing NHL statistics and data.

This package provides easy access to NHL player statistics, team data, schedules,
standings, and game information through the official NHL API endpoints.
"""

from .client import NHLAPIClient

__version__ = "1.0.0"
__author__ = "Mikhail Korotkov"
__email__ = "ma.korotkov.eu@gmail.com"
__description__ = "A comprehensive Python client for accessing NHL statistics and data"

# Make the main class available at package level
__all__ = ["NHLAPIClient"] 