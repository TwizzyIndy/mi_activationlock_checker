#Author : TwizzyIndy
#Date   : 2018/7

# Install the Python Requests library:
# `pip install requests` or `easy_install requests`

import requests
import os
import json
import datetime
import time

def send_request(strImei):
    # Request
    # GET https://i.mi.com/support/anonymous/status

    try:
        response = requests.get(
            url="https://i.mi.com/support/anonymous/status",
            params={
                "id": strImei,
                "ts": int(time.time()*1000) # timestamp added
            },
        )
        
        jsReply = json.loads(response.content)
        
        if jsReply["result"] == "ok":
            
            if not 'data' in jsReply:
                print("unexpected values found!\n")
                return
            
            data = jsReply["data"]
            
            # is locked or not

            isLocked = data["locked"]
            strLockStatus = ("ON" if isLocked is True else "OFF")
            
            # get email and phone

            phone = "-"
            email = "-"
            
            if 'email' in data:
                email = data["email"]
            
            if 'phone' in data:
                phone = data["phone"]
            
            # lost mode or not
            isLostMode = data["lost"]
            strLostModeStatus = ("LOST" if isLostMode is True else "CLEAN")

            
            log = open('log.txt', 'a')
            curTime = datetime.datetime.now().strftime("%B %d, %Y of %I:%M%p")
            
            txt = "\n" + curTime + " : " + strImei + "\nPhone : " + phone + "\nEmail : " + email + "\nActivationLockStatus : " + strLockStatus + "\nIMEI STATUS : " + strLostModeStatus + "\n"

            log.write(txt)
            log.close()
            
            print(txt)
            
        elif jsReply["result"] == "error":
            
            print("There was an error occuri in server")
            return
        
        
    except requests.exceptions.RequestException:
        print('\nConnect fail due to some network error ..')
        

def usage():
    print("\nXiaomi Activation Lock Checker ")
    print("by TwizzyIndy")
    print("2018/7")
    print("\nusage: python mi_activationlock_check.py {IMEI}")
    print("note: IMEI need to be at least 15 digit\n")
    
def main():
    
    if len(os.sys.argv) < 2:
        usage()
        return
    elif len(os.sys.argv[1]) < 15:
        usage()
        
    send_request( os.sys.argv[1] )
    
if __name__ == "__main__":
    main()
