"""Config file parser."""

import tomllib
from pathlib import Path

from xdg_base_dirs import xdg_config_home

from .const import APP_CONFIG
from .datatypes import Category, LauncherConfig


def get_config() -> LauncherConfig:
    """Get config values from .toml file."""
    config_dirs = [Path(), xdg_config_home() / "classic-launcher"]
    configs = [config_dir / APP_CONFIG for config_dir in config_dirs]

    try:
        config = next(c for c in configs if c.exists())
    except StopIteration as e:
        msg = f"No {APP_CONFIG} found in: {configs}"
        raise FileNotFoundError(msg) from e

    with config.open(mode="rb") as f:
        config_dict = tomllib.load(f)

    categories_config: set[Category] = set()
    for k, v in config_dict["categories"].items():
        if any(k == category.name for category in categories_config):
            msg = f"Category {k} duplicated in {config}"
            raise ValueError(msg)
        categories_config.add(Category(k, frozenset(v)))

    config_dict["categories"] = frozenset(categories_config)

    return LauncherConfig(**config_dict)
