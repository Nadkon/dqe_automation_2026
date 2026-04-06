import os.path
from pathlib import Path
import pytest
import csv
import pandas as pd

# Fixture to read the CSV file
@pytest.fixture(scope="session")
def read_csv():
    def _read(path_to_file):
        assert Path(path_to_file).exists(), f"Error: The file is not found on: {path_to_file}"

        with open(path_to_file, mode='r', encoding='utf-8') as f:
            return list(csv.reader(f))

    return _read


@pytest.fixture(scope="session")
def csv_data(read_csv):
    current_dir = Path(__file__).parent
    file_path = current_dir.parent / "src" / "data" / "data.csv"

    return read_csv(file_path)

# Fixture to validate the schema of the file
@pytest.fixture(scope="session")
def validate_schema():
    def _validate(actual_schema, expected_schema):
        assert actual_schema == expected_schema, (
            f"The schema is incorrect!\n"
            f"Expected: {expected_schema}\n"
            f"Received: {actual_schema}"
        )
    return _validate


@pytest.fixture(scope="session")
def expected_csv_schema():
    """Допоміжна фікстура для еталонної схеми"""
    return ["id", "name", "age", "email", "is_active"]

# Pytest hook to mark unmarked tests with a custom mark


def pytest_collection_modifyitems(items):
    for item in items:
        if not item.own_markers:
            item.add_marker(pytest.mark.unmarked)
