
import pandas as pd

class ParquetReader:
    def read_parquet_file(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_parquet(file_path)
            return df
        except Exception as e:
            print(f"Error while reading Parquet file {file_path}: {e}")
            raise e

