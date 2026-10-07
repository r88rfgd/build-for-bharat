#!/usr/bin/env python3
"""SkillLens server. Run:  python server.py   then open http://localhost:8000
Serves this folder (html + csv), forwards AI / news requests from your machine,
and saves your settings (AI provider, model, API keys) to config.json next to this file."""
import json, os, urllib.request, urllib.error
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

PORT = int(os.environ.get("PORT", 8000))
ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.environ.get("SKILLLENS_CONFIG", os.path.join(ROOT, "config.json"))
LOCAL = ("localhost", "127.0.0.1")


def read_config():
    try:
        with open(CONFIG, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def write_config(cfg):
    tmp = CONFIG + ".tmp"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)  # keys stay private to you
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    os.replace(tmp, CONFIG)
    try:
        os.chmod(CONFIG, 0o600)
    except OSError:
        pass


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def local_only(self):
        # Blocks DNS-rebinding: only accept requests addressed to localhost
        return self.headers.get("Host", "").split(":")[0] in LOCAL

    def origin_ok(self):
        # Blocks other websites from posting to this server from your browser
        o = self.headers.get("Origin")
        return not o or urlparse(o).hostname in LOCAL

    def reply(self, code, data, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def body(self):
        n = int(self.headers.get("Content-Length", 0))
        if n > 2_000_000:
            raise ValueError("body too large")
        return self.rfile.read(n)

    def do_GET(self):
        if not self.local_only():
            return self.send_error(403)
        path = urlparse(self.path).path
        if path == "/ping":
            return self.reply(200, b"ok", "text/plain")
        if path == "/config":
            return self.reply(200, json.dumps(read_config()).encode())
        if os.path.basename(path).startswith("config.json"):
            return self.send_error(404)  # never serve the key file as a static file
        if path in ("", "/"):
            self.send_response(302)
            self.send_header("Location", "/skilllens-studio.html")
            return self.end_headers()
        super().do_GET()

    def do_POST(self):
        if not self.local_only() or not self.origin_ok():
            return self.send_error(403)
        if self.path == "/config":
            try:
                if "application/json" not in self.headers.get("Content-Type", ""):
                    raise ValueError("JSON only")
                cfg = json.loads(self.body())
                if not isinstance(cfg, dict):
                    raise ValueError("config must be an object")
                write_config(cfg)
                return self.reply(200, b'{"ok":true}')
            except Exception as e:
                return self.reply(400, json.dumps({"error": {"message": str(e)}}).encode())
        if self.path != "/proxy":
            return self.send_error(404)
        try:
            req = json.loads(self.body())
            body = req.get("body")
            r = urllib.request.Request(
                req["url"],
                data=body.encode() if body else None,
                method=req.get("method", "GET"),
                headers={"User-Agent": "SkillLens/1.0", **req.get("headers", {})},
            )
            try:
                with urllib.request.urlopen(r, timeout=600) as res:
                    code, data = res.status, res.read()
            except urllib.error.HTTPError as e:
                code, data = e.code, e.read()
        except Exception as e:
            code, data = 502, json.dumps({"error": {"message": str(e)}}).encode()
        self.reply(code, data)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"SkillLens running at http://localhost:{PORT}  (Ctrl+C to stop)")
    print(f"Settings file: {CONFIG} ({'found' if os.path.exists(CONFIG) else 'will be created on first run'})")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()