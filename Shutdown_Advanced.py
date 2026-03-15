# Advanced system hibernation script
# Currently Windows only
# Author: kpb-gh
# Requires win11toast (install via pip)

from subprocess import call
from time import sleep, gmtime, strftime
from win11toast import notify
from datetime import time

def int_TryParse(string):
    try:
        return int(string)
    except ValueError:
        return None

def GetTime():
    return strftime("%Y-%m-%d %H-%M-%S", gmtime())

def NotifyUser(notify_time, shutdown_mode):
    warn_message = f"WARNING: {shutdown_mode} scheduled in {str(notify_time)} seconds. SAVE ANY WORK NOW!"
    notify(warn_message)
    print(warn_message)

def Execute(shutdown_mode, exit_on_end):
    if (shutdown_mode == "k"):
        print(f"Successfully activated at {GetTime()}")
    else:
        shutdown_cmdlet = "/s"
        if (shutdown_mode == "hibernate"):
            shutdown_cmdlet = "/h"
        call(str.split(f"shutdown {shutdown_cmdlet}"))
        print(f"Successfully activated at {GetTime()}")
        if exit_on_end:
            exit()

def GetUserInput():
    shutdown_mode = ""
    exit_on_end = True
    notify_time = 10
    delay = 60
    in_qs = input("Quick setup? (Yn): ").lower()
    if (in_qs == "n"):
        # Extended Setup
        in_ex = input("Exit after finishing? (Yn): ").lower()
        if (in_ex == "n"):
            exit_on_end = False
        in_warn = int_TryParse(input("Time for warning: "))
        if (in_warn != None) and (in_warn > 0):
            notify_time = in_warn
        in_mode = input("Program mode? (S)hutdown/(h)ibernate: ").lower()
        if (in_mode == "h") or (in_mode == "hibernate"):
            shutdown_mode = "hibernate"
        elif (in_mode == "k"):
            shutdown_mode = "k" # TODO what's this called again?
        else:
            shutdown_mode = "shutdown"
        # Quick Setup
    else:
        exit_on_end = True
        notify_time = 10
        shutdown_mode = "hibernate"
    # Both
    in_delay = int_TryParse(input("Time to shutdown: "))
    if (in_delay != None) and (in_delay > 0):
        delay = in_delay
    print(f"Starting countdown at {GetTime()}; d={delay}, n={notify_time}, m={shutdown_mode}, e={exit_on_end}")
    Countdown(delay, notify_time, shutdown_mode, exit_on_end)

def Countdown(delay, notify_time, shutdown_mode, exit_on_end):
    warned = False
    for x in range(delay):
        if (warned == False) and (delay - x < notify_time):
            NotifyUser(notify_time, shutdown_mode)
            warned = True
        sleep(1)
    Execute(shutdown_mode, exit_on_end)

def Main():
    while True:
        GetUserInput()

Main()
