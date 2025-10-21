#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path


def run_cmd(cmd: list[str]) -> None:
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        # Propagate the exit code for CI to fail fast
        sys.exit(e.returncode or 1)


def main() -> int:
    # Ensure we run from the repository root
    repo_root = Path(__file__).resolve().parents[1]
    os.chdir(repo_root)

    # 1) Run the existing nonCertBuild1.cmd (no args)
    run_cmd(["cmd", "/c", "jptools\\nonCertBuild1.cmd"])

    # 2) Run nonCertBuild2.cmd, forwarding all scons args
    # Accept arguments after '--' from the workflow step, but allow any argv
    forwarded_args = sys.argv[1:]
    cmd = ["cmd", "/c", "jptools\\nonCertBuild2.cmd"] + forwarded_args
    run_cmd(cmd)
    return 0


if __name__ == "__main__":
    sys.exit(main())

