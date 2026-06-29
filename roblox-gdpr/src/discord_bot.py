from collections import defaultdict

import discord
from discord import app_commands

import bot_config
import data_stores_api
import parser

def get_response_embed(failures: data_stores_api.DataStoreFailures) -> discord.Embed:
    if failures:
        embed = discord.Embed(
            title="Erasure Request Experienced Errors",
            description="The data deletion request for the relevant user ID(s) experienced one "
                        "or more errors.",
            color=discord.Color.red()
        )

        for place_id, place_failures in failures.items():
            description_lines = []

            for (name, scope, key), error_code, error_msg in place_failures:
                description_lines.append(
                    f'- Key "{key}" in "{scope}" scope of "{name}" data store\n'
                    f'  Code: {"Internal Error" if error_code is None else f"HTTP {error_code}"}\n'
                    f'  Error: {error_msg or "None"}'
                )

            embed.add_field(
                name=f"Place ID: {place_id}",
                value="\n".join(description_lines)
            )

        return embed

    else:
        return discord.Embed(
            title="Erasure Request Successful",
            description=f"All data stores successfully cleared for the relevant user ID(s).",
            color=discord.Color.green()
        )

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    @client.event
    async def on_ready():
        print(f"{client.user} is listening to GDPR requests")

    @client.event
    async def on_message(message: discord.Message):
        user_id, start_place_ids = parser.parse_message(message)

        if not user_id or not start_place_ids:
            return

        failures = data_stores_api.delete_user_data(user_id, start_place_ids)

        await message.reply(embed=get_response_embed(failures))

    @tree.command(name="manual-erase", description="Manually trigger a GDPR erasure")
    @app_commands.describe(
        user_ids="Comma-separated list of user ID(s)",
        game_ids="Comma-separated list of game ID(s)"
    )
    async def manual_erase(interaction: discord.Interaction, user_ids: str, game_ids: str):
        await interaction.response.defer(thinking=True)

        user_ids_set = parser.parse_command_param(user_ids)
        start_place_ids = parser.parse_command_param(game_ids)

        if not user_ids_set or not start_place_ids:
            await interaction.followup.send(embed=discord.Embed(
                title="Invalid Arguments",
                description="Arguments must be valid comma-separated lists of numbers.",
                color=discord.Color.red()
            ))

            return

        all_failures = defaultdict(list)

        for user_id in user_ids_set:
            failures = data_stores_api.delete_user_data(user_id, start_place_ids)

            for place_id, place_failures in failures.items():
                all_failures[place_id].extend(place_failures)

        await interaction.followup.send(embed=get_response_embed(all_failures))

    client.run(bot_config.BOT_TOKEN)

if __name__ == "__main__":
    run()
