#!/bin/bash

# Downloads the tools
python startagi/tool_manager.py

# Install dependencies
./install_tool_dependencies.sh

exec celery -A startagi.worker worker --beat --loglevel=info