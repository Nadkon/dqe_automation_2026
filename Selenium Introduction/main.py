import time
import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class SeleniumWebDriverContextManager:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.driver = None

    def __enter__(self):
        # Browser launch
        self.driver = webdriver.Chrome(options=self.options)
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        # Automatically browser closing
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    # Path to the report
    file_path = os.path.abspath("report.html")

    with SeleniumWebDriverContextManager() as driver:
        # Local HTML file opening
        driver.get(f"file://{file_path}")
        wait = WebDriverWait(driver, 10)

        try:
            # --- 1. WORK with TABLE ---
            table_root = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "table")))
            table_by_css = driver.find_element(By.CSS_SELECTOR, ".table")
            table_by_xpath = driver.find_element(By.XPATH, "//*[@class='table']")

            print("The table is found with the help of 3 methods!")

            columns = table_root.find_elements(By.CLASS_NAME, "y-column")
            table_data = {}

            for col in columns:
                header_text = col.find_element(By.ID, "header").text.strip()
                cells = col.find_elements(By.CLASS_NAME, "cell-text")
                # Extraction of text (without headers)
                values = [cell.text for cell in cells if cell.text != header_text]
                table_data[header_text] = values

            # Uloading the table into  CSV
            pd.DataFrame(table_data).to_csv("table.csv", index=False)
            print("table.csv is saved")

            # --- 2. WORK with DIAGRAM ---
            doughnut = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pielayer")))

            # Screenshot of the initial status (screenshot0)
            driver.save_screenshot("screenshot0.png")
            print("screenshot0.png is saved")

            # Searching for filters
            filters = driver.find_elements(By.CLASS_NAME, "traces")

            for i, f in enumerate(filters):
                ActionChains(driver).move_to_element(f).click().perform()
                time.sleep(2)

                # Screenshot of the current status
                driver.save_screenshot(f"screenshot{i + 1}.png")

                # Collecting data presented on diagram
                labels = doughnut.find_elements(By.CSS_SELECTOR, "text.slicetext[data-notex='1']")
                chart_data_list = []

                for label in labels:
                    lines = label.find_elements(By.TAG_NAME, "tspan")
                    if len(lines) >= 2:
                        chart_data_list.append({
                            "Facility Type": lines[0].text,
                            "Min Average Time Spent": lines[1].text
                        })

                # Saving CSV for the currecn filter
                if chart_data_list:
                    pd.DataFrame(chart_data_list).to_csv(f"doughnut{i}.csv", index=False)
                    print(f"Filter {i + 1} processed: screenshot and CSV are saved")

        except Exception as e:
            print(f"ERROR: {e}")
