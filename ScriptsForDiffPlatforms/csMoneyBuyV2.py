#!/usr/bin/env python
# coding: utf-8

# # settings, imports and functions

# In[1]:
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
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import logging
from pyvirtualdisplay import Display
import subprocess
import datetime



########
#CONFIG#
########

trade_lock_days_config = "4 days"

ban_list = [

]





# the current process
pid = os.getpid()

# обработка ошибок
def PrintException():
    #send an error into DB
    successStatus(False)
    succsess = 0
    print("was an error")
    # exception output
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    now = datetime.datetime.now()
    # display.stop() #linux
    driver.save_screenshot('Error' + "-" + str(now) + '.png')
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    # screen
    # close all
    mycursor.close()
    mydb.close()
    driver.close()
    driver.quit()
    sys.exit()

try:

    # from pyvirtualdisplay import Display #linux
    # import pyautogui #linux

    # start time
    now = datetime.datetime.now()
    print(str(
        now) + "----------------------------------------------------------------------------------------------------------")



    #start driver
    display = Display(visible=0, size=(1600, 900), backend='xvfb')
    display.start()


    chrome_options = Options()

    chrome_options.add_argument("user-data-dir=/home/work/profilesForAll/csMoneyBuy8")  # linux
    chrome_options.add_extension('extension.crx')
    chrome_options.add_argument("window-size=1600,900")
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
    driver.set_window_size(1600, 900)


    def PrintException_only_print():
        succsess = 0
        print("was an error")
        # exception output
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


    succsess = 1



    #script status
    def successStatus(success):
        now = datetime.datetime.now()
        if success is False:
            mycursor.execute("UPDATE scriptsStatus SET status = 'error', date = %s WHERE name = 'csMoneyBuy'", (now,))
            mydb.commit()
        else:
            mycursor.execute("UPDATE scriptsStatus SET status = 'success', date = %s, process_id = %s WHERE name = 'csMoneyBuy'",(now, pid,))
            mydb.commit()



    # NoteBook
    # driver = webdriver.Chrome(options=chromeOptions, executable_path=r'C:\\Users\\Администратор\\Desktop\\pywinautomation\\chromedriver.exe')
    # chromeOptions.add_argument("user-data-dir=C:\\Users\\Администратор\\AppData\\Local\\Google\\Chrome\\User Data\\Default")

    wait = WebDriverWait(driver, 25)  # время вылета 10сек

    # rub_usd
    rub_usd = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    rub_usd = rub_usd.json()
    rub_usd = float(rub_usd["Valute"]["USD"]["Value"])
    print("current exchange rate", rub_usd)

    # loging errors
    # Create a logging instance
    logger = logging.getLogger('csMoneyBuy_errors')
    logger.setLevel(logging.INFO)  # you can set this to be DEBUG, INFO, ERROR
    # Assign a file-handler to that instance
    fh = logging.FileHandler("errors.txt")
    fh.setLevel(logging.ERROR)  # again, you can set this differently
    # Format your logs (optional)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)  # This will set the format to the file handler
    # Add the handler to your logging instance
    logger.addHandler(fh)

    # loging info (debug mode)
    # Create a logging instance
    logger_msg = logging.getLogger('csMoneyBuy_info')
    logger_msg.setLevel(logging.INFO)  # you can set this to be DEBUG, INFO, ERROR
    # Assign a file-handler to that instance
    fh1 = logging.FileHandler("debug.txt")
    fh1.setLevel(logging.INFO)
    # Format your logs (optional)
    formatter = logging.Formatter('%(asctime)s - row:%(lineno)d - %(message)s')
    fh1.setFormatter(formatter)  # This will set the format to the file handler
    # Add the handler to your logging instance
    logger_msg.addHandler(fh1)

    # # preparation CODE

    # ## check if I'm logged into steam

    # In[2]:

except Exception as e:
    print("was an error 189")
    # exception output
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    telegram_bot_sendtext("csMoneyBuy: Возникла ошибка, нужно выяснять")




#login into steam if needed
try:
    driver.get("https://steamcommunity.com/market/")
    time.sleep(5)
    try:
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#marketWalletBalanceAmount")))
    except:
        print("cant verify login into steam on the first try")
        time.sleep(5)
        driver.get("https://steamcommunity.com/market/")
        try:
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#marketWalletBalanceAmount")))
        except:
            print("login into steam")
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
            # get 2fa code
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
                logger.exception(msg)
                raise ValueError('need to login into steam')
except Exception as e:
    print("was an error 248")
    telegram_bot_sendtext("csMoneyBuy: Возникла ошибка, нужно выяснять")
    PrintException()

# ## setup extension (Auto Confirm Trades)

# In[3]:


try:
    # настраиваем расширение
    driver.get("chrome-extension://akhapknmojfihnlefjbbjjkobfknfghb/popup.html")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#apiKey")))
    time.sleep(0.5)
    print("setup an extension")
    logger_msg.info("setup an extension")  # debug
    if len(driver.window_handles) > 1:
        print("switch window toextension")
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.1)
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(0.1)
    input_field = driver.find_element_by_css_selector('#apiKey')
    input_field.clear()
    api_key = "1C0BE04FE1021A9CA80AF10506AB5D62"
    input_field.send_keys(api_key)
    time.sleep(1)
    input_field = driver.find_element_by_css_selector('#rate')
    input_field.clear()
    time.sleep(1)
    input_field.send_keys("1")
    time.sleep(1)
    driver.find_element_by_css_selector("body > table > tbody > tr:nth-child(1) > td > label").click()
    time.sleep(1)

