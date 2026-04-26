import pandas as pd
import time
from selenium.webdriver.common.by import By


def get_table_data_from_elements(driver, filter_date=None):
    """Extracts data from HTML-table and filters it by date."""
    time.sleep(2)
    columns = driver.find_elements(By.CLASS_NAME, "y-column")
    table_data = {}

    for col in columns:
        header = col.find_element(By.ID, "header").text.strip()
        cells = col.find_elements(By.CLASS_NAME, "cell-text")
        values = [cell.text.strip() for cell in cells if cell.text.strip() != header]
        table_data[header] = values

    df = pd.DataFrame(table_data)

    # Mapping of headers
    mapping = {
        'Facility Type': 'facility_name',
        'Visit Date': 'visit_date',
        'Average Time Spent': 'min_time_spent'
    }
    df = df.rename(columns=mapping)

    # --- FILTER ---
    if filter_date and 'visit_date' in df.columns:
        df['visit_date'] = pd.to_datetime(df['visit_date']).dt.strftime('%Y-%m-%d')
        df = df[df['visit_date'] == filter_date]
    # --------------------------

    return df


def read_parquet_with_filter(folder_path, filter_date=None):
    df = pd.read_parquet(folder_path)

    # Mapping of headers
    mapping = {
        'facility_type': 'facility_name',
        'avg_time_spent': 'min_time_spent'
    }

    df = df.rename(columns=mapping)

    df = df[['facility_name', 'visit_date', 'min_time_spent']]

    df['visit_date'] = pd.to_datetime(df['visit_date']).dt.strftime('%Y-%m-%d')
    if filter_date:
        df = df[df['visit_date'] == filter_date]

    return df


def compare_dataframes(df_html, df_parquet):
    """Compares two tables."""
    for df in [df_html, df_parquet]:
        df['facility_name'] = df['facility_name'].astype(str).str.strip()
        df['visit_date'] = df['visit_date'].astype(str).str.strip()
        df['min_time_spent'] = pd.to_numeric(df['min_time_spent']).astype(float).round(2)

        df.sort_values(by=['facility_name', 'visit_date', 'min_time_spent'], inplace=True)
        df.reset_index(drop=True, inplace=True)

    if df_html.equals(df_parquet):
        return True, "Success: Data matches exactly!"
    else:
        diff = pd.concat([df_html, df_parquet]).drop_duplicates(keep=False)
        return False, f"Differences found:\n{diff.to_string()}"
