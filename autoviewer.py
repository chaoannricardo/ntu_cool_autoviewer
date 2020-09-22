# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import configparser

# read in the configurations.
config = configparser.ConfigParser()
config.read('./view_config.ini')
username = config['login_info']['username']
password = config['login_info']['password']
view_time = int(config['view_settings']['view_time'])
waiting_time = int(config['view_settings']['waiting_time'])
small_interval = int(config['view_settings']['small_interval'])
video_link_list = config['view_settings']['video_link'].split('|')
# 1: Firefox; 2: Chrome
browser_type = config['view_settings']['browser_type']
# 1: Windows; 2: Ubuntu
os_type = config['view_settings']['os_type']

# select driver based on config content
if browser_type == "2" and os_type == "1":
    driver = webdriver.Chrome(executable_path='./drivers/chromedriver.exe')
elif browser_type == "2" and os_type == "2":
    driver = webdriver.Chrome(executable_path='./drivers/chromedriver')
elif browser_type == "1" and os_type == "1":
    driver = webdriver.Firefox(executable_path='./drivers/geckodriver.exe')
elif browser_type == "1" and os_type == "2":
    driver = webdriver.Firefox(executable_path='./drivers/geckodriver')

# select 

for index, video_link in enumerate(video_link_list):
    for i in range(view_time):
        print('# Now watching:', video_link, 'for the', (i+1), 'time')
        if i == 0 and index == 0:
            driver.get(video_link)
            driver.find_element_by_xpath('//*[@id="saml"]').click()
            # input username password and log in
            elem = driver.find_element_by_id('ContentPlaceHolder1_UsernameTextBox')
            elem.clear()
            elem.send_keys(username)
            elem = driver.find_element_by_id('ContentPlaceHolder1_PasswordTextBox')
            elem.clear()
            elem.send_keys(password)
            elem = driver.find_element_by_id('ContentPlaceHolder1_SubmitButton')
            elem.click()
        else:
            driver.get(video_link)

        time.sleep(20)
        # get into the frame and start the video
        driver.switch_to.frame(driver.find_element_by_id('tool_content'))
        # elem = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[5]/button[1]')
        elem = driver.find_element_by_css_selector('.vjs-play-control')
        elem.click()
        
        # switch back to original frame
        # driver.switch_to.default_content()
        seconds_waited = 0
        waiting_batch = 10
        while seconds_waited <= waiting_time:
            time.sleep(waiting_batch)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, 0)")
            seconds_waited += (3 + waiting_batch)
        
        # small interval sleep
        time.sleep(small_interval)


    
    
    

