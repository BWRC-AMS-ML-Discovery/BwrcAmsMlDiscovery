set -eo

# Install `Shared` and `Client` packages with development extras
pip install \
    -e "./Discovery/Dev" \
    -e "./Discovery/Shared[dev]" \
    -e "./Discovery/Client[dev]" \
    -e "./AutoCkt/Shared[dev]" \
    -e "./AutoCkt/Auto[dev]"

# Set up pre-commit hooks
pre-commit install
