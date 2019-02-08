# Slack Message Deleter
Remove slack messages automatically from a channel through the Slack API.

## Who should use this?
If you using the free plan and running into the message limit.

Or if you are just as lazy as i am, and just want to cleanup some channels without getting RSI.

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
