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



#настройка и главные функции
try:



    min_perccent = "39"
    allowed_min_percent = 0.37



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



    chrome_options = Options()
    chrome_options.add_argument(
        "user-data-dir=C:\\Users\\Dr1m\\AppData\\Local\\Google\\Chrome\\User Data\\Default15")  # windows
    chrome_options.add_argument('--window-size=1600,900')  # windows
    driver = webdriver.Chrome(executable_path='C:\\Users\\Dr1m\\Desktop\\skinsStuff\\skinsautomation\\chromedriver.exe',
                              chrome_options=chrome_options)  # windows

    wait = WebDriverWait(driver, 60)





#here
#must
#be
#login
#into
#STEAM
#if needed






    # удаляем все выставленные байордера
    print("удаляем все выставленные байордера")
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
    balance = float(balance
                    )
    # удаляем байордера
    buy_orders_cancel_buttons = driver.find_elements_by_css_selector(
        "#tabContentsMyListings > div:last-child > div.market_listing_row.market_recent_listing_row > div.market_listing_edit_buttons.actual_content > div > a")
    for index in range(len(buy_orders_cancel_buttons)):
        driver.find_element_by_css_selector(
            "#tabContentsMyListings > div:last-child > div:nth-child(3) > div.market_listing_edit_buttons.actual_content > div > a").click()  # кликаем всегда на первую кнопку cancel, тк они пропадают после клика
        time.sleep(6)
    driver.find_element_by_css_selector()





#получаем предметы на tryskins
    skins_from_parser = []
    dates_diff = 777
    if dates_diff > 60:
        driver.get(
            "")
        time.sleep(6)
        element = 0
        try:
            element = driver.find_element_by_css_selector("#page-wrapper > div.row.border-bottom > nav > ul > li:nth-child(4) > a > img")
        except:pass
        if element != 0:
            driver.find_element_by_css_selector("#page-wrapper > div.row.border-bottom > nav > ul > li:nth-child(4) > a > img").click()
            time.sleep(5)
            driver.find_element_by_css_selector("#imageLogin").click()
            time.sleep(5)
            driver.get("https://www.google.com/")
            time.sleep(3)
            driver.get(
                "https://table.altskins.com/site/items?ItemsFilter%5Bknife%5D=0&ItemsFilter%5Bknife%5D=1&ItemsFilter%5Bstattrak%5D=0&ItemsFilter%5Bstattrak%5D=1&ItemsFilter%5Bsouvenir%5D=0&ItemsFilter%5Bsouvenir%5D=1&ItemsFilter%5Bsticker%5D=0&ItemsFilter%5Bsticker%5D=1&ItemsFilter%5Btype%5D=1&ItemsFilter%5Bservice1%5D=showsteama&ItemsFilter%5Bservice2%5D=showcsmoneyw&ItemsFilter%5Bunstable1%5D=1&ItemsFilter%5Bunstable2%5D=0&ItemsFilter%5Bhours1%5D=192&ItemsFilter%5Bhours2%5D=192&ItemsFilter%5BpriceFrom1%5D=22&ItemsFilter%5BpriceTo1%5D=&ItemsFilter%5BpriceFrom2%5D=&ItemsFilter%5BpriceTo2%5D=&ItemsFilter%5BsalesBS%5D=&ItemsFilter%5BsalesTM%5D=&ItemsFilter%5BsalesST%5D=3&ItemsFilter%5Bname%5D=&ItemsFilter%5Bservice1Minutes%5D=301&ItemsFilter%5Bservice2Minutes%5D=301&ItemsFilter%5BpercentFrom1%5D="+ min_perccent +"&ItemsFilter%5BpercentFrom2%5D=&ItemsFilter%5Btimeout%5D=5&ItemsFilter%5Bservice1CountFrom%5D=&ItemsFilter%5Bservice1CountTo%5D=&ItemsFilter%5Bservice2CountFrom%5D=&ItemsFilter%5Bservice2CountTo%5D=&ItemsFilter%5BpercentTo1%5D=&ItemsFilter%5BpercentTo2%5D=&refreshonoff=1")
            time.sleep(8)
            element = 0
            try:
                element = driver.find_element_by_css_selector("#page-wrapper > div.row.border-bottom > nav > ul > li:nth-child(4) > a > img")
            except: pass
            if element != 0:
                raise ValueError('tryskins login error')

        #подгружаем все элементы из parser'a
        for x in range(2):
            try:
                mainBlocks = driver.find_elements_by_css_selector('table > tbody > tr:nth-child(n)')
                len_start = len(mainBlocks)
                element = driver.find_element_by_css_selector(
                    'table > tbody > tr:nth-child(' + str(len(mainBlocks)) + ')')
                element.location_once_scrolled_into_view
                time.sleep(0.2)
                element = driver.find_element_by_css_selector(
                    'table > tbody > tr:nth-child(' + str(len(mainBlocks) - 29)  + ')')
                element.location_once_scrolled_into_view
                time.sleep(0.2)
                element = driver.find_element_by_css_selector(
                    'table > tbody > tr:nth-child(' + str(len(mainBlocks)) + ')')
                element.location_once_scrolled_into_view
            except: continue
            for ind in range (10):
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

        XML = driver.find_element_by_css_selector('#w0 > table > tbody').get_attribute('innerHTML')
        XML = XML.split('<tr class="tr"')
        del XML[0]
        for item_xml in XML:
            try:
                name = re.search('market_hash_name=([^<]*)&amp;sort_by=price', item_xml)
                name = name[1].strip()
                price_csm = re.search('attribute="pricecsmoneyw">([^<]*)</span><span', item_xml).group(1).strip()
                sales = re.search('class="sales">([^<]*)</div><img src="/images/steam', item_xml)
                sales = sales[1].strip()
                purchased_count = 0
                #получаем, сколько предметов было куплено за последние 7 дней
                close_mysql_connection()
                mycursor.execute("SELECT name FROM PurchasedItems WHERE DATE(date) > (NOW() - INTERVAL 7 DAY);")
                items_mysql_last7days = mycursor.fetchall()
                close_mysql_connection()
                connect_to_mysql("SteamBuyOrders")
                for item_mysql in items_mysql_last7days:
                    if item_mysql == name:
                        print("added count")
                        purchased_count += 1

                skins_from_parser.append({"name":name, "price_csm": float(price_csm), "sales": sales, "overstock": -1, "db_id": -1, "purchased_count": purchased_count, "allowed_count": 0, "buy_order_price": 0})
            except Exception as e:
                PrintException_only_print()
                continue






