
import os
import random
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

    input("press enter to exit")

    # screen
    now = time.strftime('%Y_%m-%d_%H_%M_%S')
    driver.save_screenshot('screens\Error' + '-' + str(now) + '.png')
    # close all
    mycursor.close()
    mydb.close()
    # display.stop() #linux
    driver.close()
    driver.quit()
    sys.exit()

try:

    # loging errors
    # Create a logging instance
    logger = logging.getLogger('csMoneyGetFloats')
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
    logger_msg = logging.getLogger('csMoneyGetFloats')
    logger_msg.setLevel(logging.INFO)  # you can set this to be DEBUG, INFO, ERROR
    # Assign a file-handler to that instance
    fh1 = logging.FileHandler("debug.txt")
    fh1.setLevel(logging.INFO)
    # Format your logs (optional)
    formatter = logging.Formatter('%(asctime)s - row:%(lineno)d - %(message)s')
    fh1.setFormatter(formatter)  # This will set the format to the file handler
    # Add the handler to your logging instance
    logger_msg.addHandler(fh1)


    # from pyvirtualdisplay import Display #linux
    # import pyautogui #linux

    # start time
    now = datetime.datetime.now()
    print(str(
        now) + "----------------------------------------------------------------------------------------------------------")

    # display = Display(visible=0, size=(1600, 900), backend='xvfb') #linux
    # display.start() #linux


    chrome_options = Options()

    # chrome_options.add_argument("user-data-dir=/home/work/profilesForAll/csMoneyBuy")  # linux
    chrome_options.add_argument(
        "user-data-dir=C:\\Users\\dr1m\\AppData\\Local\\Google\\Chrome\\User Data\\Default4")  # windows

    chrome_options.add_argument('--proxy-server=%s' % "37.9.46.247" + ":" + "8085")

    chrome_options.add_argument('--window-size=1600,900') #windows
    #prefs = {"profile.managed_default_content_settings.images": 2}  # 1 - load images, 2 - dont
    #chrome_options.add_experimental_option("prefs", prefs)

    # driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options) # linux
    driver = webdriver.Chrome(executable_path='C:\\Users\\Dr1m\\Desktop\\skinsautomation\\chromedriver.exe', chrome_options=chrome_options)  # windows



    def PrintException_only_print():
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




    # NoteBook
    # driver = webdriver.Chrome(options=chromeOptions, executable_path=r'C:\\Users\\Администратор\\Desktop\\pywinautomation\\chromedriver.exe')
    # chromeOptions.add_argument("user-data-dir=C:\\Users\\Администратор\\AppData\\Local\\Google\\Chrome\\User Data\\Default")

    wait = WebDriverWait(driver, 25)  # время вылета 10сек

    # rub_usd
    rub_usd = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    rub_usd = rub_usd.json()
    rub_usd = float(rub_usd["Valute"]["USD"]["Value"])
    print("current exchange rate", rub_usd)

    # # preparation CODE

    # ## check if I'm logged into steam

    # In[2]:

