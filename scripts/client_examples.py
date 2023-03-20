"""
# Example Discovery Client Script 
"""

from discovery import Example, SecretSpiceSimulationInput
from discovery.client import alive, version, example, secret_spice_sim

# Call the server's root endpoint.
# Gets a general health-indication of whether we can contact the server.
print(alive())

# Get the server's version
print(version())

# Call the server's example RPC endpoint, and print what comes back
print(example(Example(txt="Hello World!", num=3)))

# Now invoke a super-secret SPICE simulation
print(secret_spice_sim(SecretSpiceSimulationInput(w=1000, l=150, v=1000)))


# Requires auth


from discovery import WhoAmIInput
from discovery.client import whoami


print(
    whoami(
        WhoAmIInput(
            api_key="eyJhbGciOiJSUzI1NiIsImtpZCI6IjFlOTczZWUwZTE2ZjdlZWY0ZjkyMWQ1MGRjNjFkNzBiMmVmZWZjMTkiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiS2luZ0hhbumfqeWwmuWFuCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BR05teXhaWFpBUGFhQklUQW03WDJjcEp4c201MGZDMFZlOG5aWmE1VmRWblN3PXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2J3cmNhbXNtbGRpc2NvdmVyeWZpcmViYXNlIiwiYXVkIjoiYndyY2Ftc21sZGlzY292ZXJ5ZmlyZWJhc2UiLCJhdXRoX3RpbWUiOjE2NzkyNzY1NTQsInVzZXJfaWQiOiJNcjhuNnBXa2ZIVXduaFVrQnRXVXM2UFBxTFIyIiwic3ViIjoiTXI4bjZwV2tmSFV3bmhVa0J0V1VzNlBQcUxSMiIsImlhdCI6MTY3OTI3NjU1NCwiZXhwIjoxNjc5MjgwMTU0LCJlbWFpbCI6ImtpbmdoMDczMEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwMjU3NzkwOTQzNTM4NjgyOTc5NSJdLCJlbWFpbCI6WyJraW5naDA3MzBAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.vSp5FfUSOgXDn0qFodu02F_0tuH4_Ng55oNC2JZgumMqIuYnqgo6ERw8tJY-vRGRCeqooQo5BHgKVbCaJ7HvJMSuQhv1l1RVpyVsuwE5bBfWGqGL0HENeRaGbWe8mjsaP4m-V9UV3H8RK_i4haJ2RYZZH_EkNuRiiNE0UlQmlz9J-8DOCWyn4EMmANzh8cblhRJdc-4Emjy7W0XCO4MdVX-bBjC_6o2sQowD0kODPLr-cvApTHiAUWGQ7gQa0dDDk504BGqx-yYPMQvD3USr2UQdrvc7_aGEg8Su-klq35lH0Ww3KEiiFug6G9Bch5YohxMzP7cQpzociqXoRZUQug"
        )
    )
)
