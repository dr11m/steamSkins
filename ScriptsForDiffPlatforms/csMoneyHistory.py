#!/usr/bin/env python
# coding: utf-8

# # settings, imports and functions

# In[1]:


import os
import time
from selenium import webdriver
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
import logging
from datetime import datetime
import sys


# start time
now1 = datetime.now()
print(str(now1) + "----------------------------------------------------------------------------------------------------------")

# loging errors
# Create a logging instance
logger = logging.getLogger('csMoneyHistory_errors')
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
logger_msg = logging.getLogger('csMoneyHistory_info')
logger_msg.setLevel(logging.INFO)  # you can set this to be DEBUG, INFO, ERROR
# Assign a file-handler to that instance
fh1 = logging.FileHandler("debug.txt")
fh1.setLevel(logging.INFO)
# Format your logs (optional)
formatter = logging.Formatter('%(asctime)s - row:%(lineno)d - %(message)s')
fh1.setFormatter(formatter)  # This will set the format to the file handler
# Add the handler to your logging instance
logger_msg.addHandler(fh1)


# обработка ошибок
def PrintException():
    print("was an error")
    # exception output
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    # screen
    now = datetime.now()
    driver.save_screenshot('Error' + "-" + str(now) + '.png')
    # close all
    mycursor.close()
    mydb.close()
    driver.close()
    driver.quit()
    sys.exit()


executable_path = "/usr/bin/chromedriver"  # linux
# executable_path = "/usr/lib/chromium-browser/chromedriver" # linux2

os.environ["webdriver.chrome.driver"] = executable_path
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
prefs = {"profile.managed_default_content_settings.images": 2}  # 1 - load images, 2 - dont
options.add_experimental_option("prefs", prefs)

# options.add_argument("user-data-dir=C:\\Users\\Administrator\\Desktop\\work\\profiles\\csMoneyHistory")
options.add_argument("user-data-dir=/home/work/profiles/csMoneyHistory")  # linux

options.add_argument('--window-size=1600,900')
driver = webdriver.Chrome(executable_path=executable_path, options=options)




wait = WebDriverWait(driver, 15)  # время вылета 10сек

# outFileName = "C:\\login.txt" #windows
outFileName = "match.txt"  # linux
outFile = open(outFileName, "w")
outFile.write("1")
outFile.close()

print("if this is first time run, close it and add '1' into file named C:\\csMoneyHistoryFirstRun.txt")
logger_msg.info("if this is first time run, close it and add '1' into file named C:\\csMoneyHistoryFirstRun.txt")  # debug


# # CODE

# ## check if I'm logged into steam

# In[2]:


