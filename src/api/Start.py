#!/usr/bin/env python3

# Start.py
# Copyright (C) 2014 : Gabriel Carneiro
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#

import configparser
import os
import socket
import time

import win32com.client, win32api, win32con

readbuffer = ""
commands = []
settings = []
shell = win32com.client.Dispatch("WScript.Shell")

VK_CODE = {'spacebar':0x20}

def press(*args):
    '''
    press, release
    eg press('x', 'y', 'z')
    '''
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0, 0, 0)
        time.sleep(0.2)
        win32api.keybd_event(VK_CODE[i], 0 , win32con.KEYEVENTF_KEYUP , 0)

def addtofile():
    if len(commands) >= command_length:
        del commands[0]
        commands.extend([user[1:] + out.lower()])
    else:
        commands.extend([user[1:] + out.lower()])
            
# Directly from github.com/sunshinekitty5/TwitchPlaysPokemon
while True:
    if os.path.isfile("flappybird.config"):
        config = configparser.ConfigParser()
        config.read("flappybird.config")
        HOST = config.get('Settings', 'HOST')
        PORT = config.getint('Settings', 'PORT')
        AUTH = config.get('Settings', 'AUTH')
        NICK = config.get('Settings', 'USERNAME').lower()
        APP = config.get('Settings', 'APP')
        CHAT_CHANNEL = config.get('Settings', 'CHAT_CHANNEL').lower()
        command_length = config.getint('Settings', 'LENGTH')
        break
    else:
        print("Let's make you a config file")
        settings.append("; Settings for Twitch Plays Flappy Bird")
        settings.append("; Thanks sunshinekitty5 \n")
        
        settings.append("[Settings]\n")
        
        settings.append("; Where you're connecting to, if it's Twitch leave it as is")
        print("Where you're connecting to, if it's Twitch use irc.twitch.tv")
        settings_host = input("Hostname: ")
        settings.append("HOST = " + settings_host + "\n")
        
        settings.append("; Port number, probably should use 6667")
        print("Port number, probably should use 6667")
        settings_port = input("Port: ")
        settings.append("PORT = " + settings_port + "\n")
        
        settings.append("; Auth token, grab this from http://www.twitchapps.com/tmi")
        print("Auth token, grab this from http://www.twitchapps.com/tmi")
        settings_auth = input("Auth Token: ")
        settings.append("AUTH = " + settings_auth + "\n")
        
        settings.append("; Your Twitch Bot's Username")
        print("Your Twitch Bot's Username")
        settings_bot = input("Bot's Username: ")
        settings.append("USERNAME = " + settings_bot + "\n")
        
        settings.append("; Name of the application you run the file from, I suggest VBA")
        print("Name of the application you run the file from, if Visual Boy Advance use VisualBoyAdvance")
        settings_app = input("Application name: ")
        settings.append("APP = " + settings_app + "\n")
        
        settings.append("; Username of who's channel you're connecting to")
        print("Username of who's channel you're connecting to")
        settings_chat = input("Username: ")
        settings.append("CHAT_CHANNEL = " + settings_chat + "\n")
        
        settings.append("; The maximum number of lines in commands.txt (Useful for showing commands received in stream)")
        print("The maximum number of lines in commands.txt (Useful for showing commands received in stream)")
        settings_length = input("Length: ")
        settings.append("LENGTH = " + settings_length + "\n")
        
        with open("flappybird.config", "w") as f:
            for each_setting in settings:
                f.write(each_setting + '\n')

while True:
    with open("lastsaid.txt", "w") as f:
        f.write("")
        
    print("Starting flappybird.io")
    time.sleep(1)
    # emulator_job = Thread(target = startemulator, args = ())
    # emulator_job.start()
    
    s = socket.socket()
    s.connect((HOST, PORT))

    s.send(bytes("PASS %s\r\n" % AUTH, "UTF-8"))
    s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (NICK, HOST, NICK), "UTF-8"))
    s.send(bytes("JOIN #%s\r\n" % CHAT_CHANNEL, "UTF-8"));
    s.send(bytes("PRIVMSG #%s :Connected\r\n" % CHAT_CHANNEL, "UTF-8"))
    print("Sent connected message to channel %s" % CHAT_CHANNEL)

    while 1:
        readbuffer = readbuffer + s.recv(1024).decode("UTF-8", errors="ignore")
        temp = str.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            x = 0
            out = ""
            line = str.rstrip(line)
            line = str.split(line)

            for index, i in enumerate(line):
                if x == 0:
                    user = line[index]
                    user = user.split('!')[0]
                    user = user[0:12] + ": "
                if x == 3:
                    out += line[index]
                    out = out[1:]
                if x >= 4:
                    out += " " + line[index]
                x = x + 1
            
            # Respond to ping, squelch useless feedback given by twitch, print output and read to list
            if user == "PING: ":
                s.send(bytes("PONG tmi.twitch.tv\r\n", "UTF-8"))
            elif user == ":tmi.twitch.tv: ":
                pass
            elif user == ":tmi.twitch.: ":
                pass
            elif user == ":%s.tmi.twitch.tv: " % NICK:
                pass
            else:
                try:
                    print(user + out)
                except UnicodeEncodeError:
                    print(user)
                
            # Take in output
            if out.lower() == 'flap':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('spacebar')
                addtofile()
            if out.lower() == "wait" or out.lower() == "w":
                time.sleep(.85)
                addtofile()
            
            # Write to file for stream view
            with open("commands.txt", "w") as f:
                for item in commands:
                    f.write(item + '\n')
