"""This module will contain all needed slack-deleter-message settings."""

# Slack Legacy token, create here: https://api.slack.com/custom-integrations/legacy-tokens
TOKEN = ''

# The channel ID or Name
CHANNEL = ''

# How many messages should be deleted? Current max is 1000 each run (Limitation of the api)
MESSAGE_DELETE_COUNT = 1000

# If you don't want any interaction while running the module and just use the settings, set this to True
NON_INTERACTIVE = False
