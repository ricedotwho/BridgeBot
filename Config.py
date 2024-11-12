import json
import os
import dotenv

env_dir: str = str(os.path.dirname(os.path.abspath(__file__))) + "/.env"
dotenv.load_dotenv()
TOKEN: str = os.getenv('DISCORD_TOKEN')
GUILD_IDS: list = json.loads(os.getenv('GUILD_IDS'))
GUILD_IDS = [int(guild_id) for guild_id in GUILD_IDS]
STATUS: str = os.getenv('STATUS_ID')
ONLINE_COUNT: int = int(os.getenv('ONLINECOUNT_ID'))
BRIDGE: str = os.getenv('BRIDGE_ID')
PERM: int = int(os.getenv('PERM_ROLE_ID'))
MCPORT: int = int(os.getenv('MC_PORT'))


def getStatus():
    return STATUS


def getOnline():
    return ONLINE_COUNT


def getBridge():
    return BRIDGE


def getPerms():
    return PERM


def getMCPort():
    return MCPORT


def changeStatus(new_var: str):
    global STATUS
    STATUS = new_var
    set_env("STATUS_ID", STATUS)


def changeOnlineCount(new_var: int):
    global ONLINE_COUNT
    ONLINE_COUNT = new_var
    set_env("ONLINECOUNT_ID", str(ONLINE_COUNT))


def changeBridge(new_var: str):
    global BRIDGE
    BRIDGE = new_var
    set_env("BRIDGE_ID", BRIDGE)


def changePerms(new_var: int):
    global PERM
    PERM = new_var
    set_env("PERM_ROLE_ID", str(PERM))


def changeMCPort(new_var: int):
    global MCPORT
    MCPORT = new_var
    set_env("MC_PORT", str(MCPORT))


def set_env(key: str, value: str):
    dotenv.set_key(dotenv_path=env_dir, key_to_set=key, value_to_set=value)
