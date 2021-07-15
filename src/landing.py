import base64
import time

import matplotlib.image as mpimg
import streamlit as st
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
    
def reload_qr(landing_main):
    try:
        but = landing_main.find_element(by = By.XPATH, value = './div/div[2]/div/span/button')
        but.click()
        time.sleep(3)
        return True
    except:
        return False

def plot_qr(driver, landing_main):

    
    canvas = landing_main.find_element(by = By.XPATH, value = './div/div[2]/div/canvas')


    # get the canvas as a PNG base64 string
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)

    # decode
    canvas_png = base64.b64decode(canvas_base64)

    # # save to a file
    with open(r"scan.png", 'wb') as f:
        f.write(canvas_png)

    img = mpimg.imread(r"scan.png")
    st.image(img)
    # plt.show()

def landing_mainloop(driver):
    landing_main = get_landing_main(driver)
    reload_qr(landing_main)
    plot_qr(driver, landing_main)
