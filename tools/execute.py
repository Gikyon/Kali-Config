#!/usr/bin/env python3

import subprocess
import shutil
import sys
from pathlib import Path

# ---------- Helpers ----------

def run_cmd(cmd: list[str], require_root: bool = False):
    """
    Run a shell command safely.
    """
    if require_root and shutil.which("sudo"):
        cmd = ["sudo"] + cmd

    print(f"[+] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def command_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None


# ---------- Install Methods ----------

def apt_install(packages: list[str]):
    """
    Install packages via apt.
    """
    if not packages:
        return

    print("[*] Installing via apt...")
    run_cmd(["apt", "update"], require_root=True)
    run_cmd(["apt", "install", "-y", *packages], require_root=True)


def pipx_install(packages: list[str]):
    """
    Install Python CLI tools via pipx.
    """
    if not packages:
        return

    if not command_exists("pipx"):
        print("[!] pipx not found, installing...")
        run_cmd(["apt", "install", "-y", "pipx"], require_root=True)
        run_cmd(["pipx", "ensurepath"])

    print("[*] Installing via pipx...")
    for pkg in packages:
        run_cmd(["pipx", "install", pkg])


def git_clone(repos: dict[str, str], base_dir: str = "~/tools"):
    """
    Clone GitHub repositories.

    repos = {
        "tool-name": "https://github.com/user/repo.git"
    }
    """
    base_path = Path("/opt")
    base_path.mkdir(parents=True, exist_ok=True)

    print(f"[*] Cloning repositories into {base_path}")

    for name, url in repos.items():
        dest = base_path / name

        if dest.exists():
            print(f"[=] Skipping {name}, already exists")
            continue

        run_cmd(["git", "clone", url, str(dest)])
