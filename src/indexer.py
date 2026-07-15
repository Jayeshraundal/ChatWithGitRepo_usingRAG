from pathlib import Path
from typing import Dict, List

from repo_loader import ALLOWED_EXTENSIONS, RepositoryLoader


def load_repo_files(repo_path: Path) -> List[Dict[str, str]]:
    """Load supported files from a cloned repository.

    Each returned document contains the repo name, relative path, and file text.
    """
    documents: List[Dict[str, str]] = []

    for path in sorted(repo_path.rglob("*")):
        if not path.is_file():
            continue

        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        documents.append({
            "repo": repo_path.name,
            "path": str(path.relative_to(repo_path)),
            "text": text,
        })

    return documents


def index_repo(repo_url: str) -> None:
    repo_path = RepositoryLoader.clone_repo(repo_url)
    print(f"Repository ready in: {repo_path}")

    documents = load_repo_files(repo_path)
    print(f"Loaded {len(documents)} supported files from the repository")

    for doc in documents[:5]:
        print(f"- {doc['path']} ({len(doc['text'])} chars)")

    print("Now you can split these documents into chunks, embed them, and save the index.")
