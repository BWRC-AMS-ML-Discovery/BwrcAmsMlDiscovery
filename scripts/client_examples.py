"""
# Example Discovery Client Script 
"""

from discovery import Example
from discovery.client import alive, example

# Call the server's root endpoint.
# Gets a general health-indication of whether we can contact the server.
print(alive())

# Call the server's example endpoint, and print what comes back
print(example(Example(txt="Hello World!", num=3)))
