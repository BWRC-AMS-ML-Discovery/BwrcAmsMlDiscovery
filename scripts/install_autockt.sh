set -eo

# Install all of our packages with development extras
pip install \
    -e "./Discovery/Shared[dev]" \
    -e "./Discovery/Client[dev]" \
    -e "./Example/Shared[dev]" \
    -e "./Example/Client[dev]" \
    -e "./AutoCkt/Shared[dev]" \
    -e "./AutoCkt/Ckt[dev]" \
    -e "./AutoCkt/Auto[dev]"

# Set up pre-commit hooks
pre-commit install
