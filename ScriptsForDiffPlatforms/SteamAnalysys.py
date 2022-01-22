import os
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import linecache
import sys
import requests
import MySQLdb
import datetime
import mysql.connector
import logging
import re
import urllib
import threading





#настройка и главные функции
try:



    skins = [
        #{"name": "Fracture Case", "link":"https://steamcommunity.com/market/listings/730/Fracture%20Case"},
        #{"name": "CS20 Case", "link": "https://steamcommunity.com/market/listings/730/CS20%20Case"},
        #{"name": "Glove Case", "link": "https://steamcommunity.com/market/listings/730/Glove%20Case"},
        #{"name": "Operation Breakout Weapon Case", "link": "https://steamcommunity.com/market/listings/730/Operation%20Breakout%20Weapon%20Case"},
        #{"name": "Clutch Case", "link": "https://steamcommunity.com/market/listings/730/Clutch%20Case"},
        #{"name": "Operation Broken Fang Case", "link": "https://steamcommunity.com/market/listings/730/Operation%20Broken%20Fang%20Case"},
        {"name": "Snakebite Case", "link": "https://steamcommunity.com/market/listings/730/Snakebite%20Case"}
    ]



    def PrintException():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))



    def PrintException_only_print():
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








    #основная функция, которую будем запускать в несколько потоков
    def analyse_item(item_name, item_link):
        #driver
        #start driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
        wait = WebDriverWait(driver, 25)
        #настройки
        name = item_name
        errors = 0
        driver.get(item_link)
        time.sleep(5)
        try:
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#market_activity_section")))
        except:
            try:
                driver.get(item_link)
                wait.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "#market_activity_section")))
            except:
                raise ValueError("---------------------------cant load item's page")
        # для каждого потенциального проблемного места создаем свой счетчик ошибок
        error_in_a_row_styles = 0
        error_in_a_row_message = 0
        all_errors = 0
        #начинаем основной цикл проверки предмета
        while True:
            time.sleep(0.05)

            if error_in_a_row_styles > 2 or error_in_a_row_message > 2:
                print("qq")
                raise ValueError('3 errors in a row')

            first_div_styles = driver.find_element_by_css_selector("#market_activity_block > div:nth-child(2)").get_property('style') #получаем стили первого блока (если происходит динамическая подгрузка, то первый div меняет положение и прозрачность)
            if len(first_div_styles) > 1: #если кол-во стилей больше 1 (opacity + margin, иначе = 0)
                #ждем, когда первый блок полностью исчезнет (когда перестанет отображаться opacity и margin в стиле у блока div)
                for i in range(100):
                    time.sleep(0.01)
                    try: #при обновлении div'a, может так совпасть, что он будет пытаться найти несуществующий div
                        div_styles_length = len(driver.find_element_by_css_selector("#market_activity_block > div:nth-child(2)").get_property('style'))
                        error_in_a_row_styles = 0
                    except:
                        error_in_a_row_styles += 1
                        time.sleep(0.05)
                        print("can't take style of first div (error_in_a_row_styles)", error_in_a_row_styles)
                        continue
                    #стили пропали, получаем информацию о новой информации по предмету
                    if div_styles_length == 0:
                        time.sleep(0.05)
                        try:
                            type_of_message = driver.find_element_by_css_selector("#market_activity_block > div:last-child > span").get_attribute('innerHTML')
                            error_in_a_row_message = 0
                        except:
                            error_in_a_row_message += 1
                            print("can't take style of first div (error_in_a_row_message)", error_in_a_row_message)
                            continue

                        try:
                            #получаем статус операции и остальные значения
                            splited_row = type_of_message.split(" ")
                            price = splited_row[-1][1:]
                            sellers_avatar_link = None
                            buyers_avatar_link = None
                            buyers_name = None
                            sellers_name = None
                            status = 0

                            # куча try: except для того, что ники и ссылки часто неадекватного формата, операции мы все должны фиксировать
                            for element_of_row in splited_row:
                                #приобрел
                                if element_of_row == "purchased":
                                    status = 1
                                    splited_message = type_of_message.split("purchased")#чтобы отличить покупателя от продавца
                                    try:
                                        buyers_avatar_link = re.search('src="https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars([^<>]*)jpg"></span>', splited_message[0]).group(1).strip()
                                    except: pass
                                    try:
                                        buyers_name = re.search('market_ticker_name">([^<>]*)</span>', splited_message[0]).group(1).strip()
                                    except: pass
                                    try:
                                        sellers_avatar_link = re.search('src="https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars([^<>]*)jpg"></span>',splited_message[1]).group(1).strip()
                                    except: pass
                                    try:
                                        sellers_name = re.search('market_ticker_name">([^<>]*)</span>', splited_message[1]).group(1).strip()
                                    except: pass

                                    #mysql
                                    try:
                                        mycursor.execute(
                                            "INSERT INTO itemsAnalysys (item_name, item_price, buyers_name, buyers_link, sellers_name, sellers_link, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                            (name, price, buyers_name.encode('utf-8'), buyers_avatar_link, sellers_name.encode('utf-8'), sellers_avatar_link, status,))
                                        mydb.commit()
                                    except:
                                        mycursor.execute(
                                            "INSERT INTO itemsAnalysys (item_name, item_price, buyers_link, sellers_link, status) VALUES (%s, %s, %s, %s, %s)",
                                            (name, price, buyers_avatar_link, sellers_avatar_link, status,))
                                        mydb.commit()
                                    print(name, "+1")
                                #выставил
                                if element_of_row == "listed":
                                    status = 2
                                    try:
                                        sellers_avatar_link = re.search('src="https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars([^<>]*)jpg"></span>', type_of_message).group(1).strip()
                                    except: pass
                                    try:
                                        sellers_name = re.search('market_ticker_name">([^<>]*)</span>', type_of_message).group(1).strip()
                                    except: pass

                                    #mysql
                                    try:
                                        mycursor.execute(
                                            "INSERT INTO itemsAnalysys (item_name, item_price, sellers_name, sellers_link, status) VALUES (%s, %s, %s, %s, %s)",
                                            (name, price, sellers_name.encode('utf-8'), sellers_avatar_link, status,))
                                        mydb.commit()
                                    except:
                                        mycursor.execute(
                                            "INSERT INTO itemsAnalysys (item_name, item_price, sellers_link, status) VALUES (%s, %s, %s, %s)",
                                            (name, price, sellers_avatar_link, status,))
                                        mydb.commit()
                                    print(name, "+1")
                                # отменил
                                if element_of_row == "cancelled":
                                    status = 3
                                    try:
                                        sellers_avatar_link = re.search('src="https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars([^<>]*)jpg"></span>', type_of_message).group(1).strip()
                                    except: pass
                                    try:
                                        sellers_name = re.search('market_ticker_name">([^<>]*)</span>', type_of_message).group(1).strip()
                                    except: pass

                                    #mysql
                                    try:
                                        mycursor.execute(
                                            "INSERT INTO itemsAnalysys (item_name, item_price, sellers_name, sellers_link, status) VALUES (%s, %s, %s, %s, %s)",
                                            (name, price, sellers_name.encode('utf-8'), sellers_avatar_link, status,))
                                        mydb.commit()
                                    except:
                                        mycursor.execute(
                                            "INSERT INTO itemsAnalysys (item_name, item_price, sellers_link, status) VALUES (%s, %s, %s, %s)",
                                            (name, price, sellers_avatar_link, status,))
                                        mydb.commit()
                                    print(name, "+1")

                        except Exception as e:
                            PrintException_only_print()
                            all_errors += 1
                            print("---errors-", all_errors)  # debug
                            break
                        break



        print("function end")





    #выполняем для всего списка предметов в отдельном потоке
    threads = []
    for item in skins:
        print("start new", item)
        t = threading.Thread(target=analyse_item, args=(item["name"], item["link"],))
        threads.append(t)
        t.start()
        time.sleep(5)

    # block until all the threads finish (i.e. until all function_a functions finish)
    for t in threads:
        print("end")
        t.join()


except Exception as e:
    telegram_bot_sendtext("SteamAnalysys: Возникла ошибка, нужно выяснять")
    PrintException()
    close_script()

print("Successful")
close_script()
