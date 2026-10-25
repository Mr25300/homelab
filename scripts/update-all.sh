#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]; then
    echo "Must run as root"
    exit 1
fi

HOMELAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for stack_dir in "$HOMELAB_DIR"/*; do
    if [ -f "$stack_dir"/docker-compose.yml ]; then
        stack_name=$(basename "$stack_dir")

        (
            cd "$stack_dir" || exit 1

            running_containers=$(docker compose ps -q --status running)

            if [ -z "$running_containers" ]; then
                echo "Skipping update: $stack_name"
                exit 0
            fi
            
            echo "Checking for updates: $stack_name"
            
            docker compose pull
            
            needs_update=false
            images=$(docker compose config --images)
            
            for cid in $running_containers; do
                container_img_id=$(docker inspect --format='{{.Image}}' "$cid")
                container_img_name=$(docker inspect --format='{{.Config.Image}}' "$cid")
                local_img_id=$(docker image inspect --format='{{.Id}}' "$container_img_name")
            
                if [[ "$container_img_id" != "$local_img_id" ]]; then
                    needs_update=true
                fi
            done
            
            if [ "$needs_update" = true ]; then
                echo "Restarting: $stack_name"
            
                docker compose up -d --remove-orphans
            fi
        )
    fi
done
