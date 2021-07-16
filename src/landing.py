import base64
import time

import dash_core_components as dcc
import dash_html_components as html
import matplotlib.image as mpimg
import streamlit as st
from dash_extensions.enrich import (Dash, FileSystemStore, Input, Output,
                                    ServersideOutput, Trigger)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def is_landing_main(driver):
    try:
        driver.find_element_by_class_name("landing-main")
        return True
    except:
        return False

def get_landing_main(driver):
    landing_main = driver.find_element_by_class_name("landing-main")
    return landing_main
    
def _reload_qr(landing_main):
    try:
        but = landing_main.find_element(by = By.XPATH, value = './div/div[2]/div/span/button')
        but.click()
        time.sleep(3)
        return True
    except:
        return False

def _get_qr(driver, landing_main):

    
    canvas = landing_main.find_element(by = By.XPATH, value = './div/div[2]/div/canvas')


    # get the canvas as a PNG base64 string
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)

    return canvas_base64
    # # decode
    # canvas_png = base64.b64decode(canvas_base64)
    # # # # save to a file
    # from config import PROJECT_DIR
    # with open(str(PROJECT_DIR / 'src' / 'assets' / r"scan.png"), 'wb') as f:
    #     f.write(canvas_png)
    # return r"scan.png"
    # img = mpimg.imread(r"scan.png")
    # return img
    # st.image(img)
    # plt.show()

def landing_get_image(driver):
    landing_main = get_landing_main(driver)
    _reload_qr(landing_main)
    img = _get_qr(driver, landing_main)
    return img
