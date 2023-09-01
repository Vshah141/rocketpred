# pip install selenium
# pip install bs4

import logging
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from selenium.webdriver.common.by import By

logging.basicConfig(filename='web_scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # Set up the Chrome driver (you need to have the Chrome driver executable in the same directory or in PATH)
    driver = webdriver.Chrome()

    url = "https://finance.yahoo.com/quote/TSLA/history?period1=1661817600&period2=1693267200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
    logging.info("Opening the URL: %s", url)
    driver.get(url)
    
    driver.implicitly_wait(10)
    logging.info("Dynamic content loaded")

    # Get the page source after dynamic content is loaded
    page_source = driver.page_source

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the historical data table element
    table = soup.find('table', {'class': 'W(100%)'})

    # # Find the historical data table element using the By.XPATH locator
    # table = driver.find_element(By.XPATH, "//table[contains(@class, 'W(100%)')]")

    # Extract table data
    table_data = []
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            row_data.append(cell.get_text(strip=True))
        if row_data:
            table_data.append(row_data)
        
    # # Extract table data
    # table_data = []
    # for row in table.find_elements(By.TAG_NAME, 'tr'):
    #     row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]
    #     if row_data:  # Exclude empty rows
    #         table_data.append(row_data)

    for row in table_data:
        logging.info("Table data: %s", row)
    
    # # Print table data
    # for row in table_data:
    #     print(row)
except ( TimeoutException, NoSuchElementException) as e:
    logging.error("An exception occurred: %s", str(e))
    
finally:
    try:
        # Close the web driver
        driver.quit()
        logging.info("Web driver closed")
    except NameError:
        pass