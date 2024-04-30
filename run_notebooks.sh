#!/bin/bash
source .venv/bin/activate

# Check if a parameter is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <network-adapter-name>"
    exit 1
fi

# Use the first argument as the network adapter name
NETWORK_ADAPTER=$1

# Get the IP address of the desired network adapter
IP_ADDRESS=$(ifconfig "$NETWORK_ADAPTER" | grep 'inet ' | awk '{print $2}')

# Check if we successfully obtained an IP address
if [ -z "$IP_ADDRESS" ]; then
    echo "Could not find an IP address for the adapter: $NETWORK_ADAPTER"
    exit 1
fi

# Start the Jupyter notebook with the dynamically obtained IP address
jupyter notebook --ip="$IP_ADDRESS"