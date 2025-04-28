from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging
import os
import shutil
import time
from settings import DOWNLOAD_DIR, TARGET_DIR


def download(driver, link):
    driver.get(link)
    pass

def main():
    snapshot = os.listdir(DOWNLOAD_DIR)
    
    driver = webdriver.Chrome()
    driver.get('https://www.mtgo.com/decklists')
    decklist_list = driver.find_element(By.CLASS_NAME, 'decklists-list').find_elements(By.CLASS_NAME, 'decklists-item')
    links = [item.find_element(By.CLASS_NAME, 'decklists-link').get_attribute('href') for item in decklist_list]
    
    for link in links[:1]:
        driver.get(link)
        buttons = driver.find_elements(By.CLASS_NAME, 'decklist-download')
        
        for element in driver.find_elements(By.CLASS_NAME, 'decklist-download'):
            try:
                element.click()
                time.sleep(1)
            except Exception as e:
                logging.info(e)
                

        downloaded_files = [file for file in os.listdir(DOWNLOAD_DIR) if file not in snapshot]
        for file in downloaded_files:
            new_name = file.replace(' ', '_')
            shutil.move(DOWNLOAD_DIR + file, TARGET_DIR + new_name)
    
    
def test():
    link = 'https://www.mtgo.com/decklist/modern-league-2025-04-269065'
      
    driver = webdriver.Chrome()
    driver.get(link)
    driver.find_element(By.CLASS_NAME, 'decklist-download').click()
    time.sleep(1)
    input()
        
        
if __name__ == '__main__':
    main()
    