import pickle
import os
import RPi.GPIO as GPIO
from hx711 import HX711

from utils.google_api import Gsheet, GoogleApi
from utils.sg_motor import SG_Motor
import settings
import time

GPIO.cleanup()
BOWL_WEIGHT=98 # bowl weight
FULL_CAT_FOOD=165
LIMITED_CAT_FOOD = BOWL_WEIGHT + 5
DOUT_PIN=24
PD_SCK_PIN=23
SWAP_FILE_PATH='./utils/swap_file.swp'

def scale_swp():
    if os.path.isfile(SWAP_FILE_PATH):
        with open(SWAP_FILE_PATH, 'rb')as swap_file:
            return pickle.load(swap_file)


def main():
    # Step 1. Keep calculate weight
    GPIO.setmode(GPIO.BCM)
    hx = HX711(dout_pin=DOUT_PIN, pd_sck_pin=PD_SCK_PIN)
    hx = scale_swp()
    sg=SG_Motor()
    gs=Gsheet(settings.GOOGLE_SHEET_KEY)
    gs.create_connection()
    # get the init weight
    NOW_WEIGHT= hx.get_weight_mean(20)
    while NOW_WEIGHT:
        counter1=""
        counter2=""
        NOW_WEIGHT = hx.get_weight_mean(20)
        print("NOW_WEIGHT while loop",NOW_WEIGHT)
        if NOW_WEIGHT <= LIMITED_CAT_FOOD:
            counter1=NOW_WEIGHT
            print("get signal turn the sg motor")
            #sg=SG_Motor()
            sg.start()
            time.sleep(2)
            while True:
                print(f"Enter while true loop {NOW_WEIGHT} g")
                NOW_WEIGHT = hx.get_weight_mean(20)
                if NOW_WEIGHT >= FULL_CAT_FOOD-5:
                    counter2=NOW_WEIGHT 
                    print("ENough food", NOW_WEIGHT,"g")
                    
                    sg.stop()
                    GPIO.setmode(GPIO.BCM)
                    hx = HX711(dout_pin=DOUT_PIN, pd_sck_pin=PD_SCK_PIN)
                    hx = scale_swp()
                    
                    ADDED_WEIGHT=counter2 - counter1
                    data=GoogleApi(ADDED_WEIGHT).to_list()
                    gs.insert_rows([data])                    
                    break
        
                




    # Step 2. if below the limit start SG90
    #sg=SG_Motor()   
    #sg.start()    

    #add_cat_food(NOW_WEIGHT)


    #sg.stop()
    # Step 3. if start SG90 call google API send log to sheet
    #ADDED_WEIGHT=FULL_CAT_FOOD-NOW_WEIGHT

    #data = GoogleApi(ADDED_WEIGHT).to_list()
    #gs = Gsheet(settings.GOOGLE_SHEET_KEY)
    #gs.create_connection()
    #gs.insert_rows([data])

if __name__=="__main__":
    main()
    GPIO.cleanup()
