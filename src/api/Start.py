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
import time

import win32com.client, win32api, win32con


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
        QUICK_PRESS = config.getboolean('Settings', 'QUICK_PRESS')
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
        
        settings.append("; Oh how to explain this...")
        settings.append("; You get the chat command 'Left'")
        settings.append("; You are currently facing right")
        settings.append("; If QUICK_PRESS is true you turn left")
        settings.append("; If QUICK_PRESS is false you turn left and move one square left")
        print("Oh how to explain this...")
        print("You get the chat command 'Left'")
        print("You are currently facing right")
        print("If QUICK_PRESS is true you turn left")
        print("If QUICK_PRESS is false you turn left and move one square left")
        settings_press = input("QUICK PRESS: ")
        settings.append("QUICK_PRESS = " + settings_press + "\n")
        
        with open("settings.txt", "w") as f:
            for each_setting in settings:
                f.write(each_setting + '\n')
    
    command = input("Command: ")
    if command.lower() == "flap":
        shell.AppActivate("%s" % APP)
        press('spacebar')
    if command.lower() == "wait" or command.lower() == "w":
        time.sleep(.85)
