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
from selenium.common.exceptions import NoSuchElementException
import requests
import MySQLdb
import datetime
import mysql.connector
import logging
import re
import urllib
from pyvirtualdisplay import Display
import subprocess


print("=============")

#настройка и главные функции
try:

    #конфиг
    min_perccent = "-22"

        #конфиг
    min_perccent = "-19"
    sales_per_week = "22"
    min_price = "33"

    white_list = [
        "M4A1-S | Master Piece (Battle-Scarred)",
        "StatTrak™ M4A1-S | Hyper Beast (Well-Worn)",
        "Souvenir AWP | Acheron (Minimal Wear)",
        "Desert Eagle | Cobalt Disruption (Field-Tested)",
        "P250 | Undertow (Minimal Wear)",
        "★ Shadow Daggers | Black Laminate (Minimal Wear)",
        "StatTrak™ M4A1-S | Cyrex (Factory New)",
        "★ Shadow Daggers | Black Laminate (Field-Tested)",
        "StatTrak™ Galil AR | Chromatic Aberration (Factory New)",
        "AK-47 | Neon Rider (Well-Worn)",
        "StatTrak™ Glock-18 | Snack Attack (Factory New)",
        "★ Shadow Daggers | Gamma Doppler (Factory New)",
        "M4A1-S | Master Piece (Minimal Wear)",
        "★ Shadow Daggers | Freehand (Field-Tested)",
        "M4A1-S | Golden Coil (Factory New)",
        "★ Falchion Knife | Lore (Field-Tested)",
        "★ Hydra Gloves | Mangrove (Well-Worn)",
        "★ Shadow Daggers | Boreal Forest (Field-Tested)",
        "StatTrak™ MP9 | Food Chain (Factory New)",
        "StatTrak™ MP9 | Food Chain (Factory New)",
        "StatTrak™ MAG-7 | Justice (Factory New)",
        "StatTrak™ M4A1-S | Basilisk (Factory New)",
        "★ Navaja Knife | Blue Steel (Field-Tested)",
        "★ Shadow Daggers | Night (Field-Tested)",
        "StatTrak™ M4A1-S | Cyrex (Field-Tested)",
        "Galil AR | CAUTION! (Factory New)",
        "★ Bowie Knife | Freehand (Field-Tested)",
        "StatTrak™ Glock-18 | Bullet Queen (Minimal Wear)",
        "★ Gut Knife | Black Laminate (Well-Worn)",
        "P250 | Digital Architect (Minimal Wear)",
        "StatTrak™ AK-47 | Red Laminate (Field-Tested)",
        "USP-S | Whiteout (Factory New)",
        "★ Shadow Daggers | Bright Water (Field-Tested)",
        "★ Gut Knife | Boreal Forest (Field-Tested)",
        "Souvenir AK-47 | Black Laminate (Minimal Wear)",
        "StatTrak™ M4A1-S | Atomic Alloy (Minimal Wear)",
        "★ Huntsman Knife | Urban Masked (Field-Tested)",
        "★ Navaja Knife | Damascus Steel (Minimal Wear)",
        "★ Falchion Knife | Bright Water (Field-Tested)",
        "M4A1-S | Atomic Alloy (Minimal Wear)",
        "CZ75-Auto | The Fuschia Is Now (Field-Tested)",
        "★ Hydra Gloves | Case Hardened (Battle-Scarred)",
        "★ Bowie Knife | Black Laminate (Field-Tested)",
        "★ Shadow Daggers | Autotronic (Field-Tested)",
        "M4A1-S | Master Piece (Field-Tested)",
        "StatTrak™ M4A1-S | Hyper Beast (Field-Tested)",
        "StatTrak™ AK-47 | Aquamarine Revenge (Battle-Scarred)",
        "AK-47 | Vulcan (Well-Worn)",
        "M4A1-S | Control Panel (Factory New)",
        "P250 | Undertow (Factory New)",
        "StatTrak™ AK-47 | Slate (Factory New)",
        "StatTrak™ Desert Eagle | Ocean Drive (Field-Tested)",
        "StatTrak™ Glock-18 | Vogue (Factory New)",
        "StatTrak™ M4A4 | Spider Lily (Factory New)",
        "StatTrak™ M4A4 | In Living Color (Minimal Wear)",
        "StatTrak™ M4A4 | The Emperor (Minimal Wear)",
        "StatTrak™ USP-S | The Traitor (Field-Tested)",
        "StatTrak™ USP-S | The Traitor (Minimal Wear)",
        "USP-S | Dark Water (Field-Tested)",
        "★ Gut Knife | Freehand (Field-Tested)",
        "★ Gut Knife | Night (Field-Tested)",
        "★ Hydra Gloves | Mangrove (Battle-Scarred)",
        "★ Shadow Daggers | Forest DDPAT (Field-Tested)",
        "AK-47 | Bloodsport (Well-Worn)",
        "AK-47 | Leet Museo (Factory New)",
        "Desert Eagle | Fennec Fox (Battle-Scarred)",
        "Five-SeveN | Crimson Blossom (Factory New)",
        "MAC-10 | Gold Brick (Minimal Wear)",
        "SSG 08 | Death Strike (Battle-Scarred)",
        "Souvenir Desert Eagle | Fennec Fox (Field-Tested)",
        "StatTrak™ AK-47 | Neon Revolution (Minimal Wear)",
        "StatTrak™ AK-47 | The Empress (Battle-Scarred)",
        "StatTrak™ Desert Eagle | Crimson Web (Minimal Wear)",
        "StatTrak™ M4A1-S | Cyrex (Minimal Wear)",
        "StatTrak™ M4A1-S | Nightmare (Factory New)",
        "StatTrak™ M4A1-S | Player Two (Field-Tested)",
        "USP-S | Ancient Visions (Minimal Wear)",
        "XM1014 | Elegant Vines (Factory New)",
        "★ Falchion Knife | Gamma Doppler (Factory New)",
        "★ Navaja Knife | Ultraviolet (Field-Tested)",
        "Desert Eagle | Fennec Fox (Factory New)",
        "M4A1-S | Atomic Alloy (Factory New)",
        "M4A4 | The Coalition (Factory New)",
        "Souvenir MAC-10 | Gold Brick (Minimal Wear)",
        "StatTrak™ M4A1-S | Nightmare (Minimal Wear)",
        "XM1014 | Elegant Vines (Minimal Wear)",
        "★ Bloodhound Gloves | Bronzed (Field-Tested)",
        "★ Falchion Knife | Night (Field-Tested)",
        "AK-47 | Fuel Injector (Battle-Scarred)",
        "AUG | Sand Storm (Minimal Wear)",
        "AWP | BOOM (Field-Tested)",
        "AWP | Containment Breach (Battle-Scarred)",
        "Glock-18 | Twilight Galaxy (Factory New)",
        "Howl Pin",
        "M4A1-S | Bright Water (Minimal Wear)",
        "M4A1-S | Dark Water (Field-Tested)",
        "StatTrak™ AK-47 | The Empress (Well-Worn)",
        "StatTrak™ AWP | Wildfire (Field-Tested)",
        "StatTrak™ FAMAS | Commemoration (Field-Tested)",
        "StatTrak™ M4A1-S | Decimator (Minimal Wear)",
        "StatTrak™ M4A1-S | Player Two (Battle-Scarred)",
        "StatTrak™ USP-S | The Traitor (Battle-Scarred)",
        "Sticker | Astralis (Gold) | Stockholm 2021",
        "Sticker | Natus Vincere (Gold) | Stockholm 2021",
        "Sticker | Tyloo (Gold) | Stockholm 2021",
        "USP-S | Serum (Factory New)",
        "Valeria Phoenix Pin",
        "★ Driver Gloves | Racing Green (Battle-Scarred)",
        "★ Gut Knife",
        "★ Huntsman Knife | Bright Water (Field-Tested)",
        "★ Huntsman Knife | Rust Coat (Battle-Scarred)",
        "★ Navaja Knife | Crimson Web (Field-Tested)",
        "★ Navaja Knife | Forest DDPAT (Field-Tested)",
        "★ Navaja Knife | Night Stripe (Field-Tested)",
        "★ Navaja Knife | Scorched (Field-Tested)",
        "★ Navaja Knife | Stained (Field-Tested)",
        "★ Navaja Knife | Urban Masked (Field-Tested)",
        "P90 | Death by Kitty (Field-Tested)",
        "AWP | Wildfire (Well-Worn)",
        "CZ75-Auto | The Fuschia Is Now",
        "SSG 08 | Death Strike (Minimal Wear)",
        "StatTrak™ Desert Eagle | Printstream (Battle-Scarred)",
        "StatTrak™ M4A1-S | Guardian (Minimal Wear)",
        "StatTrak™ SSG 08 | Big Iron (Factory New)",
        "Sticker | arT (Gold) | Stockholm 2021",
        "USP-S | Target Acquired (Minimal Wear)",
        "★ Falchion Knife | Urban Masked (Field-Tested)",
        "★ Flip Knife | Autotronic (Battle-Scarred)",
        "★ Gut Knife | Safari Mesh (Field-Tested)",
        "★ Moto Gloves | Transport (Battle-Scarred)",
        "★ Navaja Knife | Damascus Steel (Factory New)",
        "★ Nomad Knife | Scorched (Field-Tested)",
        "★ Specialist Gloves | Forest DDPAT (Battle-Scarred)",
        "CZ75-Auto | The Fuschia Is Now (Factory New)",
        "P90 | Cold Blooded (Factory New)",
        "StatTrak™ AK-47 | Leet Museo (Battle-Scarred)",
        "StatTrak™ Glock-18 | Dragon Tattoo (Factory New)",
        "StatTrak™ Desert Eagle | Ocean Drive (Minimal Wear)",
        "StatTrak™ M4A1-S | Golden Coil (Field-Tested)",
        "StatTrak™ USP-S | Orion (Minimal Wear)",
        "Sticker | NiKo (Gold) | Stockholm 2021",
        "★ Bowie Knife | Bright Water (Field-Tested)",
        "★ Driver Gloves | Overtake (Well-Worn)",
        "★ Driver Gloves | Rezan the Red (Battle-Scarred)",
        "★ Falchion Knife",
        "★ Falchion Knife | Black Laminate (Battle-Scarred)",
        "★ Gut Knife | Damascus Steel (Field-Tested)",
        "★ Huntsman Knife | Forest DDPAT (Field-Tested)",
        "★ Huntsman Knife | Lore (Field-Tested)",
        "★ Moto Gloves | Blood Pressure (Battle-Scarred)",
        "★ Navaja Knife | Damascus Steel (Field-Tested)",
        "★ Shadow Daggers | Scorched (Field-Tested)",
        "★ StatTrak™ Navaja Knife"
    ]

    already_checked = [
        "Glock-18 | Pink DDPAT (Factory New)",
        "M4A1-S | Master Piece (Well-Worn)",
        "Souvenir AK-47 | Green Laminate (Factory New)",
        "StatTrak™ AK-47 | Frontside Misty (Well-Worn)",
        "★ Navaja Knife | Stained (Well-Worn)",
        "ESL One Cologne 2014 Challengers",
        "CS:GO Weapon Case",
        "ESL One Cologne 2014 Challengers",
        "Guardian Elite Pin",
        "StatTrak™ Desert Eagle | Ocean Drive (Well-Worn)",
        "P250 | Digital Architect (Factory New)",
        "StatTrak™ AK-47 | Asiimov (Battle-Scarred)",
        "StatTrak™ AK-47 | Neon Revolution (Battle-Scarred)",
        "StatTrak™ AK-47 | Redline (Well-Worn)",
        "StatTrak™ M4A1-S | Decimator (Factory New)",
        "StatTrak™ M4A1-S | Hyper Beast (Battle-Scarred)",
        "StatTrak™ M4A1-S | Mecha Industries (Battle-Scarred)",
        "StatTrak™ USP-S | The Traitor (Well-Worn)",
        "eSports 2013 Case",
        "★ Navaja Knife | Ultraviolet (Battle-Scarred)",
        "CZ75-Auto | Emerald Quartz (Field-Tested)",
        "P2000 | Ocean Foam (Factory New)",
        "StatTrak™ AWP | Electric Hive (Field-Tested)",
        "StatTrak™ M4A1-S | Dark Water (Field-Tested)",
        "StatTrak™ M4A1-S | Golden Coil (Well-Worn)",
        "★ Driver Gloves | Racing Green (Well-Worn)",
        "★ Gut Knife | Blue Steel (Field-Tested)",
        "★ Huntsman Knife | Freehand (Factory New)",
        "★ Navaja Knife | Blue Steel (Battle-Scarred)",
        "★ Shadow Daggers | Lore (Well-Worn)",
        "StatTrak™ AWP | Neo-Noir (Well-Worn)",
        "StatTrak™ Desert Eagle | Code Red (Well-Worn)",
        "StatTrak™ P250 | Undertow (Factory New)",
        "★ Huntsman Knife | Blue Steel (Field-Tested)",
        "★ Huntsman Knife | Night (Field-Tested)",
        "★ Huntsman Knife | Safari Mesh (Field-Tested)",
        "★ Navaja Knife | Safari Mesh (Battle-Scarred)"
    ]


    #loging errors
        # Create a logging instance
    logger = logging.getLogger('SteamOrderPrices')
    logger.setLevel(logging.INFO) # you can set this to be DEBUG, INFO, ERROR
        # Assign a file-handler to that instance
    fh = logging.FileHandler("ErrorsSteamOrderPrices.txt")
    fh.setLevel(logging.ERROR) # again, you can set this differently
        # Format your logs (optional)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter) # This will set the format to the file handler
        # Add the handler to your logging instance
    logger.addHandler(fh)



    def PrintException():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))



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



    def close_modals():
        try:
            driver.find_element_by_css_selector("body > div.newmodal > div.newmodal_header_border > div > div.newmodal_close").click()
        except:
            pass



    def close_mysql_connection():
        global mydb, mycursor
        try:
            mycursor.close
        except:
            pass
        try:
            mydb.close
        except:
            pass





    def close_script():
        try:
            mycursor.close()
        except:
            pass
        try:
            mydb.close()
        except:
            pass
        try:
            driver.close()
        except:
            pass
        try:
            driver.quit()
        except:
            pass
        sys.exit()



    # rub_usd
    rub_usd = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    rub_usd = rub_usd.json()
    rub_usd = float(rub_usd["Valute"]["USD"]["Value"])
    print("current exchange rate", rub_usd)




    #start driver
    display = Display(visible=0, size=(1600, 900), backend='xvfb')
    display.start()

    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=/home/work/profilesForAll/SteamOrders5")  # linux
    chrome_options.add_argument("window-size=1600,900")
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
    driver.set_window_size(1600, 900)

    wait = WebDriverWait(driver, 60)






    print("-- check if need to loging into steam")
    wait = WebDriverWait(driver, 15)
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






    # получаем, сколько предметов было куплено за последние 7 дней
    close_mysql_connection()
    mycursor.execute("SELECT name FROM PurchasedItems WHERE DATE(date) > (NOW() - INTERVAL 2 DAY);")
    items_mysql_last7days = mycursor.fetchall()
    close_mysql_connection()
    connect_to_mysql("SteamBuyOrders")



