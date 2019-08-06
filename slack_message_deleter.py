"""This module contains the SlackAPI which can delete messages from a given channel."""

import requests
import json
import logging
import time

from local_settings import LEGACY_TOKEN, CHANNEL, MESSAGE_DELETE_COUNT

# Added for Python 2 compatibility
try:
    get_input = raw_input
except NameError:
    get_input = input

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger('slack_logging')


class SlackAPI:

    BASE_API_URL = 'https://slack.com/api/'
    CHANNELS_API_URL = '{base_url}channels.list?token={token}'
    GROUP_API_URL = '{base_url}groups.list?token={token}'
    HISTORY_API_URL = '{base_url}{channel_api}.history?token={token}&count={message_count}&channel={channel}'
    DELETE_API_URL = '{base_url}chat.delete?token={token}&channel={channel}&ts={ts}'
    CHANNELS_BY_NAME = {}
    CHANNELS_BY_ID = {}
    CHANNEL = ''
    IS_PRIVATE_CHANNEL = False
    MESSAGE_COUNT = 1000
    MESSAGES = []

    def __init__(self, token):
        self.TOKEN = token

    @property
    def get_channel_api_url(self):
        return self.CHANNELS_API_URL.format(base_url=self.BASE_API_URL, token=self.TOKEN)

    @property
    def get_group_api_url(self):
        return self.GROUP_API_URL.format(base_url=self.BASE_API_URL, token=self.TOKEN)

    @property
    def get_history_api_url(self):
        channel_api = 'groups' if self.IS_PRIVATE_CHANNEL else 'channels'
        return self.HISTORY_API_URL.format(base_url=self.BASE_API_URL, channel_api=channel_api, token=self.TOKEN,
                                           message_count=self.MESSAGE_COUNT, channel=self.CHANNEL)

    def get_delete_api_url(self, ts):
        return self.DELETE_API_URL.format(base_url=self.BASE_API_URL, token=self.TOKEN, channel=self.CHANNEL, ts=ts)

    def get_private_and_public_channels(self):
        # Start getting private channels, through groups
        response = requests.get(self.get_group_api_url)
        groups = json.loads(response.content)['groups']
        for group in groups:
            if group['topic']['value'] != 'Group messaging':
                self.CHANNELS_BY_NAME[group['name']] = {'id': group['id'], 'is_private': True}
                self.CHANNELS_BY_ID[group['id']] = {'id': group['id'], 'is_private': True}

        # Get all public channels
        response = requests.get(self.get_channel_api_url)
        public_channels = json.loads(response.content)['channels']
        for public_channel in public_channels:
            self.CHANNELS_BY_NAME[public_channel['name']] = {'id': public_channel['id'], 'is_private': False}
            self.CHANNELS_BY_ID[public_channel['id']] = {'id': public_channel['id'], 'is_private': False}

    def get_channel_messages(self):
        response = requests.get(self.get_history_api_url)
        messages = json.loads(response.content)['messages']
        return messages

    def delete_channel_messages(self, messages):
        logger.info('Starting deletion of {messages} messages in channel {channel}'.format(messages=len(messages),
                                                                                           channel=self.CHANNEL))
        for message in messages:
            try:
                url = self.get_delete_api_url(message)
                requests.get(url)
                logger.info('Deleted: {message}'.format(message=message))
            except Exception as error:
                logger.error('Got an error: {error}'.format(error=error))

    def set_channel_to_delete(self):
        """Ask the user which channel to use for deleting messages."""
        while not self.CHANNEL:
            channel = get_input('\nEnter Channel Name or ID: ') if not CHANNEL else CHANNEL

            try:
                fetched_channel = self.CHANNELS_BY_NAME.get(channel)
                fetched_channel = fetched_channel if fetched_channel else self.CHANNELS_BY_ID.get(channel)
                self.CHANNEL = fetched_channel.get('id')
                self.IS_PRIVATE_CHANNEL = fetched_channel.get('is_private')
            except AttributeError:
                logger.error('Invalid channel entered!')

if __name__ == "__main__":
    legacy_token = get_input('Enter slack token: ') if not LEGACY_TOKEN else LEGACY_TOKEN

    slack_api = SlackAPI(legacy_token)
    slack_api.get_private_and_public_channels()
    for channel_name in slack_api.CHANNELS_BY_NAME:
        logger.info('Name: {channel_name}, ID: {id}, Private Channel: {is_private}'.format(
            channel_name=channel_name,
            id=slack_api.CHANNELS_BY_NAME[channel_name].get("id"),
            is_private=slack_api.CHANNELS_BY_NAME[channel_name].get("is_private")))

    slack_api.set_channel_to_delete()

    # Get the number of messages
    while True:
        delete_count = get_input('How many messages to delete? {count}: '.format(count=MESSAGE_DELETE_COUNT))
        try:
            delete_count = int(delete_count) if delete_count else MESSAGE_DELETE_COUNT
            break
        except ValueError:
            logger.error('Invalid Value\n')
            continue

    messages_to_delete = [message.get('ts') for message in slack_api.get_channel_messages()[:delete_count]]

    logger.info('Found: {count} messages...'.format(count=len(messages_to_delete)))
    while messages_to_delete:
        slack_api.delete_channel_messages(messages_to_delete)
        messages_in_channel = [message.get('ts') for message in slack_api.get_channel_messages()]
        logger.info('Ensure that all messages are deleted.')
        messages_to_delete = list(set(messages_to_delete) & set(messages_in_channel))
        if messages_to_delete:
            logger.info('Cooling down api, since {count} messages still there!'.format(count=len(messages_to_delete)))
            time.sleep(5)
    logger.info('Finished deleting messages')

