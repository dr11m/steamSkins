import linecache
import sys
import mysql.connector
import requests
import datetime
import time
import logging
import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import re


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

    # close all
    mycursor.close()
    mydb.close()
    # display.stop() #linux
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



    # # preparation CODE

    # ## check if I'm logged into steam

    # In[2]:

except Exception as e:
    telegram_bot_sendtext("csMoneyGetFloats: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()



#get items from mysql
try:
    mycursor.execute("SELECT * FROM `csMoneyFloats`")
    response = mycursor.fetchall()
    print(len(response))
    print(response[4])

    already_checked_names = []
    sorted_list = []

    index = 0
    for item1 in response:
        index += 1
        if index == 1 or index == 2 or index == 3: #эти строчки в таблице csMoneyFloats используются для работы скрипта (в них нет нужной информации))
            continue
        tuple_for_one_item = ()
        count = 0
        data_for_coef_and_intercept = []
        name = item1[0]

        if name in already_checked_names:
            continue
        float_min = float(item1[2])
        float_max = float(item1[2])
        for item2 in response:
            if item2[0] == name:
                floatValue_floatCost_list = []
                floatValue_floatCost_list.append(item2[2])
                floatValue_floatCost_list.append(item2[3])
                data_for_coef_and_intercept.append(floatValue_floatCost_list)
                count += 1
                if float(item2[2]) < float_min:
                    float_min = float(item2[2])
                if  float(item2[2]) > float_max:
                    float_max = float(item2[2])
        if count > 3:
            predict = "float_cost"
            #get coef and interception for prediction price
            data = pd.DataFrame(data_for_coef_and_intercept, columns=['float_value', 'float_cost'])
            data.index.name = 'imdex_collumn'
            data = data.sort_values(by=['float_value'], ascending=True)

            print(len(data))

            predict = "float_cost"
            list_of_ranges = []
            linear = linear_model.LinearRegression()

            list_of_row = []

            z = True

            data_part = data
            # прост опереводив все в систему координат
            x = np.array(data_part.drop([predict], 1))
            y = np.array(data_part[predict])

            for index_global in range(100):
                if z == False:
                    print("exit main loop, z= (must be false)", z)
                    break
                index_start = 0
                # убрать часть из даты, которая лежит в списках информацию, если лист больше одного
                # print("length list of row", len(list_of_row))
                if len(list_of_row) > 0:
                    indexes_to_del = []
                    for element_of_list in list_of_row:
                        for index_del in range(len(element_of_list[0])):
                            indexes_to_del.append(int(element_of_list[0].index[index_del]))

                    data_part = data.drop(indexes_to_del)
                    # print("++ new length", len(data_part),)
                    x = np.array(data_part.drop([predict], 1))
                    y = np.array(data_part[predict])
                    # print("++ new length", len(data_part), len(x), len(y))

                for index in range(len(data_part)):
                    # print("length:", len(data_part[index_start:index]))
                    if len(data_part[index_start:index]) < 2:
                        continue

                    if len(data_part[index_start:index]) == 2:
                        data_part_tmp = data_part[index_start:index]
                        x_1 = np.array(data_part_tmp.drop([predict], 1))
                        y_1 = np.array(data_part_tmp[predict])
                        model = linear.fit(x_1, y_1)

                    # print("length -", len(data_part[0:index]))
                    # print("index -", index)
                    data_part_tmp = data_part[index_start:index + 1]

                    try:
                        # print(index)
                        d = y[[index + 1]] - model.predict(x[[index + 1]])
                        # print('---float_value1', x[[index]])
                        # print("---last item of data_part_tmp", data_part_tmp.iloc[-1])
                        # print('float_value2', x[[index+1]])
                    except IndexError:
                        z = False
                        print("error (end of list)")
                        print("---------------------------------------------------------")
                        row_list = []
                        row_list.append(data_part)
                        row_list.append(index)
                        list_of_row.append(row_list)
                        break

                    print("distance: ", float(d))
                    print(model.coef_, model.intercept_)

                    if float(d) > 0.3 or float(d) < -0.3:
                        float_distance = float(x[[index + 1]]) - float(x[[index]])
                        if float_distance > 0.002 and len(data_part[index_start:index]) == 2:
                            print("splited2")
                            print("---------------------------------------------------------")
                            data_part_tmp = data_part[index_start:index]
                            row_list = []
                            row_list.append(data_part_tmp)
                            row_list.append(index)
                            list_of_row.append(row_list)
                            break
                        print("splited1")
                        print("---------------------------------------------------------")
                        row_list = []
                        row_list.append(data_part_tmp)
                        row_list.append(index)
                        list_of_row.append(row_list)
                        break



            #del all dataframes len=2 (it's a garbage)
            index_del = -1
            for item in list_of_row:
                index_del += 1
                if len(item[0]) < 3:
                    print("del length=2")
                    del list_of_row[index_del]

            # add image_test
            plt.scatter(data.float_value, data.float_cost, color='red', marker='.')

            for index in range(len(list_of_row)):
                x_2 = np.array(list_of_row[index][0].drop([predict], 1))
                y_2 = np.array(list_of_row[index][0][predict])
                model = linear.fit(x_2, y_2)
                plt.plot(x_2.ravel().tolist(), model.predict(x_2).ravel().tolist()) #add .ravel().tolist() cause it didnt work without on local pc

            now = time.strftime('%Y_%m-%d_%H_%M_%S')
            name_to_save = re.sub('[^a-zA-Z]+', '', name)
            plt.savefig('plot_images/' + str(name_to_save) + now + '.png')
            plt.clf()



            #sorting data into string
            ranges_list = []
            ranges_string = ""
            for row in list_of_row:
                min_float = row[0]["float_value"].iloc[0]
                max_float = row[0]["float_value"].iloc[-1]
                x_1 = np.array(row[0].drop([predict], 1))
                y_1 = np.array(row[0][predict])
                model = linear.fit(x_1, y_1)
                coef_list = model.coef_
                coef = coef_list[0]
                intercept = model.intercept_
                row_string = str(min_float) + "," + str(max_float) + "," + str(coef) + "," + str(intercept)
                ranges_list.append(row_string)

            index_range = 0
            for one_range in ranges_list:
                index_range += 1
                if index_range == 1:
                    ranges_string = one_range
                    continue
                ranges_string = ranges_string + "/" + str(one_range)

                print(ranges_string)
            print(len(list_of_row))
            print(len(list_of_row))
            count = 0

            for item in list_of_row:
                print(len(item[0]))
                count += len(item[0])

            print("count", count)

            # ssorting list
            # for item in list_of_row:
            # print(item[0])

            already_checked_names.append(name)
            tuple_for_one_item = (item, count, ranges_string)
            sorted_list.append(tuple_for_one_item)


    #delete all data
    mycursor.execute("DELETE FROM csMoneyFloatRangePredict")


    q = """ insert ignore into csMoneyFloatRangePredict (
            name, count, ranges )
            values (%s,%s,%s)           
        """

    mycursor.executemany(q, sorted_list)
    mydb.commit()


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
sys.exit()
