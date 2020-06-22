import requests
import websocket
import sys
import json
import random


def setup_header(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 '
                      'Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36 '
    }
    return headers


def set_nickname(token, guildid, nickname):
    payload = {'nick': nickname}
    src = requests.patch(f'https://canary.discordapp.com/api/v6/guilds/{guildid}/members/@me/nick',
                         headers=setup_header(token),
                         json=payload, timeout=10)


def set_game(token, game, type, status='online', twitchlink='twitch.com'):
    if status == "random":
        stat = ['online', 'dnd', 'idle']
        status = random.choice(stat)

    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")
    if type == "Playing":
        gamejson = {
            "name": game,
            "type": 0
        }
    elif type == 'Streaming':
        gamejson = {
            "name": game,
            "type": 1,
            "url": twitchlink
        }
    elif type == "Listening to":
        gamejson = {
            "name": game,
            "type": 2
        }
    elif type == "Watching":
        gamejson = {
            "name": game,
            "type": 3
        }
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": sys.platform,
                "$browser": "DiscordRebel.py",
                "$device": f"{sys.platform} Device"
            },
            "presence": {
                "game": gamejson,
                "status": status,
                "since": 0,
                "afk": False
            }
        },
        "s": None,
        "t": None
    }

    ws.send(json.dumps(auth))


def get_account_info(token):
    src = requests.get('https://discordapp.com/api/v6/users/@me', headers=setup_header(token), timeout=10)
    response = json.loads(src.content)
    info = {'username': response['username'], 'discriminator': response['discriminator'], 'id': response['id'],
            'email': response['email'], 'phone': response['phone'], 'language': response['locale'],
            'verified': response['verified']}
    return info


def send_message(token, message, channelid):
    payload = {"content": message}
    requests.post(f'https://discord.com/api/v6/channels/{channelid}/messages', json=payload,
                  headers=setup_header(token))


def send_dm(token, message, userid):
    payload = {'recipient_id': userid}
    src = requests.post('https://canary.discordapp.com/api/v6/users/@me/channels', headers=setup_header(token),
                        json=payload,
                        timeout=10)
    dm_json = json.loads(src.content)
    payload = {"content": message}
    src = requests.post(f"https://canary.discordapp.com/api/v6/channels/{dm_json['id']}/messages", headers=setup_header(token),
                       json=payload, timeout=10)
