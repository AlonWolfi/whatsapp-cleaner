import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CLEAR = False

def is_clear():
    global CLEAR
    return CLEAR

def get_pane_side(driver, seconds_to_wait = 50):
    pane_side = WebDriverWait(driver, seconds_to_wait).until(
        EC.presence_of_element_located((By.ID, 'pane-side'))
    )
    driver.execute_script(f'arguments[0].scrollTop = 0', pane_side)
    return pane_side

def get_chats(pane_side):
    return pane_side.find_elements(by = By.CSS_SELECTOR, value = "#pane-side>div>div>div>div")

def is_chat_unread_and_silent(chat):
    try:
#         name = chat.find_element(By.XPATH,"./div/div/div[2]/div[1]/div/span").get_attribute('title')
#         print(name)
        bar = chat.find_element(By.XPATH,"./div/div/div[2]/div[2]")
        first_div = bar.find_element(By.XPATH,"./div[2]/span[1]/div[1]")
        is_silent = first_div.get_attribute('aria-label') == "צ'אט מושתק"
        second_div = bar.find_element(By.XPATH,"./div[2]/span[1]/div[2]/span")
#         print('הודעות' in second_div.get_attribute('aria-label'))
        num_unread = second_div.text
        is_unread = num_unread != ''
        return is_unread and is_silent
    except:
        return False
    
def scroll_chats(driver, pane_side, step_size = 500):
    current_height = int(pane_side.get_attribute('scrollTop'))
    top_height = int(pane_side.get_attribute('scrollTop'))
    next_height = max(current_height + step_size, top_height)
    driver.execute_script(f'arguments[0].scrollTop = {next_height}', pane_side)
    
    finish_scrolling = (next_height == top_height)
    return finish_scrolling
 

def clear(driver):
    global CLEAR
    CLEAR = True
    pane_side = get_pane_side(driver, 10)
    finish_scrolling = False
    allclear_counter = 0
    while(not finish_scrolling):
        chats = get_chats(pane_side)
        allclear_counter += 1
        
        for chat in chats:
            if is_chat_unread_and_silent(chat):
                allclear_counter = 0
                chat.click()
                time.sleep(0.1)
        finish_scrolling = scroll_chats(driver, pane_side)
        
        if allclear_counter > 5:
            finish_scrolling = True
        time.sleep(0.5)
    time.sleep(2)
    CLEAR = False
