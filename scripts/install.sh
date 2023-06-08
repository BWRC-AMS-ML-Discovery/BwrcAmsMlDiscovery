set -eo

pip install \
    -e ./Discovery/Shared \
    -e ./Discovery/Server \
    -e ./Discovery/Client \
    -e ./Example/Shared \
    -e ./Example/Server \
    -e ./Example/Client
