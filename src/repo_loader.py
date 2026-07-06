import subprocess
import sys


def main():
    # Simple script to clone a Git repository from the URL given on the command line.
    if len(sys.argv) < 2:
        print("Usage: python repo_loader.py <git-repo-url>")
        return

    repo_url = sys.argv[1]

    try:
        subprocess.run(["git", "clone", repo_url], check=True)
        print("Repository cloned successfully.")
    except subprocess.CalledProcessError:
        print("Git clone failed. Check the repository URL or your Git installation.")
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    main()
