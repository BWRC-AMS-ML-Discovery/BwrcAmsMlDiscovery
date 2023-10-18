UPDATE: please see the journal paper for additional results on designing a two-stage folded-cascode and two-stage amplifier (https://ieeexplore.ieee.org/abstract/document/9576505). 

# AutoCkt
## CktGym Edition 

### Development 

```
# From the `BwrcAmsMlDiscovery` directory

# To install the client libraries 
conda create --name autockt-client python=3.10
conda activate autockt-client
bash scripts/install_client.sh 
python -c "import autockt"

# To install the server libraries 
conda create --name autockt-server python=3.10
conda activate autockt-server
bash scripts/install_server.sh 
python -c "import autockt_server"

```
