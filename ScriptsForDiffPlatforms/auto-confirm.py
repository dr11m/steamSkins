import os
import subprocess
import time
import datetime
import requests
import sys
import os
import linecache
import datetime
import mysql.connector

#time start
a1 = datetime.datetime.now()


# обработка ошибок
def PrintException():
    #send an error into DB
    successStatus(False)
    print("was an error")
    # exception output
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

    sys.exit()

try:

    #set status into DB
    def successStatus(success):
        now = datetime.datetime.now()
        if success is False:
            mycursor.execute("UPDATE scriptsStatus SET status = 'error', date = %s WHERE name = 'steam2fa'", (now,))
            mydb.commit()
        else:
            mycursor.execute("UPDATE scriptsStatus SET status = 'success', date = %s WHERE name = 'steam2fa'",(now,))
            mydb.commit()


    count_errors = 0
    x = 1
    while x != 0:
        try:
            os.chdir("/home/work/steamguard-cli")
            output = subprocess.check_output('build/steamguard accept-all', shell=True).decode("utf-8").strip()
            if count_errors == 3:
                print("3 errors in a row")
                raise ValueError('3 errors in a row, stop the script')
        except:
            count_errors += 1
            print("error +1")
            continue
        count_errors = 0
        now = datetime.datetime.now()
        print(str(now), "did it!")
        time.sleep(7)

        #update status every 10 minutes AND check if other scripts running correctly
        delta = now - a1
        print('every 10 minutes send status, difference is seconds -', int(delta.total_seconds()))
        if int(delta.total_seconds()) > 600:
            a1 = datetime.datetime.now()
            successStatus(True)
            #check other scripts status
            mycursor.execute("SELECT * FROM `scriptsStatus`")
            scripts_status_list = mycursor.fetchall()
            now = datetime.datetime.now()
            for script in scripts_status_list:
                if int(script[3]) == 0:
                    print("untracked script, no nedd to check (continue)")
                    continue
                script_time = script[2]
                print(now, script_time)
                time_difference = now - script_time
                time_difference = int(time_difference.total_seconds()) / 60
                print(time_difference)
                #если разница во времени больше заданной или в статусе ошибка
                if time_difference > int(script[4]) or str(script[1]) == "error":
                    print("some script is broken")
                    telegram_bot_sendtext("scriptsStatus: " + str(script[0]) + " не работает, нужно заглянуть в таблицу (scriptsStatus)")



except Exception as e:
    telegram_bot_sendtext("auto-confirm: Возникла ошибка, нужно выяснять")
    PrintException()
