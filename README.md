# Overview
This project is a personal homelab containing detailed configuration files for deploying cloud storage, media apps and game servers through Docker Compose.

# Production Setup
The homelab is lightweight and OS-agnostic, however its current production setup details are as follows:
- **Hardware & OS**: The homelab runs on a custom-built headless Debian server, with all work and maintenance done through SSH.
- **Data**: A hard drive is mounted to /data/storage in which all media is stored and important, long-term Docker volumes are bind mounted in.
- **Networking**: The server is accessed locally via its local subnet IP and remotely via Tailscale, with the DNS server set up with split-horizon resolution to map custom addresses to the right IP depending on whether the server is accessed through LAN or Tailscale.

# Services
| Category | Service Stack | Purpose | Access |
| :--- | :--- | :--- | :--- |
| DNS | Technitium | Create private DNS records for accessing homelab services and block malicious and/or unwanted sites| Port 53 |
| Reverse Proxy | Caddy | Route addresses to services and automatically handle SSL certificates for HTTPS | Port 80 / 443 |
| Cloud Storage | Immich, Nextcloud | Host photos and videos with Immich, and files, office, calendar and contacts with Nextcloud | Through Caddy |
| Torrenting | Gluetun, qBittorrent | Torrent behind Mullvad VPN using Gluetun to hide IP from peers in torrent swarms | Through Caddy |
| Media Acquisition | Radarr, Sonarr, Lidarr, Chaptarr, Prowlarr | Automatically index, monitor and download (with a torrenting client) movies, TV, music and books | Through Caddy |
| Media Playing | Jellyfin, Audiobookshelf | Add media libraries for movies, TV and music in Jellyfin, and for books and podcasts in Audiobookshelf to be played/read with progress tracking and separate user accounts | Through Caddy |
| Minecraft | playit, mc-router, minecraft-server | Access the server through playit and then route to specific server containers based on address with mc-router | A playit.gg tunnel address |

**Note**: All services in the repository that are not mentioned above are either not fully set up or are no longer used and not yet removed.

# Deployment & Maintenance
All services are deployed and managed via Docker Compose with a `docker-compose.yml` file.

The environment variables necessary for each service are documented as comments in its `docker-compose.yml` file.

To update or spin up a service:
```bash
cd /path/to/service/folder

sudo docker compose pull # Pull/update images
sudo docker compose up -d # Deploy/re-deploy containers
```
