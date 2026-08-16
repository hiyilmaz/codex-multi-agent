import io
import json
import unittest

from codex_tool_installer.dependencies import dependency_plan
from codex_tool_installer.transport import HttpMcpTransport


class Response(io.BytesIO):
    status = 200
    headers = {}
    def __enter__(self): return self
    def __exit__(self, *args): self.close()


class TransportDependencyTests(unittest.TestCase):
    def test_dependency_plans_are_official_and_scoped(self):
        self.assertEqual(("sudo", "apt-get"), dependency_plan("go", "ubuntu-24.04")[0][:2])
        self.assertEqual(("brew", "install", "uv"), dependency_plan("uv", "macos")[0])
        self.assertEqual((), dependency_plan("unknown", "macos"))

    def test_http_transport_sends_json_rpc_and_secret_only_in_header(self):
        seen = []
        def opener(request, timeout):
            seen.append((request, timeout))
            return Response(json.dumps({"jsonrpc": "2.0", "id": 1, "result": {"tools": []}}).encode())
        transport = HttpMcpTransport(opener)
        transport.sessions["github"] = "session"
        result = transport.request("github", "tools/list", {}, {"GITHUB_PAT_TOKEN": "sentinel"})
        self.assertEqual({"tools": []}, result)
        request = seen[0][0]
        self.assertEqual("Bearer sentinel", request.headers["Authorization"])
        self.assertNotIn(b"sentinel", request.data)
        self.assertEqual("tools/list", json.loads(request.data)["method"])

    def test_http_transport_parses_sse_and_rejects_rpc_error(self):
        success = lambda *_args, **_kwargs: Response(b'event: message\ndata: {"result":{"content":[{"type":"text","text":"ok"}]}}\n')
        transport = HttpMcpTransport(success); transport.sessions["deepwiki"] = "session"
        self.assertTrue(transport.request("deepwiki", "tools/list", {}, {})["content"])
        failure = lambda *_args, **_kwargs: Response(b'{"error":{"code":-1}}')
        broken = HttpMcpTransport(failure); broken.sessions["deepwiki"] = "session"
        with self.assertRaises(RuntimeError):
            broken.request("deepwiki", "tools/list", {}, {})

    def test_transport_rejects_non_https_endpoint(self):
        from codex_tool_installer.manifest import TOOL_MANIFEST
        original = TOOL_MANIFEST["deepwiki"].mcp["url"]
        TOOL_MANIFEST["deepwiki"].mcp["url"] = "http://insecure.invalid"
        transport = HttpMcpTransport(lambda *_args, **_kwargs: self.fail("must not connect"))
        transport.sessions["deepwiki"] = "session"
        try:
            with self.assertRaises(RuntimeError):
                transport.request("deepwiki", "tools/list", {}, {})
        finally:
            TOOL_MANIFEST["deepwiki"].mcp["url"] = original


if __name__ == "__main__": unittest.main()
