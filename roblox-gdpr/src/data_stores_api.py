from typing import Literal
from collections import defaultdict

import requests

import bot_config

DataStoreType = Literal["STANDARD", "ORDERED"]
DataStoreFailures = defaultdict[int, list[tuple[bot_config.DataStore, int | None, str]]]

HEADERS = {"x-api-key": bot_config.OPEN_CLOUD_API_KEY}

def delete_data_stores(place_id: int, universe_id: int, store_type: DataStoreType,
                       stores: list[bot_config.DataStore], user_id: int,
                       failures: DataStoreFailures) -> None:
    for (store_name, scope, entry_key) in stores:
        entry_key = entry_key.replace("{user_id}", str(user_id))

        response = None

        try:
            if store_type == "STANDARD":
                response = requests.delete(
                    f"https://apis.roblox.com/datastores/v1/universes/{universe_id}"
                    "/standard-datastores/datastore/entries/entry",
                    headers=HEADERS,
                    params={
                        "datastoreName": store_name,
                        "scope": scope,
                        "entryKey": entry_key
                    }
                )
            else:
                response = requests.delete(
                    f"https://apis.roblox.com/ordered-data-stores/v1/universes/{universe_id}"
                    f"/orderedDatastores/{store_name}/scopes/{scope}/entries/{entry_key}",
                    headers=HEADERS
                )

        except requests.exceptions.RequestException:
            pass

        if response is None or response.status_code not in {200, 204, 404}:
            message = ""
            status_code = None

            if response is None:
                message = "Connection failed"
            else:
                try:
                    error_payload = response.json()

                    if "errors" in error_payload:
                        message = error_payload["errors"][0].get("message", "")
                    else:
                        message = error_payload.get("message", "")

                except Exception:
                    pass

                if not message:
                    if len(response.text) > 200:
                        message = response.text[:200] + "..."
                    else:
                        message = response.text

                status_code = response.status_code

            failures[place_id].append((
                (store_name, scope, entry_key), status_code, message
            ))

def delete_user_data(user_id: int, start_place_ids: set[int]) -> DataStoreFailures:
    failures: DataStoreFailures = defaultdict(list)

    for start_place_id in start_place_ids:
        if start_place_id not in bot_config.DATA_STORE_ENTRIES:
            if not failures[start_place_id]:
                failures[start_place_id].append((
                    ("N/A", "N/A", "N/A"), None, "Game ID is not present in the configuration."
                ))

            continue

        universe_id, standard_entries, ordered_entries = bot_config.DATA_STORE_ENTRIES[start_place_id]

        delete_data_stores(start_place_id, universe_id, "STANDARD", standard_entries, user_id,
                           failures)

        delete_data_stores(start_place_id, universe_id, "ORDERED", ordered_entries, user_id,
                           failures)

    return failures
