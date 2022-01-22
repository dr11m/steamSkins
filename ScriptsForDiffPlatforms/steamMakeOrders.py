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
import json
import os
import subprocess
from urllib.parse import unquote
from pyvirtualdisplay import Display

# start time
now = datetime.datetime.now()
print(str(
    now) + "----------------------------------------------------------------------------------------------------------")


# test prints
# close all
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


# обработка ошибок
def PrintException():
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
    # screen
    now = datetime.datetime.now()
    # close all
    closeAll()


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
    # screen
    now = datetime.datetime.now()
    driver.save_screenshot('eror_print' + "-" + str(now) + '.png')



try:


    display = Display(visible=0, size=(1600, 900), backend='xvfb')
    display.start()

    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=/home/work/profilesForAll/SteamPriceChanger")  # linux
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)

    wait = WebDriverWait(driver, 10)  # время вылета 10сек

    # rub_usd
    rub_usd = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    rub_usd = rub_usd.json()
    rub_usd = float(rub_usd["Valute"]["USD"]["Value"])
    print("current exchange rate", rub_usd)



except Exception as e:
    telegram_bot_sendtext("steamPriceChangerV2: Возникла ошибка, нужно выяснять")
    PrintException()

try:
    driver.get("https://steamcommunity.com/market/")
    time.sleep(5)
    try:
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#marketWalletBalanceAmount")))
    except:
        print("cant verify login into steam on the first try (login)")
        time.sleep(50)
except Exception as e:
    telegram_bot_sendtext("steamPriceChangerV2: Возникла ошибка, нужно выяснять")
    PrintException()

