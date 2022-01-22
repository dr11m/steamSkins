#!/usr/bin/env python
# coding: utf-8

# # settings, imports and functions

# In[ ]:


import os
import random
import time
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
import urllib
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pyvirtualdisplay import Display
import subprocess



# обработка ошибок
def PrintException():
    #send an error into DB
    print("!!!!!!!!!!!!!!!!!!!!! was an error")
    # exception output
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    # screen
    driver.save_screenshot('Error.png')
    # close all
    closeAll()



try:
    #set status into DB
    def successStatus(success):
        now = datetime.now()
        if success is False:
            mycursor.execute("UPDATE scriptsStatus SET status = 'error', date = %s WHERE name = 'steamHistory'", (now,))
            mydb.commit()
        else:
            mycursor.execute("UPDATE scriptsStatus SET status = 'success', date = %s WHERE name = 'steamHistory'",(now,))
            mydb.commit()

    #close all
    def closeAll():
        try:
            mycursor.close()
        except:
            print("error-mycursor.close()")
            pass
        try:
            mydb.close()
        except:
            print("error-mydb.close()")
            pass
        try:
            driver.close()
        except:
            print("error-driver.close()")
            pass
        try:
            driver.quit()
        except:
            print("error-driver.quit()")
            pass
        try:
            display.stop()
        except:
            print("error-display.stop()")
            pass
        try:
            display.sendstop()
        except:
            print("error-display.sendstop()")
            pass
        try:
            display.popen.kill()
        except:
            print("error-display.popen.kill()")
            pass
        try:
            sys.exit()
        except:
            print("error-sys.exit()")
            pass


    # telegra

    # start time
    now = datetime.now()
    print(str(now) + "----------------------------------------------------------------------------------------------------------")




    #check other scripts status
    mycursor.execute("SELECT * FROM `scriptsStatus`")
    scripts_status_list = mycursor.fetchall()
    now = datetime.now()
    print("start checking other scripts status")
    for script in scripts_status_list:
        if int(script[3]) == 0:
            print("untracked script, no nedd to check (continue)")
            continue
        script_time = script[2]
        print(now, script_time)
        time_difference = now - script_time
        time_difference = int(time_difference.total_seconds()) / 60
        print(time_difference)
        #если разница во времени больше заданной или в статусе ошибка
        if time_difference > int(script[4]) or str(script[1]) == "error":
            print("some script is broken")
            telegram_bot_sendtext("scriptsStatus: " + str(script[0]) + " не работает, нужно заглянуть в таблицу (scriptsStatus)")



    #start driver
    display = Display(visible=0, size=(1600, 900), backend='xvfb')
    display.start()

    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=/home/work/profilesForAll/SteamHistoryTest")  # linux
    chrome_options.add_extension('/home/work/steam/steamHistory/SteamMarketHistory.crx')
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)

    # NoteBook
    # driver = webdriver.Chrome(options=chromeOptions, executable_path=r'C:\\Users\\Администратор\\Desktop\\pywinautomation\\chromedriver.exe')
    # chromeOptions.add_argument("user-data-dir=C:\\Users\\Администратор\\AppData\\Local\\Google\\Chrome\\User Data\\Default")



    wait = WebDriverWait(driver, 10)  # время вылета 10сек

    # rub_usd
    rub_usd = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    rub_usd = rub_usd.json()
    rub_usd = float(rub_usd["Valute"]["USD"]["Value"])
    print("current exchange rate", rub_usd)

except Exception as e:
    telegram_bot_sendtext("SteamHistory: Возникла ошибка, нужно выяснять")
    PrintException()
# # CODE
#

# ## check if I'm logged into steam
#

# In[ ]:


