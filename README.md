# Slack Message Deleter
Remove slack messages automatically from s chosen channel.

## How to use

- Clone this repository locally.
- Go to the directory
- Install requirements `pip install -U -r requirements.txt`
- Generate a legacy token: https://api.slack.com/custom-integrations/legacy-tokens

- Add this token in de local_settings.py
- Run `python slack_message_deleter.py`

- The application will ask some questions and start deleting

## Features

- Use a wizard to guide the user when running the code
- Present the user all available channels (public and private)
- Automatically determine if a channel is private


## ToDo:

- Add documentation in code
- Improve this readme file
- Add non-interactive mode
- Add direct messages for deletion
- Add possibility to remove more than 1000 messages each run
- Add package to pypi
