import json
import tempfile
from pathlib import Path

from yukichan_bot.plugin_loader import get_plugin_config, load_enabled_plugins


def test_get_plugin_config_creates_defaults():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        plugins_dir = tmp_path / "plugins"
        plugins_dir.mkdir()
        (plugins_dir / "plugin_a").mkdir()
        (plugins_dir / "plugin_b").mkdir()
        (plugins_dir / "__pycache__").mkdir()

        config_path = tmp_path / "data" / "plugins_config.json"

        config = get_plugin_config(plugins_dir=plugins_dir, config_path=config_path)

        assert config_path.exists()
        assert config == {"plugin_a": True, "plugin_b": True}

        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data == {"plugin_a": True, "plugin_b": True}


def test_get_plugin_config_respects_disabled_plugins():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        plugins_dir = tmp_path / "plugins"
        plugins_dir.mkdir()
        (plugins_dir / "plugin_a").mkdir()
        (plugins_dir / "plugin_b").mkdir()

        config_path = tmp_path / "data" / "plugins_config.json"
        config_path.parent.mkdir()
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump({"plugin_a": True, "plugin_b": False}, f)

        config = get_plugin_config(plugins_dir=plugins_dir, config_path=config_path)
        assert config["plugin_a"] is True
        assert config["plugin_b"] is False


def test_load_enabled_plugins_skips_disabled(monkeypatch):
    loaded_modules = []

    def mock_load_plugin(module_name: str):
        loaded_modules.append(module_name)

    monkeypatch.setattr("nonebot.load_plugin", mock_load_plugin)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        plugins_dir = tmp_path / "plugins"
        plugins_dir.mkdir()
        (plugins_dir / "alipay").mkdir()
        (plugins_dir / "chess").mkdir()

        config_path = tmp_path / "data" / "plugins_config.json"
        config_path.parent.mkdir()
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump({"alipay": True, "chess": False}, f)

        loaded = load_enabled_plugins(plugins_dir=plugins_dir, config_path=config_path)
        assert loaded == ["alipay"]
        assert loaded_modules == ["yukichan_bot.plugins.alipay"]
