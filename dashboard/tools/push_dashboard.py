#!/usr/bin/env python3

import subprocess
import sys

# Default commit message if none is passed
DEFAULT_MESSAGE = "Update dashboard data and scripts"

def run(cmd):
    """Run a shell command and print it"""
    print(f"🔧 {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("❌ Command failed.")
        sys.exit(result.returncode)

def main():
    commit_msg = " ".join(sys.argv[1:]) or DEFAULT_MESSAGE

    # Stage dashboard files
    run("git add dashboard/")

    # Commit
    run(f'git commit -m "{commit_msg}"')

    # Push
    run("git push")

if __name__ == "__main__":
    main()