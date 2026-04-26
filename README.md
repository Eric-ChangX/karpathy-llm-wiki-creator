# Karpathy LLM Wiki Creator

A [Claude Code](https://claude.com/claude-code) / [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk) skill that scaffolds a new personal knowledge base in the style proposed by [Andrej Karpathy](https://karpathy.bearblog.dev/) — an "LLM Wiki" where:

- `raw/` holds source material, **immutable** after ingest
- `wiki/` holds LLM-curated synthesis pages, accumulated over time
- `index.md` is a content-oriented navigation file (humans read it first, then drill in)
- `log.md` is a chronological append-only timeline of every ingest / query / schema change
- The whole tree is Obsidian-friendly (wikilinks, frontmatter, graph view)

The skill itself is **just a scaffold** — it creates the directory structure and seed files, then hands off to the user. Ingest of actual content is a separate workflow driven by the `AGENTS.md` schema the scaffold writes.

## Install

Skills load from `~/.claude/skills/<skill-name>/`. Copy this repo's contents into a directory there:

```bash
# Linux / macOS
git clone https://github.com/Eric-ChangX/karpathy-llm-wiki-creator.git ~/.claude/skills/karpathy-llm-wiki-creator

# Windows (PowerShell)
git clone https://github.com/Eric-ChangX/karpathy-llm-wiki-creator.git $env:USERPROFILE\.claude\skills\karpathy-llm-wiki-creator
```

Restart Claude Code (or open a new session) and the skill will appear in the available-skills list.

## Use

In a Claude Code session, just ask:

> 给 AI 研究开一个新知识库，放在 `E:/Knowledge bases/AI/`

Claude will trigger this skill, ask one or two clarifying questions (target path, domain name), then create the full directory tree, write the `AGENTS.md` schema, make the first git commit, and tell you where to drop your first source file.

## Layout

```
karpathy-llm-wiki-creator/
├── SKILL.md             # Frontmatter + step-by-step scaffold instructions for the LLM
└── templates/           # Files copied verbatim into each new knowledge base
    ├── AGENTS.md        # Canonical schema — read by Codex, @-imported by CLAUDE.md
    ├── CLAUDE.md        # One-line @AGENTS.md import (Claude Code does not read AGENTS.md natively)
    ├── index.md         # Empty content index
    ├── log.md           # Timeline log with {{DATE}} / {{DOMAIN}} placeholders
    └── gitignore        # Renamed to .gitignore on copy; ignores Obsidian workspace state
```

## License

[MIT](LICENSE)
