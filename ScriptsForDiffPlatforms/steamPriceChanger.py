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
import datetime
import mysql.connector
import requests
import datetime
from urllib.parse import unquote
import requests
import json




#описывает ошибку
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))



executable_path = "C:\\Users\\Dr1m\\Desktop\\skinsautomation\\chromedriver.exe" #windows
os.environ["webdriver.chrome.driver"] = executable_path #windows

options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

options.add_extension('C:\\Users\\Dr1m\\Desktop\\Steam-Incoming-Trades-Confirmer-master\\extension.crx') #windows
#options.add_extension('extension.crx') #linux
options.add_argument("user-data-dir=C:\\profiles\\Default1") #windows
#options.add_argument("user-data-dir=Default1") #linux
options.add_argument('--window-size=1600,900')
driver = webdriver.Chrome(executable_path=executable_path, options=options) #windows
#driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=options) #linux


wait = WebDriverWait(driver, 10) #время вылета 10сек


try:


    driver.set_page_load_timeout(10)  # timeout drive.get("")

    # usd-rub
    usd_rub = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    usd_rub = usd_rub.json()
    usd_rub = float(usd_rub["Valute"]["USD"]["Value"])
    print("current exchange rate", usd_rub)

    # driver.get("https://tradeback.io/ru")
    # driver.set_window_size("1920", "1080")

    driver.get("https://steamcommunity.com/market/")
    # проверяем, залогинены ли мы в стим
    try:
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#marketWalletBalanceAmount")))
        time.sleep(2)
    except:
        # отправляем сообщение и ожидаем ввода данныъ для входа
        telegram_bot_sendtext("SteamPriceChanger: требуется вход в стим (ввести логин, пароль и стим гуард)")
        login = input("login: ")
        password = input("pass: ")
        guard = input("guard: ")
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
        input_field.send_keys(password)
        time.sleep(2)
        driver.find_element_by_css_selector("#login_btn_signin > button > span").click()
        time.sleep(2)
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
            raise ValueError('A very specific bad thing happened.')



    print("GLOBAL ITTERATION number:", i)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.1)
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(0.1)

    # выбираем максимальное кол-во скинов в списке
    try:
        driver.find_element_by_css_selector("#my_listing_pagesize_100").click()
        time.sleep(7)
    except:
        pass

    already_checked_items = []
    index = 0

    # Первая часть. Удаление с продажи
    itemsOnSale = driver.find_elements_by_css_selector('#tabContentsMyActiveMarketListingsRows > div')
    print("Number of items That are currently on sale:", len(itemsOnSale))
    if len(itemsOnSale) > 0:
        print("Taking items prices")
        for item in itemsOnSale:
            index += 1
            print(index, "--------------New Iteration-------------- Part1")
            print("tabs count:", len(driver.window_handles))
            # удаляем вкладку, если их две
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(0.1)
                driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.1)
            # получаем цену и название со стима, цену из БД, платформу from и id
            linkToItem = item.find_element_by_css_selector(".market_listing_item_name_block> span>a").get_attribute(
                "href")
            linkToItemSplit = linkToItem.split("/")
            name_steam_remove = linkToItemSplit[6]
            name_steam_remove = unquote(name_steam_remove)
            # если этот предмет уже проверяли
            if name_steam_remove in already_checked_items:
                print("Already checked that item")
                continue
            my_steam_price = item.find_element_by_css_selector(
                "div.market_listing_right_cell.market_listing_my_price > span > span > span > span:nth-child(1)").text
            my_steam_price = my_steam_price.strip()
            my_steam_price = my_steam_price[:-5]
            my_steam_price = my_steam_price.strip()
            my_steam_price = float(my_steam_price.replace(",", "."))
            my_steam_price = float('{:.2f}'.format(my_steam_price))
            mycursor.execute(
                "SELECT * FROM skins WHERE name=%s AND status = '1' AND platform_to = '1' ORDER BY id DESC LIMIT 1",
                (name_steam_remove,))
            response = mycursor.fetchone()
            print("Trying to get an item in DB", response)
            # если этого предмета нет в нашей БД
            if response is None:
                print("This item isn't in my DB")
                continue
            price_bd = float(response[1])
            item_game_id = response[2]
            platform_from_bd = response[3]
            id_bd = response[10]
            # получаем мин процент
            mycursor.execute("SELECT min_percent FROM min_percents WHERE name_of_platform_from=%s",
                             (platform_from_bd,))
            response = mycursor.fetchone()
            print("getting min percent", response, "from platform with id:", platform_from_bd)
            min_percent_first_character = response[0][0]
            min_percent = float(response[0])
            # переводим в рубли
            price_bd = price_bd * usd_rub

            # получаем минимальную цену, за которую можно продать предмет
            if min_percent_first_character == "-":
                min_percent = min_percent * -1
                min_price = price_bd * min_percent / 0.87
            if min_percent_first_character != "-":
                min_price = price_bd / min_percent / 0.87
            min_price = float('{:.2f}'.format(min_price))
            print("min price for which an item can be sold", min_price)
            # меняем вкладку и получаем минимальную цену для предмета
            driver.execute_script('''window.open('',"_blank");''')  # создаем новую вкладку
            driver.switch_to.window(driver.window_handles[1])
            driver.get(linkToItem)
            element = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#mainContents > div.market_page_fullwidth.market_listing_firstsection")))
            time.sleep(4)
            # проверяем, в каком виде представлены цены
            is_table = 0
            is_row = 0
            try:
                is_table = driver.find_element_by_css_selector(
                    "#market_commodity_forsale_table > table > tbody > :nth-child(2) > :nth-child(1)")
                is_table = 1
            except:
                pass
            try:
                is_row = driver.find_element_by_css_selector("#searchResultsRows")
                is_row = 1
            except:
                pass
            # получаем минимальную цену
            if is_table == 1:
                print("table")
                min_price_steam_item = driver.find_element_by_css_selector(
                    "#market_commodity_forsale_table > table > tbody > :nth-child(2) > :nth-child(1)").text
                min_price_steam_item = min_price_steam_item.strip()
                min_price_steam_item = min_price_steam_item[:-5]
                min_price_steam_item = min_price_steam_item.strip()
                min_price_steam_item = float(min_price_steam_item.replace(",", "."))
                min_price_steam_item = float('{:.2f}'.format(min_price_steam_item))
            if is_row == 1:
                print("rows")
                min_price_steam_item = 1000000
                item_prices = driver.find_elements_by_css_selector(
                    "div.market_listing_price_listings_block > div.market_listing_right_cell.market_listing_their_price > span > span.market_listing_price.market_listing_price_with_fee")
                for item_price in item_prices:
                    current_min_item_price = item_price.text
                    current_min_item_price = current_min_item_price.strip()
                    current_min_item_price = current_min_item_price[:-5]
                    current_min_item_price = current_min_item_price.strip()
                    # если вместо цены стоит надпись, типо: 'продано!'
                    try:
                        current_min_item_price = float(current_min_item_price.replace(",", "."))
                    except:
                        continue
                    current_min_item_price = float('{:.2f}'.format(current_min_item_price))
                    print(current_min_item_price)
                    if current_min_item_price < min_price_steam_item:
                        min_price_steam_item = current_min_item_price

            print("min price on srteam market", min_price_steam_item)
            # добавляем проверенный предмет в список, чтобы потом не проверять дважды цену
            already_checked_items.append(name_steam_remove)
            already_checked_items.append(min_price_steam_item)
            # если цены равны, то цена предмета является минимальной
            if min_price_steam_item == my_steam_price:
                print("=== Item's price is currently minimal on market (no need to change)")
                continue
            # если минимальная цена на маркете меньше минимальной из БД, то нам это не подходит
            if min_price_steam_item < min_price:
                print("!!! Min price on market is less than", "min_price =", min_price, "min_price_steam_item = ",
                      min_price_steam_item)
                continue
            count_elements = driver.find_elements_by_css_selector(":nth-child(6) > div > a > :nth-child(2)")
            reverse_index = len(count_elements)
            print("Number of items to remove", reverse_index)
            for remove_button in count_elements:
                element = driver.find_element_by_css_selector(
                    "div:nth-child(" + str(reverse_index) + ")>div:nth-child(6) > div > a > span:nth-child(2)")
                driver.execute_script("arguments[0].scrollIntoView();", element)
                time.sleep(0.3)
                driver.find_element_by_css_selector("div:nth-child(" + str(
                    reverse_index) + ")>div:nth-child(6) > div > a > span:nth-child(2)").click()
                reverse_index = reverse_index - 1
                time.sleep(0.3)
                driver.find_element_by_css_selector("#market_removelisting_dialog_accept > span").click()
                time.sleep(1.7)

    # Вторая часть. Выставление
    mycursor.execute(
        "SELECT NAME, PRICE, game_id, platform_from, id FROM skins WHERE platform_to = '1' AND status = '1'")
    items_with_status1 = mycursor.fetchall()
    print(items_with_status1[0])
    print("length of items with status = 1:", len(items_with_status1))
    # status игры (есть ли предметы на выставление для этих игр)
    csgo = 0
    dota = 0
    rust = 0
    for item in items_with_status1:
        if item[2] == "730":
            csgo = 1
        if item[2] == "570":
            dota = 1
        if item[2] == "252490":
            rust = 1
    for index_sell in range(3):
        print(index_sell)
        # если активных предметов на выставление нет, то нам не нужно заходить в цикл выставления игры
        if index_sell == 0 and csgo == 0:
            print("CSGO inventory is empty (items with status = 1)")
            continue
        if index_sell == 1 and dota == 0:
            print("DOTA inventory is empty (items with status = 1)")
            continue
        if index_sell == 2 and rust == 0:
            print("RUST inventory is empty (items with status = 1)")
            continue

        # закрываем вторую квладку и переключаемся на первую
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(0.1)
            driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.1)

        # переходим на другой сайт, чтобы полностью обновить инвентарь в стиме при загрузке страницы #update cache by loading a different page (google)
        driver.get("https://www.google.com/")
        time.sleep(0.5)
        # если со стимом что-то не так
        try:
            # подгружаем нужные инвентари
            if index_sell == 0:
                driver.get("https://steamcommunity.com/id/Dr11m/inventory#730")
                print("load 730")
            if index_sell == 1:
                driver.get("https://steamcommunity.com/id/Dr11m/inventory#570")
                print("load 570")
            if index_sell == 2:
                driver.get("https://steamcommunity.com/id/Dr11m/inventory#252490")
                print("load 252490")
        except:
            print("! Can't properly load a page")
            continue
        try:
            element = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[9]/div[1]/div[not(contains(@style,'display: none'))]/div[3]/div/div/div[1]/a")))
        except:
            print("! items doesn't have a description")
            pass
        # выбираем только те, которые показаны на экране
        items_in_inventory = driver.find_elements_by_xpath(
            "//*[@class='inventory_page'][not(contains(@style,'display: none'))]/div[@class='itemHolder']")
        for item_in_inventory in items_in_inventory:
            print("--------------New Iteration-------------- Part 2")
            # закрываем вторую квладку и переключаемся на первую
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(0.1)
                driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.5)
            # если модальное окно после последнего выставления присутствует
            try:
                driver.find_element_by_css_selector(
                    "body > div:nth-child(5) > div.newmodal_content_border > div > div.newmodal_buttons > div > span").click()
                print("6 seconds wasn't enough to close the modal window. We did it here")
            except:
                pass
            item_in_inventory.click()
            time.sleep(0.5)
            # получаем линк и название предмета из этого линка. Если у предмета нет линка, то он точно нам не подходит
            try:
                linktoItemSell = driver.find_element_by_xpath(
                    "//div[9]/div[1]/div[not(contains(@style,'display: none'))]/div[3]/div/div/div[1]/a").get_attribute(
                    "href")
            except:
                continue
            linktoItemSellSplit = linktoItemSell.split("/")
            name_steam_sell = linktoItemSellSplit[6]
            name_steam_sell = unquote(name_steam_sell)
            print("name of the item for sale:", name_steam_sell.encode('utf-8'))
            print("link to item:", linktoItemSell)

            # находим нужный предмет
            index_status = -1
            for item1 in items_with_status1:
                index_status += 1
                if item1[0] == name_steam_sell:
                    # получаем platform_from, id, price
                    platform_from_bd_sell = item1[3]
                    unique_id = item1[4]
                    print("--", unique_id, "id of desired item", index_status,
                          "- index of iteration, that will be used in removing")
                    price_bd_sell = float(item1[1])

                    # получаем мин процент
                    mycursor.execute("SELECT min_percent FROM min_percents WHERE name_of_platform_from=%s",
                                     (platform_from_bd_sell,))
                    response = mycursor.fetchone()
                    print("min procent:", response, "from a platform with id:", platform_from_bd_sell)
                    min_percent_first_character = response[0][0]
                    min_percent = float(response[0])
                    # переводим в рубли
                    price_bd_sell = price_bd_sell * usd_rub

                    # получаем минимальную цену, за которую можно продать предмет
                    if min_percent_first_character == "-":
                        min_percent = min_percent * -1
                        min_price = price_bd_sell * min_percent / 0.87
                    if min_percent_first_character != "-":
                        min_price = price_bd_sell / min_percent / 0.87
                    min_price = float('{:.2f}'.format(min_price))

                    # проверяем, есть ли цена предмета на маркете в уже проверенных предметах (already_checked)
                    print("already_checked length -", len(already_checked_items))
                    min_price_steam_item = None
                    for index_sell in range(len(already_checked_items)):
                        if already_checked_items[index_sell] == name_steam_sell:
                            min_price_steam_item = already_checked_items[index_sell + 1]
                            print("Item is already checked in a previous iterations, price is -",
                                  min_price_steam_item)

                    # проверка на ошибку
                    my_price_exists = None
                    # если этот предмет не проверялся, то получаем его минимальную стоимость
                    if min_price_steam_item is None:
                        # меняем вкладку и получаем минимальную цену для предмета
                        driver.execute_script('''window.open('',"_blank");''')  # создаем новую вкладку
                        driver.switch_to.window(driver.window_handles[1])
                        driver.get(linktoItemSell)
                        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#mainContents > div.market_page_fullwidth.market_listing_firstsection")))
                        time.sleep(4)

                        # проверяем, есть ли мой предмет в продаже. Вообще такого не должно быть, т.к. он уже проверялся и там скорее всего произошла ошибка при удалении предмета
                        try:
                            my_price_exists = driver.find_element_by_css_selector(
                                "div.market_listing_right_cell.market_listing_my_price > span > span > span > span:nth-child(1)").text
                            print(
                                "! Caught an Error. Item is on sale, but its impossible (must be an error in removung Block)",
                                name_steam_sell.encode('utf-8'))
                            my_price_exists = my_price_exists.strip()
                            my_price_exists = my_price_exists[:-5]
                            my_price_exists = my_price_exists.strip()
                            my_price_exists = float(my_price_exists.replace(",", "."))
                            my_price_exists = float('{:.2f}'.format(my_price_exists))
                        except:
                            pass

                        # проверяем, в каком виде представлены цены
                        is_table = 0
                        is_row = 0
                        try:
                            is_table = driver.find_element_by_css_selector(
                                "#market_commodity_forsale_table > table > tbody > :nth-child(2) > :nth-child(1)")
                            is_table = 1
                        except:
                            pass
                        try:
                            is_row = driver.find_element_by_css_selector("#searchResultsRows")
                            is_row = 1
                        except:
                            pass

                        # получаем минимальную цену
                        if is_table == 1:
                            print("table")
                            min_price_steam_item = driver.find_element_by_css_selector(
                                "#market_commodity_forsale_table > table > tbody > :nth-child(2) > :nth-child(1)").text
                            min_price_steam_item = min_price_steam_item.strip()
                            min_price_steam_item = min_price_steam_item[:-5]
                            min_price_steam_item = min_price_steam_item.strip()
                            min_price_steam_item = float(min_price_steam_item.replace(",", "."))
                            min_price_steam_item = float('{:.2f}'.format(min_price_steam_item))
                        if is_row == 1:
                            print("rows")
                            min_price_steam_item = 1000000
                            item_prices = driver.find_elements_by_css_selector(
                                "div.market_listing_price_listings_block > div.market_listing_right_cell.market_listing_their_price > span > span.market_listing_price.market_listing_price_with_fee")
                            for item_price in item_prices:
                                current_min_item_price = item_price.text
                                current_min_item_price = current_min_item_price.strip()
                                current_min_item_price = current_min_item_price[:-5]
                                current_min_item_price = current_min_item_price.strip()
                                # если вместо цены стоит надпись, типо: 'продано!'
                                try:
                                    current_min_item_price = float(current_min_item_price.replace(",", "."))
                                except:
                                    continue
                                current_min_item_price = float('{:.2f}'.format(current_min_item_price))
                                print(current_min_item_price)
                                if current_min_item_price < min_price_steam_item:
                                    min_price_steam_item = current_min_item_price
                        # добавляем проверенный предмет в список, чтобы потом не проверять дважды цену
                        already_checked_items.append(name_steam_sell)
                        already_checked_items.append(min_price_steam_item)
                        print("min item price on market", min_price_steam_item, "my min possible price", min_price)
                    # проверка на ошибку
                    if my_price_exists is not None:
                        print("Caught an Error, going to the next iteration")
                        break
                    # цена, за которую будем выставлять
                    future_price = min_price_steam_item - 0.01
                    future_price = float('{:.2f}'.format(future_price))

                    # если минимальная цена на маркете меньше минимальной из БД, то нам это не подходит
                    if future_price < min_price:
                        print("!!! min possible price is less than min price on market", "min_price =", min_price,
                              "min_price_steam_item = ", min_price_steam_item)
                        print("removing an item from list (with status =1), with index:", index_status)
                        del items_with_status1[index_status]
                        break

                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(0.1)
                        driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(0.1)

                    # начинаем выставлять
                    # получаем нужный див, дабы сверить название, чтобы избежать ошибок
                    name_and_sellButton = driver.find_element_by_xpath(
                        "//div[9]/div[1]/div[not(contains(@style,'display: none'))]/div[3]")
                    name_checked = name_and_sellButton.find_element_by_xpath('div/div/div[1]/a').get_attribute(
                        "href")
                    name_checkedSplit = linktoItemSell.split("/")
                    name_checked = name_checkedSplit[6]
                    name_checked = unquote(name_checked)
                    print("item name and checked item name must be iqual:", name_steam_sell.encode('utf-8'), "==",
                          name_checked.encode('utf-8'))
                    if name_steam_sell == name_checked:
                        # начинаем выставлять
                        ButtonSell = name_and_sellButton.find_element_by_xpath("div/a").click()
                        time.sleep(1)
                        input_field = driver.find_element_by_css_selector('#market_sell_buyercurrency_input')
                        input_field.clear()
                        input_field.send_keys(str(future_price))
                        time.sleep(1)
                        price_check = driver.find_element_by_css_selector(
                            '#market_sell_currency_input').get_attribute('value')
                        price_check = price_check.strip()
                        price_check = price_check[:-5]
                        price_check = price_check.strip()
                        price_check = float(price_check.replace(",", "."))
                        price_check = float('{:.2f}'.format(price_check))
                        print("checked price:", price_check)
                        # сверяем цену
                        if price_check / 0.87 > min_price:
                            driver.find_element_by_css_selector("#market_sell_dialog_accept > span").click()
                            time.sleep(0.2)
                            # если не поставлена галочка, то проставляем её
                            try:
                                error_need_to_check = driver.find_element_by_xpath(
                                    "//div[3]/div/div[2]/div[4]/div[2][not(contains(@style,'display: none'))]")
                                time.sleep(0.2)
                                driver.find_element_by_css_selector("#market_sell_dialog_accept_ssa").click()
                                time.sleep(0.2)
                                driver.find_element_by_css_selector("#market_sell_dialog_accept > span").click()
                                time.sleep(0.2)
                            except:
                                pass
                            driver.find_element_by_css_selector("#market_sell_dialog_ok > span").click()
                            print("++++++++++++++++ successful:", name_checked.encode('utf-8'), "price:",
                                  str(future_price), "++++++++++++++++")
                            # ожидаем окошко с уведомлением
                            try:
                                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                            "body > div:nth-child(5) > div.newmodal_content_border > div > div.newmodal_buttons > div > span"))).click()
                            except:
                                pass
                            print("delete items with index:", index_status)
                            del items_with_status1[index_status]
                            break  # выходим из цикла


except Exception as e:
    r = str(random.randint(1, 10001))
    driver.save_screenshot('Error-SteamPriceChanger' + r + '.png')
    telegram_bot_sendtext("SteamPriceChanger: Возникла ошибка, нужно выяснять")
    succsess = 0
    logger.exception(e)  # Will send the errors to the file
    PrintException()
    mycursor.close()
    mydb.close()
    driver.close()
    driver.quit()
if succsess == 1:
    print("Successful")
mycursor.close()
mydb.close()
driver.close()
driver.quit()
