#!/bin/bash

# Downloads the tools
python fastagi/tool_manager.py

# Install dependencies
./install_tool_dependencies.sh

exec celery -A fastagi.worker worker --beat --loglevel=info