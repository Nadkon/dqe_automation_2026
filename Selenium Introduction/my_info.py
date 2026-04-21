# Default driver usage:
from selenium import webdriver

# Create a WebDriver instance for Firefox
driver = webdriver.Firefox()

# Open a website
driver.get("https://www.example.com")

# Close the browser
driver.quit()


# Explicit driver usage:
# Specify the path to the ChromeDriver executable
driver_path = "path/to/chromedriver"

# Create a WebDriver instance for Chrome
driver = webdriver.Chrome(executable_path=driver_path)