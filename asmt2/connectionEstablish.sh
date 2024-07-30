#!/bin/bash

# Load environment variables from .env file
if [[ -f .env ]]; then
    export $(cat .env | xargs)
fi


source "$OPENRC_FILE_PATH"



# Start SSH connection using the private key file path
ssh -i "$PRIVATE_FILE_PATH" -L 6443:$(openstack coe cluster show elastic -f json | jq -r '.master_addresses[]'):6443 ubuntu@$(openstack server show bastion -c addresses -f json | jq -r '.addresses["qh2-uom-internal"][]')

