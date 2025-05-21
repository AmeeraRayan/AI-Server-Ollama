#!/bin/bash

# Copy the .service file to systemd
sudo cp ai-server.service /etc/systemd/system/

# Reload systemd and restart service
sudo systemctl daemon-reload
sudo systemctl restart ai-server.service
sudo systemctl enable ai-server.service

# Verify service is running
if ! systemctl is-active --quiet ai-server.service; then
  echo "❌ ai-server.service is not running."
  sudo systemctl status ai-server.service --no-pager
  exit 1
fi

echo "✅ AI server deployed and running!"