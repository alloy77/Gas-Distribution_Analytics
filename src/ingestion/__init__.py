"""Pipeline ingestion package."""
from .ingestion import ingest_data
from .file_reader import read_csv

__all__ = ["ingest_data", "read_csv"]
