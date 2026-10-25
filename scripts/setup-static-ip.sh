#!/usr/bin/env bash
set -e

if [ "$EUID" -ne 0 ]; then
    echo "Must run as root"
    exit 1
fi

INTERFACE=$(ip -o -4 route show to default | awk '{print $5}')

CONFIG_FILE="/etc/network/interfaces"
OLD_CONFIG_FILE="/etc/network/interfaces.old"

if [ -f "$CONFIG_FILE" ]; then
    mv "$CONFIG_FILE" "$OLD_CONFIG_FILE"
fi

cat <<EOF > "$CONFIG_FILE"
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
allow-hotplug $INTERFACE
iface $INTERFACE inet static
    address 10.0.0.2
    netmask 255.255.255.0
    # Can replace above 2 with: address 10.0.0.2/24
    gateway 10.0.0.1
    dns-nameservers 10.0.0.2 9.9.9.9
EOF

systemctl restart networking
