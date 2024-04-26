#!/bin/bash

set -e

ansible-playbook --ask-vault-pass deploy.yml

echo "Deployment completed successfully!"
