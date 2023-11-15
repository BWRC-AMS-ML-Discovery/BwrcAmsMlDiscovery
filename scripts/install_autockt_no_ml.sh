set -eo

# Install all of our packages with development extras
pip install \
    -e "./Discovery/Dev" \
    -e "./Discovery/Shared" \
    -e "./Discovery/Client" \
    -e "./Discovery/Server" \
    -e "./AutoCkt/Shared" \
    -e "./AutoCkt/Server" \
    -e "./AutoCkt/Client" 

# The point: leaving out this one: 
##-e "./AutoCkt/ML"

# Swap to the ray/ OpenAI/ ML-stuff preferred version of protobuf
# Hdl21 includes a dependency on a newer version, 
# but we are not using the facet of Hdl21 that requires it. 
# pip uninstall protobuf -y
# pip install protobuf==3.19.1

# Set up pre-commit hooks
pre-commit install
