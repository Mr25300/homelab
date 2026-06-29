import os

BOT_TOKEN = os.environ.get("BOT_TOKEN") or ""
OPEN_CLOUD_API_KEY = os.environ.get("OPEN_CLOUD_API_KEY") or ""
ROBLOX_WEBHOOK_SECRET = os.environ.get("ROBLOX_WEBHOOK_SECRET") or ""

DataStore = tuple[str, str, str]
DataStoreEntries = dict[int, tuple[int, list[DataStore], list[DataStore]]]

DATA_STORE_ENTRIES: DataStoreEntries = {
    # Stand Testing
    6016216310: (
        2174054222,
        [
            ("DataStoreStand", "global", "{user_id}"),
            ("DataStoreStorage1", "global", "{user_id}"),
            ("DataStoreStorage2", "global", "{user_id}")
        ],
        []
    ),

    # Stand Succession (Old)
    6812358402: (
        2587536195,
        [
            ("PlayerData", "global", "{user_id}")
        ],
        []
    ),

    # Stand Testing Legacy
    16172009792: (
        5585992751,
        [
            ("StandDataStore", "global", "{user_id}")
        ],
        []
    ),

    # Stand Succession Preview
    15826698411: (
        5472202712,
        [
            ("Data_4", "global", "Player_{user_id}")
        ],
        []
    )
}
