import asyncio
import os
import platform
import time
from datetime import datetime, timedelta

import cpuinfo
import psutil
from muicebot.muice import Muice
from muicebot.utils.utils import get_version
from nonebot import __version__, get_bot, get_driver

from .config import plugin_config

muice = Muice()
driver = get_driver()
START_TIME = time.time()


def get_run_time() -> str:
    """
    获取 Muicebot 运行时间
    """
    now = time.time()
    return str(timedelta(seconds=int(now - START_TIME)))


def get_system_info() -> str:
    """
    获取系统版本信息，如: `Windows 11` `Ubuntu 24.04.1 LTS`
    """
    system = platform.system()

    if system == "Windows":
        release = platform.release()
        version = platform.version().split(".")[-1]
        # Windows 11
        if int(version) > 22000:
            release = "11"
        return f"Windows {release}"

    elif system == "Linux":
        try:
            # 读取标准的 os-release 文件
            with open("/etc/os-release", "r") as f:
                lines = f.readlines()
            info = {}
            for line in lines:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    info[k] = v.strip('"')
            name = info.get("PRETTY_NAME") or (info.get("NAME", "Linux") + " " + info.get("VERSION", ""))
            return name
        except Exception:
            return "Linux"

    elif system == "Darwin":
        mac_ver = platform.mac_ver()[0]
        return f"macOS {mac_ver}"

    else:
        return system


def get_cpu_info() -> str:
    """
    获得 CPU 品牌，如 `AMD Ryzen 9 7940HX with Radeon Graphics`
    """
    info = cpuinfo.get_cpu_info()
    return info.get("brand_raw", "Unknown CPU")


def get_cpu_percent() -> str:
    """
    获得 CPU 使用百分比信息
    """
    cpu_usage = psutil.cpu_percent() / 100
    return f"{cpu_usage:.0%}"


def get_memory_info() -> str:
    mem = psutil.virtual_memory()
    used = mem.total - mem.available
    used_gb = used / (1024**3)
    total_gb = mem.total / (1024**3)
    return f"{used_gb:.1f}/{total_gb:.1f} GB"


def get_memory_percent() -> str:
    mem = psutil.virtual_memory()
    mem_used = mem.total - mem.available
    mem_percent = mem_used / mem.total
    return f"{mem_percent:.0%}"


def get_disk_usage():
    target_disk = os.path.abspath(os.getcwd())
    usage = psutil.disk_usage(target_disk)
    used = usage.used / (1024**3)
    total = usage.total / (1024**3)
    return f"{used:.1f}/{total:.0f} GB"


async def get_token_usage() -> str:
    """
    获取 token 用量信息
    """
    today_count, total_count = await muice.database.get_model_usage()
    return f"{today_count} tokens (总 {total_count} tokens)"


async def get_conv_count() -> str:
    """
    获取总对话次数
    """
    today_count, total_count = await muice.database.get_conv_count()
    return f"{today_count} 次 (总 {total_count} 次)"


def _format_speed(bps):
    if bps >= 1024**2:
        return f"{bps / 1024 ** 2:.2f} M/s"
    elif bps >= 1024:
        return f"{bps / 1024:.2f} K/s"
    else:
        return f"{bps:.0f} B/s"


async def get_network_send() -> str:
    """
    获取网络上传信息
    """
    net1 = psutil.net_io_counters()
    await asyncio.sleep(0.5)
    net2 = psutil.net_io_counters()

    upload_speed = (net2.bytes_sent - net1.bytes_sent) / 0.5

    return _format_speed(upload_speed)


async def get_network_recv() -> str:
    """
    获取网络下行信息
    """
    net1 = psutil.net_io_counters()
    await asyncio.sleep(0.5)
    net2 = psutil.net_io_counters()

    download_speed = (net2.bytes_recv - net1.bytes_recv) / 0.5

    return _format_speed(download_speed)


async def get_info() -> dict:
    model_name = muice.model_config.model_name or "Unknown"
    return {
        "avatar": plugin_config.avatar_url,
        "background": plugin_config.backgroud_url,
        "nickname": plugin_config.nickname,
        "adapter": get_bot().adapter.get_name(),
        "run_time": get_run_time(),
        "model_name": model_name,
        "model": f"{model_name} {'(多模态)' if muice.model_config.multimodal else ''}",
        "loader": muice.model_config.loader or "(未加载)",
        "count": await get_conv_count(),
        "tokens": await get_token_usage(),
        "system": get_system_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_usage(),
        "cpu_percent": get_cpu_percent(),
        "memory_usage": get_memory_percent(),
        "network_send": await get_network_send(),
        "network_recv": await get_network_recv(),
        "nb_version": __version__,
        "version": get_version()[:10],
        "time": datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"),
    }
