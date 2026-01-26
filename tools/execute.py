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
    try:
        print("[*] Installing via apt...")
        run_cmd(["apt", "update"], require_root=True)
        run_cmd(["apt", "install", "-y", *packages], require_root=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error installing packages via apt: {e}")
        sys.exit(1)

def pipx_install(packages: list[str]):
    """
    Install Python CLI tools via pipx for all users (including root),
    with strict Python version pinning and venv recreation.
    """
    if not packages:
        return

    # ---- Python pinning (CRITICAL) ----
    PIPX_PYTHON_MAP = {
        "penelope": "python3.11",
        "bloodyad": "python3.11",
    }

    DEFAULT_PYTHON = "python3.11"

    # ---- Ensure dependencies ----
    if not command_exists("pipx"):
        run_cmd(["apt", "install", "-y", "pipx"], require_root=True)

    # Ensure compatible Python exists
    run_cmd(
        ["apt", "install", "-y", "python3.11", "python3.11-venv"],
        require_root=True,
    )

    users = []

    for home in Path("/home").iterdir():
        if home.is_dir():
            users.append((home.name, home))

    users.append(("root", Path("/root")))

    print("[*] Installing pipx packages (fresh venvs, pinned Python)...")

    for username, home in users:
        print(f"  └─ User: {username}")

        if username != "root":
            run_cmd(["sudo", "-u", username, "mkdir", "-p", f"{home}/.local"])
            run_cmd(
                ["chown", "-R", f"{username}:{username}", f"{home}/.local"],
                require_root=True,
            )

        for pkg in packages:
            python_bin = PIPX_PYTHON_MAP.get(pkg, DEFAULT_PYTHON)

            uninstall_cmd = ["pipx", "uninstall", pkg]
            install_cmd = [
                "pipx",
                "install",
                "--python",
                python_bin,
                pkg,
            ]

            if username == "root":
                # Ignore uninstall failures
                run_cmd(uninstall_cmd, check=False)
                run_cmd(install_cmd)
            else:
                run_cmd(["sudo", "-u", username] + uninstall_cmd, check=False)
                run_cmd(["sudo", "-u", username] + install_cmd)

    print("[+] pipx packages installed with correct Python versions")

def git_clone(repos: dict[str, str]):
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

def wget_download(files: dict[str, str], base_dir: str = "/opt"):
    """
    Download files using wget into their own directories.

    files = {
        "tool-name": "https://example.com/file"
    }
    """
    base_path = Path(base_dir)
    base_path.mkdir(parents=True, exist_ok=True)

    print(f"[*] Downloading files into {base_path}")

    for name, url in files.items():
        tool_dir = base_path / name
        tool_dir.mkdir(parents=True, exist_ok=True)

        filename = url.split("/")[-1]
        output_file = tool_dir / filename

        print(f"[+] Downloading {name} -> {output_file}")

        cmd = ["wget", "-O", str(output_file), url]
        run_cmd(cmd)

# ---------- more complex tools ----------

def install_vscode():
    """
    Install Visual Studio Code.
    """
    print("[*] Installing Visual Studio Code...")

    vscode_dir = "/opt/vscode"
    vscode_deb = f"{vscode_dir}/vscode.deb"

    run_cmd(["mkdir", "-p", vscode_dir], require_root=True)

    run_cmd([
        "wget",
        "-O",
        vscode_deb,
        "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
    ], require_root=True)

    # Install the .deb properly
    run_cmd(["apt", "install", "-y", f"{vscode_deb}"], require_root=True)

    # Fix any missing deps just in case
    run_cmd(["apt", "-f", "install", "-y"], require_root=True)

    print("[+] Visual Studio Code installed")

