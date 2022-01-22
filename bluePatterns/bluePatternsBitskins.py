import cv2
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging
import requests
import sys
import linecache
import cv2
import numpy as np
import urllib.request

# обработка ошибок
def PrintException():
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
    # screen
    now = time.strftime('%Y_%m-%d_%H_%M_%S')
    driver.save_screenshot('screens\Error' + '-' + str(now) + '.png')
    # close all
    #mycursor.close()
    #mydb.close()
    # display.stop() #linux
    driver.close()
    driver.quit()
    sys.exit()

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()

try:

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
        "user-data-dir=C:\\Users\\Dr1m\\AppData\\Local\\Google\\Chrome\\User Data\\Default11")  # windows

    #chrome_options.add_extension('extension.crx')

    #chrome_options.add_argument('--headless') #test
    #chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary. #test

    chrome_options.add_argument('--window-size=1600,900') #windows

    # driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options) # linux
    driver = webdriver.Chrome(executable_path='C:\\Users\\Dr1m\\Desktop\\skinsautomation\\chromedriver.exe',
                              chrome_options=chrome_options)  # windows



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


    # NoteBook
    # driver = webdriver.Chrome(options=chromeOptions, executable_path=r'C:\\Users\\Администратор\\Desktop\\pywinautomation\\chromedriver.exe')
    # chromeOptions.add_argument("user-data-dir=C:\\Users\\Администратор\\AppData\\Local\\Google\\Chrome\\User Data\\Default")

    wait = WebDriverWait(driver, 25)  # время вылета 10сек

    # loging errors
    # Create a logging instance
    logger = logging.getLogger('csMoneyBuy_errors')
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
    logger_msg = logging.getLogger('csMoneyBuy_info')
    logger_msg.setLevel(logging.INFO)  # you can set this to be DEBUG, INFO, ERROR
    # Assign a file-handler to that instance
    fh1 = logging.FileHandler("debug.txt")
    fh1.setLevel(logging.INFO)
    # Format your logs (optional)
    formatter = logging.Formatter('%(asctime)s - row:%(lineno)d - %(message)s')
    fh1.setFormatter(formatter)  # This will set the format to the file handler
    # Add the handler to your logging instance
    logger_msg.addHandler(fh1)

    # # preparation CODE

    # ## check if I'm logged into steam

    # In[2]:

except Exception as e:
    telegram_bot_sendtext("csMoneyBuy: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()



try:
    # создаём вторую вкладку и получаем минимальную цену для предмета
    driver.execute_script('''window.open('',"_blank");''')  # создаем новую вкладку
    driver.switch_to.window(driver.window_handles[0])
    inspected_already_links = []
    items_links = ["https://bitskins.com/?market_hash_name=Five-SeveN+%7C+Case+Hardened+%28Field-Tested%29&advanced=1&appid=730&is_stattrak=0&has_stickers=0&is_souvenir=0&show_trade_delayed_items=0&sort_by=price&order=asc",
                   "https://bitskins.com/?market_hash_name=Five-SeveN+%7C+Case+Hardened+%28Factory+New%29&advanced=1&appid=730&is_stattrak=0&has_stickers=0&is_souvenir=0&show_trade_delayed_items=0&sort_by=price&order=asc",
                   "https://steamcommunity.com/market/listings/730/Five-SeveN%20%7C%20Case%20Hardened%20%28Minimal%20Wear%29"
                   ]

    #load items
    for item_link in items_links:
        driver.get("https://www.google.com/")
        driver.get(item_link)
        time.sleep(10)
        try:
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div:nth-child(9) > div > div:nth-child(3) > div > div > div:nth-child(1) > div > div.item-icon.lazy > p:nth-child(4) > a:nth-child(3)")))
        except:
            msg = "cant load first item"
            logger.exception(msg)
            raise ValueError("cant load first item")
        #get inspects links
        for index in range(10):
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.2)
            index += 1
            inspects_link = driver.find_element_by_css_selector(
                "body > div:nth-child(9) > div > div:nth-child(3) > div > div > div:nth-child("+str(index)+") > div > div.item-icon.lazy > p:nth-child(4) > a:nth-child(3)").get_attribute('href')
            #go to broskins to get an image from csmoney
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(0.2)
            driver.get("https://broskins.com/index.php?pages/csgo-skin-screenshot/")
            try:
                element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "#inspect")))
            except:
                msg = "cant load broskins"
                logger.exception(msg)
                raise ValueError("cant load broskins")
            time.sleep(0.5)
            #insert link to item
            input_field = driver.find_element_by_css_selector('#inspect')
            input_field.clear()
            print(inspects_link)
            input_field.send_keys(inspects_link)
            driver.find_element_by_css_selector("#sendbtn").click()
            time.sleep(1.5)
            driver.find_element_by_css_selector("#sendbtn").click()
            time.sleep(0.2)
            driver.find_element_by_css_selector("#sendbtn").click()
            time.sleep(10)
            did_upload_correct = driver.find_elements_by_css_selector("div#dialog > div:nth-child(1)  > li:nth-child(n)")
            if len(did_upload_correct) == 9:
                try:
                    image_csmoney = driver.find_element_by_css_selector("div#dialog > div:nth-child(3)  > li:nth-child(3) > a").get_attribute('href')
                    print(image_csmoney)
                except:
                    print("cant get an image link (continue)")
                    continue
                # link to an image
                req = opener.open(image_csmoney)
                try:
                    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                except:
                    print("cant load an image")
                    continue
                resim = cv2.imdecode(arr, -1)  # 'Load it as it is'

                # resim = cv2.imread("b2.jpg") #local

                # cv2.imshow("n1.jpg", resim) #show

                Area_top = resim[186:330, 144:1740]
                Area_bottom = resim[1550:1714, 270:1796]

                # cv2.imwrite('savedImage.jpg', Area) #to save
                # cv2.imwrite('savedImage.jpg', Area) #to save

                hsv_top = cv2.cvtColor(Area_top, cv2.COLOR_BGR2HSV)
                hsv_bottom = cv2.cvtColor(Area_bottom, cv2.COLOR_BGR2HSV)

                lower_blue = np.array([70, 34, 60])
                upper_blue = np.array([141, 147, 254])

                mask_top = cv2.inRange(hsv_top, lower_blue, upper_blue)
                mask_bottom = cv2.inRange(hsv_bottom, lower_blue, upper_blue)
                res_top = cv2.bitwise_and(Area_top, Area_top, mask=mask_top)
                res_bottom = cv2.bitwise_and(Area_bottom, Area_bottom, mask=mask_bottom)

                # cv2.imshow('frame', Area_top)
                # cv2.imshow('mask', mask)
                # cv2.imshow('res_top', res_top)
                # cv2.imshow('res_bottom', res_bottom)

                percentage_top = res_top.mean()
                percentage_bottom = res_bottom.mean()
                time.sleep(5)

                print("percentages: ", percentage_top, percentage_bottom, type(percentage_top))
                if int(percentage_top) > 30 and int(percentage_bottom) > 30:
                    print("gotcha!")
                    telegram_bot_sendtext("patternsBlue: индекс предмета - " + str(index) + "нашел предмет - " + str(item_link))


                #get percentages

except Exception as e:
    telegram_bot_sendtext("bluePatterns: Возникла ошибка, нужно выяснять")
    logger.exception(e)  # Will send the errors to the file
    PrintException()
