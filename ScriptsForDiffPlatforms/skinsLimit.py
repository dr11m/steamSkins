import requests
import mysql.connector
import MySQLdb
import math
import time
import sys
import os
import linecache
import datetime



succsess = 1 #to properly end the script
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))






try:
    a = datetime.datetime.now()

    now = time.strftime('%Y-%m-%d %H:%M:%S')
    my_data = []

    # get items into a list
    response = requests.get("https://api.steamapis.com/market/items/730?api_key=LZ13AgadysjFkJ7W3NyFTbJGlNM")
    index = 0

    # получаю предметы, которые на продаже, далее вычитаю их из общего count
    mycursor.execute("SELECT name FROM `skins` WHERE `sold_id` IS null")
    list_from_BD = mycursor.fetchall()


    if len(response.json()["data"]) == 0:
        raise ValueError('bad api response')

    print("all items length -", len(response.json()["data"]))
    for item in response.json()["data"]:
        if float(item["prices"]["sold"]["last_24h"]) < 30:
            continue
        count = math.floor(item["prices"]["sold"]["last_24h"] / 10)
        if count > 0:
            name = item["market_name"]
            price = float(item["prices"]["safe"])
            if price < 0.25:
                continue
            how_many_in_list = 0
            for item_BD in list_from_BD:
                if item_BD[0] == name:
                    how_many_in_list += 1
            if how_many_in_list != 0:
                count = count - how_many_in_list
                #print("subtracted number -", how_many_in_list)
                #print("new count -", count)
            if count > 0:
                tuple_for_request = (name, count, price,  now)
                my_data.append(tuple_for_request)

    print("list to add length -", len(my_data))

    # insert items into DB
    # delete items in table
    mycursor.execute("DELETE FROM skinsLimit")
    mydb.commit()
    # insert list
    cursor = db.cursor()
    query = 'INSERT INTO skinsLimit (name,count,price,date_updated) VALUES(%s, %s, %s, %s)'
    cursor.executemany(query, my_data)
    db.commit()



except Exception as e:
    telegram_bot_sendtext("skinsLimit: Возникла ошибка, нужно выяснять")
    PrintException()
    mycursor.close()
    mydb.close()
    sys.exit()



cursor.close()
mycursor.close()
mydb.close()
sys.exit()
