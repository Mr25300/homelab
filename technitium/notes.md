# Recursion ACL

> Settings > Recursion > Network Access Control List (ACL)

```
10.0.0.0/24
100.64.0.0/10
172.18.0.0/16
```

# Split Horizon App Config

> Apps > Split Horizon > Config

```json
{
    "appPreference": 40,
    "networks": {},
    "enableAddressTranslation": false,
    "domainGroupMap": {},
    "networkGroupMap": {
        "10.0.0.0/24": "lan",
        "100.64.0.0/10": "tailnet",
        "172.18.0.0/16": "docker"
    },
    "groups": [
        {
            "name": "lan",
            "enabled": true,
            "translateReverseLookups": true,
            "externalToInternalTranslation": {}
        },
        {
            "name": "tailnet",
            "enabled": true,
            "translateReverseLookups": true,
            "externalToInternalTranslation": {}
        },
        {
            "name": "docker",
            "enabled": true,
            "translateReverseLookups": true,
            "externalToInternalTranslation": {}
        }
    ]
}
```

# DNS APP Record

**App Name:** Split Horizon
**Class Path:** SplitHorizon.SimpleAddress
**Record Data:**
```json
{
  "10.0.0.0/24": [
    "10.0.0.5"
  ],
  "100.64.0.0/10": [
    "100.109.151.81"
  ],
  "172.18.0.0/16": [
    "10.0.0.5"
  ]
}
```
