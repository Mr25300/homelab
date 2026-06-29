import time
import hmac
import hashlib
import re
import base64

import bot_config

def parse_footer(message) -> tuple[str, int]:
    if not message.embeds[0].footer or not message.embeds[0].footer.text:
        return "", 0

    footer_match = re.match(
        r"Roblox-Signature: (.*), Timestamp: (.*)",
        message.embeds[0].footer.text
    )

    if not footer_match:
        return "", 0
    else:
        signature = footer_match.group(1)
        timestamp = int(footer_match.group(2))

        return signature, timestamp

def validate_request(message, signature, timestamp) -> bool:
    if not message or not signature or not timestamp:
        return False

    request_timestamp_ms = timestamp * 1000
    window_time_ms = 300 * 1000
    oldest_timestamp_allowed = round(time.time() * 1000) - window_time_ms

    if request_timestamp_ms < oldest_timestamp_allowed:
        return False

    timestamp_message = f"{timestamp}.{message.embeds[0].description}"

    digest = hmac.new(
        bot_config.ROBLOX_WEBHOOK_SECRET.encode(),
        msg=timestamp_message.encode(),
        digestmod=hashlib.sha256
    ).digest()

    validated_signature = base64.b64encode(digest).decode()

    return signature == validated_signature

def parse_message(message) -> tuple[int, set[int]]:
    if len(message.embeds) != 1 or not message.embeds[0].description:
        return 0, set()

    description_match = re.match(
        r"You have received a new notification for Right to Erasure for the User Id: (.*) in " +
        r"the game\(s\) with Ids: (.*)",
        message.embeds[0].description
    )

    if not description_match:
        return 0, set()

    try:
        user_id = int(description_match.group(1))
        start_place_ids = {int(item.strip()) for item in description_match.group(2).split(",")}

    except ValueError:
        return 0, set()

    signature, timestamp = parse_footer(message)

    if validate_request(message, signature, timestamp):
        return user_id, start_place_ids
    else:
        return 0, set()

def parse_command_param(param_str: str) -> set[int]:
    try:
        return {int(val) for val in param_str.split(",")}

    except ValueError:
        return set()
