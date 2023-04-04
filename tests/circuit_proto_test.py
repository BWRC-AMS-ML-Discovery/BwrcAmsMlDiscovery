"""
# Tests for circuit object creation (https://github.com/Vlsir/schema-proto/blob/main/circuit.proto)
"""

from discovery import *
from discovery.client import *

for i in range(1, 5):
    print("Created new module #" + str(i) + "\n")
    new_module = create_module(TestModuleInput(new_name="test1", new_i=1, new_o=i, new_s=3))
    print("\n" + new_module.tostring() + "\n")


    '''
    send point request
    print point request

    send ...
    '''

    def testModule_test():
        new_module = create_module(TestModuleInput(new_name="test1", new_i=1, new_o=2, new_s=3))
        result = '''Type: TestModuleOutput
Attributes:
  Name: Module(name=test1)
  o: Signal(name=None, width=2, vis=<Visibility.PORT: 1>, direction=<PortDir.OUTPUT: 1>, desc=None)'''
        assert isinstance(new_module, TestModuleOutput)
        assert new_module.tostring() == result