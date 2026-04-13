import pandas as pd


class DataQualityLibrary:
    """
    A library of static methods for performing data quality checks on pandas DataFrames.

    This class is intended to be used in a PyTest-based testing framework to validate
    the quality of data in DataFrames. Each method performs a specific data quality
    check and uses assertions to ensure that the data meets the expected conditions.
    """

    @staticmethod
    def check_duplicates(df, column_names=None):
        target_data = df[column_names] if column_names else df

        total_rows = len(target_data)
        unique_rows_count = len(target_data.drop_duplicates())

        assert total_rows == unique_rows_count, (
            f"The duplicated rows have been found! Total number of rows received: {total_rows}, "
            f"number of unique rows: {unique_rows_count}"
        )

    @staticmethod
    def check_count(source_count, target_count):
        source_count = len(source_count)
        target_count = len(target_count)
        assert source_count == target_count, \
            f"Row number is not the same: Postgres={source_count}, Parquet={target_count}"

    @staticmethod
    def check_data_full_data_set(source_count, target_count):
        pd.testing.assert_frame_equal(source_count, target_count)

    @staticmethod
    def check_dataset_is_not_empty(df):
        assert not df.empty, "The dataset is empty! No data found."

    @staticmethod
    def check_not_null_values(df, column_names=None):
        for col in column_names:
            null_count = df[col].isnull().sum()
            assert null_count == 0, (
                f"Column '{col}' contains {null_count} null values! "
                f"Validation failed for the dataset."
            )
