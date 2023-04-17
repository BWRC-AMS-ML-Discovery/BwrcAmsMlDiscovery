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
            api_key="eyJhbGciOiJSUzI1NiIsImtpZCI6ImM4MjNkMWE0MTg5ZjI3NThjYWI4NDQ4ZmQ0MTIwN2ViZGZhMjVlMzkiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiV2F5bmUgV2FuZyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BR05teXhaV0l5ZzYzTDFrQTZ5LVVpR3R1aVFpZkF2YzN4RXpRVUVSalgzRThnPXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2J3cmNhbXNtbGRpc2NvdmVyeWZpcmViYXNlIiwiYXVkIjoiYndyY2Ftc21sZGlzY292ZXJ5ZmlyZWJhc2UiLCJhdXRoX3RpbWUiOjE2NzkyODMyMTUsInVzZXJfaWQiOiJlRkRJSGxZOGFoUWRCY0tKaWUwYWpQb1Y1WWYyIiwic3ViIjoiZUZESUhsWThhaFFkQmNLSmllMGFqUG9WNVlmMiIsImlhdCI6MTY4MTY5MDk4OSwiZXhwIjoxNjgxNjk0NTg5LCJlbWFpbCI6IndoaC5iZWFyQGJlcmtlbGV5LmVkdSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTEyNzkxMzI1NTM2NzUyOTgxNzExIl0sImVtYWlsIjpbIndoaC5iZWFyQGJlcmtlbGV5LmVkdSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.QFfGvIQiSm-16buzJlXnaiJoTHOnTZxQ75gewjONRFe0Rmv0Tk2gicgqA5gtrhBSy2_dgsSPiT_okUHXiu3DazRss3hbNyu1l3fcOgYjpfKWP8TZfMZmJ4DEJjZ9Bt6LQ6i2AuYp0MW5SRXx65PdngG5Hd9P4mGyVhFkokB9x0lVPxuSReQ0t1rxM76wRC7xgxmzqMgk6F-ZXoitx7AWFgPRkCeCeU5l3xy4ZAmC6YLsJgqLTo_FIm97BxhISPYYCe6_UJaiNB9eY8VlcQ4RE4wHczPKei3W7fh3pkv0KcVgJd_CcfXLTWmLfFarLxzRnIjkpTyEQEXQg4rw1368_A"
        )
    )
)
