from nonebot import get_plugin_config
from pydantic import BaseModel


class ScopeConfig(BaseModel):
    avatar_url: str = "https://s2.loli.net/2025/04/20/oK6pncNCeWfIyE3.jpg"
    """头像url"""
    backgroud_url: str = "https://s2.loli.net/2025/04/20/nYN2kbs38Xc6zBj.jpg"
    """背景url"""
    nickname: str = "MuikaAI"
    """Bot昵称"""

    priority: int = 5
    """指令优先级"""


class Config(BaseModel):
    status: ScopeConfig = ScopeConfig()


plugin_config = get_plugin_config(Config).status
