from agentsrc.fetch.cache import CacheManager
from agentsrc.fetch.unpack import extract_archive


def test_cache_manager(tmp_path):
    cache = CacheManager(cache_dir=str(tmp_path))
    assert not cache.is_cached("dummy_hash")

    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")
    # In a real test we'd calculate hash and add it


def test_extract_archive(tmp_path):
    import tarfile

    ar_path = tmp_path / "dummy.tar.gz"
    out_path = tmp_path / "out"
    out_path.mkdir()

    # Create simple tar.gz
    content_file = tmp_path / "file.py"
    content_file.write_text("print('test')")

    with tarfile.open(ar_path, "w:gz") as tar:
        tar.add(content_file, arcname="file.py")

    extract_archive(str(ar_path), str(out_path))
    assert (out_path / "file.py").exists()
