
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_wh_app(driver):
    wh_app = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'app'))
        )
    return wh_app

def is_taken(driver):
    try:
        wh_app = get_wh_app(driver)
        new_path = wh_app.find_element_by_xpath('./div/div/div/div/div/div/div').text
        is_closed = new_path == 'WhatsApp פתוח במחשב או דפדפן אחר. לחץ/י על "השתמש כאן" כדי להשתמש ב-WhatsApp Web בחלון זה.'
        return is_closed
    except:
        return False
    
def refresh(driver):
    wh_app = get_wh_app(driver)
    refresh_button = wh_app.find_element_by_xpath('./div/div/div/div/div/div/div/div[2]/div/div')
    refresh_button.click()
    time.sleep(5)

def log_out(driver):
    wh_app = get_wh_app(driver)
    quit_button = wh_app.find_element_by_xpath('./div/div/div/div/div/div/div/div[1]/div/div')
    quit_button.click()
    time.sleep(15)

