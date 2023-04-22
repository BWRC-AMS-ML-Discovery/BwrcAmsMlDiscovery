from discovery.shared.auth import inputs
from discovery.shared import user


inp_auth_types = {
    "whoami": inputs.WhoAmIInputAuth,
}

out_types = {
    "whoami": user.WhoAmIOutput,
}