# CODE
# delete from sale
try:
    # создаём вторую вкладку и получаем минимальную цену для предмета
    driver.execute_script('''window.open('',"_blank");''')  # создаем новую вкладку
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(5)

    print("--start deleting items--")
    # получаем предметы на продажи в стиме и в бдl
    items_on_sale = driver.find_elements_by_css_selector("#tabContentsMyActiveMarketListingsRows > div")
    print("items currently on sale in steam -", len(items_on_sale))
    # get items on sale from DB
    mycursor.execute("SELECT `NAME` FROM `skins` WHERE `status` <> 3")
    items_available_to_sale = mycursor.fetchall()
    print("items currently on sale in DB -", len(items_available_to_sale))
    try:
        print("one item from bd -", items_available_to_sale[0])
    except:
        pass

    # если предметы есть, то проверяем их
    if len(items_on_sale) > 0 and len(items_available_to_sale) > 0:
        already_checked_items_for_deleting = []
        errors_count = 0
        # начинаем проверять каждый предмет в стиме
        for item_on_sale in items_on_sale:
            driver.switch_to.window(driver.window_handles[0])
            # если случилось три ошибки в ряд за проход
            if errors_count == 3:
                raise ValueError('3 errorsd in a row')
            name = item_on_sale.find_element_by_css_selector(
                "div.market_listing_item_name_block >  span> a").text.strip()
            print("name - ", name.encode('utf-8'))
            # если предмет уже проверяли
            if name in already_checked_items_for_deleting:
                print("already checked this item (continue)")
                continue
            is_name_exist_in_bd = False
            # проверяем, есть ли предмет в бд
            for item_bd in items_available_to_sale:
                if item_bd[0] == name:
                    print("item exists in DB (break) - ", name.encode('utf-8'))
                    is_name_exist_in_bd = True
                    break
            # если предмета нет в нашей БД, идём к следующему
            if is_name_exist_in_bd == False:
                print("item does not exist in DB (continue) - ", name.encode('utf-8'))
                already_checked_items_for_deleting.append(name)
                continue
            my_listed_price = item_on_sale.find_element_by_css_selector(
                "div.market_listing_right_cell.market_listing_my_price > span > span > span > span:nth-child(1)").text
            my_listed_price = float(my_listed_price.strip().replace(',', '.')[:-5])
            print("my listed price -", my_listed_price)
            link = item_on_sale.find_element_by_css_selector(".market_listing_item_name_block> span>a").get_attribute(
                "href")
            print("link to item -", link)
            # получаем минимальную цену в стиме
            driver.switch_to.window(driver.window_handles[1])
            driver.get("https://www.google.com/")
            driver.get(link)
            try:
                time.sleep(5)  # 5 секунд на один запрос
                element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#listings")))
            except:
                print("cant load item's link properly (continue and errors count +1)")
                errors_count += 1
                continue
            errors_count = 0
            # get tlisted type
            is_table_prices = driver.find_elements_by_css_selector(
                "#market_commodity_forsale_table > table > tbody > :nth-child(2) > :nth-child(1)")
            is_row_prices = driver.find_elements_by_css_selector("#searchResultsRows")
            print("length table prices and row prices -", len(is_table_prices), len(is_row_prices))
            # if row prices - get lowest and  on market
            if len(is_row_prices) > 0:
                print("is_row_prices")
                price_from_market = 100000000
                steam_second_low_price = 100000000
                steam_listed_prices = driver.find_elements_by_css_selector(
                    "div.market_listing_price_listings_block > div.market_listing_right_cell.market_listing_their_price > span > span.market_listing_price.market_listing_price_with_fee")
                # get lowest price
                print("getting lowest price")
                for steam_listed_price in steam_listed_prices:
                    price_from_market_2 = steam_listed_price.text
                    # бывают не цены, а надписи sold
                    try:
                        price_from_market_2 = float(price_from_market_2.strip().replace(',', '.')[:-5])
                    except:
                        continue
                    print("price_from_market_2 -", price_from_market_2)
                    if price_from_market_2 < price_from_market:
                        price_from_market = price_from_market_2
                # get 2nd lowest price
                print("getting 2nd lowest price")
                for steam_listed_price in steam_listed_prices:
                    price_from_market_2 = steam_listed_price.text
                    try:
                        price_from_market_2 = float(price_from_market_2.strip().replace(',', '.')[:-5])
                    except:
                        continue
                    print("price_from_market_2 -", price_from_market_2)
                    if price_from_market < price_from_market_2 < steam_second_low_price:
                        steam_second_low_price = price_from_market_2
            # if table prices - get lowest on market
            if len(is_table_prices) > 0:
                print("is_table_prices")
                price_from_market = driver.find_element_by_css_selector(
                    "#market_commodity_forsale_table > table > tbody > :nth-child(2) > :nth-child(1)").text
                price_from_market = float(price_from_market.strip().replace(',', '.')[:-5])
                steam_second_low_price = driver.find_element_by_css_selector(
                    "#market_commodity_forsale_table > table > tbody > :nth-child(3) > :nth-child(1)").text
                steam_second_low_price = float(steam_second_low_price.strip().replace(',', '.')[:-5])
            print("lowest price is -", price_from_market)
            print("second low price is -", steam_second_low_price)
            print("name -", name.encode('utf-8'))
            already_checked_items_for_deleting.append(name)
            print("add item's name in a list (already_checked_items_for_deleting)")

            # если моя цена и минимальная в стиме равна, то надо проверить, на сколько далеко моя цена от второй цены (если больше чем на рубль, то перевыставляем)
            if price_from_market == my_listed_price:
                print("lowest steam price and my listed price is equal")
                if steam_second_low_price - my_listed_price < 1:
                    print(
                        "difference between my listed price (lowest on steam) and 2nd lowest price is less than 1 rub (continue)")
                    continue

            # delete from sale
            is_bitton_to_remove_exists = driver.find_elements_by_css_selector(
                "div:nth-child(6) > div > a > span:nth-child(2)")
            if len(is_bitton_to_remove_exists) > 0:
                for remove_button in is_bitton_to_remove_exists:
                    try:
                        remove_button.click()
                        time.sleep(0.5)
                        driver.find_element_by_css_selector("#market_removelisting_dialog_accept > span").click()
                        # проверяем, закрылось ли окно
                        for i in range(30):
                            time.sleep(0.3)
                            element = driver.find_element_by_css_selector("#market_removelisting_dialog")
                            if element.is_displayed():
                                print("modal window still exists (continue)")
                                continue
                            else:
                                print("modal window doesnt exist anymore (break)")
                                break
                        element = driver.find_element_by_css_selector("#market_removelisting_dialog")
                        if element.is_displayed():
                            print("9 seconds wasnt enough, modal window still exists (break)")
                    except Exception as e:
                        print("was an error (continue). Error info below")
                        PrintException_only_print()
                        continue


