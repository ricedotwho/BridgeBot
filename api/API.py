import json
import uuid
from typing import Any

import dotenv
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from urllib3.util.retry import Retry
from discord_webhook import DiscordWebhook
from Config import getAvatar, getApiKey, getWebhook

dotenv.load_dotenv()
avatar_url = "https://minotar.net/avatar/{name}/100"
mc_url = "http://localhost:{port}{path}"


def create_object(**kwargs):
    if 'ApiKey' in kwargs:
        kwargs['Api-Key'] = kwargs.pop('ApiKey')
    return kwargs


def send_message_discord(message, avatar=True):
    if avatar:
        DiscordWebhook(url=getWebhook(), content=message["message"], username=message["name"],
                       avatar_url=avatar_url.format(name=message["name"])).execute()
    else:
        DiscordWebhook(url=getWebhook(), content=message["message"], username=message["name"], avatar_url=getAvatar()).execute()


def get_status(mc_port):
    session = requests.Session()
    retry = Retry(
        total=1,  # num of retrt
        status_forcelist=[500, 502, 503, 504]  # ignored errors
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)

    try:
        response = session.get(mc_url.format(port=mc_port, path="/status"))
        if response.status_code == 200:
            return True  # great success
        else:
            return False  # response but not ok

    except ConnectionError:
        return False  # api is offline


def get_online(mc_port) -> list[Any]:
    session = requests.Session()
    retry = Retry(
        total=1,  # num of retrt
        status_forcelist=[500, 502, 503, 504]  # ignored errors
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)

    try:
        response = session.get(mc_url.format(port=mc_port, path="/online"))
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return []  # response but not ok

    except ConnectionError:
        return []  # api is offline


def send_message_minecraft(name: str, message: str, mc_port: int, target: str = "all"):
    requests.post(mc_url.format(port=mc_port, path="/message"),
                  json=create_object(message=message, name=name, target=target))


def send_command_minecraft(command: str, mc_port: int):
    requests.post(mc_url.format(port=mc_port, path="/command"),
                  json=create_object(command=command, ApiKey=getApiKey()))
