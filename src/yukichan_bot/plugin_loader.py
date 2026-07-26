import json
from pathlib import Path
from typing import Optional

import nonebot
from nonebot.log import logger

DEFAULT_CONFIG_PATH = Path("./data/plugins_config.json")
DEFAULT_PLUGINS_DIR = Path(__file__).parent / "plugins"


def get_plugin_config(
    plugins_dir: Optional[Path] = None, config_path: Optional[Path] = None
) -> dict[str, bool]:
    p_dir = plugins_dir or DEFAULT_PLUGINS_DIR
    c_path = config_path or DEFAULT_CONFIG_PATH

    c_path.parent.mkdir(parents=True, exist_ok=True)

    discovered_plugins = [
        item.name
        for item in p_dir.iterdir()
        if item.is_dir() and not item.name.startswith("_")
    ]
    discovered_plugins.sort()

    config: dict[str, bool] = {}
    if c_path.exists():
        try:
            with open(c_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            logger.warning(f"读取插件配置文件失败: {e}，将使用默认配置")
            config = {}

    updated = False
    for plugin_name in discovered_plugins:
        if plugin_name not in config:
            config[plugin_name] = True
            updated = True

    if updated or not c_path.exists():
        with open(c_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    return config


def load_enabled_plugins(
    plugins_dir: Optional[Path] = None, config_path: Optional[Path] = None
) -> list[str]:
    config = get_plugin_config(plugins_dir, config_path)
    loaded_plugins: list[str] = []

    for plugin_name, enabled in config.items():
        if enabled:
            module_name = f"yukichan_bot.plugins.{plugin_name}"
            try:
                nonebot.load_plugin(module_name)
                loaded_plugins.append(plugin_name)
                logger.info(f"成功加载插件: {plugin_name}")
            except Exception as e:
                logger.error(f"加载插件 {plugin_name} 失败: {e}")
        else:
            logger.info(f"插件已禁用: {plugin_name}")

    return loaded_plugins
