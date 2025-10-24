#!/usr/bin/env python3
import sys
import os
import time
import shutil
import re
from modules import msol, adfs, owa, okta, anyConnect

# Check if TrevorSpray is installed and available in the PATH
def checkTrevor():
    tool = 'Trevorspray'
    if shutil.which(tool):
        print(f"[*] {tool} is installed and available in your PATH.")
    else:
        print(f"[!] {tool} is not installed or not available in your PATH.")
        print("\n[*] Please install Trevor Spray before running this script.")
        sys.exit()
# Clear the console screen based on the operating system
def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')


def is_valid_email(email):
    pattern = re.compile(
        r"^(?!\.)[\w!#$%&'*+/=?^`{}|~.-]+(?<!\.)"
        r"@"
        r"(?!-)[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*(\.[A-Za-z]{2,})$"
    )
    return pattern.match(email) is not None

# Check if a file exists at the given path
def file_exists(path):
    return os.path.isfile(path)


# Reaed the configuration from a file
def readConfig():
    
    # Check if the configuration file exists
    if os.path.exists("./config.txt"):
        pass
    else:
        print("[*] Configuration file not found.")
        sys.exit()
            
    # Define the configuration parameters
    configs = ['target', 'emails', 'passwords', 'module', 'delay', 'jitter', 'lockout', 'proxy', 'type']
    my_configs = dict.fromkeys(configs)
    
    # Load the configuration from the file
    try:
        with open("./config.txt", "r") as file:
            for line in file:
                #sanity check
                #print(line)
                if not line.strip() or line.startswith('#'):
                    continue
                elif ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if key in my_configs:
                        my_configs[key] = value
                    else:
                        print(f"[*] Unknown configuration key: {key}")                          
            
            if any(value is None for value in my_configs.values()):
                print("[*] Configuration file is incomplete.")
                print("[*] Configuration keys must be: Emails file, Passwords file, module, delay, jitter, lockout, and proxy")
                sys.exit()
            else:
                print("[*] Configuration loaded successfully.")
                print("[*] The following configurations will be used for the password spray:\n")
                print("  - Target URL:", my_configs['target'])
                print("  - Emails File:", my_configs['emails'])
                print("  - Passwords File:", my_configs['passwords'])
                print("  - Module:", my_configs['module'])
                print("  - Delay:", my_configs['delay'])
                print("  - Jitter:", my_configs['jitter'])
                print("  - Ignore lockouts:", my_configs['lockout'])
                print("  - Proxy:", my_configs['proxy'])
                # print("  - Proxy Type:", my_configs['type'])
                print("\n[!] ATTENTION: By default, the spray will used random user agents, and wll not attempt to loot if a valid user and password is found.")
                print("==========================================================================================================================================")
                #print(f"{key}: {value}")
                
                print("[*] Do you want to continue? (y/n)")
                if input().lower() == 'y':
                    clear_screen()
                    return my_configs
                else:
                    clear_screen()
                    print("[*] Exiting...")
                    sys.exit()
    except FileNotFoundError:
        print("Something went wrong loading the config file.")

    
def sprayManager(configs):
    print("[*] Password Spray Manager starting....")
    
    # Check if log file exists, and warn the user
    if os.path.exists("sprayManager.log"):
        print("[*] Log file already exists, this will be overwritten.")
        input("[*] Press Enter to continue or Ctrl+C to exit...")
    
    # Check if the email file exist and verify list.
    if file_exists(configs['emails']):
        print(f"[*] Emails file found: {configs['emails']}")
        print("[*] Verify Email addresses in file.")
        emails = []
        with open(configs['emails'], 'r') as ef:
            for line in ef:
                email = line.strip()
                if email.startswith("#") or not email:
                    continue  # Skip comments and empty lines
                if not is_valid_email(email):
                    print(f"[!] Invalid email format: {email}. Skipping this email.")
                    # Save inavlid email on file
                    with open("invalid_emails.txt", 'a') as invalid_file:
                        invalid_file.write(email + '\n')
                    continue
                else:
                    #print(f"[*] Valid email found: {email}")
                    emails.append(email.lower() + '\n')
                    
        emails = list(set(emails))  # Remove duplicates
        with open(configs['emails'], 'w') as ef:
            ef.writelines(emails)

        # Press enter to continue
        print("[*] Emails file verified and cleaned.")
        input("[*] Press Enter to continue...")  
    else:
        print(f"[!] Emails file not found: {configs['emails']}")
        sys.exit()
    # Check if the passwords file exists
    if file_exists(configs['passwords']):
        pass
    else:
        print(f"[!] Passwords file not found: {configs['passwords']}")
        sys.exit()
    
    # Calling module based on the configuration    
    if configs['module'] == 'msol':
        print("[*] Using MSOL module for password spray.")
        msol.msolSpray(configs)
    elif configs['module'] == 'adfs':
        print("[*] Using ADFS module for password spray.")
        adfs.adfsSpray(configs)
    elif configs['module'] == 'owa':
        print("[*] Using OWA module for password spray.")
        owa.owaSpray(configs)
    elif configs['module'] == 'okta':
        print("[*] Using Okta module for password spray.")
        okta.oktaSpray(configs)
    elif configs['module'] == 'anyconnect':
        print("[*] Using AnyConnect module for password spray.")
        anyConnect.anySpray(configs)
    else:
        print(f"[!] Unknown module specified: {configs['module']}")
        sys.exit()




def main():
    clear_screen()
    print("\n         Trevor Manager Version 1.0         \n")
    checkTrevor()
    sprayManager(readConfig())



if __name__ == "__main__":
    main()
