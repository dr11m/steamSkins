import os
import random
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

date_format = "%d/%m/%Y"


#loging errors
# Create a logging instance
logger = logging.getLogger('DmarketHistory')
logger.setLevel(logging.INFO) # you can set this to be DEBUG, INFO, ERROR
# Assign a file-handler to that instance
fh = logging.FileHandler("LogDmarketHistory.txt")
fh.setLevel(logging.ERROR) # again, you can set this differently
# Format your logs (optional)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter) # This will set the format to the file handler
# Add the handler to your logging instance
logger.addHandler(fh)

succsess = 1

# обработка ошибок
def PrintException():
    succsess = 0
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


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
options.add_argument("user-data-dir=/home/work/profiles/DmarketHistory")  # linux

options.add_argument('--window-size=1600,900')
driver = webdriver.Chrome(executable_path=executable_path, options=options)




wait = WebDriverWait(driver, 10)  # время вылета 10сек

# rub_usd
rub_usd = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
rub_usd = rub_usd.json()
rub_usd = float(rub_usd["Valute"]["USD"]["Value"])
print("current exchange rate", rub_usd)

# outFileName = "C:\\login.txt" #windows
outFileName = "/home/login.txt"  # linux
outFile = open(outFileName, "w")
outFile.write("")
outFile.close()


src_csgo = "https://cdn-front.dmarket.com/images-all/5938a31c-0be7-43ee-98ef-8698e47be5b8.jpg"
src_rust = "https://cdn-front.dmarket.com/images-all/cb3b8829-b82d-4f52-b469-c1634dc883cf.png"
src_tf2 = "https://cdn-front.dmarket.com/images-all/e9c65fe3-db87-41c5-861a-e6b417f0c073.png"
src_dota = "https://cdn-front.dmarket.com/images-all/b14d6f32-5d9d-416e-badb-bbecf0fdc69a.jpg"

#get_mobth
def monthToNum(shortMonth):
    return {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12'
    }[shortMonth]

