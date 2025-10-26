import os
import shutil
from pathlib import Path


def overlay_copy(src: Path, dst: Path) -> None:
    for root, dirs, files in os.walk(src):
        r = Path(root)
        rel = r.relative_to(src)
        target_dir = dst / rel
        target_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            s = r / f
            d = target_dir / f
            shutil.copy2(s, d)


def main() -> int:
    # This script is intended to be run from repoRoot/miscDepsJp
    cwd = Path.cwd()
    src = cwd / "source"
    # Destination is the repository root 'source' directory
    dst = cwd.parent / "source"

    # Copy all files under miscDepsJp/source as-is into repo source.
    # Any content policy (e.g. not placing espeak-data here) is enforced at repo level.
    if not src.exists():
        print(f"[ERROR] JP overlay source not found: {src}")
        print("        Ensure miscDepsJp/source exists in this working tree.")
        return 2
    # Perform the copy
    overlay_copy(src, dst)
    # Basic sanity check for common JP assets to catch partial/missing payloads early
    # Only check for files expected to be provided by overlay payload.
    # libopenjtalk.dll may be built/installed by separate jtalk build steps.
    must_exist = [
        dst / "synthDrivers" / "jtalk" / "libmecab.dll",
    ]
    missing = [str(p) for p in must_exist if not p.exists()]
    if missing:
        print("[ERROR] JP overlay completed but required files are missing:")
        for m in missing:
            print(f"        {m}")
        print("        Verify miscDepsJp/source contains jtalk DLLs and try again.")
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

