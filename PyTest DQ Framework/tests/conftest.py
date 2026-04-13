import pytest
from src.connectors.postgres.postgres_connector import PostgresConnectorContextManager
from src.data_quality.data_quality_validation_library import DataQualityLibrary
from src.connectors.file_system.parquet_reader import ParquetReader

def pytest_addoption(parser):
    parser.addoption("--db_host", action="store", default="localhost", help="Database host")
    parser.addoption("--db_port", action="store", default="5432")
    parser.addoption("--db_name", action="store", default="postgres")
    parser.addoption("--db_user", action="store", required=True)
    parser.addoption("--db_password", action="store", required=True)
    parser.addoption("--parquet_path", action="store", required=True)

def pytest_configure(config):
    """
    Validates that all required command-line options are provided.
    """
    required_options = [
        "--db_user", "--db_password", "db_host", "parquet_path"
    ]
    for option in required_options:
        if not config.getoption(option):
            pytest.fail(f"Missing required option: {option}")

@pytest.fixture(scope='session')
def db_connection(request):
    db_params = {
        "db_host": request.config.getoption("--db_host"),
        "db_port": request.config.getoption("--db_port"),
        "db_name": request.config.getoption("--db_name"),
        "db_user": request.config.getoption("--db_user"),
        "db_password": request.config.getoption("--db_password"),
    }
    try:
        with PostgresConnectorContextManager(**db_params) as db_connector:
            yield db_connector
    except Exception as e:
        pytest.fail(f"Failed to initialize PostgresConnectorContextManager: {e}")


@pytest.fixture(scope='session')
def parquet_reader():
    try:
        reader = ParquetReader()
        yield reader
    except Exception as e:
        pytest.fail(f"Failed to initialize ParquetReader: {e}")


@pytest.fixture(scope='session')
def data_quality_library():
    try:
        library = DataQualityLibrary()
        yield library
    except Exception as e:
        pytest.fail(f"Failed to initialize DQ Library: {e}")

# 5. Фікстури для ДАНИХ (DataFrames), які ми будемо передавати в тести
@pytest.fixture(scope='session')
def source_data(db_connection):
    """Отримуємо дані з Postgres"""
    return db_connection.get_data_sql("SELECT * FROM core_table")

@pytest.fixture(scope='session')
def target_data(request, parquet_reader):
    """Отримуємо дані з Parquet файлу"""
    path = request.config.getoption("--parquet_path")
    return parquet_reader.read_parquet_file(path)