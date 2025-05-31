from pathlib import Path

from arclet.alconna import Alconna
from nonebot import require

from .config import plugin_config
from .info import get_info

require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")
require("muicebot")

from muicebot.plugin import PluginMetadata  # noqa: E402
from nonebot_plugin_alconna import CommandMeta, on_alconna  # noqa: E402
from nonebot_plugin_alconna.uniseg import Image as UniImage  # noqa: E402
from nonebot_plugin_alconna.uniseg import UniMessage  # noqa: E402
from nonebot_plugin_htmlrender import template_to_pic  # noqa: E402

__meta__ = PluginMetadata(name="MuiceBot 图片状态插件", description="", usage=".status")

COMMAND_PREFIXES = [".", "/"]

TEMPLATE_PATH = str(Path(__file__).parent / "template")
TEMPLATE_NAME = "index.html.jinja"
TEMPLATE_CSS = Path(__file__).parent / "static" / "css" / "output.css"

command_schedule = on_alconna(
    Alconna(COMMAND_PREFIXES, "status", meta=CommandMeta("Muicebot 图片状态")),
    priority=plugin_config.priority,
    block=True,
)


@command_schedule.handle()
async def status():
    info = await get_info()
    info["inline_css"] = TEMPLATE_CSS.read_text()

    pic = await template_to_pic(
        template_path=TEMPLATE_PATH,
        template_name=TEMPLATE_NAME,
        templates=info,
        pages={"viewport": {"width": 450, "height": 10}},
        wait=2,
    )

    await UniMessage(UniImage(raw=pic)).finish()
