set -eo

pip install \
    -e ./Discovery/Shared[dev] \
    -e ./Discovery/Server[dev] \
    -e ./Discovery/Client[dev] \
    -e ./Example/Shared[dev] \
    -e ./Example/Server[dev] \
    -e ./Example/Client[dev]
