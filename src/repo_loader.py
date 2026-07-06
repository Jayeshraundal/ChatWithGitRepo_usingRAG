import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_EXTENSIONS = {
    ".md",
    ".py",
    ".java",
    ".c",
    ".cpp",
    ".js",
    ".ts",
    ".json",
    ".yml",
    ".yaml",
    ".txt",
    ".html",
    ".css",
}
EXCLUDED_DIRS = {"node_modules", ".venv", "__pycache__", ".git"}
DEFAULT_REPOS_DIR = Path("data/repos")


def get_repo_name(repo_url: str) -> str:
    parsed_url = urlparse(repo_url.strip())
    repo_name = Path(parsed_url.path).name
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]
    return repo_name or "repo"


def _remove_readonly(func, path, exc_info):
    os.chmod(path, 0o666)
    func(path)


def clean_repo(repo_path: Path) -> None:
    for excluded in EXCLUDED_DIRS:
        excluded_path = repo_path / excluded
        if excluded_path.exists():
            if excluded_path.is_dir():
                shutil.rmtree(excluded_path, onerror=_remove_readonly)
            else:
                try:
                    excluded_path.unlink()
                except PermissionError:
                    os.chmod(excluded_path, 0o666)
                    excluded_path.unlink()

    for path in repo_path.rglob("*"):
        if path.is_file():
            if path.suffix.lower() not in ALLOWED_EXTENSIONS:
                try:
                    path.unlink()
                except PermissionError:
                    os.chmod(path, 0o666)
                    path.unlink()

    for path in sorted((p for p in repo_path.rglob("*") if p.is_dir()), key=lambda p: len(str(p)), reverse=True):
        if not any(path.iterdir()):
            try:
                path.rmdir()
            except PermissionError:
                os.chmod(path, 0o777)
                path.rmdir()


def clone_repo(repo_url: str) -> Path:
    repo_name = get_repo_name(repo_url)
    repo_path = DEFAULT_REPOS_DIR / repo_name
    DEFAULT_REPOS_DIR.mkdir(parents=True, exist_ok=True)

    if repo_path.exists():
        print(f"Repository already exists at: {repo_path}")
        return repo_path

    print(f"Cloning into: {repo_path}")
    subprocess.run(["git", "clone", "--depth", "1", repo_url, str(repo_path)], check=True)
    clean_repo(repo_path)
    return repo_path


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python repo_loader.py <git-repo-url>")
        return

    repo_url = sys.argv[1]

    try:
        repo_path = clone_repo(repo_url)
        print(f"Repository ready in: {repo_path}")
    except subprocess.CalledProcessError:
        print("Git clone failed. Check the repository URL or your Git installation.")
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    main()
