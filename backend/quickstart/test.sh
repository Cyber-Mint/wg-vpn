#!/bin/bash
# Copyright (c) 2023, Cyber-Mint (Pty) Ltd
# License MIT: https://opensource.org/licenses/MIT

# exit term handler to cleanup docker after testing
sigterm_handler() {
  tput reset
  docker compose down --remove-orphans --volumes --rmi local
  exit 0
}

# Setup signal trap
trap 'trap " " SIGINT SIGTERM SIGHUP; kill 0; wait; sigterm_handler' SIGINT SIGTERM SIGHUP

# Bring down containers in compose file
docker compose down --remove-orphans

# Bring up containers in compose file
docker compose up --build
