set -eo

# Install all of our packages with development extras
pip install \
    -e "./Discovery/Dev" \
    -e "./Discovery/Shared[dev]" \
    -e "./Discovery/Server[dev]" \
    -e "./Discovery/Client[dev]" \
    -e "./Example/Shared[dev]" \
    -e "./Example/Server[dev]" \
    -e "./Example/Client[dev]" \

# Set up pre-commit hooks
pre-commit install
