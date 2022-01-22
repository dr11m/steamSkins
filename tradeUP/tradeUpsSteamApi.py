import os
import random
import time
import linecache
import sys
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


# loging info (debug mode)
# Create a logging instance
logger_msg = logging.getLogger('TradeUp_info')
logger_msg.setLevel(logging.INFO)  # you can set this to be DEBUG, INFO, ERROR
# Assign a file-handler to that instance
fh1 = logging.FileHandler("debug.txt")
fh1.setLevel(logging.INFO)
# Format your logs (optional)
formatter = logging.Formatter('%(asctime)s - row:%(lineno)d - %(message)s')
fh1.setFormatter(formatter)  # This will set the format to the file handler
# Add the handler to your logging instance
logger_msg.addHandler(fh1)

logger_msg.info("--------------------------------")  # debug

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





    #предметы со стима
    response = requests.get('https://api.steamapis.com/market/items/730?api_key=API_KEY')
    itemsLF = response.json()["data"]
    print(itemsLF[0]["market_name"])
    print(itemsLF[0]["prices"]["sold"]["last_7d"])
    response = 0
    print("stean items length -", len(itemsLF))

    final_tradeups = []

    #все коллекции
    st = 'SELECT DISTINCT collection FROM minmaxFloats'
    query = mycursor.execute(st)
    list_col = mycursor.fetchall()
    print("collections from bd (length)", len(list_col), "first one", list_col[0])
    final_list_of_effective_tradeUps = []
    #global_index = 0
    #проходим по всем коллекциям
    for col_in_list in list_col:
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

            #stattrack
            exterior_list.append("StatTrak™ " + item[0] + " (Factory New)")
            exterior_list.append("StatTrak™ " + item[0] + " (Minimal Wear)")
            exterior_list.append("StatTrak™ " + item[0] + " (Field-Tested)")
            exterior_list.append("StatTrak™ " + item[0] + " (Well-Worn)")
            exterior_list.append("StatTrak™ " + item[0] + " (Battle-Scarred)")
            print("exterior list", exterior_list)
            #проходим по выбранному предмету
            for exterior in exterior_list:
                #ищем совпадения на площадке
                for itemLF in itemsLF:
                    if itemLF["market_name"] == exterior:
                        #if int(itemLF["have"]) < 0: #не брать предметы, которых нет
                            #break
                        # на лутфарм цены не в дролларах, для перевода делим на сто и умножаем на 10 (кол-во в контракте)
                        if itemLF["prices"]["safe"] == "0":
                            print("------------------------ price = 0 (break)")
                            break
                        trade_cost = float(itemLF["prices"]["safe"] * 10)
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
                        if re.search(r'\b(Factory New)\b', itemLF["market_name"]):
                            min = 0
                            print("min float -", float(item[1]))
                            if 0 < float(item[1]) < 0.07:
                                print('name', itemLF["market_name"], ", not default float value of the item",", item from bd", item)
                                min = float(item[1])
                            max = 0.07
                            print("max float -", float(item[2]))
                            if 0 < float(item[2]) < 0.07:
                                print('name', itemLF["market_name"], ", not default float value of the item", ", item from bd", item)
                                max = float(item[2])
                            float_range.append(min)
                            float_range.append(max)
                            print("float range -", float_range)

                        if re.search(r'\b(Minimal Wear)\b', itemLF["market_name"]):
                            min = 0.07
                            print("min float -", float(item[1]))
                            if 0.07 < float(item[1]) < 0.15:
                                print('name', itemLF["market_name"], ", not default float value of the item",", item from bd", item)
                                min = float(item[1])
                            max = 0.15
                            print("max float -", float(item[2]))
                            if 0.07 < float(item[2]) < 0.15:
                                print('name', itemLF["market_name"], ", not default float value of the item", ", item from bd", item)
                                max = float(item[2])
                            float_range.append(min)
                            float_range.append(max)
                            print("float range -", float_range)

                        if re.search(r'\b(Field-Tested)\b', itemLF["market_name"]):
                            min = 0.15
                            print("min float -", float(item[1]))
                            if 0.15 < float(item[1]) < 0.38:
                                print('name', itemLF["market_name"], ", not default float value of the item",", item from bd", item)
                                min = float(item[1])
                            max = 0.38
                            print("max float -", float(item[2]))
                            if 0.15 < float(item[2]) < 0.38:
                                print('name', itemLF["market_name"], ", not default float value of the item", ", item from bd", item)
                                max = float(item[2])
                            float_range.append(min)
                            float_range.append(max)
                            print("float range -", float_range)

                        if re.search(r'\b(Battle-Scarred)\b', itemLF["market_name"]):
                            min = 0.38
                            print("min float -", float(item[1]))
                            if 0.38 < float(item[1]) < 0.45:
                                print('name', itemLF["market_name"], ", not default float value of the item",", item from bd", item)
                                min = float(item[1])
                            max = 0.45
                            print("max float -", float(item[2]))
                            if 0.38 < float(item[2]) < 0.45:
                                print('name', itemLF["market_name"], ", not default float value of the item", ", item from bd", item)
                                max = float(item[2])
                            float_range.append(min)
                            float_range.append(max)
                            print("float range -", float_range)

                        if re.search(r'\b(Well-Worn)\b', itemLF["market_name"]):
                            min = 0.45
                            print("min float -", float(item[1]))
                            if 0.45 < float(item[1]) < 1:
                                print('name', itemLF["market_name"], ", not default float value of the item",", item from bd", item)
                                min = float(item[1])
                            max = 1
                            print("max float -", float(item[2]))
                            if 0.45 < float(item[2]) < 1:
                                print('name', itemLF["market_name"], ", not default float value of the item", ", item from bd", item)
                                max = float(item[2])
                            float_range.append(min)
                            float_range.append(max)
                            print("float range -", float_range)


                        # most important part (find items from contract)
                        avg_float = float_range[0]
                        effective_trades = []
                        first = 1
                        #задаем порог проверки
                        while avg_float < float_range[1]:
                            avg_float += 0.0051
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
                                if exterior[0:8] == "StatTrak":
                                    full_outcome_name = "StatTrak™ " + full_outcome_name
                                #print("name of used item", exterior, "avg float -", avg_float, "outcome name",full_outcome_name, "float outcome", outcome_float)
                                outcome_stop = 1
                                for item2LF in itemsLF:
                                    if item2LF["market_name"] == full_outcome_name:
                                        if item2LF["prices"]["safe"] == "0":
                                            print("-------------price = 0 (break) (outcome_stop) == 1")
                                            break
                                        outcome_price = float(item2LF["prices"]["safe"])
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

                                #sales count > 700 - предел, всё что выше, не так и важно, но если не поставить это ограничение, то в итоговой сортировке предметы с огромным кол-вом продаж будут сильно подниматься в топе, а с низким наоборот улетят вниз
                                sales = int(itemLF["prices"]["sold"]["last_7d"])
                                if sales > 700:
                                    sales = 700
                                if sales == 0:
                                    sales = 1

                                #add all to dict
                                one_outcome = {"parent": itemLF["market_name"],
                                               "trade_efficiency": None,
                                               "profit": None,
                                               "trade_float_max": float_range[1],
                                               "trade_cost": trade_cost,
                                               "avg_float_parent": avg_float,
                                               "full_outcome_name": full_outcome_name,
                                               "name": outcome_name,
                                               "exterior": outcome_exterior,
                                               "price": outcome_price,
                                               "float": outcome_float,
                                               "sales": sales}
                                outcomes_calculated.append(one_outcome)



                            #подсчитываем эффективность контракта
                            if len(outcome_items_list) == len(outcomes_calculated) and len(outcomes_calculated) != 0 and trade_cost != 0:
                                avg_profit_price = 0
                                prices_string = ""
                                names_outcomes = ""
                                for outcome1 in outcomes_calculated:
                                    avg_profit_price += float(outcome1["price"])
                                    if len(prices_string) == 0:
                                        price_to_add = float(outcome1["price"]) * 0.87
                                        price_to_add = float('{:.3f}'.format(price_to_add))
                                        prices_string = str(price_to_add)
                                        names_outcomes = str(outcome1["full_outcome_name"])
                                        continue
                                    price_to_add = float(outcome1["price"]) * 0.87
                                    price_to_add = float('{:.3f}'.format(price_to_add))
                                    prices_string = str(prices_string) + "," + str(price_to_add)
                                    name_to_add = str(outcome1["full_outcome_name"])
                                    names_outcomes = str(names_outcomes) + "," + name_to_add

                                avg_profit_price = float(avg_profit_price) * 0.87 / len(outcomes_calculated)
                                avg_profit_price = float('{:.3f}'.format(avg_profit_price))
                                profit = avg_profit_price - float(outcomes_calculated[0]["trade_cost"])
                                profit = float('{:.3f}'.format(profit))
                                trade_efficiency = avg_profit_price / trade_cost - 1
                                trade_efficiency = float('{:.3f}'.format(trade_efficiency))
                                print("trade_efficiency", trade_efficiency)
                                for one_element in outcomes_calculated:
                                    one_element["trade_efficiency"] = trade_efficiency
                                    one_element["profit"] = profit

                                tradUp = {"parent": outcomes_calculated[0]["parent"],
                                          "trade_efficiency": outcomes_calculated[0]["trade_efficiency"],
                                          "trade_efficiency_N": 0, #Normalized
                                          "profit": outcomes_calculated[0]["profit"],
                                          "profit_N": 0, #Normalized
                                          "trade_cost": outcomes_calculated[0]["trade_cost"],
                                          "avg_float_parent": outcomes_calculated[0]["avg_float_parent"],
                                          "avg_float_parent_N": outcomes_calculated[0]["trade_float_max"], #Normalized
                                          "outcome_sum": avg_profit_price,
                                          "outcome_prices": prices_string,
                                          "sales": outcomes_calculated[0]["sales"],
                                          "sales_N": 0,
                                          "outcomes_names": names_outcomes,
                                          "weights": 0}

                                print(tradUp)

                                if len(final_tradeups) == 0:
                                    if float(tradUp["trade_efficiency"]) > 0:
                                        final_tradeups.append(tradUp)

                                index_tradeups = -1
                                #проверяем, нет ли такого же трейдапа в списке, есле есть, то удаляем его и добавляем новый, так как у новог осредний флоат выше. Если нет такого, то добавляем
                                for tradeup_in_list in final_tradeups:
                                    index_tradeups += 1
                                    if tradeup_in_list["parent"] == tradUp["parent"] and tradeup_in_list["outcome_sum"] == tradUp["outcome_sum"] and float(tradUp["trade_efficiency"]) > 0:
                                        print("del")
                                        del final_tradeups[index_tradeups]
                                        final_tradeups.append(tradUp)
                                        break
                                    if len(final_tradeups) - 1 == index_tradeups:
                                        print("add!")
                                        if float(tradUp["trade_efficiency"]) > 0:
                                            final_tradeups.append(tradUp)
                                print("length tradeUps -", len(final_tradeups))
                        #break
                #break # test
            #break  # test
        #break  # test

    print("length of final_list", len(final_tradeups))

    #we need to get max numbers of collumns: profit, float (for each), and trade efficiency.
    max_profit = 0.01
    max_trade_eff = 0.01
    for row in final_tradeups:
        if max_profit < float(row["profit"]):
            max_profit = float(row["profit"])
        if max_trade_eff < float(row["trade_efficiency"]):
            max_trade_eff = float(row["trade_efficiency"])
    max_trade_eff = float('{:.3f}'.format(max_trade_eff))
    max_profit = float('{:.3f}'.format(max_profit))
    #print("max numbers:", max_profit, max_trade_eff)
    #need to update list (final_tradeup) with new normalized collumns #now its a test, after success we will normalized selected collumns (_N)
    index_max = -1
    for row in final_tradeups:
        index_max += 1
        final_tradeups[index_max]["profit_N"] = max_profit
        final_tradeups[index_max]["trade_efficiency_N"] = max_trade_eff
    #normalized collumns
    index_N = -1
    for row in final_tradeups:
        index_N += 1
        #float
        avg_float_parent_N = float(row["avg_float_parent"]) / float(row["avg_float_parent_N"])
        avg_float_parent_N = float('{:.2f}'.format(avg_float_parent_N))
        final_tradeups[index_N]["avg_float_parent_N"] = avg_float_parent_N
        #profit
        profit_N = float(row["profit"]) / float(row["profit_N"])
        profit_N = float('{:.4f}'.format(profit_N))
        final_tradeups[index_N]["profit_N"] = profit_N
        #efficiency
        trade_efficiency_N = float(row["trade_efficiency"]) / float(row["trade_efficiency_N"])
        trade_efficiency_N = float('{:.2f}'.format(trade_efficiency_N))
        final_tradeups[index_N]["trade_efficiency_N"] = trade_efficiency_N
        #sales
        sales_N = int(row["sales"]) / 700
        final_tradeups[index_N]["sales_N"] = sales_N



        #weight
        #float_W = float(avg_float_parent_N) * 0.03  # weight of float
        profit_W = float(profit_N) * 1  # weight of profit
        #sales_W = float(sales_N) * 0.02  # weight of profit
        weight = profit_W
        #print("weight", weight)
        final_tradeups[index_N]["weights"] = weight


    #need to make weights for each normalized collumn and then sort by that collumn
    #wights (раздаем вес на каждую срптированную (normalized) колонку
    index_W = -1
    for row in final_tradeups:
        index_N += 1


    #result
    with open('resultPandas.txt', 'w', encoding='utf-8') as f:
        first_row = "parent" + ">" +\
                    "trade_efficiency" + ">" +\
                    "profit" + ">" +\
                    "avg_float_parent" + ">" + \
                    "sales" + ">" + \
                    "trade_cost" + ">" + \
                    "weights" + ">" + \
                    "outcome_sum" + ">" +\
                    "outcome_prices" + ">" +\
                    "outcome_names"
        f.write("%s\n" % first_row)
        #print(first_row)
        index = 0
        for one_line_ris in final_tradeups:
            index += 1
            string = str(one_line_ris["parent"]) + ">" +\
                     str(one_line_ris["trade_efficiency"]) + ">" +\
                     str(one_line_ris["profit"]) + ">" +\
                     str(one_line_ris["avg_float_parent"]) + ">" + \
                     str(one_line_ris["sales"]) + ">" + \
                     str(one_line_ris["trade_cost"]) + ">" + \
                     str(one_line_ris["weights"]) + ">" + \
                     str(one_line_ris["outcome_sum"]) + ">" +\
                     str(one_line_ris["outcome_prices"]) + ">" +\
                     str(one_line_ris["outcomes_names"])
            f.write("%s\n" % string)

    #sorted by efficiency
    df = pd.read_csv('resultPandas.txt', delimiter='>')
    #print(df.columns)
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
