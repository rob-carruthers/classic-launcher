import configparser
import logging
from pathlib import Path

from xdg_base_dirs import xdg_data_dirs, xdg_data_home

from .config import get_config
from .types import DesktopEntry

logger = logging.getLogger(__name__)


def main() -> None:
    desktop_dirs = [*xdg_data_dirs(), xdg_data_home()]
    application_dirs: list[Path] = [Path(d) / "applications" for d in desktop_dirs]

    for application_dir in application_dirs:
        for file in application_dir.glob("*.desktop"):
            parser = configparser.ConfigParser(interpolation=None)
            parser.read(file)
            desktop_entry = DesktopEntry(**parser["Desktop Entry"])  # ty:ignore[invalid-argument-type]

    launcher_config = get_config()


if __name__ == "__main__":
    main()