try:
    driver.get("https://steamcommunity.com/market/")
    time.sleep(5)
    try:
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#marketWalletBalanceAmount")))
    except:
        print("cant verify login into steam on the first try")
        time.sleep(5)
        driver.get("https://steamcommunity.com/market/")
        print("trying one more time")
        try:
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#marketWalletBalanceAmount")))
        except:
            print("failed - login into steam")
            # входим в стим
            driver.find_element_by_css_selector("#global_action_menu > a").click()
            time.sleep(1)
            # login
            input_field = driver.find_element_by_css_selector('#input_username')
            input_field.clear()
            time.sleep(2)
            # pass
            input_field = driver.find_element_by_css_selector('#input_password')
            input_field.clear()
            time.sleep(3)
            input_field = driver.find_element_by_css_selector('#twofactorcode_entry')
            #get 2fa code
            os.chdir("/home/work/steamguard-cli")
            guard = subprocess.check_output('build/steamguard 2fa', shell=True).decode("utf-8").strip()
            print(guard)
            input_field.clear()
            input_field.send_keys(guard)
            time.sleep(2)
            driver.find_element_by_css_selector(
                "#login_twofactorauth_buttonset_entercode > div.auth_button.leftbtn > div.auth_button_h5").click()
            time.sleep(10)
            # снова проверяем, вошли ли мы в систему
            try:
                element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#marketWalletBalanceAmount")))
            except:
                msg = "need to login into steam"
                raise ValueError('need to login into steam')
except Exception as e:
    telegram_bot_sendtext("SteamHistory: Возникла ошибка, нужно выяснять")
    PrintException()


# ## setup extension

# In[ ]:


try:

    # переходим в историю продаж
    driver.find_element_by_css_selector('#tabMyMarketHistory > span').click()
    time.sleep(7)
    # переходим в настройки
    driver.find_element_by_css_selector('#smhp_container > div.smhp_btn_options_container > a > span').click()
    time.sleep(2)
    # если вторая вкладка не открылась, то закрываем программу
    if len(driver.window_handles) == 1:
        print("Can't get into extension's settings")
        raise ValueError('A very specific bad thing happened.')
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.5)
    # меняем максимальное кол-во предметов, отображаемых в истории
    select = Select(driver.find_element_by_id('items_per_page'))
    select.select_by_value('500')
    # проверяем чекбоксы, чтобы избежать пометки о выставлении предметов и отмене выставления в истории стима
    x = driver.find_element_by_css_selector("#hide_listing_created").is_selected()
    y = driver.find_element_by_css_selector("#hide_listing_canceled").is_selected()
    print("must be True", x, y)
    # если один из False
    if x == False:
        driver.find_element_by_css_selector("#hide_listing_created").click()
        time.sleep(0.5)
    if y == False:
        driver.find_element_by_css_selector("#hide_listing_canceled").click()
        time.sleep(0.5)
    # повторная проверка
    x = driver.find_element_by_css_selector("#hide_listing_created").is_selected()
    y = driver.find_element_by_css_selector("#hide_listing_canceled").is_selected()
    print("must be True", x, y)
    # если один из чекбоксов False
    if x == False:
        print("Error. Checkboxes are still False")
        raise ValueError("extension don't load properly")
    if y == False:
        print("Error. Checkboxes are still False")
        raise ValueError("extension don't load properly")

    # переходим на основную вкладку и удаляем вторую
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.1)
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(0.1)

except Exception as e:
    telegram_bot_sendtext("SteamHistory: Возникла ошибка, нужно выяснять")
    PrintException()


# ## get items from steam's history

# In[ ]:


