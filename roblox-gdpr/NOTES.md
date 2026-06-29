Workflow:
- Roblox webhook listens to GDPR requests and sends them to the given URL (Discord webhook)
- Discord webhook takes the requests and sends them into the gdpr channel
- Discord bot looks at all messages sent and parses them if they are gdpr request messages
- Discord bot then makes API requests to Roblox's Open Cloud to delete the relevant data
