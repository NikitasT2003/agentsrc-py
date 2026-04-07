import json
from pathlib import Path
from agentsrc.storage.writer import StorageWriter
from agentsrc.models import PackageManifest

def test_initialize_structure(tmp_path):
    root = tmp_path / ".agentsrc"
    writer = StorageWriter(root_dir=str(root))
    writer.initialize_structure()
    
    assert (root / "pypi").exists()
    assert (root / "cache").exists()

def test_update_sources_index_atomicity(tmp_path):
    root = tmp_path / ".agentsrc"
    writer = StorageWriter(root_dir=str(root))
    writer.initialize_structure()
    
    manifest = PackageManifest(
        name="testpkg",
        version="1.0.0",
        normalized_name="testpkg",
        source_type="sdist",
        artifact_url="http://example.com",
        artifact_filename="testpkg-1.0.0.tar.gz",
        artifact_hash="sha256:123"
    )
    
    # First sync
    writer.update_sources_index(manifest)
    
    with open(root / "sources.json", "r") as f:
        data = json.load(f)
        assert len(data["packages"]) == 1
        assert data["packages"][0]["name"] == "testpkg"

    # Second sync (update)
    manifest.version = "1.1.0"
    writer.update_sources_index(manifest)
    
    with open(root / "sources.json", "r") as f:
        data = json.load(f)
        assert len(data["packages"]) == 1 # Still 1 package
        assert data["packages"][0]["version"] == "1.1.0"

def test_update_sources_index_corrupt_json(tmp_path):
    root = tmp_path / ".agentsrc"
    writer = StorageWriter(root_dir=str(root))
    writer.initialize_structure()
    
    # Write corrupt JSON
    with open(root / "sources.json", "w") as f:
        f.write("{ corrupt")
        
    manifest = PackageManifest(
        name="testpkg",
        version="1.0.0",
        normalized_name="testpkg",
        source_type="sdist",
        artifact_url="http://example.com",
        artifact_filename="testpkg-1.0.0.tar.gz",
        artifact_hash="sha256:123"
    )
    
    # Should handle gracefully (overwrite or reset)
    writer.update_sources_index(manifest)
    
    with open(root / "sources.json", "r") as f:
        data = json.load(f)
        assert len(data["packages"]) == 1

def test_update_sources_index_path_normalization(tmp_path):
    root = tmp_path / ".agentsrc"
    writer = StorageWriter(root_dir=str(root))
    writer.initialize_structure()
    
    manifest = PackageManifest(
        name="testpkg",
        version="1.0.0",
        normalized_name="testpkg",
        source_type="sdist",
        artifact_url="http://example.com",
        artifact_filename="testpkg-1.0.0.tar.gz",
        artifact_hash="sha256:123"
    )
    
    writer.update_sources_index(manifest)
    
    with open(root / "sources.json", "r") as f:
        data = json.load(f)
        path = data["packages"][0]["path"]
        # On Windows, path.relative_to might use backslashes. 
        # We MUST ensure it's normalized to forward slashes.
        assert "\\" not in path
        assert "/" in path