#получаем предметы на tryskins
    skins_from_parser = []
    dates_diff = 777
    if dates_diff > 60:
        driver.get("https://skins-table.xyz/table/")
        time.sleep(6)
        element = 0
        try:
            element = driver.find_element_by_css_selector("div.form-group.form-group--sm > a")
        except:pass
        if element != 0:
            driver.find_element_by_css_selector("div.form-group.form-group--sm > a").click()
            time.sleep(5)
            driver.find_element_by_css_selector("#imageLogin").click()
            time.sleep(5)
            driver.get("https://www.google.com/")
            time.sleep(3)
            driver.get("https://skins-table.xyz/table/")
            time.sleep(8)
            element = 0
            try:
                element = driver.find_element_by_css_selector("div.form-group.form-group--sm > a")
            except: pass
            if element != 0:
                raise ValueError('skinstable login error')

        ###############
        # настраиваем #
        ###############
        driver.find_element_by_css_selector("#scroll > div > div.sites.first > div:nth-child(27)").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#scroll > div > div.sites.second > div:nth-child(42)").click()
        time.sleep(2)

        input_field = driver.find_element_by_css_selector('#name')
        input_field.clear()
        time.sleep(2)                                              #min price
        input_field.send_keys(Keys.TAB, Keys.TAB, "2222", Keys.TAB, min_price)
        time.sleep(10)

        input_field = driver.find_element_by_css_selector('#bs1')
        input_field.clear()
        time.sleep(2)                  #sales per week
        input_field.send_keys(Keys.TAB, sales_per_week, Keys.TAB, min_perccent, Keys.TAB)
        time.sleep(5)

        driver.save_screenshot('screen1' + '.png')

        # подгружаем все элементы из parser'a
        for x in range(2):
            try:
                mainBlocks = driver.find_elements_by_css_selector('table > tbody > tr:nth-child(n)')
                len_start = len(mainBlocks)
                element = driver.find_element_by_css_selector(
                    'table > tbody > tr:nth-child(' + str(len(mainBlocks)) + ')')
                element.location_once_scrolled_into_view
                time.sleep(0.2)
                element = driver.find_element_by_css_selector(
                    'table > tbody > tr:nth-child(' + str(len(mainBlocks) - 29) + ')')
                element.location_once_scrolled_into_view
                time.sleep(0.2)
                element = driver.find_element_by_css_selector(
                    'table > tbody > tr:nth-child(' + str(len(mainBlocks)) + ')')
                element.location_once_scrolled_into_view
            except:
                continue
            for ind in range(15):
                mainBlocks = driver.find_elements_by_css_selector('table > tbody > tr:nth-child(n)')
                len_after_scroll = len(mainBlocks)
                if len_start == len_after_scroll:
                    time.sleep(0.5)
                if len_start != len_after_scroll:
                    break
            mainBlocks = driver.find_elements_by_css_selector('table > tbody > tr:nth-child(n)')
            len_after_scroll = len(mainBlocks)
            if len_start == len_after_scroll:
                break

        a = datetime.datetime.now()
        XML = driver.find_element_by_css_selector('#data-table > tbody').get_attribute('innerHTML')
        XML = XML.split('<tr data-id')
        print(len(XML))
        del XML[0]
        # print(XML[0])
        itemsLF = []
        for item_xml in XML:
            # try:
            name = re.search('clipboard-text="([^<]*)">', item_xml)
            name = name[1].strip()
            price = re.search('block-price-old">([^<]*)<i', item_xml).group(1).strip()[2:]
            purchased_count = 0
            for item_mysql in items_mysql_last7days:
                if item_mysql[0] == name:
                    #print("added count")
                    purchased_count += 1

            #если было уже куплено, то пропускаем
            if purchased_count != 0:
                print("item has been bought already")
                continue

            #если нет в списке избранных, то не добавляем
            if name not in white_list:
                #если нет в списке избранных, то не добавляем
                if name not in already_checked:
                    print("--need to check")
                continue

            skins_from_parser.append({"name":name, "price": float(price), "db_id": -1, "purchased_count": purchased_count, "allowed_count": 0, "buy_order_price": 0})



    driver.save_screenshot('screen2' + '.png')
    print("items length to add - ", len(skins_from_parser))
