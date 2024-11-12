import os
import dotenv
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from urllib3.util.retry import Retry
from discord_webhook import DiscordWebhook

dotenv.load_dotenv()
URL: str = os.getenv('WEBHOOK')
AVATAR: str = os.getenv('AVATAR')
avatar_url = "https://minotar.net/avatar/{name}/100"
mc_url = "http://localhost:{port}{path}"


def create_message(message: str, target=None, name: str = "BridgeBot"):
    return {"name": name, "message": message, "target": target}


def send_message_discord(message, avatar=True):
    if avatar:
        DiscordWebhook(url=URL, content=message["message"], username=message["name"],
                       avatar_url=avatar_url.format(name=message["name"])).execute()
    else:
        DiscordWebhook(url=URL, content=message["message"], username=message["name"], avatar_url=AVATAR).execute()


def get_status(mc_port):
    session = requests.Session()
    retry = Retry(
        total=3,  # num of retrt
        backoff_factor=0.2,  # wait time before retry
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


def send_message_minecraft(name: str, message: str, mc_port: int, target=None):
    requests.post(mc_url.format(port=mc_port, path="/message"), json=create_message(message=message, name=name, target=target))