#проверяем, есть ли смысл получать оверсток на сайте (это нужно делать каждые 24 часа)
    need_to_check_on_cs_money = False
    mycursor.execute("SELECT name,quanity,date,id FROM csMoneyLimits")
    items_mysql = mycursor.fetchall()
    now = datetime.datetime.now()
    for item_db in items_mysql:
        for item_parser in skins_from_parser:
            if item_db[0] == item_parser["name"]:
                item_parser["db_id"] = item_db[3] #add table's id
                delta = now - item_db[2]
                # кол-во часов
                time_diff_in_hours =  int(delta.total_seconds()) / 60 / 60
                print('time difference: ', time_diff_in_hours)
                if time_diff_in_hours < 24:
                    item_parser["overstock"] = item_db[1]
                break

    #проверяем, нужно ли заходить на csm ндля получения overstocka (есть ли предметы overstock == -1)
    for item in skins_from_parser:
        if item["overstock"] == -1:
            need_to_check_on_cs_money = True
    print("need to open csMoney", need_to_check_on_cs_money)






#нужно получить оверстоки с сайта csmoney
    if need_to_check_on_cs_money == True:
        #check if I'm logged into csMoney
        driver.get("https://old.cs.money/")
        try:
            element = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.header_menu_mobile > div.balance_header.superclass_space.block_balance")))
            time.sleep(1)
        except:
            #входим в csMoney
            print("start entering into csMoney")
            driver.find_element_by_css_selector("#authenticate_button > a").click()
            time.sleep(1)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#imageLogin")))
            driver.find_element_by_css_selector("#imageLogin").click()
            time.sleep(5)
            # снова проверяем, вошли ли мы в систему
            try:
                element = wait.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div.header_menu_mobile > div.balance_header.superclass_space.block_balance")))
            except:
                raise ValueError('need to login into csMoney')

        #надо полностью прогрузить страницу
        try:
            time.sleep(10)
            element = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#main_container_bot > div.items > div:nth-child(1)")))
        except:
            raise ValueError('cant properly load csmoney')

        #проверяем оверстоки
        driver.find_element_by_css_selector("#header_panel > ul.header_menu > li:nth-child(1) > a").click()
        time.sleep(5)
        for item in skins_from_parser:
            if item["overstock"] == -1:
                input_field = driver.find_element_by_css_selector('#universal_skin_input')
                input_field.clear()
                time.sleep(0.2)
                input_field.send_keys(item["name"])
                time.sleep(0.2)
                driver.find_element_by_css_selector("#check_skin_status_btn > a").click()
                time.sleep(2)
                try:
                    overstock_csm = driver.find_element_by_css_selector("#overstock_difference").text
                    overstock_csm = int(overstock_csm)
                    print("overstock -", overstock_csm)
                except:
                    print("was error getting overstock_difference")
                    continue

                #либо обновляем информацию у предмета в бд, либо добавляем новую запись
                #если предмета не было в бд
                if item["db_id"] == -1:
                    mycursor.execute(
                        "INSERT INTO csMoneyLimits (name, quanity) VALUES (%s, %s)",
                        (item["name"], str(overstock_csm),))
                    mydb.commit()
                #если предмет был в бд
                if item["db_id"] != -1:
                    #сперва удаляем устаревший предмет из бд
                    mycursor.execute(
                        "DELETE FROM `csMoneyLimits` WHERE id = %s",
                        (item["db_id"],))
                    mydb.commit()
                    #теперь добавляем новый
                    mycursor.execute(
                        "INSERT INTO csMoneyLimits (name, quanity) VALUES (%s, %s)",
                        (item["name"], str(overstock_csm),))
                    mydb.commit()

                #проставляем оверсток
                item["overstock"] = int(overstock_csm)






