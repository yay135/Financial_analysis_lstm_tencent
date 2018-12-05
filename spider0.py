from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp
import time
import csv

def init_spider(keyword):
    url = 'http://index.baidu.com/'
    # specify chrome driver directory
    driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')
    driver.get(url)
    cookies=[
{
    "domain": ".baidu.com",
    "expirationDate": 3679589691.479167,
    "hostOnly": False,
    "httpOnly": False,
    "name": "BAIDUID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "DBE7140369D767FA9EB28F8D0B666970:FG=1",
    "id": 1
},
{
    "domain": ".baidu.com",
    "expirationDate": 1543961549.202327,
    "hostOnly": False,
    "httpOnly": True,
    "name": "bdindexid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "t6fmmlo9ff3lgsj9bv6igdv050",
    "id": 2
},
{
    "domain": ".baidu.com",
    "expirationDate": 1543974483.244976,
    "hostOnly": False,
    "httpOnly": False,
    "name": "BDORZ",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "B490B5EBF6F3CD402E515D22BCDA1598",
    "id": 3
},
{
    "domain": ".baidu.com",
    "hostOnly": False,
    "httpOnly": False,
    "name": "BDRCVFR[feWj1Vr5u3D]",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": True,
    "storeId": "0",
    "value": "I67x6TjHwwYf0",
    "id": 4
},
{
    "domain": ".baidu.com",
    "expirationDate": 1803075143.939925,
    "hostOnly": False,
    "httpOnly": True,
    "name": "BDUSS",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "WgxLXdrOFFyVDF-YlRGaHA4TWs3am1MR253cGN-RnpyVVZFWW5mc05SRklOeTFjQVFBQUFBJCQAAAAAAAAAAAEAAADPAD3qeWFuZnkxMzUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEiqBVxIqgVcb",
    "id": 5
},
{
    "domain": ".baidu.com",
    "expirationDate": 3679589691.479224,
    "hostOnly": False,
    "httpOnly": False,
    "name": "BIDUPSID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "DBE7140369D767FA9EB28F8D0B666970",
    "id": 6
},
{
    "domain": ".baidu.com",
    "hostOnly": False,
    "httpOnly": False,
    "name": "delPer",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": True,
    "storeId": "0",
    "value": "0",
    "id": 7
},
{
    "domain": ".baidu.com",
    "hostOnly": False,
    "httpOnly": False,
    "name": "H_PS_PSSID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": True,
    "storeId": "0",
    "value": "26524_1447_21120_26350_27244_22157",
    "id": 8
},
{
    "domain": ".baidu.com",
    "hostOnly": False,
    "httpOnly": False,
    "name": "PSINO",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": True,
    "storeId": "0",
    "value": "7",
    "id": 9
},
{
    "domain": ".baidu.com",
    "expirationDate": 3679589691.479264,
    "hostOnly": False,
    "httpOnly": False,
    "name": "PSTM",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "1532106046",
    "id": 10
},
{
    "domain": ".index.baidu.com",
    "hostOnly": False,
    "httpOnly": False,
    "name": "Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": True,
    "storeId": "0",
    "value": "1543888086",
    "id": 11
},
{
    "domain": ".index.baidu.com",
    "expirationDate": 1575424085,
    "hostOnly": False,
    "httpOnly": False,
    "name": "Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "1543875118,1543883360,1543886628,1543888086",
    "id": 12
},
{
    "domain": "index.baidu.com",
    "expirationDate": 1543961545.526042,
    "hostOnly": True,
    "httpOnly": False,
    "name": "CHKFORREG",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "a61c5b4f1f43a131b3d2718753287819",
    "id": 13
}]
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
keywords = ['王者荣耀','微信','英雄联盟','qq']
Set = set()
for key in keywords:
    Set.clear()
    driver = init_spider(key)
    time.sleep(2)
    WebDriverWait(driver,10,0.5).until(exp.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[2]/div/canvas")))
    canvas = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[2]/div/canvas")
    ActionChains(driver).move_to_element_with_offset(canvas,1244,376).click().perform()
    mIter = 0
    data = []
    while mIter<50:
        WebDriverWait(driver, 10, 0.5).until(exp.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[1]/div/div[1]/canvas")))
        time.sleep(1)
        dIter = 0
        while dIter<30:
            if dIter == 0:
                ActionChains(driver).move_to_element_with_offset(canvas,1253,241).perform()
                time.sleep(1)
            else:
                ActionChains(driver).move_by_offset(-43,0).perform()
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

        ActionChains(driver).move_to_element_with_offset(canvas, 1244 - (mIter+1)*12, 376).click().perform()
        time.sleep(1)

        mIter += 1

    with open('scrapyData_{c}.txt'.format(c=key),'w') as datafile:
        for da in data:
            datafile.write('{a} {b}\n'.format(a=da[0],b=da[-1]))
