from agentsrc.providers.pypi import PyPIClient


def test_fetch_real_pypi_metadata():
    client = PyPIClient()
    # Use a real immutable package and version for the real network test
    manifest = client.get_package_metadata("colorama", "0.4.6")

    assert manifest.name == "colorama"
    assert manifest.version == "0.4.6"
    assert "packagetype" in manifest.source_type or manifest.source_type in (
        "sdist",
        "bdist_wheel",
        "unknown",
    )
    assert manifest.artifact_url.startswith("https://files.pythonhosted.org/")

    # Check the known SHA256 of colorama 0.4.6
    assert isinstance(manifest.artifact_hash, str)
    assert len(manifest.artifact_hash) > 10
