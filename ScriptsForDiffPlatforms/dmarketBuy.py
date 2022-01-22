import os
from selenium import webdriver
import random
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import linecache
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import mysql.connector
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import requests


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


executable_path = "C:\\Users\\Dr1m\\Desktop\\skinsautomation\\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = executable_path


chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_extension('C:\\Users\\Dr1m\\Desktop\\skins\\TradeAssistant.crx')
chrome_options.add_argument("user-data-dir=C:\\Default1")
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)





wait = WebDriverWait(driver, 10)  # время вылета 10сек

driver.set_window_size("1920", "1080")

now = datetime.now()
date_start = now.strftime("%d/%m/%Y %H:%M:%S")


def dates_between(d_now, d_get):
    d_get = datetime.strptime(d_get, "%d/%m/%Y %H:%M:%S")
    d_now = datetime.strptime(d_now, "%d/%m/%Y %H:%M:%S")
    return abs((d_now - d_get).seconds)
wait = WebDriverWait(driver, 20) # время вылета 10сек



try:

    # переходим на dmarket
    driver.get("https://dmarket.com/ru/ingame-items/item-list/rust-skins")
    time.sleep(10)
    driver.find_element_by_css_selector("market-side > div > filters > div > div > div:nth-child(2)").click()
    time.sleep(1)
    driver.find_element_by_css_selector("#mat-input-0").send_keys("0.4")
    time.sleep(1)
    driver.find_element_by_xpath('//div[2]/market-side/div/filters/div/div/filters-area/div/div[1]/button/mat-icon').click()
    time.sleep(1)
    driver.find_element_by_css_selector("sort-items > div > div > div > div").click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[text()="Date: Newest First"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//exchange/div/div[2]/market-side/div/filters/div/div/div[4]/button').click()
    time.sleep(4)
    #рабочий цикл всей программы
    already_sent = []
    for i in range(1000):
        driver.find_element_by_xpath('//exchange/div/div[2]/market-side/div/filters/div/div/div[4]/button').click()
        time.sleep(4)
        now = datetime.now()
        date_now = now.strftime("%d/%m/%Y %H:%M:%S")
        #получаем время из бд (если есть)
        mycursor.execute("SELECT date FROM parsersToSteam LIMIT 1")
        date_bd = mycursor.fetchone()
        #устанавливаем разницу во времени
        if date_bd is not None:
            date_bd = date_bd[0]
            dates_diff = dates_between(date_now, str(date_bd)) / 60
            print(dates_diff)
        #если ответ из бд пустой, то в бд пусто, нужно её заполнить
        if date_bd is None:
            dates_diff = 777
            print(dates_diff)

        if dates_diff > 60:
            already_sent = []
            #удаляем все записи
            mycursor.execute("DELETE FROM parsersToSteam")
            mydb.commit()
            driver.get(
                "https://table.altskins.com/site/items?ItemsFilter%5Bknife%5D=0&ItemsFilter%5Bknife%5D=1&ItemsFilter%5Bstattrak%5D=0&ItemsFilter%5Bstattrak%5D=1&ItemsFilter%5Bsouvenir%5D=0&ItemsFilter%5Bsouvenir%5D=1&ItemsFilter%5Bsticker%5D=0&ItemsFilter%5Bsticker%5D=1&ItemsFilter%5Btype%5D=4&ItemsFilter%5Bservice1%5D=r_showsteam&ItemsFilter%5Bservice2%5D=r_showsteam&ItemsFilter%5Bunstable1%5D=1&ItemsFilter%5Bunstable2%5D=1&ItemsFilter%5Bhours1%5D=192&ItemsFilter%5Bhours2%5D=192&ItemsFilter%5BpriceFrom1%5D=0.6&ItemsFilter%5BpriceTo1%5D=&ItemsFilter%5BpriceFrom2%5D=&ItemsFilter%5BpriceTo2%5D=&ItemsFilter%5BsalesBS%5D=&ItemsFilter%5BsalesTM%5D=&ItemsFilter%5BsalesST%5D=222&ItemsFilter%5Bname%5D=&ItemsFilter%5Bservice1Minutes%5D=301&ItemsFilter%5Bservice2Minutes%5D=301&ItemsFilter%5BpercentFrom1%5D=&ItemsFilter%5BpercentFrom2%5D=&ItemsFilter%5Btimeout%5D=5&ItemsFilter%5Bservice1CountFrom%5D=&ItemsFilter%5Bservice1CountTo%5D=&ItemsFilter%5Bservice2CountFrom%5D=&ItemsFilter%5Bservice2CountTo%5D=&ItemsFilter%5BpercentTo1%5D=&ItemsFilter%5BpercentTo2%5D=")
            time.sleep(8)
            # подгружаем все элементы из tradeback'a
            for x in range(10):
                mainBlocks = driver.find_elements_by_css_selector('#w0 > table > tbody > tr:nth-child(n)')
                len_start = len(mainBlocks)
                element = driver.find_element_by_css_selector(
                    '#w0 > table > tbody > tr:nth-child(' + str(len(mainBlocks)) + ')')
                element.location_once_scrolled_into_view
                time.sleep(4)
                mainBlocks = driver.find_elements_by_css_selector('#w0 > table > tbody > tr:nth-child(n)')
                len_after_scroll = len(mainBlocks)
                if len_start == len_after_scroll:
                    break
            mainBlocks = driver.find_elements_by_css_selector('#w0 > table > tbody > tr:nth-child(n)')
            print("tryskins", len(mainBlocks))
            for item in mainBlocks:
                name = item.find_element_by_css_selector('td:nth-child(1) > span').text
                price = item.find_element_by_css_selector('td:nth-child(5) > span.edit').text
                insertIntoDatabase = """
                                            INSERT INTO parsersToSteam (name, price, game, date)
                                            VALUES
                                                (%s, %s, %s, %s)
                                        """
                mycursor.execute(insertIntoDatabase, (name, price, "rust", date_now))
                mydb.commit()
                time.sleep(0.1)

            driver.get("https://tradeback.io/ru/comparison#{%22app%22:5,%22services%22:[%22steamcommunity.com%22,%22steamcommunity.com%22],%22updated%22:[1111,1111],%22categories%22:[[%22normal%22],[%22normal%22]],%22hold_time_range%22:[8,1],%22price%22:[[0.6],[]],%22count%22:[[],[]],%22profit%22:[[],[]]}")
            time.sleep(8)
            #подгружаем все элементы из tradeback'a
            for x in range(10):
                mainBlocks = driver.find_elements_by_css_selector('#table-body > tr:nth-child(n)')
                len_start = len(mainBlocks)
                element = driver.find_element_by_css_selector('#table-body > tr:nth-child(' + str(len(mainBlocks)) + ')')
                element.location_once_scrolled_into_view
                time.sleep(4)
                mainBlocks = driver.find_elements_by_css_selector('#table-body > tr:nth-child(n)')
                len_after_scroll = len(mainBlocks)
                if len_start == len_after_scroll:
                    break
            mainBlocks = driver.find_elements_by_css_selector('#table-body > tr:nth-child(n)')
            print("tradeback", len(mainBlocks))
            for item in mainBlocks:
                time.sleep(0.1)
                name = item.find_element_by_css_selector('td.copy-name').text
                mycursor.execute("SELECT * FROM parsersToSteam WHERE name=%s", (name,))
                date_bd = mycursor.fetchone()
                print(date_bd)
                if date_bd is not None:
                    print("уже есть в бд")
                    continue
                price = item.find_element_by_css_selector('td:nth-child(7) > div.first-line > span').get_attribute("data-price")
                insertIntoDatabase = """
                                            INSERT INTO parsersToSteam (name, price, game, date)
                                            VALUES
                                                (%s, %s, %s, %s)
                                        """
                mycursor.execute(insertIntoDatabase, (name, price, "rust", date_now))
                mydb.commit()
                time.sleep(0.1)

            # переходим на dmarket
            driver.get("https://dmarket.com/ru/ingame-items/item-list/rust-skins")
            time.sleep(8)
            driver.find_element_by_css_selector("market-side > div > filters > div > div > div:nth-child(2)").click()
            time.sleep(0.5)
            driver.find_element_by_css_selector("#mat-input-0").send_keys("0.4")
            time.sleep(0.5)
            driver.find_element_by_xpath('//div[2]/market-side/div/filters/div/div/filters-area/div/div[1]/button/mat-icon').click()
            time.sleep(0.5)
            driver.find_element_by_css_selector("sort-items > div > div > div > div").click()
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[text()="Date: Newest First"]').click()
            time.sleep(0.5)
            driver.find_element_by_xpath('//exchange/div/div[2]/market-side/div/filters/div/div/div[4]/button').click()
            time.sleep(4)

        mycursor.execute("SELECT name, price FROM parsersToSteam")
        items_from_bd = mycursor.fetchall()
        print(len(items_from_bd))
        mainBlocks = driver.find_elements_by_xpath('/html/body/app-root/mat-sidenav-container/mat-sidenav-content/exchange/div/div[2]/market-side/div/market-inventory/assets-card-scroll/div/div/asset-card')
        index = 0
        for item in mainBlocks:
            if index > 25:
                break
            index += 1
            try:
                name_dm = item.find_element_by_xpath('asset-card-layout/div/div[2]/div/img').get_attribute("alt")
            except:
                continue
            #print(name_dm)
            for item_bd in items_from_bd:
                if item_bd[0] == name_dm:
                    try:
                        price_dm = item.find_element_by_xpath('asset-card-layout/div/div[1]/div[1]/asset-card-price/strong/span/price').text
                    except:
                        break
                    price_dm = price_dm[1:]
                    profit = (float(price_dm) / (float(item_bd[1])* 0.87) -1) * -1
                    print(name_dm, price_dm)
                    if profit > 0.3:
                        if name_dm in already_sent:
                            break
                        already_sent.append(name_dm)
                        print(profit,"----------------------------------------------------------- dm:",name_dm, price_dm, "bd:", item_bd)
                        mess = str(profit) + name_dm
                        telegram_bot_sendtext(mess)



except:
    PrintException()
    driver.close()
    driver.quit()

driver.close()
driver.quit()
