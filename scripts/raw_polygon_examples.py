"""
# Raw Polygon Examples
"""
import time
from discovery import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def cprint(message, test):
    message = str(message)
    if test in message:
        print(bcolors.OKGREEN + message + bcolors.ENDC)
    else:
        print(bcolors.FAIL + message + bcolors.ENDC)

rootpoint_status = alive()
cprint(rootpoint_status, "alive")
print("\n")

for i in range(1, 5):
    print("Created new point #" + str(i) + "\n")
    new_point = point(PointInput(x=i, y=5-i))
    print("\n" + str(new_point) + "\n")
    time.sleep(1)