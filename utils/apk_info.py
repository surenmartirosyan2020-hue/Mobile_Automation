from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path


def _find_aapt_tools() -> list[str]:
    tools: list[str] = []
    for name in ("aapt", "aapt2"):
        found = shutil.which(name)
        if found:
            tools.append(found)

    sdk = Path.home() / "AppData" / "Local" / "Android" / "Sdk" / "build-tools"
    if sdk.exists():
        versions = sorted(
            [p for p in sdk.iterdir() if p.is_dir()],
            key=lambda p: p.name,
            reverse=True,
        )
        for version_dir in versions:
            for name in ("aapt.exe", "aapt", "aapt2.exe", "aapt2"):
                candidate = version_dir / name
                if candidate.exists():
                    tools.append(str(candidate))
            break

    seen: set[str] = set()
    unique: list[str] = []
    for tool in tools:
        if tool not in seen:
            seen.add(tool)
            unique.append(tool)
    return unique


def get_apk_info(apk_path: str | Path) -> dict[str, str]:
    apk = Path(apk_path).resolve()
    if not apk.exists():
        raise FileNotFoundError(f"APK not found: {apk}")

    tools = _find_aapt_tools()
    if not tools:
        raise RuntimeError("aapt/aapt2 not found. Add Android SDK build-tools to PATH.")

    output = ""
    for aapt in tools:
        result = subprocess.run(
            [aapt, "dump", "badging", str(apk)],
            capture_output=True,
            text=True,
            check=False,
        )
        output = result.stdout or result.stderr
        if "package:" in output:
            break
    else:
        raise RuntimeError(f"Failed to read APK info:\n{output}")

    package_match = re.search(r"package: name='([^']+)'", output)
    activity_match = re.search(
        r"launchable-activity: name='([^']+)'|"
        r"activity: name='([^']+)'",
        output,
    )

    package = package_match.group(1) if package_match else ""
    activity = ""
    if activity_match:
        activity = activity_match.group(1) or activity_match.group(2) or ""

    return {
        "path": str(apk),
        "package": package,
        "activity": activity,
        "raw_snippet": "\n".join(output.splitlines()[:8]),
    }


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("Usage: python -m utils.apk_info <path-to-apk>")
        return 1

    info = get_apk_info(args[0])
    print(f"path:     {info['path']}")
    print(f"package:  {info['package']}")
    print(f"activity: {info['activity'] or ''}")
    print()
    print("app:")
    print(f'  path: "{info["path"].replace(chr(92), "/")}"')
    print(f'  package: "{info["package"]}"')
    print(f'  activity: "{info["activity"]}"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
