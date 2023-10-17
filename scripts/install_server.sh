set -eo

# Install `Shared` and `Server` packages with development extras
pip install \
    -e "./Discovery/Dev" \
    -e "./Discovery/Shared[dev]" \
    -e "./Discovery/Server[dev]" \
    -e "./AutoCkt/Shared[dev]" \
    -e "./AutoCkt/Server[dev]"

# Set up pre-commit hooks
pre-commit install