#сортируем и выставляем разрешенное кол-во покупок
    index = -1
    for item in skins_from_parser:
        index += 1
        if item["overstock"] == -1:
            del skins_from_parser[index]
            continue
        predicted_purchases = 0
        if int(item["sales"]) > 0:
            predicted_purchases = int(int(item["sales"]) / 3)
        allowed_count = int(item["overstock"]) - (predicted_purchases + int(item["purchased_count"]))
        item["allowed_count"] = allowed_count
        if allowed_count < 1:
            del skins_from_parser[index]






    # опустили, так как всеравно нужно открывать страницу каждого скина для выставления байордера (там и будем брать мин цену)
    """
    #получаем usd-rub, для этого возможно нужно будет загрузить несколько предметов
        #проверяем, нет ли у нас готового курса в бд (не старше 3ч часов)
        mycursor.execute("SELECT quanity, date FROM csMoneyLimits WHERE id = 38")
        exchange_rate_and_date = mycursor.fetchone()
        exchange_rate = 0
        #получаем, если не старше 4х часов
        now = datetime.datetime.now()
        delta = now - exchange_rate_and_date[1]
        # кол-во часов
        time_diff_in_hours = int(delta.total_seconds()) / 60 / 60
        print('time difference exchange rate: ', time_diff_in_hours)
        if time_diff_in_hours < 4:
            exchange_rate = exchange_rate_and_date[0]

        #получаем курс валют (сравнивая цену доллара на парсере и цену в рублях в стиме у нескольких предметов)
        if exchange_rate == 0:
            skins_for_exchange_rate = []
            #получаем минимальную цену ордера в рублях
            for index in range(3):
                print("index exchange rate -", index)
                url_name = urllib.parse.quote(skins_from_parser[index]["name"])
                driver.get("https://steamcommunity.com/market/listings/730/"+url_name)
                try:
                    element = wait.until(EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "span.market_commodity_orders_header_promote:last-child")))
                except:
                    raise ValueError('cant get exchange rate')
                try:
                    driver.find_element_by_css_selector("#market_buyorder_info_show_details > span").click() #View more details
                except: pass

                lowest_prices = driver.find_elements_by_css_selector("span.market_commodity_orders_header_promote:last-child")
                if len(lowest_prices) == 1:
                    print("lenth is 1")
                    lowest_price = lowest_prices[0].text
                if len(lowest_prices) == 2:
                    print("lenth is 2")
                    lowest_price = lowest_prices[1].text
                lowest_price = float(lowest_price.strip().replace(',', '.')[:-5])

                print("name -", skins_from_parser[index]["name"], "lowest price -", lowest_price)
                skins_for_exchange_rate.append({"name": skins_from_parser[index]["name"], "price_usd": skins_from_parser[index]["price"], "price_rub": lowest_price})



            #получаем курс валют и проверяем его на адекватность
            print("skins_for_exchange_rate", skins_for_exchange_rate)
            rates = []
            #получаем курс для трех предметов
            index = 0
            for item in skins_for_exchange_rate:
                index += 1
                compared_price = float(item["price_rub"]) / float(item["price_usd"])
                rates.append({"name":index, "exchange_rate": compared_price})
            print("rates", rates)
            #сравниваем курсы валют
            for rate_1 in rates:
                for rate_2 in rates:
                    if rate_1["name"] == rate_2["name"]:
                        continue
                    rates_difference = rate_1["exchange_rate"] - rate_2["exchange_rate"]
                    if rates_difference < 0:
                        rates_difference = rates_difference * -1
                    #если значение больше, то берем!
                    print("rates_difference -", rates_difference)
                    if rates_difference < 0.1:
                        print("gotcha!")
                        #берем наибольший курс валют
                        if rate_1["exchange_rate"] > rate_2["exchange_rate"]:
                            exchange_rate = rate_1["exchange_rate"]
                        if rate_1["exchange_rate"] < rate_2["exchange_rate"]:
                            exchange_rate = rate_2["exchange_rate"]
                        break

            #проставляем курс валют в бд
            if exchange_rate != 0:
                now = datetime.datetime.now()
                mycursor.execute(
                    "UPDATE `csMoneyLimits` SET `quanity`=%s,`date`=%s WHERE id = 38",
                    (exchange_rate, now,))
                mydb.commit()

        print("exchange rate -", exchange_rate)

        # проставляем цену для байордера для каждого предмета
        for item in skins_from_parser:
                                    #usd min market price  #exchange rate #plus 1 rubble
            item["buy_order_price"] = item["price"] * float(exchange_rate) + 1
    """






    #{"name":name, "price_csm": float(price_csm), "sales": sales, "overstock": -1, "db_id": -1, "purchased_count": purchased_count, "allowed_count": 0, "buy_order_price": 0}
#выставляем байордера
    errors = 0

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

        #проверяем, подходит ли предмет по профиту
        print("lowest_price", lowest_price)
        lowest_price = float(lowest_price) + 3  # прибавляем рубль к цене
        dep_price_rub = item["price_csm"] * rub_usd * 0.96
        expected_profit = (lowest_price / dep_price_rub -1) * -1
        print("expected profit -", expected_profit)
        if expected_profit < allowed_min_percent:
            print("expected profit is less than allowed min profit")
            continue

        #проверяем, хватает ли баланса на покупку предмета
        if lowest_price > balance:
            print("items's price is more than balance")
            continue

        #получаем имя предмета со страницы (доп проверка)
        name_of_the_item_on_page = driver.find_element_by_css_selector("#mainContents > div.market_listing_nav_container > div.market_listing_nav > a:nth-child(2)").text.strip()
        if name_of_the_item_on_page != item["name"]:
            print("name on the market page doesn't math with the actual item name")
            continue

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




#test print
#for item in skins_from_parser:
#    print(item)


print("Successful")
close_script()
