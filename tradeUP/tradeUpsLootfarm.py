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
import pandas as pd

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


    def PrintException():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))




    # получаем кол-во подаж
    response_steam_api = requests.get("https://api.steamapis.com/market/items/730?api_key=LZ13AgadysjFkJ7W3NyFTbJGlNM")

    #предметы с lootfarm
    response = requests.get('https://loot.farm/fullprice.json')
    itemsLF = json.loads(response.text)
    response = 0
    print("all items from lootfarm (length)", len(itemsLF))
    print("first one", itemsLF[0])

    final_tradeups = []

    #все коллекции
    st = 'SELECT DISTINCT collection FROM minmaxFloats'
    query = mycursor.execute(st)
    list_col = mycursor.fetchall()
    print("collections from bd (length)", len(list_col), "first one", list_col[0])
    final_list_of_effective_tradeUps = []
    global_index = 0
    #проходим по всем коллекциям
    for col_in_list in list_col:
        global_index += 1
        if global_index == 100:
            break #test
        print("collection", col_in_list)
        #получаем все предметы коллекции
        mycursor.execute(
            "SELECT * FROM minmaxFloats WHERE collection=%s",
            (col_in_list[0],))
        list_items_col = mycursor.fetchall()
        print("items from one collection (length)", len(list_items_col), "first one", list_items_col[0])
        #проходим по всем предметам коллекции
        for item in list_items_col:
            if item[3] == "Covert": #если качество наивысшее, то оно ни во что не грейдится
                print("item type is Covert (continue)")
                continue
            #указываем все возможеые качества для предмета
            exterior_list = []
            exterior_list.append(item[0] + " (Factory New)")
            exterior_list.append(item[0] + " (Minimal Wear)")
            exterior_list.append(item[0] + " (Field-Tested)")
            exterior_list.append(item[0] + " (Well-Worn)")
            exterior_list.append(item[0] + " (Battle-Scarred)")
            print("exterior list", exterior_list)
            #проходим по выбранному предмету
            for exterior in exterior_list:
                #ищем совпадения на площадке
                for itemLF in itemsLF:
                    if itemLF["name"] == exterior:
                        #if int(itemLF["have"]) < 0: #не брать предметы, которых нет
                            #break
                        # на лутфарм цены не в дролларах, для перевода делим на сто и умножаем на 10 (кол-во в контракте)
                        trade_cost = float(itemLF["price"] / 100 * 10)
                        print("json of item (lootfarm)", itemLF, "trade cost", trade_cost)
                        #узнаем, какие предметы по качеству могут получиться
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
                        #добавляем все предметы, которые могут получится в нашем контракте
                        for item1 in list_items_col:
                            if item1[3] == outcome_type:
                                outcome_items_list.append(item1)
                        print("previous type is", item[3], ", outcome list is (first length number)",len(outcome_items_list), outcome_items_list)
                        outcome_final = []
                        float_range = []

                        #получаем float-range для нашего предмета (бывает разный)
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

                        for item_api in response_steam_api.json()["data"]:
                            if item_api["market_name"] == itemLF["name"]:
                                outcome_have = item_api["prices"]["sold"]["last_7d"]
                                break
                        # most important part (find items from contract)
                        avg_float = float_range[0]
                        effective_trades = []
                        first = 1
                        #задаем порог проверки
                        while avg_float < float_range[1]:
                            avg_float += 0.005
                            #если превысили порог, то выходим
                            if avg_float > float_range[1]:
                                break
                            outcomes_calculated = []
                            #список предметов, которые получаются на выходе
                            for outcome_item in outcome_items_list:
                                min_float = float(outcome_item[1])
                                max_float = float(outcome_item[2])
                                #print("min-max floats", min_float, max_float)
                                #считаем итоговый float предмета
                                outcome_float = avg_float * (max_float - min_float) + min_float
                                outcome_name = outcome_item[0]
                                #получаем качество предмета на выходе
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
                                        outcome_price = float(item2LF["price"]) / 100 * 0.95
                                        outcome_stop = 0
                                        break
                                #если не нашли предмет в списке
                                if outcome_stop == 1:
                                    break
                                #2знака после запятой
                                trade_cost = float('{:.3f}'.format(trade_cost))
                                avg_float = float('{:.3f}'.format(avg_float))
                                outcome_price = float('{:.3f}'.format(outcome_price))
                                outcome_float = float('{:.3f}'.format(outcome_float))
                                #add all to dict
                                one_outcome = {"trade_efficiency": None, "parent": itemLF["name"],"outcome_have": outcome_have, "trade_cost": trade_cost, "avg_float_parent": avg_float, "name": outcome_name, "exterior": outcome_exterior,
                                               "price": outcome_price, "float": outcome_float}
                                outcomes_calculated.append(one_outcome)



                            #подсчитываем эффективность контракта
                            if len(outcome_items_list) == len(outcomes_calculated) and len(outcomes_calculated) != 0 and trade_cost != 0:
                                avg_profit_price = 0
                                for outcome1 in outcomes_calculated:
                                    avg_profit_price += outcome1["price"]
                                avg_profit_price = float('{:.3f}'.format(avg_profit_price))
                                trade_efficiency = avg_profit_price / len(outcomes_calculated) / trade_cost - 1
                                trade_efficiency = float('{:.3f}'.format(trade_efficiency))
                                print("trade_efficiency", trade_efficiency)
                                for one_element in outcomes_calculated:
                                    one_element["trade_efficiency"] = trade_efficiency

                                tradUp = {"trade_efficiency": outcomes_calculated[0]["trade_efficiency"],"outcome_have": outcomes_calculated[0]["outcome_have"], "parent": outcomes_calculated[0]["parent"], "trade_cost": outcomes_calculated[0]["trade_cost"], "avg_float_parent": outcomes_calculated[0]["avg_float_parent"], "avg_profit_price": avg_profit_price}
                                print(tradUp)
                                #input("test")

                                if len(final_tradeups) == 0:
                                    print("++++++++++++")
                                    final_tradeups.append(tradUp)

                                index_tradeups = -1
                                #проверяем, нет ли такого же трейдапа в списке, есле есть, то удаляем его и добавляем новый, так как у новог осредний флоат выше. Если нет такого, то добавляем
                                for tradeup_in_list in final_tradeups:
                                    index_tradeups += 1
                                    if tradeup_in_list["parent"] == tradUp["parent"] and tradeup_in_list["avg_profit_price"] == tradUp["avg_profit_price"]:
                                        print("del")
                                        del final_tradeups[index_tradeups]
                                        final_tradeups.append(tradUp)
                                        break
                                    if len(final_tradeups) - 1 == index_tradeups:
                                        print("add!")
                                        final_tradeups.append(tradUp)
                                print("length tradeUps -", len(final_tradeups))
                #input("test") #break  # test
            #break  # test
        #break  # test

    print("final_tradeups -", final_tradeups)
    with open('resultPandas.txt', 'w', encoding='utf-8') as f:
        first_row = "trade_efficiency" + ">" + "parent" + ">" + "outcome_have" + ">" + "trade_cost" + ">" + "avg_float_parent" + ">" + "avg_profit_price"
        f.write("%s\n" % first_row)
        print(first_row)
        index = 0
        for one_line_ris in final_tradeups:
            index += 1
            string = str(one_line_ris["trade_efficiency"]) + ">" + str(one_line_ris["parent"]) + ">" + str(one_line_ris["outcome_have"]) + ">" + str(one_line_ris["trade_cost"]) + ">" + str(one_line_ris["avg_float_parent"]) + ">" + str(one_line_ris["avg_profit_price"])
            f.write("%s\n" % string)

    #sort and save to csv file
    df = pd.read_csv('resultPandas.txt', delimiter='>')
    print(df.columns)
    df = df.sort_values('trade_efficiency', ascending=False)
    df.to_csv('sorted.csv', sep='\t')

except Exception as e:
    #telegram_bot_sendtext("SteamOrderPrices: Возникла ошибка, нужно выяснять")
    #logger.exception(e) # Will send the errors to the file
    PrintException()
    mycursor.close()
    mydb.close()
    #driver.close()
    #driver.quit()


print("Successful")
mycursor.close()
mydb.close()
#driver.close()
#driver.quit()
