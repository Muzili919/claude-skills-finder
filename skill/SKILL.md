---
name: claude-skills-finder
description: Search GitHub for Claude Code skills, plugins, and agents. Use when the user asks to find, discover, or list community Claude Code skills, or asks "what skills exist for X" (e.g. SEO, testing, deployment, content).
---

# Claude Skills Finder

Search GitHub for community-built Claude Code skills, plugins, and agents.
Results are ranked by stars + relevance to "claude code" + keyword matches.

## When to use

Invoke this skill when the user asks any of:

- "find a claude skill for X"
- "what skills exist for X"
- "show me claude code plugins"
- "is there a claude code agent that does X"

## How to use

Run the bundled `search.py` from this skill's directory:

```bash
python search.py "<keywords>"
```

### Examples

| Goal | Command |
|---|---|
| SEO / content skills | `python search.py "seo content"` |
| Test automation | `python search.py "testing automation"` |
| Frontend / web | `python search.py "frontend web"` |
| DevOps / deploy | `python search.py "devops deploy"` |
| JSON output for piping | `python search.py --json "research"` |
| Top 5 only | `python search.py --limit 5 "data"` |

### Ranking

Each repo gets a score:

- `log10(stars + 1) * 2`
- `+10` if name/description/topics contains "claude code" or "claude-code"
- `+2` per match of `skill` / `plugin` / `agent` / `tool`
- `+1` per query keyword match (length > 2)

## Notes

- No API key needed — GitHub's unauthenticated search allows 60 requests/hour.
- For higher limits (5000/hr), `export GITHUB_TOKEN=ghp_...` before running.
- Web version (no install): <https://muzi.studio/tools/claude-skills>
