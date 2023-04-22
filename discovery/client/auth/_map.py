from discovery.shared.auth import inputs
from discovery import shared


inp_auth_types = {
    "whoami": inputs.WhoAmIInputAuth,
}

out_types = {
    "whoami": shared.user.WhoAmIOutput,
}