try:
    driver.get("https://steamcommunity.com/market/")
    try:
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#marketWalletBalanceAmount")))
        time.sleep(1)
    except:
        print("type login, pass and guard into a file C:\login.txt")
        logger_msg.info("type login, pass and guard into a file C:\login.txt")  # debug
        # отправляем сообщение и ожидаем ввода данных для входа
        telegram_bot_sendtext(
            "csMoneyHistory: требуется вход в стим (ввести логин, пароль и стим гуард в текстовый файл C:\login.txt)")
        stop = 1
        for i in range(30):
            # with open('C:\\login.txt') as f: #windows
            with open('/home/login.txt') as f:  # linux
                lines = f.readlines()
            if len(lines) == 0:
                time.sleep(2)
            else:
                stop = 0
                break
        if stop == 1:
            raise ValueError('need to login into steam')
        if len(lines) == 3:
            login = lines[0]
            password = lines[1]
            guard = lines[2]

        # удаляем данные
        # outFileName = "C:\\login.txt" #windows
        outFileName = "/home/login.txt"  # linux
        outFile = open(outFileName, "w")
        outFile.write("")
        outFile.close()
        # входим в стим
        driver.find_element_by_css_selector("#global_action_menu > a").click()
        time.sleep(1)
        # login
        input_field = driver.find_element_by_css_selector('#input_username')
        input_field.clear()
        input_field.send_keys(login)
        time.sleep(2)
        # pass
        input_field = driver.find_element_by_css_selector('#input_password')
        input_field.clear()
        input_field.send_keys(password, Keys.RETURN)
        time.sleep(3)
        input_field = driver.find_element_by_css_selector('#twofactorcode_entry')
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
    telegram_bot_sendtext("csMoneyHistory: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()


# ## check if I'm logged into csMoney

# In[3]:


try:
    driver.get("https://old.cs.money/en")
    time.sleep(3)

    # LOGIN
    need_to_login = None
    try:
        need_to_login = driver.find_element_by_css_selector("#authenticate_button > a")
    except:
        pass
    if need_to_login is not None:
        driver.find_element_by_css_selector("#authenticate_button > a").click()
        time.sleep(5)
        driver.find_element_by_css_selector("#imageLogin").click()
        time.sleep(3)
        try:
            need_to_login = driver.find_element_by_css_selector("#authenticate_button > a")
            msg = "failed to login into csMoney"
            logger.exception(msg)
            raise ValueError('failed to login into csMoney')
        except:
            pass

except Exception as e:
    telegram_bot_sendtext("csMoneyHistory: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()


# ## open up history section

# In[4]:
first = 0

try:

    # проверяем, не первый ли запуск и устанавливаем safe-traffic-mode, если первый
    try:
        # with open('C:\\csMoneyHistoryFirstRun.txt') as f: #windows
        with open('/home/csMoneyHistoryFirstRun.txt') as f:  # linux
            first = f.readline()
    except:
        pass
    if first == "1":
        print("first time running program (adding safe-traffic-mode)")
        logger_msg.info("first time running program (adding safe-traffic-mode)")  # debug
        driver.find_element_by_css_selector("div.header_menu_container > div.header_setting > svg").click()
        time.sleep(2)
        driver.find_element_by_css_selector(
            "div.modal_content_settings_row.displaying > div:nth-child(1) > div").click()
        time.sleep(2)
        print("(first run) safe traffic mode was turned ON")
        logger_msg.info("(first run) safe traffic mode was turned ON")  # debug
        # screen
        now = datetime.now()
        driver.save_screenshot('safe_traffic_mode' + "-" + str(now) + '.png')
        driver.find_element_by_css_selector("#settings_modal > a > svg").click()
        time.sleep(0.5)
        #del file info
        #outFileName = "C:\\csMoneyHistoryFirstRun.txt" #windows
        outFileName = "/home/csMoneyHistoryFirstRun.txt"  # linux
        outFile = open(outFileName, "w")
        outFile.write("")
        outFile.close()

    # переходим на страницу истории продаж
    # открываем меню в верхнем правом углу
    element_to_hover_over = driver.find_element_by_css_selector(
        "#header > div > div.profile.block_menu > a > div.profile_arrow > svg")
    ActionChains(driver).move_to_element(element_to_hover_over).perform()
    time.sleep(0.5)
    # кликаем на personal area
    driver.find_element_by_css_selector(
        "#header > div > div.profile.block_menu > div > ul > li:nth-child(1) > a > div").click()
    element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#personal_content_transaction > div:nth-child(1)")))
    # переходим в меню, где мы выберем 'accepted'
    element_to_hover_over = driver.find_element_by_css_selector("#personal_menu_title_transactions")
    ActionChains(driver).move_to_element(element_to_hover_over).perform()
    time.sleep(0.5)
    # кликаем на 'accepted'
    driver.find_element_by_css_selector(
        "#pa_status_filter > div.personal_menu_status > div.personal_menu_status_transactions > div:nth-child(2)").click()
    # убираем курсор, чтобы избежать ошибок
    element_to_hover_over = driver.find_element_by_css_selector(
        "#personal_area > :nth-child(5) > :nth-child(1) > :nth-child(4)")
    ActionChains(driver).move_to_element(element_to_hover_over).perform()
    # ожидаем появления
    element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#personal_content_transaction > div:nth-child(1)")))
    # если не получилось выбрать нужные, то завершаем работу
    is_accepted = driver.find_element_by_css_selector("#personal_menu_title_transactions").text
    print("is_accepted (must be 'ACCEPTED') - " + str(is_accepted.strip()))
    logger_msg.info("is_accepted (must be 'ACCEPTED') - " + str(is_accepted.strip()))  # debug
    if is_accepted.strip() != "ACCEPTED":
        raise ValueError("not a list of accepted trades")
except Exception as e:
    telegram_bot_sendtext("csMoneyHistory: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()


# ## check if need to turn on traffic safe mode

# In[1]:


try:
    go_again = 0
    rows = driver.find_elements_by_xpath('//*[@id="personal_content_transaction"]/div')
    index = 0
    stop = 0
    for row in rows:
        if stop == 1:
            break
        index += 1
        next_iteration = 0
        row.location_once_scrolled_into_view
        list_exists = None
        try:
            list_exists = row.find_element_by_css_selector("div > div.personal_trade_id > svg")
        except:
            pass
        # если есть подсписок
        if list_exists is not None:
            # для выхода из основного цикла
            next_iteration = 1
            # открываем список
            list_exists.click()
            time.sleep(0.2)
            # выбираем все предметы в списке, используя индекс
            rows_in_list = driver.find_elements_by_xpath('//*[@id="personal_content_transaction"]/div[' + str(index) + ']/div[2]/div/div')
            # проверяем предметы в списке
            for row_list in rows_in_list:
                row_list.location_once_scrolled_into_view
                response1 = None
                if response1 == None:
                    print("start checking sublist for traffic mode")
                    # перетаскиваем курсор в свободное место
                    element_to_hover_over = driver.find_element_by_css_selector(
                        "#personal_area > div.personal_modal_content > div.personal_title > div.personal_title_text_main.superclass_space > div:nth-child(3) > div > div")
                    ActionChains(driver).move_to_element(element_to_hover_over).perform()
                    time.sleep(0.2)
                    # перетаскиваем на элемент 'items'
                    element_to_hover_over = row_list.find_element_by_css_selector(".personal_skins_text")
                    ActionChains(driver).move_to_element(element_to_hover_over).perform()
                    time.sleep(0.1)
                    # перетаскиваем на элемент 'items' для точности второй раз
                    element_to_hover_over = row_list.find_element_by_css_selector(".personal_skins_text")
                    ActionChains(driver).move_to_element(element_to_hover_over).perform()
                    time.sleep(0.2)
                    # качество, нужное для полного имени ксго предмета, так же для определения игры
                    try:
                        exterior = driver.find_element_by_css_selector(".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item > .s_c > .r").text
                    except:
                        continue

                    # для определения игры
                    game_id = "730"
                    # получаем название предмета (есть два варианта)
                    try:
                        name = driver.find_element_by_css_selector(".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item > .im_min_ws").text
                        stop = 1
                        break
                    except:
                        try:
                            name = driver.find_element_by_css_selector(".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item > .im_min_wst").text
                            stop = 1
                            break
                        except:
                            #set up traffic mode
                            print("set up traffic mode")
                            driver.find_element_by_css_selector("#personal_area > a > svg").click()
                            driver.find_element_by_css_selector("div.header_menu_container > div.header_setting > svg").click()
                            time.sleep(2)
                            driver.find_element_by_css_selector(
                                "div.modal_content_settings_row.displaying > div:nth-child(1) > div").click()
                            time.sleep(2)
                            print("(first run) safe traffic mode was turned ON")
                            logger_msg.info("(first run) safe traffic mode was turned ON")  # debug
                            # screen
                            now = datetime.now()
                            driver.save_screenshot('safe_traffic_mode' + "-" + str(now) + '.png')
                            driver.find_element_by_css_selector("#settings_modal > a > svg").click()
                            time.sleep(0.5)
                            stop = 1
                            go_again = 1
                            break


            continue
        print("sublist doesn't exist for traffic mode")
        response1 = None
        if response1 == None:
            # перетаскиваем курсор в свободное место
            element_to_hover_over = driver.find_element_by_css_selector(
                "#personal_area > div.personal_modal_content > div.personal_title > div.personal_title_text_main.superclass_space > div:nth-child(3) > div > div")
            ActionChains(driver).move_to_element(element_to_hover_over).perform()
            time.sleep(0.2)
            # перетаскиваем на элемент 'items'
            element_to_hover_over = row.find_element_by_css_selector(".personal_skins_text")
            ActionChains(driver).move_to_element(element_to_hover_over).perform()
            time.sleep(0.1)
            # перетаскиваем на элемент 'items' для точности второй раз
            element_to_hover_over = row.find_element_by_css_selector(".personal_skins_text")
            ActionChains(driver).move_to_element(element_to_hover_over).perform()
            time.sleep(0.5)
            # качество, нужное для полного имени ксго предмета, так же для определения игры
            try:
                exterior = driver.find_element_by_css_selector(".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item > .s_c > .r").text
            except:
                continue
            # для определения игры
            game_id = "730"
            # получаем название предмета (есть два варианта)
            try:
                name = driver.find_element_by_css_selector(".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item > .im_min_ws").text
                stop = 1
                break
            except:
                try:
                    name = driver.find_element_by_css_selector(".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item > .im_min_wst").text
                    stop = 1
                    break
                except:
                    #set up traffic mode
                    print("set up traffic mode")
                    driver.find_element_by_css_selector("#personal_area > a > svg").click()
                    driver.find_element_by_css_selector("div.header_menu_container > div.header_setting > svg").click()
                    time.sleep(2)
                    driver.find_element_by_css_selector(
                        "div.modal_content_settings_row.displaying > div:nth-child(1) > div").click()
                    time.sleep(2)
                    print("(first run) safe traffic mode was turned ON")
                    logger_msg.info("(first run) safe traffic mode was turned ON")  # debug
                    # screen
                    now = datetime.now()
                    driver.save_screenshot('safe_traffic_mode' + "-" + str(now) + '.png')
                    driver.find_element_by_css_selector("#settings_modal > a > svg").click()
                    time.sleep(0.5)
                    stop = 1
                    go_again = 1
                    break

except Exception as e:
    telegram_bot_sendtext("csMoneyHistory: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()


# ## take items and upload into DB

# In[5]:


try:
    # если мы меняли траффик мод, то заходим еще раз
    if go_again == 1:
       # переходим на страницу истории продаж
        # открываем меню в верхнем правом углу
        element_to_hover_over = driver.find_element_by_css_selector(
            "#header > div > div.profile.block_menu > a > div.profile_arrow > svg")
        ActionChains(driver).move_to_element(element_to_hover_over).perform()
        time.sleep(0.5)
        # кликаем на personal area
        driver.find_element_by_css_selector(
            "#header > div > div.profile.block_menu > div > ul > li:nth-child(1) > a > div").click()
        element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#personal_content_transaction > div:nth-child(1)")))
        # переходим в меню, где мы выберем 'accepted'
        element_to_hover_over = driver.find_element_by_css_selector("#personal_menu_title_transactions")
        ActionChains(driver).move_to_element(element_to_hover_over).perform()
        time.sleep(0.5)
        # кликаем на 'accepted'
        driver.find_element_by_css_selector(
            "#pa_status_filter > div.personal_menu_status > div.personal_menu_status_transactions > div:nth-child(2)").click()
        # убираем курсор, чтобы избежать ошибок
        element_to_hover_over = driver.find_element_by_css_selector(
            "#personal_area > :nth-child(5) > :nth-child(1) > :nth-child(4)")
        ActionChains(driver).move_to_element(element_to_hover_over).perform()
        # ожидаем появления
        element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#personal_content_transaction > div:nth-child(1)")))
        # если не получилось выбрать нужные, то завершаем работу
        is_accepted = driver.find_element_by_css_selector("#personal_menu_title_transactions").text
        print("is_accepted (must be 'ACCEPTED') - " + str(is_accepted.strip()))
        logger_msg.info("is_accepted (must be 'ACCEPTED') - " + str(is_accepted.strip()))  # debug
        if is_accepted.strip() != "ACCEPTED":
            raise ValueError("not a list of accepted trades")

    orders = "0"
    time.sleep(3)
    for index_page in range(15): #pages
        index = 0
        rows = driver.find_elements_by_xpath('//*[@id="personal_content_transaction"]/div')
        for row in rows:
            index += 1
            next_iteration = 0
            row.location_once_scrolled_into_view
            # проверяем, нет ли подсписка в строчке (несколько предметов в одном обмене)
            # получаем дату, так как её нет внутри списка
            trade_date = row.find_element_by_css_selector(".personal_date").text
            print("trade date is - ", trade_date)
            logger_msg.info("trade date is - " + str(trade_date))  # debug
            list_exists = None
            try:
                list_exists = row.find_element_by_css_selector("div > div.personal_trade_id > svg > use")
            except:
                pass
            # если есть подсписок
            if list_exists is not None:
                print("sublist exists")
                logger_msg.info("sublist exists")  # debug
                # для выхода из основного цикла
                next_iteration = 1
                # открываем список
                driver.find_element_by_css_selector("#personal_content_transaction > div:nth-child(" + str(index) + ") > div.personal_row > div.personal_trade_id").click()
                time.sleep(0.5)
                # если не получилось открыть с первого раза
                try:
                    added_or_withdrawn = driver.find_element_by_xpath('//*[@id="personal_content_transaction"]/div[1]/div[2]/div[1]/div/div[5]/span').text
                    added_or_withdrawn = added_or_withdrawn.strip()
                    if added_or_withdrawn != "Withdrawn from balance:":
                        print("couldnt open sublist properly, will try 1more time")
                        driver.find_element_by_css_selector("#personal_content_transaction > div:nth-child(" + str(index) + ") > div.personal_row > div.personal_trade_id").click()
                        time.sleep(0.5)
                except: pass
                # выбираем все предметы в списке, используя индекс
                rows_in_list = driver.find_elements_by_xpath(
                    '//*[@id="personal_content_transaction"]/div[' + str(index) + ']/div[2]/div/div')
                print("sublist length is - ", str(len(rows_in_list)))
                logger_msg.info("sublist length is - " + str(len(rows_in_list)))  # debug
                # проверяем предметы в списке
                for row_list in rows_in_list:
                    row_list.location_once_scrolled_into_view
                    # получаем ти транзакции (вывод баланса или ввод)
                    added_or_withdrawn = row_list.find_element_by_xpath('div[5]/span').text
                    added_or_withdrawn = added_or_withdrawn.strip()
                    print("withdrawn or added (must be 'Withdrawn from balance:') - ", added_or_withdrawn)
                    logger_msg.info(
                        "withdrawn or added (must be 'Withdrawn from balance:') - " + str(added_or_withdrawn))  # debug
                    # нам нужен только вывод
                    if added_or_withdrawn != "Withdrawn from balance:":
                        print("balance was added (continue)")
                        logger_msg.info("balance was added (continue)")  # debug
                        continue
                    price = row_list.find_element_by_css_selector(".personal_offered").text
                    price = float(price[12:])
                    print("price is - ", str(price))
                    logger_msg.info("price is - " + str(price))  # debug
                    trade_id = row_list.find_element_by_css_selector(".personal_trade_id").text
                    trade_id = trade_id.strip()
                    trade_id = trade_id[10:]
                    print("trade id is - ", str(trade_id))
                    logger_msg.info("trade id is - " + str(trade_id))  # debug
                    # проверяем, нет ли предмета в БД
                    mycursor.execute("SELECT price, id  FROM skins WHERE unique_platform_id = %s LIMIT 1", (trade_id,))
                    response = mycursor.fetchone()
                    if response != None:
                        print("item is already exists in DB (no need to add it) - ", str(response))
                        logger_msg.info("item is already exists in DB (no need to add it) - " + str(response))  # debug
                        # если нет
                    if response == None:
                        print("there is no such item in DB (that's cool)")
                        logger_msg.info("there is no such item in DB (that's cool)")  # debug
                        # перетаскиваем курсор в свободное место
                        element_to_hover_over = driver.find_element_by_css_selector(
                            "#personal_area > div.personal_modal_content > div.personal_title > div.personal_title_text_main.superclass_space > div:nth-child(3) > div > div")
                        ActionChains(driver).move_to_element(element_to_hover_over).perform()
                        time.sleep(0.2)
                        # перетаскиваем на элемент 'items'
                        element_to_hover_over = row_list.find_element_by_css_selector(".personal_skins_text")
                        ActionChains(driver).move_to_element(element_to_hover_over).perform()
                        time.sleep(0.1)
                        # перетаскиваем на элемент 'items' для точности второй раз
                        element_to_hover_over = row_list.find_element_by_css_selector(".personal_skins_text")
                        ActionChains(driver).move_to_element(element_to_hover_over).perform()
                        time.sleep(0.2)
                        # качество, нужное для полного имени ксго предмета, так же для определения игры
                        exterior = driver.find_element_by_css_selector(
                            ".skins_list > .skin_list > .skin_list_row > :nth-child(3) > div.item:nth-child(2) > .s_c > .r").text

                        # для определения игры
                        game_id = "730"
                        # получаем название предмета (есть два варианта)
                        try:
                            name = driver.find_element_by_css_selector(
                                ".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item > .im_min_ws").text
                        except:
                            name = driver.find_element_by_css_selector(
                                ".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item > .im_min_wst").text
                        # strip для переменных
                        exterior = exterior.strip()
                        print("exterior is - ", str(exterior))
                        logger_msg.info("exterior is - " + str(exterior))  # debug
                        name = name.strip()
                        print("name is - ", str(name.encode('utf-8')))
                        logger_msg.info("name is - " + str(name.encode('utf-8')))  # debug
                        # если есть одно из этих качетсв, то предмет из доты
                        if exterior == "Common" or exterior == "Uncommon" or exterior == "Mythical" or exterior == "Rare" or exterior == "Immortal" or exterior == "Legendary" or exterior == "Arcana":
                            game_id = "570"
                            print("game id is 570 (dota)")
                            logger_msg.info("game id is 570 (dota)")  # debug
                        # получаем полное качество предмета из ксго
                        if game_id == "730":
                            print("game id is 730 (csgo)")
                            logger_msg.info("game id is 730 (csgo)")  # debug
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
                        print("full exterior is - ", str(exterior))
                        logger_msg.info("full exterior is - " + str(exterior))  # debug
                        name = name + " " + exterior
                        name = name.strip()
                        print("full item's name is - ", str(name.encode('utf-8')))
                        logger_msg.info("full item's name is - " + str(name.encode('utf-8')))  # debug
                        # counter items and add all
                        count_items = driver.find_elements_by_css_selector(
                            ".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item")
                        if len(count_items) != 1:
                            print("items in sublist is more than 1, need to divide price. items length in sublist is -",
                                  str(len(count_items)))
                            logger_msg.info(
                                "items in sublist is more than 1, need to divide price. items length in sublist is -" + str(
                                    len(count_items)))  # debug
                            price = price / len(count_items)
                            print("new price is - ", str(price))
                            logger_msg.info("new price is - " + str(price))  # debug
                        for count_item in count_items:
                            if game_id == "730":
                                # проверяем, нет ли предмета в БД
                                mycursor.execute(
                                    "SELECT name FROM `skins` WHERE `unique_platform_id` IS null AND `platform_from` = '2' AND `DATE` > DATE_ADD(NOW(), INTERVAL -1 HOUR) AND `NAME` = %s ;",(name,))
                                response_check = mycursor.fetchall()
                                if len(response_check) > 0:
                                    print("item is already exists (continue)")
                                    continue

                                mycursor.execute(
                                    "INSERT INTO skins (NAME, PRICE, game_id, platform_from, platform_to, DATE, unique_platform_id, orders) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                    (name, price, game_id, '2', '1', trade_date, trade_id, orders,))
                                mydb.commit()
                                print(mycursor.rowcount, "record(s) affected")
                                logger_msg.info(str(mycursor.rowcount) + "record(s) affected")  # debug
                                print("------------------------------------------------------------------------",
                                      name.encode('utf-8'))
                                logger_msg.info(
                                    "------------------------------------------------------------------------" + str(
                                        name.encode('utf-8')))  # debug
                            if game_id == "570":
                                # проверяем, нет ли предмета в БД
                                mycursor.execute(
                                    "SELECT name FROM `skins` WHERE `unique_platform_id` IS null AND `platform_from` = '2' AND `DATE` > DATE_ADD(NOW(), INTERVAL -1 HOUR) AND `NAME` = %s ;",
                                    (name,))
                                response_check = mycursor.fetchall()
                                if len(response_check) > 0:
                                    print("item is already exists (continue)")
                                    continue
                                mycursor.execute(
                                    "INSERT INTO skins (NAME, PRICE, game_id, platform_from, platform_to, DATE, unique_platform_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                    (name, price, game_id, '2', '1', trade_date, trade_id,))
                                mydb.commit()
                                print(mycursor.rowcount, "record(s) affected")
                                logger_msg.info(str(mycursor.rowcount) + "record(s) affected")  # debug
                                print("------------------------------------------------------------------------",
                                      name.encode('utf-8'))
                                logger_msg.info(
                                    "------------------------------------------------------------------------" + str(
                                        name.encode('utf-8')))  # debug

            # если был подсписок
            if next_iteration == 1:
                print("was a sublist, continue")
                logger_msg.info("was a sublist, continue")  # debug
                continue
            print("sublist doesn't exist")
            logger_msg.info("sublist doesn't exist")  # debug
            # получаем ти транзакции (вывод баланса или ввод)
            added_or_withdrawn = row.find_element_by_xpath('div[5]/span').text
            added_or_withdrawn = added_or_withdrawn.strip()
            print("withdrawn or added (must be 'Withdrawn from balance:') - ", added_or_withdrawn)
            logger_msg.info(
                "withdrawn or added (must be 'Withdrawn from balance:') - " + str(added_or_withdrawn))  # debug
            # нам нужен только вывод
            if added_or_withdrawn != "Withdrawn from balance:":
                print("balance was added (continue)")
                logger_msg.info("balance was added (continue)")  # debug
                continue
            price = row.find_element_by_css_selector(".personal_offered").text
            price = float(price[12:])
            print("price is - ", str(price))
            logger_msg.info("price is - " + str(price))  # debug
            trade_id = row.find_element_by_css_selector(".personal_trade_id").text
            trade_id = trade_id.strip()
            trade_id = trade_id[10:]
            print("trade id is - ", str(trade_id))
            logger_msg.info("trade id is - " + str(trade_id))  # debug
            # проверяем, нет ли предмета в БД
            mycursor.execute("SELECT price, id FROM skins WHERE DATE = %s AND unique_platform_id = %s LIMIT 1",
                             (trade_date, trade_id,))
            response = mycursor.fetchone()
            if response != None:
                print("item is already exists in DB (no need to add it) - ", str(response))
                logger_msg.info("item is already exists in DB (no need to add it) - " + str(response))  # debug
                # если нет
            if response == None:
                print("there is no such item in DB (that's cool)")
                logger_msg.info("there is no such item in DB (that's cool)")  # debug
                # перетаскиваем курсор в свободное место
                element_to_hover_over = driver.find_element_by_css_selector(
                    "#personal_area > div.personal_modal_content > div.personal_title > div.personal_title_text_main.superclass_space > div:nth-child(3) > div > div")
                ActionChains(driver).move_to_element(element_to_hover_over).perform()
                time.sleep(0.2)
                # перетаскиваем на элемент 'items'
                element_to_hover_over = row.find_element_by_css_selector(".personal_skins_text")
                ActionChains(driver).move_to_element(element_to_hover_over).perform()
                time.sleep(0.1)
                # перетаскиваем на элемент 'items' для точности второй раз
                element_to_hover_over = row.find_element_by_css_selector(".personal_skins_text")
                ActionChains(driver).move_to_element(element_to_hover_over).perform()
                time.sleep(0.5)
                # качество, нужное для полного имени ксго предмета, так же для определения игры
                exterior = driver.find_element_by_css_selector(
                    ".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item > .s_c > .r").text
                # для определения игры
                game_id = "730"
                # получаем название предмета (есть два варианта)
                try:
                    name = driver.find_element_by_css_selector(
                        ".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item > .im_min_ws").text
                except:
                    name = driver.find_element_by_css_selector(
                        ".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item > .im_min_wst").text
                # strip для переменных
                exterior = exterior.strip()
                print("exterior is - ", str(exterior))
                logger_msg.info("exterior is - " + str(exterior))  # debug
                name = name.strip()
                print("name is ", str(name.encode('utf-8')))
                logger_msg.info("name is - " + str(name.encode('utf-8')))  # debug
                # если есть одно из этих качетсв, то предмет из доты
                if exterior == "Common" or exterior == "Uncommon" or exterior == "Mythical" or exterior == "Rare" or exterior == "Immortal" or exterior == "Legendary" or exterior == "Arcana":
                    print("game id is 570 (dota)")
                    logger_msg.info("game id is 570 (dota)")  # debug
                    game_id = "570"
                # получаем полное качество предмета из ксго
                if game_id == "730":
                    print("game id is 730 (csgo)")
                    logger_msg.info("game id is 730 (csgo)")  # debug
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
                print("full exterior is - ", str(exterior))
                logger_msg.info("full exterior is - " + str(exterior))  # debug
                name = name + " " + exterior
                name = name.strip()
                print("full item's name is - ", str(name.encode('utf-8')))
                logger_msg.info("full item's name is - " + str(name.encode('utf-8')))  # debug
                # counter items and add all
                count_items = driver.find_elements_by_css_selector(
                    ".skins_list > .skin_list > .skin_list_row > :nth-child(3) > .item")
                if len(count_items) != 1:
                    print("items in sublist is more than 1, need to divide price. items length in sublist is -",
                          str(len(count_items)))
                    logger_msg.info(
                        "items in sublist is more than 1, need to divide price. items length in sublist is -" + str(
                            len(count_items)))  # debug
                    price = price / len(count_items)
                    print("new price is - ", str(price))
                    logger_msg.info("new price is - " + str(price))  # debug
                for count_item in count_items:
                    if game_id == "730":
                        # проверяем, нет ли предмета в БД
                        mycursor.execute(
                            "SELECT name FROM `skins` WHERE `unique_platform_id` IS null AND `platform_from` = '2' AND `DATE` > DATE_ADD(NOW(), INTERVAL -1 HOUR) AND `NAME` = %s ;",
                            (name,))
                        response_check = mycursor.fetchall()
                        if len(response_check) > 0:
                            print("item is already exists (continue)")
                            continue

                        mycursor.execute(
                            "INSERT INTO skins (NAME, PRICE, game_id, platform_from, platform_to, DATE, unique_platform_id, orders) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (name, price, game_id, '2', '1', trade_date, trade_id, orders,))
                        mydb.commit()
                        print(mycursor.rowcount, "record(s) affected")
                        logger_msg.info(str(mycursor.rowcount) + "record(s) affected")  # debug
                        print("------------------------------------------------------------------------",
                              name.encode('utf-8'))
                        logger_msg.info(
                            "------------------------------------------------------------------------" + str(
                                name.encode('utf-8')))  # debug
                    if game_id == "570":
                        # проверяем, нет ли предмета в БД
                        mycursor.execute(
                            "SELECT name FROM `skins` WHERE `unique_platform_id` IS null AND `platform_from` = '2' AND `DATE` > DATE_ADD(NOW(), INTERVAL -1 HOUR) AND `NAME` = %s ;",
                            (name,))
                        response_check = mycursor.fetchall()
                        if len(response_check) > 0:
                            print("item is already exists (continue)")
                            continue

                        mycursor.execute(
                            "INSERT INTO skins (NAME, PRICE, game_id, platform_from, platform_to, DATE, unique_platform_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (name, price, game_id, '2', '1', trade_date, trade_id,))
                        mydb.commit()
                        print(mycursor.rowcount, "record(s) affected")
                        logger_msg.info(str(mycursor.rowcount) + "record(s) affected")  # debug
                        print("------------------------------------------------------------------------",
                              name.encode('utf-8'))
                        logger_msg.info(
                            "------------------------------------------------------------------------" + str(
                                name.encode('utf-8')))  #debug

        #меняем страницу
        driver.find_element_by_css_selector(
            "#transactions_pages_list > .transactions_footer_lists > .transactions_footer_next > .transactions_arrow").click()
        print("click to the new page")
        logger_msg.info("click to the new page")  #debug
        time.sleep(4)
        element = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#personal_content_transaction > div:nth-child(1)")))


except Exception as e:
    telegram_bot_sendtext("csMoneyHistory: Возникла ошибка, нужно выяснять")
    logger.exception(e)  #Will send the errors to the file
    PrintException()


# ## end program

# In[ ]:


print("successfully!")
# start time
now = datetime.now()
print(str(now) + "----------------------------------------------------------------------------------------------------------")
logger_msg.info("successfully!")  #debug
#close all
mycursor.close()
mydb.close()
driver.close()
driver.quit()
sys.exit()
