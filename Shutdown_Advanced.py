# Advanced system hibernation script
# Currently Windows/Linux
#   WARN: Linux support is UNTESTED!
# Author: kpb-gh
# Optional: desktop-notifier (install via pip)
#   Provides system notifications.

from subprocess import call
from time import sleep, gmtime, strftime
import asyncio
from datetime import time
from platform import system

NOTIF_AV = False
try:
    from desktop_notifier import DesktopNotifier
    NOTIFIER = DesktopNotifier(app_name="ShutdownAdvanced")
    NOTIF_AV = True
except: 
    print("Notifications unavailable. Possibly not installed.")

def int_TryParse(string):
    try:
        return int(string)
    except ValueError:
        return None

def GetTime():
    return strftime("%Y-%m-%d %H-%M-%S", gmtime())

async def NotifyUser(notify_time, shutdown_mode):
    warn_message = f"WARNING: {shutdown_mode} scheduled in {str(notify_time)} seconds. SAVE ANY WORK NOW!"
    print(warn_message)
    if (NOTIF_AV):
        await NOTIFIER.send(title="Shutdown Imminent", message=warn_message)

def Execute(shutdown_mode, exit_on_end):
    if (shutdown_mode == "k"):
        print(f"Successfully activated at {GetTime()}")
    elif (system() == "Windows":
        shutdown_cmdlet = "/s"
        if (shutdown_mode == "hibernate"):
            shutdown_cmdlet = "/h"
        call(str.split(f"shutdown {shutdown_cmdlet} /t 0"))
        print(f"Successfully activated at {GetTime()}")
        if exit_on_end:
            exit()
    elif (system() == "Linux"):
        shutdown_cmdlet = "shutdown -P now"
        call(str.split(shutdown_cmdlet)) #hibernate unsupported, requires root by default

async def GetUserInput():
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
        in_mode = input("Program mode? (S)hutdown/(h)ibernate/warn(K): ").lower()
        if (in_mode == "h") or (in_mode == "hibernate"):
            shutdown_mode = "hibernate"
            if (system() == "Linux"):
                print("WARNING: Hibernate on Linux is not supported. System will instead SHUT DOWN!")
        elif (in_mode == "k"):
            shutdown_mode = "k" # warn only
        else:
            shutdown_mode = "shutdown"
        # Quick Setup
    else:
        exit_on_end = True
        notify_time = 10
        shutdown_mode = "shutdown"
    # Both
    in_delay = int_TryParse(input("Time to shutdown: "))
    if (in_delay != None) and (in_delay > 0):
        delay = in_delay
    print(f"Starting countdown at {GetTime()}; d={delay}, n={notify_time}, m={shutdown_mode}, e={exit_on_end}")
    await Countdown(delay, notify_time, shutdown_mode, exit_on_end)

async def Countdown(delay, notify_time, shutdown_mode, exit_on_end):
    warned = False
    for x in range(delay):
        if (warned == False) and (delay - x < notify_time):
            await NotifyUser(notify_time, shutdown_mode)
            warned = True
        sleep(1)
    Execute(shutdown_mode, exit_on_end)

async def Main():
    while True:
        await GetUserInput()

asyncio.run(Main())