#удаляем все выставленные байордера
    driver.get("https://steamcommunity.com/market/")
    time.sleep(3)
    try:
        element = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#result_0")))
    except:
        raise ValueError('cant load steam market page')

    # получаем баланс, чтобы отсеить дорогие предметы
    balance = driver.find_element_by_css_selector("#header_wallet_balance").text.strip()[:-5]
    try:
        balance = balance.replace(',', '.')  # если целое число (без запятой)
    except:
        print("integer price")
        pass
    balance = float(balance)
    high_limit_of_orders = balance * 10
    #удаляем байордера
    buy_orders_cancel_buttons = driver.find_elements_by_css_selector(
        "#tabContentsMyListings > div:last-child > div.market_listing_row.market_recent_listing_row > div.market_listing_edit_buttons.actual_content > div > a")
    for index in range(len(buy_orders_cancel_buttons)):
        driver.find_element_by_css_selector(
            "#tabContentsMyListings > div:last-child > div:nth-child(3) > div.market_listing_edit_buttons.actual_content > div > a").click()  # кликаем всегда на первую кнопку cancel, тк они пропадают после клика
        time.sleep(6)





#нужно получить цену байордера и проверить, не отличается ли она на более чем 2 процента от цену парсера (если отличается - continue)
#выставляем байордера
    errors = 0
    spent_money = 0

    for item in skins_from_parser:

        #если за проход мы получаем >= 3 ошибки, то перкращаем работу и открываем логи
        if errors == 3:
            raise ValueError('got 3 errors while placing buy orders')

        #открываем предмет
        url_name = urllib.parse.quote(item["name"])
        driver.get("https://steamcommunity.com/market/listings/730/" + url_name)
        time.sleep(7)
        try:
            element = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "span.market_commodity_orders_header_promote:last-child")))
        except:
            print("can load items page +1 error")
            errors += 1
            continue
        try:
            driver.find_element_by_css_selector("#market_buyorder_info_show_details > span").click() #View more details
        except: pass

        #получаем мин цену
        lowest_prices = driver.find_elements_by_css_selector("span.market_commodity_orders_header_promote:last-child")
        if len(lowest_prices) == 1:
            print("lenth is 1")
            lowest_price = lowest_prices[0].text
        if len(lowest_prices) == 2:
            print("lenth is 2")
            lowest_price = lowest_prices[1].text
        lowest_price = lowest_price.strip()[:-5]
        try:
            lowest_price = lowest_price.replace(',', '.') #если целое число (без запятой)
        except:
            print("integer price")
            pass

        #проверяем, подходит ли предмет
        print("lowest_price", lowest_price)
        lowest_price = float(lowest_price) + 2  # прибавляем рубль к цене
        difference_bettween_prices = item["price"] / lowest_price
        print("difference between prices -", difference_bettween_prices)

        if difference_bettween_prices < 0.98 or difference_bettween_prices > 1.02:
            print("difference between prices e more than 2%")
            continue

        #проверяем, хватает ли баланса на покупку предмета
        if lowest_price > balance:
            print("items's price is more than balance")
            continue

        #получаем имя предмета со страницы (доп проверка)
        name_of_the_item_on_page = driver.find_element_by_css_selector("#mainContents > div.market_listing_nav_container > div.market_listing_nav > a:nth-child(2)").text.strip()
        if name_of_the_item_on_page != item["name"]:
            print("name on the market page doesn't matсh with the actual item name")
            continue

        spent_money += lowest_price
        #в стиме верхняя планка это х10 от баланса
        if spent_money > high_limit_of_orders:
            print("limit exceeded", spent_money, high_limit_of_orders)
            break

        #выставляем ордер
        if len(lowest_prices) == 1:
            driver.find_element_by_css_selector("#market_buyorder_info > div:nth-child(1) > div:nth-child(1) > a > span").click() #place buy order
        if len(lowest_prices) == 2:
            driver.find_element_by_css_selector("#market_commodity_order_spread > div:nth-child(2) > div > div.market_commodity_orders_header > a > span").click()
        time.sleep(1)
        input_field = driver.find_element_by_css_selector('#market_buy_commodity_input_price')
        input_field.clear()
        time.sleep(0.2)
        input_field.send_keys(str(lowest_price)) #вводим цену
        time.sleep(0.2)
        driver.find_element_by_css_selector("#market_buyorder_dialog_purchase > span").click() #выставляем ордер
        time.sleep(0.2)

        #проверяем, не появилась ли ошибка при попытке выставить ордер (нужно поставить галочку)
        try:
            error_text = driver.find_element_by_css_selector("#market_buyorder_dialog_error_text").text.strip()
        except:
            pass
        if error_text == "You must agree to the terms of the Steam Subscriber Agreement to complete this transaction.":
            print("tick!")
            driver.find_element_by_css_selector("#market_buyorder_dialog_accept_ssa").click() #ставим халочку
            time.sleep(0.2)
            driver.find_element_by_css_selector("#market_buyorder_dialog_purchase > span").click() #снова выставляем ордер
            time.sleep(0.2)

        time.sleep(4)
        close_modals()

except Exception as e:
    telegram_bot_sendtext("SteamOrderPrices: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()
    close_script()



print("Successful")
close_script()
