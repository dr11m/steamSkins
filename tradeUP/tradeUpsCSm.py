
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
import requests
import json




def PrintException():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))



#loging errors
# Create a logging instance
logger = logging.getLogger('TradeUps')
logger.setLevel(logging.INFO) # you can set this to be DEBUG, INFO, ERROR
# Assign a file-handler to that instance
fh = logging.FileHandler("TradeUps_Log.txt")
fh.setLevel(logging.ERROR) # again, you can set this differently
# Format your logs (optional)
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter) # This will set the format to the file handler
# Add the handler to your logging instance
logger.addHandler(fh)


try:
    succsess = 1 #to properly end the script
#logging
    #loging errors
    # Create a logging instance
    #logger = logging.getLogger('SteamOrderPrices')
    #logger.setLevel(logging.INFO) # you can set this to be DEBUG, INFO, ERROR
    # Assign a file-handler to that instance
    #fh = logging.FileHandler("ErrorsSteamOrderPrices.txt")
    #fh.setLevel(logging.ERROR) # again, you can set this differently
    # Format your logs (optional)
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #fh.setFormatter(formatter) # This will set the format to the file handler
    # Add the handler to your logging instance
    #logger.addHandler(fh)




    # предметы с steam
    # loging errors
    # Create a logging instance
    logger = logging.getLogger('SteamOrderPrices')
    logger.setLevel(logging.INFO)  # you can set this to be DEBUG, INFO, ERROR
    # Assign a file-handler to that instance
    fh = logging.FileHandler("ErrorsSteamOrderPrices.txt")
    fh.setLevel(logging.ERROR)  # again, you can set this differently
    # Format your logs (optional)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)  # This will set the format to the file handler
    # Add the handler to your logging instance
    logger.addHandler(fh)

    executable_path = "C:\\Users\\Dr1m\\Desktop\\skinsStuff\\skinsautomation\\chromedriver94.exe"
    os.environ["webdriver.chrome.driver"] = executable_path
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("user-data-dir=C:\\Users\\Dr1m\\AppData\\Local\\Google\\Chrome\\User Data\\Default8")
    chrome_options.add_argument('--window-size=1600,900')
    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)

    itemsLF = []


    ##############################
    # получаем предметы с пасера #
    ##############################
    driver.get(
        "https://table.altskins.com/site/items?ItemsFilter%5Bknife%5D=0&ItemsFilter%5Bstattrak%5D=0&ItemsFilter%5Bstattrak%5D=1&ItemsFilter%5Bsouvenir%5D=0&ItemsFilter%5Bsouvenir%5D=1&ItemsFilter%5Bsticker%5D=0&ItemsFilter%5Btype%5D=1&ItemsFilter%5Bservice1%5D=showcsmoneyw&ItemsFilter%5Bservice2%5D=showsteam&ItemsFilter%5Bunstable1%5D=1&ItemsFilter%5Bunstable2%5D=1&ItemsFilter%5Bhours1%5D=1&ItemsFilter%5Bhours2%5D=192&ItemsFilter%5BpriceFrom1%5D=0.2&ItemsFilter%5BpriceTo1%5D=&ItemsFilter%5BpriceFrom2%5D=&ItemsFilter%5BpriceTo2%5D=&ItemsFilter%5BsalesBS%5D=&ItemsFilter%5BsalesTM%5D=&ItemsFilter%5BsalesST%5D=11&ItemsFilter%5Bname%5D=&ItemsFilter%5Bservice1Minutes%5D=&ItemsFilter%5Bservice2Minutes%5D=3011&ItemsFilter%5BpercentFrom1%5D=&ItemsFilter%5BpercentFrom2%5D=&ItemsFilter%5Btimeout%5D=5&ItemsFilter%5Bservice1CountFrom%5D=0&ItemsFilter%5Bservice1CountTo%5D=&ItemsFilter%5Bservice2CountFrom%5D=&ItemsFilter%5Bservice2CountTo%5D=&ItemsFilter%5BpercentTo1%5D=&ItemsFilter%5BpercentTo2%5D=")
    time.sleep(6)
    element = 0
    try:
        element = driver.find_element_by_css_selector(
            "#page-wrapper > div.row.border-bottom > nav > ul > li:nth-child(4) > a > img")
    except:
        pass
    if element != 0:
        driver.find_element_by_css_selector(
            "#page-wrapper > div.row.border-bottom > nav > ul > li:nth-child(4) > a > img").click()
        time.sleep(5)
        driver.find_element_by_css_selector("#imageLogin").click()
        time.sleep(5)

    driver.get("https://www.google.com/")
    time.sleep(3)
    driver.get(
        "https://table.altskins.com/site/items?ItemsFilter%5Bknife%5D=0&ItemsFilter%5Bstattrak%5D=0&ItemsFilter%5Bstattrak%5D=1&ItemsFilter%5Bsouvenir%5D=0&ItemsFilter%5Bsouvenir%5D=1&ItemsFilter%5Bsticker%5D=0&ItemsFilter%5Btype%5D=1&ItemsFilter%5Bservice1%5D=showcsmoneyw&ItemsFilter%5Bservice2%5D=showcsmoney&ItemsFilter%5Bunstable1%5D=1&ItemsFilter%5Bunstable2%5D=1&ItemsFilter%5Bhours1%5D=1&ItemsFilter%5Bhours2%5D=192&ItemsFilter%5BpriceFrom1%5D=0.5&ItemsFilter%5BpriceTo1%5D=&ItemsFilter%5BpriceFrom2%5D=&ItemsFilter%5BpriceTo2%5D=&ItemsFilter%5BsalesBS%5D=&ItemsFilter%5BsalesTM%5D=&ItemsFilter%5BsalesST%5D=11&ItemsFilter%5Bname%5D=&ItemsFilter%5Bservice1Minutes%5D=&ItemsFilter%5Bservice2Minutes%5D=3011&ItemsFilter%5BpercentFrom1%5D=&ItemsFilter%5BpercentFrom2%5D=&ItemsFilter%5Btimeout%5D=5&ItemsFilter%5Bservice1CountFrom%5D=0&ItemsFilter%5Bservice1CountTo%5D=&ItemsFilter%5Bservice2CountFrom%5D=5&ItemsFilter%5Bservice2CountTo%5D=&ItemsFilter%5BpercentTo1%5D=&ItemsFilter%5BpercentTo2%5D=")
    time.sleep(8)

    element = 0
    try:
        element = driver.find_element_by_css_selector(
            "#page-wrapper > div.row.border-bottom > nav > ul > li:nth-child(4) > a > img")
    except:
        pass

    if element != 0:
        mycursor.close()
        mydb.close()
        driver.close()
        driver.quit()
        raise ValueError('A very specific bad thing happened.')

    # подгружаем все элементы из parser'a
    for x in range(10):
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
        for ind in range(35):
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
    XML = driver.find_element_by_css_selector('#w0 > table > tbody').get_attribute('innerHTML')
    XML = XML.split('<tr class="tr"')
    print(len(XML))
    print(XML[1])
    del XML[0]
    # print(XML[0])
    for item_xml in XML:
        try:
            name = re.search('market_hash_name=([^<]*)&amp;sort_by=price', item_xml)
            name = name[1].strip()
            price_dep = re.search('attribute="pricecsmoneyw">([^<]*)</span><span', item_xml).group(1).strip()
            price = re.search('attribute="pricecsmoney">([^<]*)</span><span', item_xml).group(1).strip()
            print(name, price, price_dep)
            dict_item = {"name": name, "price": price, "price_dep": price_dep}
            print(dict_item)
            itemsLF.append(dict_item)
        except:
            continue

        print("length items CSm -", len(itemsLF))
    driver.close()
    driver.quit()



    #######################################
    # получаем коллекции и педметы из них #
    #######################################
    st = 'SELECT * FROM minmaxFloats'
    query = mycursor.execute(st)
    itemsBd = mycursor.fetchall()
    print("all items from bd (length)",len(itemsBd))
    print("first one",itemsBd[0])
    query = 0
    st = 'SELECT DISTINCT collection FROM minmaxFloats'
    query = mycursor.execute(st)
    list_col = mycursor.fetchall()
    print("collections from bd (length)", len(list_col), "first one", list_col[0])
    final_list_of_effective_tradeUps = []
    global_index = 0
    for col_in_list in list_col:
        global_index += 1
        if global_index == 100: #test
            break #test
        print("collection", col_in_list)
        mycursor.execute(
            "SELECT * FROM minmaxFloats WHERE collection=%s",
            (col_in_list[0],))
        list_items_col = mycursor.fetchall()
        print("items from one collection (length)", len(list_items_col), "first one", list_items_col[0])
        for item in list_items_col:
            if item[3] == "Covert":
                print("item type is Covert (continue)")
                continue
            exterior_list = []
            exterior_list.append(item[0] + " (Factory New)")
            exterior_list.append(item[0] + " (Minimal Wear)")
            exterior_list.append(item[0] + " (Field-Tested)")
            exterior_list.append(item[0] + " (Well-Worn)")
            exterior_list.append(item[0] + " (Battle-Scarred)")
            print("exterior list", exterior_list)
            #########################################################
            # свеpяем предметы из коллекции с предметами из парсера #
            #########################################################
            for exterior in exterior_list:
                for itemLF in itemsLF:
                    if itemLF["name"] == exterior:
                        #if int(itemLF["have"]) < 2: #не брать предметы, которых нет
                            #break
                        trade_cost = float(itemLF["price"]) * 10
                        print("json of item (lootfarm)", itemLF, "trade cost", trade_cost)
                        outcome_items_list = []
                        if item[3] == "Consumer Grade":
                            outcome_type = "Industrial Grade"
                        if item[3] == "Industrial Grade":
                            outcome_type = "Mil-Spec"
                        if item[3] == "Mil-Spec":
                            outcome_type = "Restricted"
                        if item[3] == "Restricted":
                            outcome_type = "Classified"
                        if item[3] == "Classified":
                            outcome_type = "Covert"
                        #предметы на выходе с контракта
                        for item1 in list_items_col:
                            if item1[3] == outcome_type:
                                outcome_items_list.append(item1)
                        print("previous type is", item[3], ", outcome list is (first length number)",len(outcome_items_list), outcome_items_list)
                        outcome_final = []
                        float_range = []


                        #задаем флоат предмета и меняем, если он нестандартный
                        if re.search(r'\b(Factory New)\b', itemLF["name"]):
                            min = 0
                            print("min float -", float(item[1]))
                            if 0 < float(item[1]) < 0.07:
                                print('name', itemLF["name"], ", not default float value of the item",", item from bd", item)
                                min = float(item[1])
                            max = 0.07
                            print("max float -", float(item[2]))
                            if 0 < float(item[2]) < 0.07:
                                print('name', itemLF["name"], ", not default float value of the item", ", item from bd", item)
                                max = float(item[2])
                            float_range.append(min)
                            float_range.append(max)
                            print("float range -", float_range)

                        if re.search(r'\b(Minimal Wear)\b', itemLF["name"]):
                            min = 0.07
                            print("min float -", float(item[1]))
                            if 0.07 < float(item[1]) < 0.15:
                                print('name', itemLF["name"], ", not default float value of the item",", item from bd", item)
                                min = float(item[1])
                            max = 0.15
                            print("max float -", float(item[2]))
                            if 0.07 < float(item[2]) < 0.15:
                                print('name', itemLF["name"], ", not default float value of the item", ", item from bd", item)
                                max = float(item[2])
                            float_range.append(min)
                            float_range.append(max)
                            print("float range -", float_range)

                        if re.search(r'\b(Field-Tested)\b', itemLF["name"]):
                            min = 0.15
                            print("min float -", float(item[1]))
                            if 0.15 < float(item[1]) < 0.38:
                                print('name', itemLF["name"], ", not default float value of the item",", item from bd", item)
                                min = float(item[1])
                            max = 0.38
                            print("max float -", float(item[2]))
                            if 0.15 < float(item[2]) < 0.38:
                                print('name', itemLF["name"], ", not default float value of the item", ", item from bd", item)
                                max = float(item[2])
                            float_range.append(min)
                            float_range.append(max)
                            print("float range -", float_range)

                        if re.search(r'\b(Battle-Scarred)\b', itemLF["name"]):
                            min = 0.38
                            print("min float -", float(item[1]))
                            if 0.38 < float(item[1]) < 0.45:
                                print('name', itemLF["name"], ", not default float value of the item",", item from bd", item)
                                min = float(item[1])
                            max = 0.45
                            print("max float -", float(item[2]))
                            if 0.38 < float(item[2]) < 0.45:
                                print('name', itemLF["name"], ", not default float value of the item", ", item from bd", item)
                                max = float(item[2])
                            float_range.append(min)
                            float_range.append(max)
                            print("float range -", float_range)

                        if re.search(r'\b(Well-Worn)\b', itemLF["name"]):
                            min = 0.45
                            print("min float -", float(item[1]))
                            if 0.45 < float(item[1]) < 1:
                                print('name', itemLF["name"], ", not default float value of the item",", item from bd", item)
                                min = float(item[1])
                            max = 1
                            print("max float -", float(item[2]))
                            if 0.45 < float(item[2]) < 1:
                                print('name', itemLF["name"], ", not default float value of the item", ", item from bd", item)
                                max = float(item[2])
                            float_range.append(min)
                            float_range.append(max)
                            print("float range -", float_range)


                        #поиск и подсчет стоимости контракта
                        avg_float = float_range[0]
                        effective_trades = []
                        first = 1
                        while avg_float < float_range[1]:
                            avg_float += 0.005
                            if avg_float > float_range[1]:
                                break
                            outcomes_calculated = []
                            for outcome_item in outcome_items_list:
                                min_float = float(outcome_item[1])
                                max_float = float(outcome_item[2])
                                #print("min-max floats", min_float, max_float)
                                outcome_float = avg_float * (max_float - min_float) + min_float
                                outcome_name = outcome_item[0]
                                if 0 < outcome_float < 0.07:
                                    outcome_exterior = "(Factory New)"
                                if 0.07 < outcome_float < 0.15:
                                    outcome_exterior = "(Minimal Wear)"
                                if 0.15 < outcome_float < 0.38:
                                    outcome_exterior = "(Field-Tested)"
                                if 0.38 < outcome_float < 0.45:
                                    outcome_exterior = "(Well-Worn)"
                                if 0.45 < outcome_float < 1:
                                    outcome_exterior = "(Battle-Scarred)"
                                full_outcome_name = outcome_name + " " + outcome_exterior
                                #print("name of used item", exterior, "avg float -", avg_float, "outcome name",full_outcome_name, "float outcome", outcome_float)
                                outcome_stop = 1
                                for item2LF in itemsLF:
                                    if item2LF["name"] == full_outcome_name:
                                        outcome_price = float(item2LF["price_dep"])
                                        outcome_stop = 0
                                        break
                                if outcome_stop == 1:
                                    break
                                one_outcome = {"trade_efficiency": None, "parent": item[0],"trade_cost": trade_cost,"number_of_sales": "0", "avg_float_parent": avg_float, "name": full_outcome_name, "price": outcome_price, "float": outcome_float, "exterior": outcome_exterior}
                                outcomes_calculated.append(one_outcome)


                            #отсекаем ненужные
                            if len(outcome_items_list) == len(outcomes_calculated) and len(outcomes_calculated) != 0 and trade_cost != 0:

                                avg_profit_price = 0
                                for outcome1 in outcomes_calculated:
                                    avg_profit_price += outcome1["price"]
                                trade_efficiency = avg_profit_price / len(outcomes_calculated) / trade_cost - 1
                                #print("trade_efficiency", trade_efficiency)
                                for one_element in outcomes_calculated:
                                    one_element["trade_efficiency"] = trade_efficiency

                                if first == 1:
                                    print(first)
                                    reflected_outcome_list = outcomes_calculated
                                    effective_trades.append(outcomes_calculated)
                                    print(effective_trades)
                                    first = 0


                                #если уже есть, то удаляем
                                if first != 1:
                                    to_add = 0
                                    ind = -1
                                    for element in outcomes_calculated:
                                        ind += 1
                                        if element["name"] == reflected_outcome_list[ind]["name"] and element["exterior"] == reflected_outcome_list[ind]["exterior"]:
                                            to_add += 1
                                    if to_add != len(outcomes_calculated):
                                        effective_trades.append(outcomes_calculated)
                                        reflected_outcome_list = outcomes_calculated
                                    if to_add == len(outcomes_calculated):
                                        for eff_trade in effective_trades:
                                            del effective_trades[-1]
                                            effective_trades.append(outcomes_calculated)
                                            print(effective_trades)


                                print("length",len(effective_trades))
                        final_list_of_effective_tradeUps.append(effective_trades)

                print("length final_list", len(final_list_of_effective_tradeUps))
                if len(final_list_of_effective_tradeUps) > 0:
                    print(final_list_of_effective_tradeUps[-1])



    print("lengt!!!!!!!! ---", len(final_list_of_effective_tradeUps))
    print(final_list_of_effective_tradeUps[1])
    print("lengt!!!!!!!! ---", len(final_list_of_effective_tradeUps))
    #сотируем
    if len(final_list_of_effective_tradeUps) > 10:
        # sort
        unsorted = []
        sorted = []
        x = -100
        for elem1 in final_list_of_effective_tradeUps:
            for elem2 in elem1:
                unsorted.append(elem2)
        print("unsorted length -", len(unsorted))
        for e1 in unsorted:
            y = 1
            for e2 in unsorted:
                if y == 1:
                    y = 0
                    eff = e2[0]["trade_efficiency"]
                if e2[0]["trade_efficiency"] > eff:
                    stop = 0
                    for sort1 in sorted:
                        if sort1[0]["trade_efficiency"] == e2[0]["trade_efficiency"]:
                            stop = 1
                    if stop == 1:
                        continue
                    eff = e2[0]["trade_efficiency"]
                    list_edd = e2
            sorted.append(list_edd)

        unrisk = []
        print("sorted length -", len(sorted))
        # print("1st sorted -", sorted[0])
        # print("2 prices", sorted[0][0]["trade_cost"], sorted[0][0]["price"])
        # получаем предметы без риска
        for item in sorted:
            dont_add = 0
            for item2 in item:
                if float(item2["trade_cost"]) > float(item2["price"]):
                    dont_add = 1
            if dont_add == 0:
                unrisk.append(item)
        print(unrisk)


        #получаем кол-во подаж
        response = requests.get("https://api.steamapis.com/market/items/730?api_key=LZ13AgadysjFkJ7W3NyFTbJGlNM")
        for item in response.json()["data"]:
            name_steam_api = item["market_name"]
            for elem in unrisk:
                if elem["parent"] == name_steam_api:
                    elem["number_of_sales"] = item["prices"]["sold"]["last_7d"]
            for elem2 in sorted:
                if elem["parent"] == name_steam_api:
                    elem["number_of_sales"] = item["prices"]["sold"]["last_7d"]


        with open('resultsCSmRiskOff.txt', 'w', encoding='utf-8') as f:
            for one_line_ris in unrisk:
                f.write("%s\n" % one_line_ris)

        print("sorted length -", len(sorted))

        with open('resultsCSm.txt', 'w', encoding='utf-8') as f:
            for one_line in sorted:
                f.write("%s\n" % one_line)

        with open('resultsCSmUNSORTED.txt', 'w', encoding='utf-8') as f:
            for one_line in unsorted:
                f.write("%s\n" % one_line)




except Exception as e:
    print("done")
    #telegram_bot_sendtext("SteamOrderPrices: Возникла ошибка, нужно выяснять")
    succsess = 0
    #logger.exception(e) # Will send the errors to the file
    PrintException()
    mycursor.close()
    mydb.close()

if succsess == 1:
    print("Successful")
    mycursor.close()
    mydb.close()
