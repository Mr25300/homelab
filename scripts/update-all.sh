#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]; then
    echo "Must run as root"
    exit 1
fi

HOMELAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

update_stack() {
    local base_dir="$1"
    local stack_dir

    for stack_dir in "$base_dir"/*; do
	if [ ! -d "$stack_dir" ]; then
	    continue
	fi

	if [ ! -f "$stack_dir"/docker-compose.yml ]; then
	    update_stack "$stack_dir"
	    continue
	fi

        local stack_name=$(basename "$stack_dir")

        (
            cd "$stack_dir" || exit 1

            local running_containers=$(docker compose ps -q -a)

            if [ -z "$running_containers" ]; then
                echo "Skipping update: $stack_name"
                exit 0
            fi

            echo "Checking for updates: $stack_name"

            docker compose pull

            local needs_update=false
            local images=$(docker compose config --images)

            for cid in $running_containers; do
                local container_img_id=$(docker inspect --format='{{.Image}}' "$cid")
                local container_img_name=$(docker inspect --format='{{.Config.Image}}' "$cid")
                local local_img_id=$(docker image inspect --format='{{.Id}}' "$container_img_name")

                if [[ "$container_img_id" != "$local_img_id" ]]; then
                    needs_update=true
                fi
            done

            if [ "$needs_update" = true ]; then
                echo "Restarting: $stack_name"

                docker compose up -d --remove-orphans
            fi
        )
    done
}

update_stack "$HOMELAB_DIR"