except Exception as e:
    print("was an error 2866")
    telegram_bot_sendtext("csMoneyBuy: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()



# ## check if I'm logged into csMoney

# In[4]:


try:

    driver.get("https://old.cs.money/")
    try:
        element = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.header_menu_mobile > div.balance_header.superclass_space.block_balance")))
        time.sleep(1)
    except:
        print("start entering into csMoney")
        logger_msg.info("start entering into csMoney")  # debug
        # входим в csMoney
        driver.find_element_by_css_selector("#authenticate_button > a").click()
        time.sleep(1)
        # входим в csMoney
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#imageLogin")))
        # входим в tradeback
        driver.find_element_by_css_selector("#imageLogin").click()
        time.sleep(5)
        # снова проверяем, вошли ли мы в систему
        try:
            element = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.header_menu_mobile > div.balance_header.superclass_space.block_balance")))
        except:
            msg = "need to login into csMoney"
            logger_msg.info(msg)  # debug
            raise ValueError('need to login into csMoney')
except Exception as e:
    print("was an error 325")
    telegram_bot_sendtext("csMoneyBuy: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()

# ## set safe traffic mode (if needed)

# In[5]:


try:

    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#main_container_bot > div.items > div:nth-child(1)")))
    # проверяем, есть ли имя
    name_exists = 0
    try:
        driver.find_element_by_css_selector("#main_container_bot > div.items > div:nth-child(1) > div.im_min").text
        print("got name1 (if not need to set safe traddic mode)")
        logger_msg.info("got name1 (if not need to set safe traddic mode)")  # debug
        name_exists = 1
    except:
        pass
    try:
        driver.find_element_by_css_selector("#main_container_bot > div.items > div:nth-child(1) > div.im_min_st").text
        print("got name2 (if not need to set safe traddic mode)")
        logger_msg.info("got name2 (if not need to set safe traddic mode)")  # debug
        name_exists = 1
    except:
        pass
    try:
        driver.find_element_by_css_selector("#main_container_bot > div.items > div:nth-child(1) > div.im_min_ws").text
        print("got name3 (if not need to set safe traddic mode)")
        logger_msg.info("got name3 (if not need to set safe traddic mode)")  # debug
        name_exists = 1
    except:
        pass
    try:
        driver.find_element_by_css_selector("#main_container_bot > div.items > div:nth-child(1) > div.im_min_wst").text
        print("got name4 (if not need to set safe traddic mode)")
        logger_msg.info("got name4 (if not need to set safe traddic mode)")  # debug
        name_exists = 1
    except:
        pass
    if name_exists == 0:
        print("setting up safe traffic mode")
        logger_msg.info("setting up safe traffic mode")  # debug
        driver.find_element_by_css_selector("div.header_menu_container > div.header_setting > svg").click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#settings_modal > div.modal_title.setting_svg")))
        time.sleep(0.5)
        driver.find_element_by_css_selector(
            "div.modal_content_settings_row.displaying > div:nth-child(1) > div").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#settings_modal > a > svg").click()
        time.sleep(5)


    #set small images of items
    driver.find_element_by_css_selector("#header_panel > div.header_menu_mobile > div.header_menu_container > div.header_setting > svg").click()
    time.sleep(2)
    source_element = driver.find_element_by_css_selector(
        "#settings_modal > div.modal_content_settings > div.modal_content_settings_row.zoom_settings > div > div.main__point.superactive")
    dest_element = driver.find_element_by_css_selector(
        "#settings_modal > div.modal_content_settings > div.modal_content_settings_row.zoom_settings > div > div:nth-child(3) > div")
    action = ActionChains(driver)
    action.click_and_hold(source_element).pause(2).move_to_element(dest_element).release(dest_element).perform()
    time.sleep(1)
    driver.find_element_by_css_selector("#settings_modal > a > svg").click()
    time.sleep(0.5)



    ##############################################
    #высставляем ограничение тейдбана у прредметов
    ##############################################

    #выставляем по мод (если нужно)
    if driver.find_element_by_css_selector("body > div.body_scroll > div.main > div.content.login_test_3.auth > div.trade_container.wrapper > div.row > div.column_2 > div > div.filter_mobile > div > div.pro_version_container > div > div:nth-child(1) > div.lite_step_text > span").is_displayed():
        print("need to switch to pro mode")
        driver.find_element_by_css_selector("div.trade_container.wrapper > div.row > div.column_2 > div > div.filter_mobile > div > div.sidebar_switcher_title.superclass_space.pro_version_label > label > input").click()

    #открываем возможноть проcтавления дней
    try:
        driver.find_element_by_css_selector("body > div.body_scroll > div.main > div.content.login_test_3.auth > div.trade_container.wrapper > div.row > div.column_2 > div > div.filter_mobile > div > div.trade_lock_list_container.pro_version_off.slider.superclass_space.inactive")
        driver.find_element_by_css_selector("#tradeLockSwitcher").click()
    except: pass

    #перетягиваем на нужное кол-во дней (для этого мы получаем нынешнее кол-во дней и перетасскиваем внудную стоону по пикелям, пока придем к нужному чисслу)
    trade_lock_days_site = driver.find_element_by_css_selector("#trade_lock_text").text.strip()
    print(trade_lock_days_site, trade_lock_days_config)
    logger_msg.info("trade_locck_days (site and config)" + str(trade_lock_days_site) + str(trade_lock_days_config))  # debug
    for index in range(100):
        trade_lock_days_site = driver.find_element_by_css_selector("#trade_lock_text").text.strip()
        #выходим
        if trade_lock_days_config == trade_lock_days_site:
            break
        #уменьшаем
        if float(trade_lock_days_config[0]) < float(trade_lock_days_site[0]):
            source_element = driver.find_element_by_css_selector("#slider_trade_lock > div > div:last-child > div")
            action = ActionChains(driver)
            action.drag_and_drop_by_offset(source_element, -5, 0).perform()
            time.sleep(2)
        #увеличиваем
        if float(trade_lock_days_config[0]) > float(trade_lock_days_site[0]):
            source_element = driver.find_element_by_css_selector("#slider_trade_lock > div > div:last-child > div")
            action = ActionChains(driver)
            action.drag_and_drop_by_offset(source_element, 5, 0).perform()
            time.sleep(2)

    trade_lock_days_site = driver.find_element_by_css_selector("#trade_lock_text").text.strip()
    if trade_lock_days_site != trade_lock_days_config:
        raise ValueError("tradeLock days is different from a fiven amount")
    print(trade_lock_days_site, trade_lock_days_config)
    logger_msg.info("trade_locck_days (site and config)" + str(trade_lock_days_site) + str(trade_lock_days_config))  # debug

except Exception as e:
    print("was an error 439")
    telegram_bot_sendtext("csMoneyBuy: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()

# ## set safe traffic mode (if needed)

# In[5]:


try:

    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#main_container_bot > div.items > div:nth-child(1)")))
    # проверяем, есть ли имя
    name_exists = 0
    try:
        driver.find_element_by_css_selector("#main_container_bot > div.items > div:nth-child(1) > div.im_min").text
        print("got name1 (if not need to set safe traddic mode)")
        logger_msg.info("got name1 (if not need to set safe traddic mode)")  # debug
        name_exists = 1
    except:
        pass
    try:
        driver.find_element_by_css_selector("#main_container_bot > div.items > div:nth-child(1) > div.im_min_st").text
        print("got name2 (if not need to set safe traddic mode)")
        logger_msg.info("got name2 (if not need to set safe traddic mode)")  # debug
        name_exists = 1
    except:
        pass
    try:
        driver.find_element_by_css_selector("#main_container_bot > div.items > div:nth-child(1) > div.im_min_ws").text
        print("got name3 (if not need to set safe traddic mode)")
        logger_msg.info("got name3 (if not need to set safe traddic mode)")  # debug
        name_exists = 1
    except:
        pass
    try:
        driver.find_element_by_css_selector("#main_container_bot > div.items > div:nth-child(1) > div.im_min_wst").text
        print("got name4 (if not need to set safe traddic mode)")
        logger_msg.info("got name4 (if not need to set safe traddic mode)")  # debug
        name_exists = 1
    except:
        pass
    if name_exists == 0:
        print("setting up safe traffic mode")
        logger_msg.info("setting up safe traffic mode")  # debug
        driver.find_element_by_css_selector("div.header_menu_container > div.header_setting > svg").click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#settings_modal > div.modal_title.setting_svg")))
        time.sleep(0.5)
        driver.find_element_by_css_selector(
            "div.modal_content_settings_row.displaying > div:nth-child(1) > div").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#settings_modal > a > svg").click()
        time.sleep(5)


except Exception as e:
    print("was an error 497")
    telegram_bot_sendtext("csMoneyBuy: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()

# ## set other settings on csMoney

# In[7]:


try:

    input_field = driver.find_element_by_css_selector('#user_search_input')
    input_field.clear()
    input_field.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, "1")
    time.sleep(3)

    element_to_hover_over = driver.find_element_by_css_selector("div.bot_sort")
    ActionChains(driver).move_to_element(element_to_hover_over).perform()
    time.sleep(0.2)
    ActionChains(driver).move_to_element(element_to_hover_over).perform()
    time.sleep(0.2)

    driver.find_element_by_css_selector("div.bot_sort > div  > div > div > ul > li:nth-child(4) > a").click()
    time.sleep(0.2)

    driver.find_element_by_css_selector("div.bot_sort > div  > div > div > ul > li:nth-child(4) > a").click()
    time.sleep(0.2)

    element_to_hover_over = driver.find_element_by_css_selector("#offer_container_bot")
    ActionChains(driver).move_to_element(element_to_hover_over).perform()

    try:
        driver.find_element_by_css_selector("body > div.body_scroll > div.main > div.content.login_test_3.auth > div.trade_container.wrapper > div.row > div.column_2 > div > div.filter_mobile > div > div.trade_lock_list_container.pro_version_off.slider.superclass_space.inactive")
    except:
        driver.find_element_by_css_selector("#tradeLockSwitcher").click()
        pass


except Exception as e:
    print("was an error 537")
    telegram_bot_sendtext("csMoneyBuy: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()

# # main code

# In[ ]:


try:
    #send process id into mysql
    successStatus(True)

    # first run (забираем цены и оверсток)
    mycursor.execute("SELECT name,price,count FROM skinsLimit")
    items_bd = mycursor.fetchall()
    print("items DB length -", len(items_bd))
    logger_msg.info("items DB length - " + str(len(items_bd)))  # debug
    if len(items_bd) < 5:
        time.sleep(5)
        mycursor.execute("SELECT name,price,count FROM skinsLimit")
        items_bd = mycursor.fetchall()
        if len(items_bd) < 5:
            logger_msg.info('cant get items from DB')  # debug
            raise ValueError('cant get items from DB')
    time_get_items = datetime.datetime.now()



    x = 0
    while x < 5000000:
        x += 1

        a1 = datetime.datetime.now()  # time to click on item
        #забираем XML для парса
        XML = driver.find_element_by_css_selector('#main_container_bot > div.items').get_attribute('innerHTML')
        str_split = XML.split('style="background-image:')
        del str_split[0]

        #print("items length -", len(str_split))
        logger_msg.info('items length - ' + str(len(str_split)))  # debug

        #переменные, обнуляемые каждый проход
        index = 0
        click_times = 0
        list_trade = []
        trade_cost = 0
        stop = 0

        if len(str_split) == 0:
            time.sleep(0.1)
            continue

        for item_xml in str_split:
            profit = -0.9 #для непонятных ситуаций, где может использоваться прошлое значение профита
            index += 1
            try:
                #получаем название и цену
                name = re.search('<div class="im_mi([^<]*)</div>', item_xml)
                name = name.group(1).split(">")
                name = name[1].strip()
                exterior = re.search('<div class="r">([^<>]*)</div>', item_xml)
                exterior = exterior.group(1).strip()
                price = re.search('</span>([^<>]*)</div>', item_xml)
                price = price.group(1)
                price = float(price.strip())
            except Exception as e:
                print("was an error name, exterior or price 605")
                PrintException_only_print()
                logger_msg.info(item_xml)  # debug
                continue
            if len(exterior) > 1:
                if exterior == "FN":
                    exterior = '(Factory New)'
                if exterior == "MW":
                    exterior = '(Minimal Wear)'
                if exterior == "BS":
                    exterior = '(Battle-Scarred)'
                if exterior == "WW":
                    exterior = '(Well-Worn)'
                if exterior == "FT":
                    exterior = '(Field-Tested)';
                # делаем полное имя для предмета ксго
                # print("full exterior is - ", str(exterior))
                name = name + " " + exterior
            #ban_list
            if name in ban_list:
                continue
            #получаем профит, если нужный предмет есть в бд
            for item_bd in items_bd:
                if name == item_bd[0]:
                    if item_bd[1] is None:
                        print("price is null")
                        continue
                    profit = float(item_bd[1]) * 0.87 / price - 1
                    #print("match! - name, price steam, price csmoney and profit", item_bd[0].encode('utf-8'), item_bd[1], price, profit)  # test
                    logger_msg.info("match! - name, price steam, price csmoney and profit " + str(item_bd[0].encode('utf-8')) +" "+ str(item_bd[1]) +" "+ str(price) +" "+ str(profit))  # debug
                    break
            #если профит подходит, то кликаем на предмет
            if profit > -0.32:
                print("profit > 20")
                logger_msg.info("profit > 20")  # debug
                if click_times == 0:
                    print("stop live feed (must be 0)", click_times)
                    logger_msg.info("stop live feed (must be 0) " + str(click_times))  # debug
                    #stop live feed
                    try:
                        driver.find_element_by_css_selector("#control_skins_live > div.control_skins_ticker_stop > div:nth-child(1)").click()
                    except:
                        try:
                            driver.find_element_by_css_selector("#control_skins_live > div.control_skins_ticker_stop > div:nth-child(1)").click()
                        except: pass
                #проверяем, добавился ли предмет
                trade_length = driver.find_elements_by_css_selector("#offer_container_bot > div.items > div:nth-child(n)")
                print("trade_length", len(trade_length))
                logger_msg.info("trade_length " + str(len(trade_length)))  # debug
                driver.find_element_by_css_selector("#main_container_bot > div.items > div:nth-child("+ str(index - click_times) +")").click()
                time.sleep(0.01)
                b1 = datetime.datetime.now()
                delta1 = b1 - a1
                print('time to click on item: ', int(delta1.total_seconds() * 1000))
                logger_msg.info("time to click on item: " + str(int(delta1.total_seconds() * 1000)))  # debug
                trade_length2 = driver.find_elements_by_css_selector("#offer_container_bot > div.items > div:nth-child(n)")
                print("trade_length2", len(trade_length2))
                logger_msg.info("trade_length2 " + str(len(trade_length2)))  # debug
                #tckb lj,fdbkcz
                if len(trade_length) != len(trade_length2):
                    print("item was successfuly aded")
                    logger_msg.info("item was successfuly aded")  # debug
                    click_times += 1
                    dict_item = {"name": name, "price": price}
                    list_trade.append(dict_item)
                    trade_cost += price
            #индекс - сколько предметов мы будем смотреть в цикле, клик_тайм - максимальное числ ов одном трейде
            if index > 24 or click_times > 5:
                #print("if index > 24 or click_times > 5 --> break")
                logger_msg.info("if index > 24 or click_times > 5 --> break")  # debug
                break



        #если был клик
        if click_times > 0:
            #проверяем, равна ли стоимость трейда
            print("click_times number (>0) -", click_times)
            logger_msg.info("click_times number (>0) - " + str(click_times))  # debug
            #print("list_trade:", list_trade.encode('utf-8'))
            logger_msg.info("list_trade length - " + str(len(list_trade)))  # debug
            end_trade_cost = driver.find_element_by_css_selector("#difference_balance").text
            end_trade_cost = float(end_trade_cost[1:])
            trade_cost = float('{:.2f}'.format(trade_cost)) #2 знака после запятой
            print("end_trade_cost -", end_trade_cost, "trade_cost -", trade_cost, "-- must be equal")
            logger_msg.info("end_trade_cost - " + str(end_trade_cost) + "trade_cost - " + str(trade_cost) + " -- must be equal")  # debug
            if end_trade_cost == trade_cost:
                print("trade costs equal")
                logger_msg.info("trade costs equal")  # debug
                #два прохода из-за неизвестного бага на ксмоней, позволяющего получить уже зарезервированные предметы
                for index_trade in range(2):
                    print("click trade button")
                    logger_msg.info("click trade button")  # debug
                    driver.find_element_by_css_selector("#trade_btn").click()
                    b2 = datetime.datetime.now()
                    delta1 = b2 - a1
                    print('time to click trade button: ', int(delta1.total_seconds() * 1000))
                    logger_msg.info("time to click trade button: " + str(int(delta1.total_seconds() * 1000)))  # debug

                    print("updating items from db")
                    logger_msg.info("updating items from db")  # debug
                    mycursor.execute("SELECT name,price,count FROM skinsLimit")
                    items_bd = mycursor.fetchall()
                    if len(items_bd) < 5:
                        time.sleep(5)
                        mycursor.execute("SELECT name,price,count FROM skinsLimit")
                        items_bd = mycursor.fetchall()
                        if len(items_bd) < 5:
                            logger.exception("cant get items from DB")
                            raise ValueError('cant get items from DB')
                    time.sleep(9)
                    try:
                        status_failed = driver.find_element_by_css_selector("#trade_modal > div.modal_content > div.waiting > div > div:nth-child(1) > div > svg#fail_trade_icon").is_displayed()
                    except:
                        status_failed = False
                    print("is failed trade -", status_failed)
                    logger_msg.info("is failed trade - " + str(status_failed))  # debug
                    #если неудачный трейд
                    if status_failed == True:
                        print("trade was failed")
                        logger_msg.info("trade was failed")  # debug
                        #идём на второй круг
                        if index_trade == 0:
                            # add statistic and screen
                            now = datetime.datetime.now()
                            outFileName = "statistic.txt"  # windows
                            outFile = open(outFileName, "a")
                            outFile.write(str(now) + "/" + "FALSE" + "/" + "trade_0" + "/" + str(
                                int(delta1.total_seconds() * 1000)) + "\n")
                            outFile.close()
                            # screen
                            now = time.strftime('%Y_%m-%d_%H_%M_%S')
                            #driver.save_screenshot('screens\Trade' + '-' + str(now) + '.png')

                            print("first trade was failed - continue")
                            logger_msg.info("first trade was failed - continue")  # debug
                            # закрываем окно
                            try:
                                driver.find_element_by_css_selector("#trade_modal > a > svg").click()
                                time.sleep(0.2)
                            except:
                                #close modal anti-scam
                                try:
                                    driver.find_element_by_css_selector("body > div.antiscam__wrapper > div > svg.antiscam__close").click()
                                    driver.find_element_by_css_selector("#trade_modal > a > svg").click()
                                except:
                                    logger.exception("can't close modal window")
                                    now = datetime.datetime.now()
                                    # display.stop() #linux
                                    driver.save_screenshot('Error' + "-" + str(now) + '.png')
                                    raise ValueError("can't close modal window")
                            continue
                        #удаляем несвободные элементы и повторяем трейд
                        if index_trade == 1:
                            # add statistic and screen
                            now = datetime.datetime.now()
                            outFileName = "statistic.txt"  # windows
                            outFile = open(outFileName, "a")
                            outFile.write(str(now) + "/" + "FALSE" + "/" + "trade_1" +  "/" + str(int(delta1.total_seconds() * 1000)) + "\n")
                            outFile.close()
                            # screen
                            now = time.strftime('%Y_%m-%d_%H_%M_%S')
                            #driver.save_screenshot('screens\Trade' + '-' + str(now) + '.png')
                            print("second trade was failed - delete trash items and try to start new one")
                            logger_msg.info("second trade was failed - delete trash items and try to start new one")  # debug
                            #закрываем окно
                            print("close modal window")
                            logger_msg.info("close modal window")  # debug
                            try:
                                driver.find_element_by_css_selector("#trade_modal > a > svg").click()
                                time.sleep(0.2)
                            except:
                                try:
                                    driver.find_element_by_css_selector("#trade_modal > a > svg").click()
                                    time.sleep(0.2)
                                except:
                                    logger.exception("can't close modal window")
                                    raise ValueError("can't close modal window")
                            #получаем эти элементы и удаляем если нет span (цены)
                            elements_to_del = driver.find_elements_by_css_selector("#offer_container_bot > div.items > div:nth-child(n) > div.wrapper__price > div.p")
                            print("elements_to_del length -", len(elements_to_del))
                            logger_msg.info("elements_to_del length - " + str(len(elements_to_del)))  # debug
                            for item_del in elements_to_del:
                                try:
                                    item_del.find_element_by_css_selector("span")
                                    print("nice item - continue")
                                    logger_msg.info("nice item - continue")  # debug
                                    continue
                                except:
                                    print("trash item - delete")
                                    logger_msg.info("trash item - delete")  # debug
                                    try:
                                        item_del.click()
                                    except: pass
                                    time.sleep(0.2)
                            elements_to_del = driver.find_elements_by_css_selector("#offer_container_bot > div.items > div:nth-child(n)")
                            print("elements_to_trade if > 0 -> start new trade", len(elements_to_del))
                            logger_msg.info("elements_to_trade if > 0 -> start new trade " + str(len(elements_to_del)))  # debug
                            if len(elements_to_del) > 0:
                                print("start new trade")
                                logger_msg.info("start new trade")  # debug
                                driver.find_element_by_css_selector("#trade_btn").click()

                                print("updating items from db")
                                logger_msg.info("updating items from db")  # debug
                                mycursor.execute("SELECT name,price,count FROM skinsLimit")
                                items_bd = mycursor.fetchall()
                                if len(items_bd) < 5:
                                    time.sleep(5)
                                    mycursor.execute("SELECT name,price,count FROM skinsLimit")
                                    items_bd = mycursor.fetchall()
                                    if len(items_bd) < 5:
                                        logger.exception("cant get items from DB")
                                        raise ValueError('cant get items from DB')
                                time.sleep(9)
                                try:
                                    status_failed1 = driver.find_element_by_css_selector("#trade_modal > div.modal_content > div.waiting > div > div:nth-child(1) > div > svg#fail_trade_icon").is_displayed()
                                except:
                                    status_failed1 = False
                                print("is failed trade -", status_failed1)
                                logger_msg.info("is failed trade - " + str(status_failed1))  # debug
                                # если неудачный трейд
                                if status_failed1 == True:
                                    # add statistic and screen
                                    now = datetime.datetime.now()
                                    outFileName = "statistic.txt"  # windows
                                    outFile = open(outFileName, "a")
                                    outFile.write(str(now) + "/" + "FALSE" + "/" + "trade_2" + "/" + str(int(delta1.total_seconds() * 1000)) + "\n")
                                    outFile.close()
                                    # screen
                                    now = time.strftime('%Y_%m-%d_%H_%M_%S')
                                    #driver.save_screenshot('screens\Trade' + '-' + str(now) + '.png')
                                    print("failed x3")
                                    logger_msg.info("failed x3")  # debug
                                if status_failed1 == False:
                                    # add statistic and screen
                                    now = datetime.datetime.now()
                                    outFileName = "statistic.txt"  # windows
                                    outFile = open(outFileName, "a")
                                    outFile.write(
                                        str(now) + "/" + "TRUE" + "/" + "trade_2" + "/" + str(
                                            int(delta1.total_seconds() * 1000)) + "\n")
                                    outFile.close()
                                    # screen
                                    now = time.strftime('%Y_%m-%d_%H_%M_%S')
                                    #driver.save_screenshot('screens\Trade' + '-' + str(now) + '.png')

                                    print("success!!!")
                                    logger_msg.info("success!!!")  # debug
                                    print("mysql")
                                    logger_msg.info("mysql")  # debug
                                    XML_trade = driver.find_element_by_css_selector('#trade_modal > div.modal_content > div.modal_trade_main_container > div').get_attribute('innerHTML')
                                    XML_split = XML_trade.split('<div class="modal_trade_row superclass_space')
                                    del XML_split[0]

                                    for item_trade in XML_split:
                                        name_trade = re.search('<div class="im_mi([^<]*)</div>', item_trade)
                                        name_trade = name_trade.group(1).split(">")
                                        name_trade = name_trade[1].strip()
                                        exterior_trade = re.search('<div class="r">([^<>]*)</div>', item_trade)
                                        exterior_trade = exterior_trade.group(1).strip()
                                        if len(exterior_trade) > 1:
                                            if exterior_trade == "FN":
                                                exterior_trade = '(Factory New)'
                                            if exterior_trade == "MW":
                                                exterior_trade = '(Minimal Wear)'
                                            if exterior_trade == "BS":
                                                exterior_trade = '(Battle-Scarred)'
                                            if exterior_trade == "WW":
                                                exterior_trade = '(Well-Worn)'
                                            if exterior_trade == "FT":
                                                exterior_trade = '(Field-Tested)';
                                            # делаем полное имя для предмета ксго
                                            # print("full exterior is - ", str(exterior))
                                            name_trade = name_trade + " " + exterior_trade
                                        #price
                                        price_trade = re.search('</span>([^<>]*)</div>', item_trade)
                                        try:
                                            price_trade = price_trade.group(1)
                                            price_trade = float(price_trade.strip())
                                        except:
                                            # удаляем данные
                                            outFileName = "XML.txt"  # windows
                                            now = time.strftime('%Y_%m-%d_%H_%M_%S')
                                            outFile = open(outFileName, "a")
                                            outFile.write(str(now) + " ----------------------------------" + "\n")
                                            outFile.write(str(XML_trade) + "\n")
                                            outFile.close()
                                            print("XML saved in XML.txt")
                                            print("item price is reserved/gone")
                                            #got price
                                            for item_in_list in list_trade:
                                                if item_in_list["name"] == name_trade:
                                                    print("got new price")
                                                    price_trade = float(item_in_list["price"])

                                        print("name and price to mysql", name_trade.encode('utf-8'), price_trade)
                                        logger_msg.info("name and price to mysql " + str(name_trade) + " " + str(price_trade))  # debug
                                        game_id = "730"
                                        now = time.strftime('%Y-%m-%d %H:%M:%S')
                                        mycursor.execute(
                                            "INSERT INTO skins (NAME, PRICE, game_id, platform_from, platform_to, DATE) VALUES (%s, %s, %s, %s, %s, %s)",
                                            (name_trade, price_trade, game_id, '2', '1', now,))
                                        mydb.commit()
                                        print("------------------------------------------------------------------------",name_trade.encode('utf-8'))
                                        logger_msg.info("------------------------------------------------------------------------ " + str(name_trade.encode('utf-8')))  # debug



                    if status_failed == False:
                        # add statistic and screen
                        now = datetime.datetime.now()
                        outFileName = "statistic.txt"  # windows
                        outFile = open(outFileName, "a")
                        outFile.write(str(now) + "/" + "TRUE" + "/" + "trade_" + str(index_trade) + "/" + str(
                            int(delta1.total_seconds() * 1000)) + "\n")
                        outFile.close()
                        # screen
                        now = time.strftime('%Y_%m-%d_%H_%M_%S')
                        #driver.save_screenshot('screens\Trade' + '-' + str(now) + '.png')

                        print("success!!!")
                        logger_msg.info("success!!!")  # debug
                        print("mysql")
                        logger_msg.info("mysql")  # debug
                        XML_trade = driver.find_element_by_css_selector(
                            '#trade_modal > div.modal_content > div.modal_trade_main_container > div').get_attribute(
                            'innerHTML')
                        XML_split = XML_trade.split('<div class="modal_trade_row superclass_space')
                        del XML_split[0]

                        for item_trade in XML_split:
                            name_trade = re.search('<div class="im_mi([^<]*)</div>', item_trade)
                            name_trade = name_trade.group(1).split(">")
                            name_trade = name_trade[1].strip()
                            exterior_trade = re.search('<div class="r">([^<>]*)</div>', item_trade)
                            exterior_trade = exterior_trade.group(1).strip()
                            if len(exterior_trade) > 1:
                                if exterior_trade == "FN":
                                    exterior_trade = '(Factory New)'
                                if exterior_trade == "MW":
                                    exterior_trade = '(Minimal Wear)'
                                if exterior_trade == "BS":
                                    exterior_trade = '(Battle-Scarred)'
                                if exterior_trade == "WW":
                                    exterior_trade = '(Well-Worn)'
                                if exterior_trade == "FT":
                                    exterior_trade = '(Field-Tested)';
                                # делаем полное имя для предмета ксго
                                # print("full exterior is - ", str(exterior))
                                name_trade = name_trade + " " + exterior_trade
                            #got price
                            price_trade = re.search('</span>([^<>]*)</div>', item_trade)
                            try:
                                price_trade = price_trade.group(1)
                                price_trade = float(price_trade.strip())
                            except:
                                # удаляем данные
                                #outFileName = "XML.txt"  # windows
                                #now = time.strftime('%Y_%m-%d_%H_%M_%S')
                                #outFile = open(outFileName, "a")
                                #outFile.write(str(now) + " ----------------------------------" + "\n")
                                #outFile.write(str(XML_trade) + "\n")
                                #outFile.close()
                                #print("XML saved in XML.txt")
                                #print("item price is reserved/gone")
                                # got price
                                for item_in_list in list_trade:
                                    if item_in_list["name"] == name_trade:
                                        print("got new price")
                                        price_trade = float(item_in_list["price"])

                            print("name and price to mysql", name_trade.encode('utf-8'), price_trade)
                            logger_msg.info("name and price to mysql " + str(name_trade) + " " + str(price_trade))  # debug
                            game_id = "730"
                            now = time.strftime('%Y-%m-%d %H:%M:%S')
                            mycursor.execute(
                                "INSERT INTO skins (NAME, PRICE, game_id, platform_from, platform_to, DATE) VALUES (%s, %s, %s, %s, %s, %s)",
                                (name_trade, price_trade, game_id, '2', '1', now,))
                            mydb.commit()
                            print("------------------------------------------------------------------------",name_trade.encode('utf-8'))
                            logger_msg.info("------------------------------------------------------------------------ " + str(name_trade.encode('utf-8')))  # debug
                        # close modal window
                        print("close modal window")
                        logger_msg.info("close modal window")  # debug
                        try:
                            driver.find_element_by_css_selector("#trade_modal > a > svg").click()
                            time.sleep(0.2)
                        except:
                            try:
                                driver.find_element_by_css_selector("#trade_modal > a > svg").click()
                                time.sleep(0.2)
                            except:
                                #close modal anti-scam
                                try:
                                    driver.find_element_by_css_selector("body > div.antiscam__wrapper > div > svg.antiscam__close").click()
                                    driver.find_element_by_css_selector("#trade_modal > a > svg").click()
                                except:
                                    logger.exception("can't close modal window")
                                    raise ValueError("can't close modal window")
                        print("break if trade was successful")
                        logger_msg.info("break if trade was successful")  # debug
                        break


            # close modal window
            print("close modal window")
            logger_msg.info("close modal window")  # debug
            try:
                driver.find_element_by_css_selector("#trade_modal > a > svg").click()
                time.sleep(0.2)
            except: pass
            # delete items
            elements_to_del = driver.find_elements_by_css_selector("#offer_container_bot > div.items > div:nth-child(n)")
            print("elements_to_del length -", len(elements_to_del))
            logger_msg.info("elements_to_del length - " + str(len(elements_to_del)))  # debug
            for item_del in elements_to_del:
                item_del.click()
                print("deleted!")
                logger_msg.info("deleted!")  # debug
                time.sleep(0.2)



            #x2 for confidence start live feed again
            try:
                print("start live feed")
                logger_msg.info("start live feed")  # debug
                driver.find_element_by_css_selector("#control_skins_live > div.control_skins_ticker_play").click()
            except:
                try:
                    driver.find_element_by_css_selector("#control_skins_live > div.control_skins_ticker_play").click()
                except:
                    logger.exception("cant start live feed")
                    raise ValueError('cant start live feed')
            print("new live feed")
            logger_msg.info("new live feed")  # debug
            element_to_hover_over = driver.find_element_by_css_selector("div.bot_sort")
            ActionChains(driver).move_to_element(element_to_hover_over).perform()
            time.sleep(0.2)
            ActionChains(driver).move_to_element(element_to_hover_over).perform()
            time.sleep(0.2)
            driver.find_element_by_css_selector("div.bot_sort > div  > div > div > ul > li:nth-child(4) > a").click()
            time.sleep(0.2)
            driver.find_element_by_css_selector("div.bot_sort > div  > div > div > ul > li:nth-child(4) > a").click()
            time.sleep(0.2)
            element_to_hover_over = driver.find_element_by_css_selector("#sell_mode_call > div > span")
            ActionChains(driver).move_to_element(element_to_hover_over).perform()





        #updating live feed (length > 100)
        if len(str_split) > 100:
            print("updating live feed (length > 100)")
            logger_msg.info("updating live feed (length > 100)")  # debug
            element_to_hover_over = driver.find_element_by_css_selector("div.bot_sort")
            ActionChains(driver).move_to_element(element_to_hover_over).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector("div.bot_sort > div  > div > div > ul > li:nth-child(4) > a").click()
            time.sleep(0.2)
            element_to_hover_over = driver.find_element_by_css_selector("#sell_mode_call > div > span")
            ActionChains(driver).move_to_element(element_to_hover_over).perform()



        # обновляем список
        now = datetime.datetime.now()
        delta = now - time_get_items
        #обновляем список цен и оверсток
        if int(delta.total_seconds()) > 600:
            #set True status into DB
            successStatus(True)
            #update script status
            #overstock check
            non_overstock_items_length = driver.find_elements_by_css_selector("#main_container_user > div.items > div:nth-child(n) > div.wrapper__price > div > span")
            if len(non_overstock_items_length) > 0:
                telegram_bot_sendtext("CSmoney: какие-то предметы вышли из overstock'a")
            driver.find_element_by_css_selector("#refresh_inventory_user > svg").click()
            time.sleep(5)
            print("refresh inventory")
            print("updating items from db (every 10 minutes)")
            logger_msg.info("updating items from db (every 10 minutes)")  # debug
            mycursor.execute("SELECT name,price,count FROM skinsLimit")
            items_bd = mycursor.fetchall()
            if len(items_bd) < 5:
                time.sleep(5)
                mycursor.execute("SELECT name,price,count FROM skinsLimit")
                items_bd = mycursor.fetchall()
                if len(items_bd) < 5:
                    logger.exception("cant get items from DB")
                    raise ValueError('cant get items from DB')
            time_get_items = datetime.datetime.now()

        time.sleep(0.1)






except Exception as e:
    print("was an error 1102")
    telegram_bot_sendtext("csMoneyBuy: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()

# # end of code

# In[ ]:


if succsess == 1:
    # close all
    now = datetime.datetime.now()
    print(str(now), "successfully!")
    logger_msg.info(str(now) + "successfully!")  # debug
    # start time
    mycursor.close()
    mydb.close()
    # display.stop() #linux
    driver.close()
    driver.quit()
    sys.exit()
