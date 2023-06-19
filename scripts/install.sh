set -eo

pip install \
    -e ./Discovery/Shared \
    -e ./Discovery/Server \
    -e ./Discovery/Client \
    -e ./Example/Shared \
    -e ./Example/Server \
    -e ./Example/Client \
    -e "./AutoCkt/Shared[dev]" \
    -e "./AutoCkt/Ckt[dev]" \
    -e "./AutoCkt/Auto[dev]" \
    -e "./CktRL/Auto[dev]" \