except Exception as e:
    telegram_bot_sendtext("steamPriceChangerV2: Возникла ошибка, нужно выяснять")
    PrintException()

# sell items
try:
    print("--start selling items--")
    driver.switch_to.window(driver.window_handles[0])
    driver.get("https://www.google.com/")
    driver.get("https://steamcommunity.com/id/Dr11m/inventory#730")
    try:
        time.sleep(5)  # 5 секунд на один запрос
        element = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#active_inventory_page > div:nth-child(2) > div:first-child")))
    except:
        print("cant load steams inventory (try 1 more time)")
        driver.get("https://steamcommunity.com/id/Dr11m/inventory")
        try:
            time.sleep(5)  # 5 секунд на один запрос
            element = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#active_inventory_page > div:nth-child(2) > div:first-child")))
        except:
            raise ValueError('cant load steam inventory')

    # get items are ready to be put on sale
    mycursor.execute(
        "SELECT NAME, PRICE, game_id, platform_from, id FROM skins WHERE platform_to = '1' AND (status = '1' OR status = '2') AND orders = '0' AND sold_id is NULL ORDER BY id DESC")
    items_for_sale = mycursor.fetchall()
    print("items for sale length -", len(items_for_sale))
    try:
        print("one item from bd -", items_available_to_sale[0])
    except:
        pass

    if len(items_for_sale) > 0:
        already_checked_items_for_selling = []
        #2nd page loop
        for index_next_page in range(2):
            index_next_page += 1
            next_item = 0
            for index_inventory in range(25):
                # close modals if didn't
                try:
                    driver.find_element_by_css_selector(
                        "#market_sell_dialog > div.newmodal_header_border > div > div").click()
                    time.sleep(0.2)
                except:
                    pass
                next_item += 1
                print("----------next item (index) -", next_item)
                driver.switch_to.window(driver.window_handles[0])
                try:
                    item_id = driver.find_element_by_css_selector(
                        "#inventories > div:nth-child(2) > div:first-child > div:nth-child(1) > div > a").get_attribute("href")
                    print("item id - ", item_id)
                except Exception as e:
                    print("cant get item id (continue). Error info below")
                    PrintException_only_print()
                    continue
                #пытаюсь нажать на предмет, если ошибка, то перехожу к следующему
                try:
                    driver.find_element_by_xpath('//*[@id="inventories"]/div[2]/div['+str(index_next_page)+']/div['+str(next_item)+']').click()
                except Exception as e:
                    try:
                        driver.find_element_by_css_selector("div.newmodal_buttons > div > span").click()
                    except:
                        pass
                    print("error occured")
                    PrintException_only_print()
                    continue
                time.sleep(1)
                print("click on item")
                try:
                    link = driver.find_element_by_xpath(
                        "//div[contains(@style,'opacity: 1')]/div[3]/div/div/div[1]/a").get_attribute("href")
                    print("link -", link)
                except:
                    print("link is not existed (continue)")
                    continue
                full_link = link
                link = link.split("/")
                name_url = link[len(link) - 1]
                name = unquote(name_url).strip()
                print("name -", name.encode('utf-8'))

                index_deleted = -1
                for item_for_sale in items_for_sale:
                    index_deleted += 1
                    if name == item_for_sale[0]:
                        print("match! -", item_for_sale[0].encode('utf-8'))
                        # delete from list (DB items) not to use it anymore
                        del items_for_sale[index_deleted]
                        print("deted with index -", index_deleted)
                        price_DB = float(item_for_sale[1])
                        print("price from DB -", price_DB)
                        platform_from = str(item_for_sale[3])
                        bd_id = str(item_for_sale[4])
                        price_DB = price_DB * rub_usd
                        print("updated price , platform from and bd id -", price_DB, platform_from, bd_id)
                        # get percentage for platform
                        mycursor.execute(
                            "SELECT min_percent FROM min_percents WHERE name_of_platform_from = %s",
                            (platform_from,))
                        percent_from_DB = mycursor.fetchone()
                        print("percent from DB sql request -", percent_from_DB)
                        min_price = 0
                        first_character = percent_from_DB[0][0]
                        print("percent from DB and first character -", percent_from_DB, first_character)
                        percent_from_DB = float(percent_from_DB[0])
                        # get min price
                        if str(first_character) == "-":
                            percent_from_DB = percent_from_DB * -1
                            min_price = price_DB * percent_from_DB / 0.87
                        if str(first_character) != "-":
                            min_price = price_DB / percent_from_DB / 0.87
                        print("min price -", min_price)

                        if name in already_checked_items_for_selling:
                            for index_checked in range(len(already_checked_items_for_selling)):
                                if name == already_checked_items_for_selling[index_checked]:
                                    lowest_steam_price = float(already_checked_items_for_selling[index_checked + 1])
                                    print("item was already cheked, lowest steam price is -", lowest_steam_price)

                        if not name in already_checked_items_for_selling:
                            print("name wasnt checked already, taking lowest steam price now")
                            driver.switch_to.window(driver.window_handles[1])
                            driver.get(full_link)
                            time.sleep(5)
                            try:
                                time.sleep(5)  # 5 секунд на один запрос
                                element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#listings")))
                            except:
                                print("cant load item's link properly (continue and errors count +1)")
                                continue
                            # get tlisted type
                            is_table_prices = driver.find_elements_by_css_selector(
                                "#market_commodity_forsale_table > table > tbody > :nth-child(2) > :nth-child(1)")
                            is_row_prices = driver.find_elements_by_css_selector("#searchResultsRows")
                            print("length table prices and row prices -", len(is_table_prices), len(is_row_prices))
                            # if row prices - get lowest and  on market
                            if len(is_row_prices) > 0:
                                print("is_row_prices")
                                price_from_market = 100000000
                                steam_second_low_price = 100000000
                                steam_listed_prices = driver.find_elements_by_css_selector(
                                    "div.market_listing_price_listings_block > div.market_listing_right_cell.market_listing_their_price > span > span.market_listing_price.market_listing_price_with_fee")
                                # get lowest price
                                print("getting lowest price")
                                for steam_listed_price in steam_listed_prices:
                                    price_from_market_2 = steam_listed_price.text
                                    # бывают не цены, а надписи sold
                                    try:
                                        price_from_market_2 = float(price_from_market_2.strip().replace(',', '.')[:-5])
                                    except:
                                        continue
                                    print("price_from_market_2 -", price_from_market_2)
                                    if price_from_market_2 < price_from_market:
                                        price_from_market = price_from_market_2
                            # if table prices - get lowest on market
                            if len(is_table_prices) > 0:
                                print("is_table_prices")
                                price_from_market = driver.find_element_by_css_selector(
                                    "#market_commodity_forsale_table > table > tbody > :nth-child(2) > :nth-child(1)").text
                                price_from_market = float(price_from_market.strip().replace(',', '.')[:-5])
                            try:
                                lowest_steam_price = price_from_market
                            except:
                                print("cant get lowest steam price (break)")
                                break
                            already_checked_items_for_selling.append(name)
                            already_checked_items_for_selling.append(lowest_steam_price)
                            print("lowest price is -", lowest_steam_price)
                            print("min price -", min_price)
                            print("name -", name.encode('utf-8'))
                            print("add item's name in a list (already_checked_items_for_selling)")

                        if lowest_steam_price < min_price:
                            print("!!!!!!!!!!! lowest price is less that min price! (break)")

                        if lowest_steam_price > min_price:
                            print("start selling the item")
                            driver.switch_to.window(driver.window_handles[0])
                            lowest_steam_price = lowest_steam_price - 0.01
                            lowest_steam_price = float('{:.2f}'.format(lowest_steam_price))
                            print("lowest price (sold price) and min price -", lowest_steam_price, min_price)
                            # получаем название для проверки
                            link_checked = driver.find_element_by_xpath(
                                "//div[not(contains(@style,'display: none'))][@class='inventory_iteminfo']/div[3]/div[1]/div[1]/div[1]/a").get_attribute(
                                "href")
                            print("link checked -", link_checked)
                            link_checked_list = link_checked.split("/")
                            name_url_checked = link_checked_list[len(link_checked_list) - 1]
                            name_checked = unquote(name_url_checked).strip()
                            print("name checked -", name_checked.encode('utf-8'))
                            if name == name_checked:
                                driver.find_element_by_xpath(
                                    "//div[not(contains(@style,'display: none'))][@class='inventory_iteminfo']/div[3]/div[1]/a").click()
                                print("click sell button (first one)")
                                time.sleep(0.2)
                                try:
                                    wait.until(EC.visibility_of_element_located(
                                        (By.CSS_SELECTOR, "#market_sell_buyercurrency_input")))
                                except:
                                    break
                                # вводим цену
                                input_field = driver.find_element_by_css_selector('#market_sell_buyercurrency_input')
                                input_field.clear()
                                time.sleep(0.1)
                                input_field.send_keys(str(lowest_steam_price))
                                time.sleep(0.1)
                                price_checked = driver.find_element_by_css_selector(
                                    "#market_sell_buyercurrency_input").get_attribute('value')
                                print("price checked -", price_checked)
                                try:
                                    price_checked = float(price_checked)
                                except:
                                    print("cant get a price (break)")
                                    break
                                print("price checked, sthat we texted -", price_checked)
                                if price_checked > min_price:
                                    print("price_checked > min price")
                                    driver.find_element_by_css_selector("#market_sell_dialog_accept > span").click()
                                    time.sleep(0.5)
                                    if driver.find_element_by_css_selector("#market_sell_dialog_error").is_displayed():
                                        print("tick")
                                        driver.find_element_by_css_selector("#market_sell_dialog_accept_ssa").click()
                                        time.sleep(0.2)
                                        driver.find_element_by_css_selector("#market_sell_dialog_accept > span").click()
                                        time.sleep(0.5)
                                    driver.find_element_by_css_selector("#market_sell_dialog_ok > span").click()
                                    print("putt item on sale")
                                    # status = 2
                                    mycursor.execute(
                                        "UPDATE `skins` SET `status`= '2' WHERE `id` = %s",
                                        (bd_id,))
                                    mydb.commit()
                                    time.sleep(10)
                                    # close modal windows
                                    try:
                                        driver.find_element_by_css_selector("div.newmodal_buttons > div > span").click()
                                        time.sleep(0.2)
                                    except:
                                        pass
                                    try:
                                        driver.find_element_by_css_selector(":nth-child(5) > .newmodal_header_border > .newmodal_header > .newmodal_close").click()
                                        time.sleep(0.2)
                                    except:
                                        pass
                                    try:
                                        driver.find_element_by_css_selector(".newmodal_close").click()
                                        time.sleep(0.2)
                                    except:
                                        pass
                                    # для проверки, не обновится ли кеш инвентаря
                                    try:
                                        item_id_checked = driver.find_element_by_css_selector(
                                            "#inventories > div:nth-child(2) > div:first-child > div:nth-child(1) > div > a").get_attribute(
                                            "href")
                                        print("item id checked - ", item_id_checked)
                                    except:
                                        print("cant get item id checked")
                                        break
                                    if item_id_checked != item_id:
                                        print("page reloaded, no need to inspect next item (next_item += -1)")
                                        next_item += -1

                        break  # cause we dont need to find name anymore
            if index_next_page == 1:
                driver.find_element_by_css_selector("#pagebtn_next").click()
                print("----------click on the second page")
                time.sleep(10)


except Exception as e:
    telegram_bot_sendtext("steamPriceChangerV2: Возникла ошибка, нужно выяснять")
    PrintException()

print("success")
closeAll()
