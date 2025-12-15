"""Data Sources Package

Dit package bevat alle implementaties voor verschillende databronnen.

Het Strategy Pattern wordt hier toegepast: verschillende implementaties
(DatabaseSource, CSVSource) kunnen uitgewisseld worden zonder dat de
rest van de applicatie aangepast moet worden.
"""

from .database_source import DatabaseSource
from .csv_source import CSVSource

__all__ = ['DatabaseSource', 'CSVSource']
