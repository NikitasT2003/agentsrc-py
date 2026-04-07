import tarfile
import zipfile
from pathlib import Path


def extract_archive(archive_path: str, target_dir: str, original_filename: str = ""):
    path = Path(archive_path)
    target = Path(target_dir)
    target.mkdir(parents=True, exist_ok=True)

    filename = original_filename or path.name

    if filename.endswith(".zip") or filename.endswith(".whl"):
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(target)
    elif filename.endswith(".tar.gz") or filename.endswith(".tgz"):
        with tarfile.open(path, "r:gz") as tar_ref:
            tar_ref.extractall(target)
    elif filename.endswith(".tar"):
        with tarfile.open(path, "r:") as tar_ref:
            tar_ref.extractall(target)
    else:
        raise ValueError(f"Unsupported archive format: {filename}")
