"""
# Circuit data test v0
"""
import time
from discovery import *
from discovery.client import *

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
    print("Created new module #" + str(i) + "\n")
    new_module = create_module(TestModuleInput(new_name="test1", new_i=1, new_o=i, new_s=3))
    print("\n" + new_module.tostring() + "\n")
    time.sleep(1)


    '''
    send point request
    print point request

    send ...
    '''

    def test_1():
        assert 1 == 1

    def test_2():
        new_module = create_module(TestModuleInput(new_name="test1", new_i=1, new_o=2, new_s=3))
        result = '''Type: TestModuleOutput
Attributes:
  Name: Module(name=test1)
  o: Signal(name=None, width=2, vis=<Visibility.PORT: 1>, direction=<PortDir.OUTPUT: 1>, desc=None)'''
        assert new_module.tostring() == result