#!/usr/bin/env python
# coding: utf-8

# # settings, imports and functions

# In[1]:


import os
import random
import time
import linecache
import sys
import mysql.connector
import urllib
import requests
import datetime
import time
import re
import logging
from itertools import cycle
import MySQLdb
import urllib.parse





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
    now = time.strftime('%Y_%m-%d_%H_%M_%S')
    # close all
    mycursor.close()
    mydb.close()
    # display.stop() #linux
    sys.exit()

try:

    # from pyvirtualdisplay import Display #linux
    # import pyautogui #linux

    # start time
    now = datetime.datetime.now()
    print(str(
        now) + "----------------------------------------------------------------------------------------------------------")
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




    # loging errors
    # Create a logging instance
    logger = logging.getLogger('steamParser_errors')
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
    logger_msg = logging.getLogger('steamBuyNotifier_info')
    logger_msg.setLevel(logging.INFO)  # you can set this to be DEBUG, INFO, ERROR
    # Assign a file-handler to that instance
    fh1 = logging.FileHandler("debug.txt")
    fh1.setLevel(logging.INFO)
    # Format your logs (optional)
    formatter = logging.Formatter('%(asctime)s - row:%(lineno)d - %(message)s')
    fh1.setFormatter(formatter)  # This will set the format to the file handler
    # Add the handler to your logging instance
    logger_msg.addHandler(fh1)

except Exception as e:
    telegram_bot_sendtext("SteamMakeOrders-csMoney: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()


try:
    #get items to parse
    mycursor.execute("SELECT name, id, date, price_csm FROM tradebackMakeOrders")
    response = mycursor.fetchall()
    print(response[0])
    if len(response) < 1:
        raise ValueError('get nothin after request from table tradebackMakeOrders')
    a1 = response[0][2]
    b1 = datetime.datetime.now()
    delta1 = b1 - a1
    print('time difference ', int(delta1.total_seconds()))
    if int(delta1.total_seconds()) > 7200:
        raise ValueError("need to update table's skins (tradebackMakeOrders)")


    #get list of proxies
    with open('proxy_http_ip.txt', 'r') as f:
        proxy_from_file = f.readlines()

    list_proxy = []
    for single_proxy in proxy_from_file:
        full_proxy_url = "http://" + str(single_proxy)
        list_proxy.append(full_proxy_url)
    proxy_cycle = cycle(list_proxy)




    #get usd_rub of steam
    try:
        proxy = next(proxy_cycle)
        proxies = {"http": proxy}
        try:
            response_1 = requests.get(
                url="https://steamcommunity.com/market/priceoverview/?currency=5&appid=730&market_hash_name=AK-47%20|%20Redline%20(Field-Tested)",
                proxies=proxies)
        except:
            proxy = next(proxy_cycle)
            proxies = {"http": proxy}
            response_1 = requests.get(
                url="https://steamcommunity.com/market/priceoverview/?currency=5&appid=730&market_hash_name=AK-47%20|%20Redline%20(Field-Tested)",
                proxies=proxies)

        proxy = next(proxy_cycle)
        proxies = {"http": proxy}
        try:
            response_2 = requests.get(
                url="https://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=AK-47%20|%20Redline%20(Field-Tested)",
                proxies=proxies)
        except:
            proxy = next(proxy_cycle)
            proxies = {"http": proxy}
            response_2 = requests.get(
                url="https://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=AK-47%20|%20Redline%20(Field-Tested)",
                proxies=proxies)
        response_1 = response_1.json()
        response_2 = response_2.json()
        price_rub = response_1["lowest_price"].replace(',', '.')[:-5]
        print(price_rub)
        price_usdt = response_2["lowest_price"][1:]
        print(price_usdt)
        rub_usdt1 = float(price_rub) / float(price_usdt)
        rub_usdt1 = float('{:.2f}'.format(rub_usdt1))
    except:
        raise ValueError("cant get usd_rub of steam")

    time.sleep(5)

    try:
        proxy = next(proxy_cycle)
        proxies = {"http": proxy}
        try:
            response_1 = requests.get(url="https://steamcommunity.com/market/priceoverview/?currency=5&appid=730&market_hash_name=AK-47%20|%20Redline%20(Field-Tested)",proxies=proxies)
        except:
            proxy = next(proxy_cycle)
            proxies = {"http": proxy}
            response_1 = requests.get(url="https://steamcommunity.com/market/priceoverview/?currency=5&appid=730&market_hash_name=AK-47%20|%20Redline%20(Field-Tested)",proxies=proxies)

        proxy = next(proxy_cycle)
        proxies = {"http": proxy}
        try:
            response_2 = requests.get(url="https://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=AK-47%20|%20Redline%20(Field-Tested)",proxies=proxies)
        except:
            proxy = next(proxy_cycle)
            proxies = {"http": proxy}
            response_2 = requests.get(url="https://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=AK-47%20|%20Redline%20(Field-Tested)",proxies=proxies)

        response_1 = response_1.json()
        response_2 = response_2.json()
        price_rub = response_1["lowest_price"].replace(',', '.')[:-5]
        print(price_rub)
        price_usdt = response_2["lowest_price"][1:]
        print(price_usdt)
        rub_usdt2 = float(price_rub) / float(price_usdt)
        rub_usdt2 = float('{:.2f}'.format(rub_usdt2))
    except:
        raise ValueError("cant get usd_rub of steam")

    #check if we get right usdt
    print(rub_usdt1, rub_usdt2)
    error = 1
    if rub_usdt1 == rub_usdt2:
        error = 0
    elif rub_usdt1 - rub_usdt2 < 0.5:
        error = 0
    elif rub_usdt2 - rub_usdt1 < 0.5:
        error = 0

    if error == 1:
        raise ValueError("first rub_usdt is much different than second rub_usdt")
    rub_usdt = rub_usdt1


    print("length mysql response", len(response))
    for item in response:
        name_response = item[0]
        id_response = item[1]
        price_csm_response = float(item[3])

        proxy = next(proxy_cycle)
        proxies = {"http": proxy}
        #request
        name_quoted = urllib.parse.quote(name_response, safe='')
        full_link = "https://api.steamapis.com/market/item/730/" + str(name_quoted) + '?api_key=LZ13AgadysjFkJ7W3NyFTbJGlNM'
        try:
            response = requests.get(url=full_link, proxies=proxies)
            r = response.json()
        except:
            logger_msg.info("steamParser / steam / error / 1 / null")  # debug
            continue

        highest_steam_order_rub = float(r["histogram"]["highest_buy_order"]) * rub_usdt
        highest_steam_order_rub = float('{:.2f}'.format(highest_steam_order_rub))

        profit = (highest_steam_order_rub / price_csm_response -1) * -100
        profit = float('{:.2f}'.format(profit))

        print(profit, highest_steam_order_rub)

        mycursor.execute(
            "UPDATE tradebackMakeOrders SET price_steam_order = %s, profit = %s WHERE id = %s",
            (highest_steam_order_rub, profit, id_response,))
        mydb.commit()


except Exception as e:
    telegram_bot_sendtext("SteamMakeOrders-csMoney: Возникла ошибка, нужно выяснять")
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
sys.exit()
