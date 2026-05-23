# Claude Skills Finder

> Search GitHub for **Claude Code** skills, plugins, and agents — ranked by relevance + stars.

**Live demo (enhanced version with daily trending):** [muzi.studio/tools/claude-skills](https://muzi.studio/tools/claude-skills)

---

## Why

The Claude Code ecosystem is exploding with community-built skills, plugins, and agents. GitHub's default search is noisy — most "claude" results are about Claude Shannon, not Claude Code. This tool filters and ranks by:

- Star count (logarithmic, so 100k stars doesn't drown out a great 200-star skill)
- "claude code" / "claude-code" mentions (+10)
- `skill` / `plugin` / `agent` / `tool` keywords (+2 each)
- Your query keyword matches (+1 each)

## Two ways to use

### 1. As a Claude Code skill (recommended)

```bash
git clone https://github.com/Muzili919/claude-skills-finder ~/.claude/skills/claude-skills-finder
```

Then in Claude Code, just ask:

> *"find me a claude skill for SEO"*
> *"what skills exist for test automation?"*

The skill auto-triggers and runs `search.py` for you.

You can also run it directly:

```bash
python ~/.claude/skills/claude-skills-finder/skill/search.py "seo content"
python ~/.claude/skills/claude-skills-finder/skill/search.py --json "testing" --limit 5
```

### 2. As a web page (no install)

Open `web/index.html` in any browser, or host it on GitHub Pages — pure vanilla JS, calls GitHub API directly.

Live hosted version: [muzi.studio/tools/claude-skills](https://muzi.studio/tools/claude-skills)

## Examples

```bash
$ python skill/search.py "seo content"

★  4321  someone/claude-code-seo-skill
         A Claude Code skill for SEO audits, keyword research, and content briefs.
         https://github.com/someone/claude-code-seo-skill

★   892  another/content-repurpose
         Turn one blog post into 10 social posts using Claude Code.
         https://github.com/another/content-repurpose
...
```

## Higher rate limits

GitHub's unauthenticated search allows **60 requests/hour per IP**. For 5000/hr:

```bash
export GITHUB_TOKEN=ghp_your_token_here
python skill/search.py "your query"
```

The web version always uses unauth (browser CORS) — if you hit the limit, switch to the CLI.

## Zero dependencies

- `skill/search.py` — Python 3 stdlib only (no pip install)
- `web/index.html` — Single HTML file, vanilla JS, no build step

## License

MIT — see [LICENSE](LICENSE).

## Related

Built by [muzi.studio](https://muzi.studio) — a workshop of small AI tools. If you like this, the [enhanced version on muzi.studio](https://muzi.studio/tools/claude-skills) has daily trending updates and a slightly smarter ranker.
