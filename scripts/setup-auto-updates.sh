#!/usr/bin/env bash
set -e

if [ "$EUID" -ne 0 ]; then
    echo "Must run as root"
    exit 1
fi

apt update
apt install unattended-upgrades apt-listchanges needrestart
dpkg-reconfigure --priority=low unattended-upgrades
