from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    path = config_path or DEFAULT_CONFIG_PATH
    with path.open(encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}

    raw_path = config.get("app", {}).get("path", "")
    if raw_path:
        apk = Path(raw_path)
        if not apk.is_absolute():
            apk = PROJECT_ROOT / apk
        config["app"]["path"] = str(apk.resolve())

    return config
