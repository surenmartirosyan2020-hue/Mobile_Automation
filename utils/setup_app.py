from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from utils.apk_info import get_apk_info

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"


def _replace_app_block(yaml_text: str, path: str, package: str, activity: str) -> str:
    path_norm = path.replace("\\", "/")
    new_block = (
        "app:\n"
        f'  path: "{path_norm}"\n'
        f'  package: "{package}"\n'
        f'  activity: "{activity}"\n'
    )
    pattern = re.compile(r"^app:\n(?:[ \t].*\n)*", re.MULTILINE)
    if pattern.search(yaml_text):
        return pattern.sub(new_block, yaml_text, count=1)
    return new_block + "\n" + yaml_text


def _replace_device(yaml_text: str, name: str | None, platform: str | None) -> str:
    text = yaml_text
    if name:
        text = re.sub(
            r'(device:\n(?:[ \t].*\n)*?[ \t]name:\s*)"[^"]*"',
            rf'\1"{name}"',
            text,
            count=1,
        )
    if platform:
        text = re.sub(
            r'(device:\n(?:[ \t].*\n)*?[ \t]platform_version:\s*)"[^"]*"',
            rf'\1"{platform}"',
            text,
            count=1,
        )
    return text


def setup_app(
    apk_path: str,
    device_name: str | None = None,
    platform_version: str | None = None,
) -> dict[str, str]:
    info = get_apk_info(apk_path)
    if not info["package"]:
        raise RuntimeError("Could not read package from APK.")
    if not info["activity"]:
        print("WARNING: launchable activity not found, using .MainActivity")
        info["activity"] = ".MainActivity"

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config not found: {CONFIG_PATH}")

    original = CONFIG_PATH.read_text(encoding="utf-8")
    updated = _replace_app_block(
        original, info["path"], info["package"], info["activity"]
    )
    updated = _replace_device(updated, device_name, platform_version)
    CONFIG_PATH.write_text(updated, encoding="utf-8")

    apps_dir = PROJECT_ROOT / "apps"
    apps_dir.mkdir(exist_ok=True)

    return info


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Update config.yaml from APK")
    parser.add_argument("apk", help="Path to .apk file")
    parser.add_argument("--device", default=None, help="Device name")
    parser.add_argument("--platform", default=None, help="Android platform version")
    args = parser.parse_args(argv)

    info = setup_app(args.apk, args.device, args.platform)
    print(f"path:     {info['path']}")
    print(f"package:  {info['package']}")
    print(f"activity: {info['activity']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
