import time

import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from clear_massages import clear
from landing import is_landing_main, landing_mainloop
from taken import is_taken, log_out, refresh
from utils import read_data, save_data


@st.cache
def init_driver():
    url = 'https://web.whatsapp.com/'

    # chrome_driver_path = 'chromedriver_win32/chromedriver.exe'
    # op = webdriver.ChromeOptions()
    # # op.add_argument('headless')

    # driver = webdriver.Chrome(chrome_driver_path)
    # driver.get(url)

    
    options = FirefoxOptions()
    # options.add_argument("--headless")

    driver = webdriver.Firefox(executable_path = 'geckodriver-v0.29.1-win64/geckodriver.exe', options=options)#, chrome_options=op)
    driver.get(url)

    time.sleep(20)
    url = driver.command_executor._url
    session_id = driver.session_id 

    return url, session_id

def get_driver(url, session_id):
    driver = webdriver.Remote(command_executor=url,desired_capabilities={})
    # driver.close()   # this prevents the dummy browser
    driver.session_id = session_id
    st.write(is_landing_main(driver))
    return driver


def randomUserAgent():
    from random_user_agent.user_agent import UserAgent

    # software_types  = [SoftWareType.FIREFOX.value]
    # software_names   = [SoftWareName.WEB_BROWSER.value]
    user_agent_rotator = UserAgent()#(software_names=software_names,software_types=software_types)
    ua = user_agent_rotator.get_random_user_agent()
    return ua

class SessionRemote(webdriver.Remote):
    def start_session(self, desired_capabilities, browser_profile=None):
        # Skip the NEW_SESSION command issued by the original driver
        # and set only some required attributes
        self.w3c = True

def attach_to_session(executor_url, session_id):
    
    original_execute = webdriver.Remote.execute
    # def new_command_execute(self, command, params=None):
    #     if command == "newSession":
    #         # Mock the response
    #         return {'success': 0, 'value': None, 'sessionId': session_id}
    #     else:
    #         return original_execute(self, command, params)
    new_command_execute = original_execute
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute

    ua = randomUserAgent()
    opts = RemoteWebDriverOptions()
    opts.add_argument(ua)

    driver = SessionRemote(command_executor=executor_url, desired_capabilities={}, options = opts)
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver

def app():
    st.title('Whatsapp Cleaner')
    
    url, session_id = init_driver()
    driver = attach_to_session(url, session_id)
    
    if is_landing_main(driver):
        st.write('load QR:')
        landing_mainloop(driver)
    elif is_taken(driver):
        st.write('משתמשים במקום אחר. מה לעשות?')
        if st.button('Refresh'):
            refresh(driver)
        if st.button('Sign out'):
            log_out(driver)
        
    else:
        if st.button('Clear !'):
            clear(driver)


if __name__ == "__main__":
    app()
