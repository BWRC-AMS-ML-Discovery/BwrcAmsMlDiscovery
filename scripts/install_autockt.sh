set -eo

# Install all of our packages with development extras
pip install \
    -e "./Discovery/Shared[dev]" \
    -e "./Discovery/Client[dev]" \
    -e "./Discovery/Server[dev]" \
    -e "./AutoCkt/Shared[dev]" \
    -e "./AutoCkt/Ckt[dev]" \
    -e "./AutoCkt/Auto[dev]"

# Swap to the ray/ OpenAI/ ML-stuff preferred version of protobuf
# Hdl21 includes a dependency on a newer version, 
# but we are not using the facet of Hdl21 that requires it. 
pip uninstall protobuf -y
pip install protobuf==3.19.1

# Set up pre-commit hooks
pre-commit install
