"""
# Example Discovery Client Script 
"""

#import sys
#sys.path.append("/Users/aakarshv1/Desktop/bwrc-ams/BwrcAmsMlDiscovery") #put your own path name


from discovery.shared import Example, ObjParams, Measurements
from discovery.client import alive, version, example, measure

# Call the server's root endpoint.
# Gets a general health-indication of whether we can contact the server.
print(alive())

# Get the server's version
print(version())

# Call the server's example RPC endpoint, and print what comes back
print(example(Example(txt="Hello World!", num=3)))

# Now invoke a super-secret SPICE simulation
print(measure(ObjParams(w=1000, l=150, v=1000)))
