from functools import wraps

import irc.bot
import requests


def try_method(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        try:
            return f(*args, **kwds)
        except Exception as e:
            print("Endpoint failed - {}".format(e))

    return wrapper


class BotEndpoints(object):
    domain = "https://www.observerurf.com/api/bot-commands/"

    @classmethod
    @try_method
    def bet(cls, user_id, display_name, color, amount):
        resp = requests.get("{}bet/?user_id={}&username={}&color={}&amount={}".format(cls.domain, user_id, display_name,
                                                                                      color, amount))
        return resp.json().get("message")

    @classmethod
    @try_method
    def free(cls, user_id, display_name):
        resp = requests.get("{}free/?user_id={}&username={}".format(cls.domain, user_id, display_name))
        return resp.json().get("message")

    @classmethod
    @try_method
    def commands(cls):
        resp = requests.get("{}text-list/".format(cls.domain))
        return resp.json().get("commands")

    @classmethod
    @try_method
    def balance(cls, user_id, display_name):
        resp = requests.get("{}balance/?user_id={}&username={}".format(cls.domain, user_id, display_name))
        return resp.json().get("message")

    @classmethod
    @try_method
    def game_info(cls):
        resp = requests.get("{}game-info/".format(cls.domain))
        data = resp.json()
        if isinstance(data, list):
            return data[0]
        return data.get("url")


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)
        print("Joined " + self.channel)

    def get_user(self, event):
        user = {}
        for item in event.tags:
            user[item['key']] = item['value']
        return user

    def on_pubmsg(self, socket, event):

        # If a chat message starts with an exclamation point, try to run it as a command
        if event.arguments[0][:1] == '!':
            tmp = event.arguments[0].split(' ')
            cmd = tmp[0][1:].upper()
            self.do_command(event, cmd, tmp[1:])
        return

    def do_command(self, event, cmd, arguments):
        c = self.connection
        user = self.get_user(event)

        if cmd in ["BLUE", "RED"]:
            msg = BotEndpoints.bet(user.get("user-id"), user.get("display-name"), cmd, arguments[0])
        elif cmd == "COMMANDS":
            msg = BotEndpoints.commands()
        elif cmd == "FREE":
            msg = BotEndpoints.free(user.get("user-id"), user.get("display-name"))
        elif cmd == "BALANCE":
            msg = BotEndpoints.balance(user.get("user-id"), user.get("display-name"))
        elif cmd == "GAMEINFO":
            msg = BotEndpoints.game_info()
        else:
            msg = "Sorry {}.  Unknown Command: {}".format(user.get('display-name'), cmd)
        c.privmsg(self.channel, msg)


if __name__ == "__main__":
    username = "xxobserverurfbotxx"
    client_id = "aqzxc0g0rygyfz3990vu4ho14nnkte"
    token = "8qeyxl5dkx1nb77ljm58us8d6lhf64"  # https://twitchapps.com/tmi/
    channel = "observerurf"

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()
