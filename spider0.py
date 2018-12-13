"""
Author Fengyao Yan/University of South Carolina
All Rights Reserved
"""

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp

import json
import time

def init_spider(keyword):
    url = 'http://index.baidu.com/'
    # specify chrome driver directory
    driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')
    driver.get(url)
    with open('cookies.json') as cookieFile:
        cookies = json.load(cookieFile)
    print(cookies)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(url)
    time.sleep(3)
    driver.refresh()
    WebDriverWait(driver, 10, 0.5).until(
        exp.element_to_be_clickable((By.XPATH, "//input[@class='search-input']")))
    driver.find_element_by_xpath("//input[@class='search-input']").send_keys(keyword)
    WebDriverWait(driver, 10, 0.5).until(
        exp.element_to_be_clickable((By.XPATH, "//span[@class='search-input-cancle']")))
    driver.find_element_by_xpath("//span[@class='search-input-cancle']").click()
    driver.maximize_window()
    return driver


# change the keyword you want to use here
keywords = ['王者荣耀','微信','英雄联盟']
Set = set()
for key in keywords:
    Set.clear()
    driver = init_spider(key)
    time.sleep(2)
    WebDriverWait(driver,10,0.5).until(exp.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[2]/div/canvas")))
    canvas = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[2]/div/canvas")
    ActionChains(driver).move_to_element_with_offset(canvas,1189,376).click().perform()
    mIter = 0
    data = []
    while mIter<50:
        WebDriverWait(driver, 10, 0.5).until(exp.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[1]/div/div[1]/canvas")))
        time.sleep(1)
        dIter = 0
        while dIter<30:
            if dIter == 0:
                ActionChains(driver).move_to_element_with_offset(canvas,1196,174).perform()
                time.sleep(1)
            else:
                ActionChains(driver).move_by_offset(-42,0).perform()
                time.sleep(0.1)
            element = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[1]/div")
            Str = element.text
            raw = Str.split()
            if len(raw)>=4 and raw[0] not in Set:
                p = []
                p.append(raw[0])
                p.append(raw[-1])
                print(p)
                data.append(p)
                Set.add(raw[0])
            dIter += 1

        ActionChains(driver).move_to_element_with_offset(canvas, 1244 - (mIter+1)*11, 376).click().perform()
        time.sleep(1)

        mIter += 1

    with open('scrapyData_{c}.txt'.format(c=key),'w') as datafile:
        for da in data:
            datafile.write('{a} {b}\n'.format(a=da[0],b=da[-1]))