try:

    driver.get("https://steamcommunity.com/market/")
    time.sleep(3)

    try:
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#marketWalletBalanceAmount")))
        time.sleep(2)
    except:
        print("type login, pass and guard into a file C:\login.txt")
        # отправляем сообщение и ожидаем ввода данных для входа
        telegram_bot_sendtext("DmarketHistory: требуется вход в стим (ввести логин, пароль и стим гуард в текстовый файл C:\login.txt)")
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

        #удаляем данные
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

    driver.get("https://dmarket.com/ingame-items/item-list/csgo-skins")
    time.sleep(5)
    #decline all notifications
    try:
        driver.find_element_by_css_selector("#onesignal-slidedown-cancel-button").click()
        time.sleep(1)
    except: pass
    #accept cookies
    try:
        driver.find_element_by_css_selector("div.c-cookieBanner__textWrapper > button").click()
        time.sleep(1)
    except: pass
    #close a newbie instruction
    try:
        driver.find_element_by_css_selector("seo-area-header > button > mat-icon").click()
        time.sleep(1)
    except: pass
    #close a banner of a summer sale
    try:
        driver.find_element_by_css_selector("summer-sale-banner > div > button > mat-icon").click()
        time.sleep(1)
    except: pass
    #close live feed if it opens
    try:
        driver.find_element_by_css_selector("market-inventory > live-feed-desktop > div > div > a")
        driver.find_element_by_css_selector("mat-sidenav-container > mat-sidenav-content > exchange > div > div.c-exchange__container > market-side > div > market-inventory > live-feed-desktop > div > div > button > span.mat-button-wrapper > i").click()
        time.sleep(1)
    except: pass


    need_to_login_dmarket = driver.find_elements_by_css_selector("div.c-exchangeHeader__inner.c-exchangeHeader__inner--market > header-navigation > navigation-controls > header-user-auth-btn > div > button.c-navigationAuth__authBtn.c-navigationAuth__authBtn--logIn")
    if len(need_to_login_dmarket) > 0:
        need_to_login_dmarket[0].click()
        time.sleep(2)
        driver.find_element_by_css_selector("auth-flows > div > login-flow > div > auth-footer > div > vendor-auth-link > button").click()
        time.sleep(5)
        try:
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#openidForm > div > div.OpenID_UserContainer > div.OpenID_UserName > div.OpenID_loggedInName")))
        except:
            raise ValueError('need to login into dmarket')
        driver.find_element_by_css_selector("#imageLogin").click()
        time.sleep(5)
        driver.get("https://dmarket.com/ingame-items/item-list/csgo-skins")
        time.sleep(5)

    # close a banner of a summer sale
    try:
        driver.find_element_by_css_selector("summer-sale-banner > div > button > mat-icon").click()
        time.sleep(1)
    except: pass

    #if necessary page is already opened, we close it
    try:
        driver.find_element_by_css_selector("div.c-historyDialog__tabs > button.c-historyDialog__tab.is-active")
        driver.find_element_by_css_selector("history-dialog > div > div.c-historyDialog__header > button > mat-icon").click()
    except: pass

    #if non english version of the site
    try:
        driver.find_element_by_css_selector("mat-sidenav-content > exchange > div > div.c-exchangeHeader > div.c-exchangeHeader__inner.c-exchangeHeader__inner--market > header-navigation > div > button.c-exchangeHeader__button.c-exchangeHeader__button--language.ng-star-inserted > i > svg > symbol#icon-flag-usa")
    except:
        driver.find_element_by_css_selector("div.c-exchangeHeader__inner.c-exchangeHeader__inner--market > header-navigation > div > button.c-exchangeHeader__button.c-exchangeHeader__button--language.ng-star-inserted").click()
        time.sleep(3)
        driver.find_element_by_css_selector("#mat-select-2 > div > div.mat-select-arrow-wrapper").click()
        time.sleep(2)
        driver.find_element_by_css_selector("mat-option:nth-child(2)").click()
        time.sleep(2)
        driver.find_element_by_css_selector("localization-settings > form > div.c-localization__buttons.c-localization__buttons--bottom > button").click()


    driver.find_element_by_css_selector("mat-sidenav-content > exchange > div > div.c-exchangeHeader > div.c-exchangeHeader__inner.c-exchangeHeader__inner--market > header-navigation > navigation-controls > header-user-dropdown > div > i > svg").click()
    time.sleep(5)
    driver.find_element_by_css_selector("button.mat-focus-indicator.c-dropdown__item.mat-menu-item.ng-star-inserted:nth-child(4)").click()
    try:
        time.sleep(4)
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "app-history-item:nth-child(2) > div:nth-child(4) > p")))
    except:
        raise ValueError('History is not available rn')

    for i in range(20): #amount of loaded pages
        driver.find_element_by_css_selector("div > app-pagination-v2 > div > button").click()
        time.sleep(3)


    items = driver.find_elements_by_css_selector("app-history > div > div > app-history-item:nth-child(n)")
    print("number of items -", len(items))
    if len(items) > 0:
        for item in items:

            #get date and skip ancient trades
            date = item.find_element_by_css_selector("div.c-history__cell.c-history__cell--date > p").text
            date_splited = date.split(" ")
            print("splited date -", date_splited)
            month_number = monthToNum(date_splited[1])
            date_dmarket = str(date_splited[0]) + "/" + str(month_number) + "/" + str(date_splited[2])
            date_start = "20/06/2021" #till wich date not take any rows into our DB
            print("dates -", date_dmarket, date_start)
            a = datetime.strptime(date_start, date_format)
            b = datetime.strptime(date_dmarket, date_format)
            delta = b - a
            print("date diff -",delta.days)
            if delta.days < 0:
                print("date diff less than 0 (continue)")
                continue
            date_dmarket = date_dmarket + " " + str(date_splited[3])
            print("full date from dm -", date_dmarket)

            #type of transaction
            type_of_transaction = item.find_element_by_css_selector("div:nth-child(2)").text
            print("type of transaction -", type_of_transaction)
            if type_of_transaction != "Purchase":
                print("type of transaction is not 'Purchase' (continue)")
                continue

            #game id
            src = item.find_element_by_css_selector("div:nth-child(3) > img").get_attribute("src")
            print("source img is -", src)
            if src == src_csgo:
                game_id = "730"
            if src == src_dota:
                game_id = "570"
            if src == src_rust:
                game_id = "252490"
            if src == src_tf2:
                game_id = "440"

            print("game id -", game_id)

            #name
            name = item.find_element_by_css_selector("div:nth-child(4) > p").text
            print("name -", name)

            #price
            price = item.find_element_by_css_selector("div:nth-child(5) > p > span").text
            print("price -", name)

            #unique id
            unique_id = item.find_element_by_css_selector("div:nth-child(8) > div > span").text
            print("unique id -", unique_id)

            #converted date
            date_dmarket_list = date_dmarket.split(" ")
            hour = date_dmarket_list[1]
            if len(hour) == 4:
                hour = "0" + hour
            date_dmarket_list_d_m_y = date_dmarket_list[0].split("/")
            day = date_dmarket_list_d_m_y[0]
            month = date_dmarket_list_d_m_y[1]
            year = date_dmarket_list_d_m_y[2]
            converted_date = year + "-" + month + "-" + day + " " + hour
            print("converted date -", converted_date)

            # check if exists in my DB
            mycursor.execute("SELECT * FROM skins WHERE DATE =%s AND unique_platform_id =%s AND platform_from ='6' LIMIT 1",
                             (converted_date, unique_id,))
            response = mycursor.fetchone()
            print("response (if exists we dont want to add this item):", response)
            if response == None:

                #mysql request
                print(name.encode('utf-8'), "------------------------------------------------------------------------")
                mycursor.execute(
                    "INSERT INTO skins (NAME, PRICE, game_id, platform_from, platform_to, DATE, unique_platform_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, price, game_id, '6', '1', converted_date, unique_id,))
                mydb.commit()
                print(mycursor.rowcount, "record(s) affected")
                print("------------------------------------------------------------------------")





except Exception as e:
    r = str(random.randint(1, 10001))
    driver.save_screenshot('Error-SteamHistory' + r + '.png')
    telegram_bot_sendtext("DmarketHistory: Возникла ошибка, нужно выяснять")
    logger.exception(e) # Will send the errors to the file
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