try:
    for index_global in range(1):  # если нужно больше одного оповторения работы программы
        # получаем все уже проданные предметы
        mycursor.execute("SELECT sold_id FROM skins WHERE sold_id IS NOT null")
        myresult3 = mycursor.fetchall()
        list_of_uniq_ids = []
        for item1 in myresult3:
            list_of_uniq_ids.append(item1[0])
        print("length items that already have been sold from table skins:", len(list_of_uniq_ids))

        # получаем все уже проданные предметы
        mycursor.execute("SELECT sold_id FROM PurchasedItems WHERE sold_id IS NOT null")
        myresult3 = mycursor.fetchall()
        list_of_uniq_ids_purchased_items = []
        for item1 in myresult3:
            list_of_uniq_ids_purchased_items.append(item1[0])
        print("length items that already have been sold from table skins:", len(list_of_uniq_ids_purchased_items))

        # обновляем кэш и открываем историю
        driver.get("https://www.google.com/")
        time.sleep(1)
        driver.get("https://steamcommunity.com/market/")
        time.sleep(3)
        driver.find_element_by_css_selector('#tabMyMarketHistory > span').click()
        time.sleep(7)
        # сколько страниц будет проходить за один проход
        index = 0
        for i in range(5):
            index += 1
            print("page number is -", index)
            # получаем все предметы в таблице
            mainBlocks = driver.find_elements_by_css_selector(
                '#tabContentsMyMarketHistoryRows > div.market_listing_row.market_recent_listing_row.smhp_processed')
            for item in mainBlocks:
                # определяем предмет был куплен или продан
                buyOrSold = item.find_element_by_css_selector('div:nth-child(1)').text
                buyOrSold = buyOrSold.strip()
                print("buy or sold -", buyOrSold)
                # если был продан
                if buyOrSold == '-':
                    unique_sold_id = item.get_attribute("id")
                    print("sold id -", unique_sold_id)
                    mycursor.execute("SELECT * FROM skins WHERE sold_id=%s", (unique_sold_id,))
                    myresult2 = mycursor.fetchone()
                    if myresult2 is not None:
                        print("Error. Didn't catch a sold id in a previous code. Did it here")
                        continue
                    name = item.find_element_by_css_selector('div:nth-child(7) > span > a').get_attribute("href")
                    name = name.split('/')
                    name = name[6]
                    name = urllib.parse.unquote(urllib.parse.unquote(name))
                    mycursor.execute("SELECT name, id FROM skins WHERE name=%s AND sold_id IS null;", (name,))
                    myresult = mycursor.fetchone()
                    if myresult != None:
                        un_id = myresult[1]
                        price = item.find_element_by_css_selector(
                            'div.market_listing_right_cell.market_listing_their_price > span.market_table_value > span').text
                        price = price.strip()
                        price = price[:-4]
                        price = price.replace(',', '.')
                        price = float(price) / rub_usd
                        price = float('{:.3f}'.format(price))
                        price = str(price)
                        mycursor.execute(
                            "UPDATE skins SET status = 3, sold_id = %s, price_sold = %s WHERE name=%s AND id = %s",
                            (unique_sold_id, price, name, un_id,))
                        mydb.commit()
                        print(mycursor.rowcount, "record(s) affected")
                        print("---------------------------------------",
                              name.encode('utf-8'))

                # если был продан
                if buyOrSold == '+':
                    unique_buy_id = item.get_attribute("id")  # unique id
                    # проверяем, нет ли предмета в базе
                    if unique_buy_id in list_of_uniq_ids_purchased_items:
                        continue
                    # повторная проверка, есть ли предмет в базе
                    mycursor.execute("SELECT * FROM PurchasedItems WHERE sold_id=%s", (unique_buy_id,))
                    myresult2 = mycursor.fetchone()
                    if myresult2 is not None:
                        print("Error. Didn't catch a sold id in a previous code. Did it here")
                        continue
                    # название предмета
                    name = item.find_element_by_css_selector('div:nth-child(7) > span > a').get_attribute("href")
                    name = name.split('/')
                    name = name[6]
                    name = urllib.parse.unquote(urllib.parse.unquote(name))
                    # цена предмета
                    price = item.find_element_by_css_selector(
                        'div.market_listing_right_cell.market_listing_their_price > span.market_table_value > span').text
                    price = price.strip()
                    price = price[:-4]
                    price = price.replace(',', '.')
                    price = float(price)
                    price = float('{:.2f}'.format(price))
                    price = str(price)
                    mycursor.execute(
                        "INSERT INTO PurchasedItems (name, price_purchased, platform_from, sold_id) VALUES (%s, %s, %s, %s)",
                        (name, price, "1", unique_buy_id,))
                    mydb.commit()
                    print(mycursor.rowcount, "record(s) affected")
                    print("---------------------------------------",
                          name.encode('utf-8'))

            element = driver.find_element_by_css_selector('#tabContentsMyMarketHistory_btn_next')
            element.location_once_scrolled_into_view
            driver.find_element_by_css_selector('#tabContentsMyMarketHistory_btn_next').click()
            time.sleep(11)

except Exception as e:
    telegram_bot_sendtext("SteamHistory: Возникла ошибка, нужно выяснять")
    PrintException()


# close all
now = datetime.now()
print(str(now), "successfully!")
# close all
closeAll()
