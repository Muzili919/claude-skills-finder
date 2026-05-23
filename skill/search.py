#!/usr/bin/env python3
"""Search GitHub for Claude Code skills, plugins, and agents.

Zero third-party dependencies — uses only Python stdlib.
Optionally honors GITHUB_TOKEN env var for higher rate limits (5000/hr vs 60/hr).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com/search/repositories"
UA = "claude-skills-finder/0.1 (+https://github.com/Muzili919/claude-skills-finder)"


def _ssl_context() -> ssl.SSLContext:
    """Build an SSLContext that works on Python installs missing the system CA bundle
    (a common macOS-with-python.org gotcha). Tries certifi first, then SSL_CERT_FILE,
    then OS default. Raises with a helpful message if all fail."""
    try:
        import certifi  # type: ignore
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    cert_file = os.environ.get("SSL_CERT_FILE")
    if cert_file and os.path.exists(cert_file):
        return ssl.create_default_context(cafile=cert_file)
    return ssl.create_default_context()


def _http_get(url: str) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": UA}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    ctx = _ssl_context()
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        return json.loads(r.read())


def search_github(q: str) -> list[dict]:
    params = urllib.parse.urlencode({
        "q": f"{q} in:name,description,readme",
        "sort": "stars",
        "order": "desc",
        "per_page": "30",
    })
    data = _http_get(f"{API}?{params}")
    return [
        {
            "name": it["full_name"],
            "description": it.get("description") or "",
            "stars": it.get("stargazers_count", 0),
            "language": it.get("language") or "",
            "url": it["html_url"],
            "topics": it.get("topics") or [],
            "updated_at": it.get("updated_at", ""),
        }
        for it in data.get("items", [])
    ]


def rank(repos: list[dict], q: str) -> list[dict]:
    q_lower = q.lower()
    scored = []
    for r in repos:
        score = math.log10(r["stars"] + 1) * 2
        blob = f"{r['name']} {r['description']} {' '.join(r['topics'])}".lower()
        if "claude code" in blob:
            score += 10
        if "claude-code" in blob:
            score += 10
        for kw in ("skill", "plugin", "agent", "tool"):
            if kw in blob:
                score += 2
        for w in q_lower.split():
            if len(w) > 2 and w in blob:
                score += 1
        scored.append((score, r))
    return [r for _, r in sorted(scored, key=lambda x: -x[0])]


def find(query: str) -> list[dict]:
    queries = [f'"claude code" {query}', f"claude-code {query}"]
    all_repos: list[dict] = []
    seen: set[str] = set()
    for qq in queries:
        try:
            for r in search_github(qq):
                if r["name"] in seen:
                    continue
                seen.add(r["name"])
                all_repos.append(r)
        except urllib.error.HTTPError as e:
            print(f"warn: GitHub returned {e.code} for {qq!r}", file=sys.stderr)
        except urllib.error.URLError as e:
            reason = str(getattr(e, "reason", e))
            if "CERTIFICATE_VERIFY_FAILED" in reason:
                print(
                    "error: SSL certificate verification failed.\n"
                    "  Fix on macOS (python.org install): "
                    "/Applications/Python\\ 3.X/Install\\ Certificates.command\n"
                    "  Or:  pip install certifi   (script will auto-detect it)\n"
                    "  Or:  export SSL_CERT_FILE=/path/to/cacert.pem",
                    file=sys.stderr,
                )
                return []
            print(f"warn: query {qq!r} failed: {reason}", file=sys.stderr)
        except Exception as e:
            print(f"warn: query {qq!r} failed: {e}", file=sys.stderr)
    return rank(all_repos, query)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Find Claude Code skills, plugins, and agents on GitHub.",
    )
    p.add_argument("query", nargs="*", help="search keywords (default: 'claude code skill')")
    p.add_argument("--json", action="store_true", help="output as JSON")
    p.add_argument("--limit", type=int, default=20, help="max results (default: 20)")
    args = p.parse_args()

    q = " ".join(args.query) if args.query else "claude code skill"
    repos = find(q)[: args.limit]

    if args.json:
        print(json.dumps(repos, indent=2, ensure_ascii=False))
        return 0

    if not repos:
        print("No results. Try different keywords.", file=sys.stderr)
        return 1

    for r in repos:
        print(f"★ {r['stars']:>5}  {r['name']}")
        if r["description"]:
            desc = r["description"][:90] + ("…" if len(r["description"]) > 90 else "")
            print(f"         {desc}")
        print(f"         {r['url']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
