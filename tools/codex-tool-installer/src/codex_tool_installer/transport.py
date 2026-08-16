from __future__ import annotations

import json
import urllib.request
import urllib.error

from .manifest import TOOL_MANIFEST


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _secure_open(request, timeout):
    return urllib.request.build_opener(_NoRedirect).open(request, timeout=timeout)


class HttpMcpTransport:
    def __init__(self, opener=None): self.opener, self.counter, self.sessions = opener or _secure_open, 0, {}

    def request(self, name, method, params, environ):
        if name not in self.sessions:
            self._initialize(name, environ)
        return self._request(name, method, params, environ)

    def _request(self, name, method, params, environ, notification=False):
        definition = TOOL_MANIFEST[name]
        if not str(definition.mcp["url"]).startswith("https://"):
            raise RuntimeError("MCP endpoint must use HTTPS")
        self.counter += 1
        message = {"jsonrpc": "2.0", "method": method, "params": params}
        if not notification:
            message["id"] = self.counter
        body = json.dumps(message).encode()
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        credential_name = definition.credential_env
        if credential_name and environ.get(credential_name):
            headers["Authorization"] = "Bearer " + environ[credential_name]
        if self.sessions.get(name):
            headers["Mcp-Session-Id"] = self.sessions[name]
        request = urllib.request.Request(definition.mcp["url"], data=body, headers=headers, method="POST")
        with self.opener(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            session = response.headers.get("Mcp-Session-Id") if hasattr(response, "headers") else None
            if session:
                self.sessions[name] = session
        if notification and not raw.strip():
            return {}
        if raw.startswith("event:") or "\ndata:" in raw:
            data_lines = [line[5:].strip() for line in raw.splitlines() if line.startswith("data:")]
            raw = data_lines[-1]
        payload = json.loads(raw)
        if payload.get("error"):
            raise RuntimeError("MCP JSON-RPC error")
        return payload.get("result", {})

    def _initialize(self, name, environ):
        self.sessions[name] = ""
        self._request(name, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "codex-tool-installer", "version": "1.0.0"}}, environ)
        self._request(name, "notifications/initialized", {}, environ, notification=True)
