import execute

# ---------- Example Usage ----------

def main():
    apt_packages = [
        "impacket",
        "bloodhound",
        "pspy",
        "cewl",
        "seclists",
        "docker.io",
        "rlwrap",
        "keepassxc",
        "code"
    ]

    pipx_packages = [
        "git-dumper",
        "uploadserver",
        "penelope",
        "bloodyAD",
        "pygpoabuse"
    ]

    git_repos = {
        "rusthound": "https://github.com/NH-RED-TEAM/RustHound.git",
        "runascs": "https://github.com/antonioCoco/RunasCs.git",
        "chisel": "https://github.com/jpillora/chisel.git",
        "ligolo": "https://github.com/nicocha30/ligolo-ng.git",
        "username-anarchy": "https://github.com/urbanadventurer/username-anarchy.git",
        "shcheck": "https://github.com/santoru/shcheck.git",
        "Graph-Runner": "https://github.com/dafthack/GraphRunner.git"
    }

    execute.apt_install(apt_packages)
    execute.pipx_install(pipx_packages)
    execute.git_clone(git_repos)


if __name__ == "__main__":
    main()