except Exception as e:
    telegram_bot_sendtext("csMoneyGetFloats: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()



# ## check if I'm logged into csMoney

# In[4]:
time.sleep(5)
input("test input")

try:
    driver.get("https://cs.money/ru/csgo/trade/?sort=price&order=asc&minPrice=11&hasRareFloat=true")
    time.sleep(20)
    driver.find_element_by_css_selector("#__next > div > div.styles_container__3vLR9 > div.styles_functional_wrap__2Px_I > div:nth-child(2) > div > div > div.styles_delimiter__225-J").click()
    time.sleep(1.5)
    driver.find_element_by_css_selector("#modal > div > div.styles_wrapper__1pcux > div > div.styles_body__2Vakr > div > div > div:nth-child(2)").click()
    time.sleep(1.5)
    driver.find_element_by_css_selector("#modal > div > div.styles_wrapper__1pcux > div > div.styles_body__2Vakr > div > div > div:nth-child(2) > div.MediaQueries_desktop__TwhBE > div > div.styles_content__1idcQ.styles_bottom_container__3SBTu > div.styles_scrollview__1RLVF > div#USD").click()
    time.sleep(1.5)
    driver.find_element_by_css_selector("#modal > div > div.styles_wrapper__1pcux > div > button").click()
    time.sleep(1)
    try:
        driver.find_element_by_css_selector("#modal > div > div.styles_wrapper__1pcux > div > button").click()
        time.sleep(1)
    except:
        pass
except Exception as e:
    telegram_bot_sendtext("csMoneyGetFloats: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()

# ## change price filter and load items

# In[5]:
try:
    price_filter = 11
    mycursor.execute("SELECT `price` FROM `csMoneyFloats` WHERE id = 1;")
    response = mycursor.fetchone()
    print(response)
    try:
        if float(response[0]) > price_filter:
            price_filter = float(response[0])
    except: pass

    print(price_filter)
    input_field = driver.find_element_by_css_selector('div:nth-child(1) > form > input')
    input_field.clear()
    input_field.send_keys(str(price_filter), Keys.TAB)
    time.sleep(8)

    # подгружаем все элементы из parser'a
    for x in range(23): #СКОЛЬКО ПОДГРУЗОК БУДЕТ
        time.sleep(8)
        try:
            mainBlocks = driver.find_elements_by_css_selector('div.bot-listing_body__3xI0X > div > div.list_list__2q3CF.list_small__g3Hxe > div:nth-child(n)')
            len_start = len(mainBlocks)
            element = driver.find_element_by_css_selector(
                'div.bot-listing_body__3xI0X > div > div.list_list__2q3CF.list_small__g3Hxe > div:nth-child(' + str(len(mainBlocks)) + ')')
            element.location_once_scrolled_into_view
            time.sleep(0.2)
            element = driver.find_element_by_css_selector(
                'div.bot-listing_body__3xI0X > div > div.list_list__2q3CF.list_small__g3Hxe > div:nth-child(' + str(len(mainBlocks) - 29) + ')')
            element.location_once_scrolled_into_view
            time.sleep(0.2)
        except:
            continue
        for ind in range(20):
            mainBlocks = driver.find_elements_by_css_selector('table > tbody > tr:nth-child(n)')
            len_after_scroll = len(mainBlocks)
            if len_start == len_after_scroll:
                time.sleep(0.8)
            if len_start != len_after_scroll:
                print("new items loaded")
                break
        mainBlocks = driver.find_elements_by_css_selector('table > tbody > tr:nth-child(n)')
        len_after_scroll = len(mainBlocks)
        if len_start == len_after_scroll:
            print("new items didn't load")
            break


except Exception as e:
    telegram_bot_sendtext("csMoneyGetFloats: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()



# get items



try:

    #div.bot-listing_body__3xI0X > div > div.list_list__2q3CF.list_small__g3Hxe > div:nth-child(1) >
    mainBlocks = driver.find_elements_by_css_selector('div.bot-listing_body__3xI0X > div > div.list_list__2q3CF.list_small__g3Hxe > div:nth-child(n) > div > div > div > div.actioncard_card__19Ydi > div > div > div > footer > div.BaseCard_price__27L2x > div > span > span')
    print("items length -", len(mainBlocks))
    index = 0
    for item in mainBlocks:
        index += 1
        #get last checked price every 10 itterations
        if index % 10 == 0:
            print("update last checked price (id - 2)")
            mycursor.execute("UPDATE csMoneyFloats SET price = %s WHERE id = 1", (price,))
            mydb.commit()
            print("done! price is -", price)
        try:
            #move cursor
            element_to_hover_over = driver.find_element_by_css_selector("#__next > div > div:nth-child(3) > div:nth-child(1) > div > div:nth-child(1) > div.user-listing_cart__cGE80 > div > div.TradeCart_header__ZfcJZ > div:nth-child(2) > div > div")
            ActionChains(driver).move_to_element(element_to_hover_over).perform()
            #right click on item
            action = ActionChains(driver)
            action.move_to_element(item).perform();
            action.context_click().perform()
            #name
            type = driver.find_element_by_css_selector("h2.csm_ui__text__f444b.csm_ui__body_14_regular__f444b.SkinName_name_and_quality__6Efwt > span:nth-child(1)").text.strip() #awp/m4a4/five-seven
            print(type)
            name_of_skin = driver.find_element_by_css_selector("h2.csm_ui__text__f444b.csm_ui__headline_18_medium__f444b.SkinName_pattern_name__3WLUp").text.strip() #redline/desert-strike
            print(name_of_skin)
            exterior = driver.find_element_by_css_selector("h2.csm_ui__text__f444b.csm_ui__body_14_regular__f444b.SkinName_name_and_quality__6Efwt > span:nth-child(2)").text.strip() #fn/ft/mw
            exterior = exterior[1:].strip()
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
            print(exterior)
            full_name = type + " | " + name_of_skin + " " + exterior
            print("full_name", full_name)
            #float
            float_value = driver.find_element_by_css_selector("#tooltips > div > aside > section.Card_skin_properties_section__3ZJkN > div:nth-child(2) > span.csm_ui__text__f444b.csm_ui__body_14_regular__f444b.SkinProperty_value__15x0M").text.strip()
            print("float_value", float_value)
            #float cost
            rows_overprice = driver.find_elements_by_css_selector("#tooltips > div > aside > section.Card_overprice_section__30Gwz > div:nth-child(n) > span")
            next_span_is_float_cost = 0
            for row in rows_overprice:
                if next_span_is_float_cost == 1:
                    float_cost = row.text.strip()
                    float_cost = float_cost[1:].strip()
                    float_cost = float_cost[1:].strip()
                    break
                if row.text.strip() == "Редкий float":
                    next_span_is_float_cost = 1


            print("float_cost", float_cost)
            price = item.text.strip()
            price = price[1:].strip()
            print("price", price)

            mycursor.execute("SELECT name, float_value FROM csMoneyFloats WHERE name=%s AND float_value=%s ORDER BY id DESC LIMIT 1",(full_name,float_value,))
            response = mycursor.fetchone()
            print("response (must be None to add an item)", response)
            if response is None:
                mycursor.execute(
                    "INSERT INTO csMoneyFloats (name, price, float_value, float_cost) VALUES (%s, %s, %s, %s)",
                    (full_name, price, float_value, float_cost,))
                mydb.commit()
                print("++++++++++++++++++++")

                """
                #debug
                logger_msg.info("name - " + str(full_name) + " price - " + str(price) + " float_value - " + str(float_value) + " float_cost - " + str(float_cost))  # debug
                # screen
                now = time.strftime('%Y_%m-%d_%H_%M_%S')
                driver.save_screenshot('screens\item' + '-' + str(now) + '.png')
                """



        except Exception as e:
            print("was an error (page down)")
            PrintException_only_print()
            continue






except Exception as e:
    telegram_bot_sendtext("csMoneyGetFloats: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()




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
