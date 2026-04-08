import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Optional
from urllib.parse import parse_qs, urlparse

from agentsrc.storage.writer import StorageWriter


class SymbolQueryHandler(BaseHTTPRequestHandler):
    """
    Handles JSON API requests for indexed symbols.
    Endpoints:
      GET /packages          - List all synced packages
      GET /package/{name}    - Get manifest for a package
      GET /package/{name}/symbols - Get symbol map for a package
      GET /search?q={query}  - Search symbols across all packages
    """

    def _set_headers(self, status: int = 200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def _send_json(self, data: Any, status: int = 200):
        self._set_headers(status)
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path.strip("/")
        query_params = parse_qs(parsed_url.query)

        # Config used for future extensions (e.g. custom store paths)
        writer = StorageWriter()
        store_path = writer.pypi_dir

        try:
            if path == "packages":
                self._handle_list_packages(store_path)
            elif path.startswith("package/"):
                parts = path.split("/")
                package_name = parts[1]
                if len(parts) == 2:
                    self._handle_get_package(store_path, package_name)
                elif len(parts) == 3 and parts[2] == "symbols":
                    self._handle_get_symbols(store_path, package_name)
                else:
                    self._send_json({"error": "Invalid path"}, 404)
            elif path == "search":
                q = query_params.get("q", [""])[0]
                self._handle_search(store_path, q)
            elif path == "" or path == "health":
                self._send_json({"status": "ok", "version": "0.1.0"})
            else:
                self._send_json({"error": "Not found"}, 404)
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def _handle_list_packages(self, store_path: Path):
        packages = []
        if not store_path.exists():
            self._send_json([])
            return

        for pkg_dir in store_path.iterdir():
            if not pkg_dir.is_dir():
                continue

            # Find latest version or all versions? For v1, we just return the directory names
            # which include versions (e.g. rich/13.7.0)
            for version_dir in pkg_dir.iterdir():
                if not version_dir.is_dir():
                    continue

                manifest_path = version_dir / "manifest.json"
                if manifest_path.exists():
                    try:
                        with open(manifest_path, "r", encoding="utf-8") as f:
                            manifest = json.load(f)
                            packages.append(
                                {
                                    "name": manifest.get("name"),
                                    "version": manifest.get("version"),
                                    "summary": manifest.get("summary"),
                                }
                            )
                    except Exception:
                        pass

        self._send_json(packages)

    def _handle_get_package(self, store_path: Path, package_name: str):
        # Format name/version or just name
        manifest_path = self._find_manifest(store_path, package_name)
        if not manifest_path:
            self._send_json({"error": f"Package {package_name} not found"}, 404)
            return

        with open(manifest_path, "r", encoding="utf-8") as f:
            self._send_json(json.load(f))

    def _handle_get_symbols(self, store_path: Path, package_name: str):
        version_dir = self._find_version_dir(store_path, package_name)
        if not version_dir:
            self._send_json({"error": f"Package {package_name} not found"}, 404)
            return

        symbols_path = version_dir / "symbols.json"
        if not symbols_path.exists():
            self._send_json({"error": "Symbols not yet indexed"}, 404)
            return

        with open(symbols_path, "r", encoding="utf-8") as f:
            self._send_json(json.load(f))

    def _handle_search(self, store_path: Path, query: str):
        results = []
        if not query:
            self._send_json([])
            return

        query = query.lower()
        if not store_path.exists():
            self._send_json([])
            return

        for pkg_dir in store_path.iterdir():
            for version_dir in pkg_dir.iterdir():
                symbols_path = version_dir / "symbols.json"
                if not symbols_path.exists():
                    continue

                try:
                    with open(symbols_path, "r", encoding="utf-8") as f:
                        symbols_data = json.load(f)
                        # Search classes, functions, etc.
                        for category in ["classes", "functions", "exceptions"]:
                            for item in symbols_data.get(category, []):
                                name = item.get("name", "")
                                if query in name.lower():
                                    results.append(
                                        {
                                            "package": pkg_dir.name,
                                            "version": version_dir.name,
                                            "type": category[:-1],  # singular
                                            "name": name,
                                            "docstring": item.get("docstring"),
                                        }
                                    )
                except Exception:
                    continue

        self._send_json(results[:50])  # Limit to 50 results

    def _find_version_dir(self, store_path: Path, package_name: str) -> Optional[Path]:
        """Finds the directory for a package name (possibly containing version)."""
        if "/" in package_name:
            name, version = package_name.split("/", 1)
            path = store_path / name / version
            return path if path.exists() else None

        # If only name given, find latest version dir
        pkg_dir = store_path / package_name
        if not pkg_dir.exists():
            return None

        versions = [d for d in pkg_dir.iterdir() if d.is_dir()]
        if not versions:
            return None

        # Sort by version name for now
        versions.sort(reverse=True)
        return versions[0]

    def _find_manifest(self, store_path: Path, package_name: str) -> Optional[Path]:
        version_dir = self._find_version_dir(store_path, package_name)
        if version_dir:
            manifest_path = version_dir / "manifest.json"
            return manifest_path if manifest_path.exists() else None
        return None


def start_server(host: str, port: int):
    server = ThreadingHTTPServer((host, port), SymbolQueryHandler)
    print(f"Starting agentsrc query server on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.server_close()


if __name__ == "__main__":
    start_server("127.0.0.1", 4319)
