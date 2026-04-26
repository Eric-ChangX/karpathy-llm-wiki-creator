# Karpathy LLM Wiki Creator

A [Claude Code](https://claude.com/claude-code) / [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk) skill that scaffolds a new personal knowledge base in the style proposed by [Andrej Karpathy](https://karpathy.bearblog.dev/) — an "LLM Wiki" where:

- `raw/` holds source material, organized into 6 typed subdirs (`articles/`, `clippings/`, `images/`, `pdfs/`, `notes/`, `personal/`); **immutable** after ingest. `pdfs/` and `images/` require same-name `.md` sidecar metadata so the LLM has a real ingest entry point.
- `wiki/` holds LLM-curated synthesis pages, **subdirectorized by type** (`sources/`, `entities/`, `concepts/`, `synthesis/`)
- `wiki/index.md` is a content-oriented navigation file; `wiki/overview.md` is the high-level summary + Health Dashboard; `wiki/QUESTIONS.md` is the open-question queue
- `log.md` is a chronological append-only timeline of every ingest / query / schema / lint / scaffold operation
- `scripts/lint.py` runs 9 mechanical health checks: broken wikilinks (with cross-subdir ambiguity detection), orphan pages, frontmatter validity, type enum, source-raw integrity, outputs ref integrity, index completeness, log format, and type-vs-subdir consistency. Honours frontmatter `aliases:` for cross-language names.
- Page frontmatter supports `aliases: []` for cross-language names (English/Chinese, abbreviations, common typos)
- The whole tree is Obsidian-friendly (wikilinks, frontmatter, graph view)
- The scaffolded KB ships with a `README.md` runbook (quick start, per-raw-subdir usage, daily workflow, hand-edit safety rules) so future-you can pick it up cold

The skill itself is **just a scaffold** — it creates the directory structure and seed files, then hands off to the user. Ingest of actual content is a separate workflow driven by the `AGENTS.md` schema the scaffold writes.

## Install

Skills load from `~/.claude/skills/<skill-name>/`. Clone this repo there:

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

Claude will trigger this skill, ask one or two clarifying questions (target path, domain name), then create the full directory tree, write the schema files, run `scripts/lint.py` to verify, make the first git commit, and tell you where to drop your first source file.

## Layout

What you get after scaffold (this is the end-state structure of every new KB):

```
<your-kb>/
├── AGENTS.md              # Canonical schema (read by Codex; @-imported by CLAUDE.md)
├── CLAUDE.md              # Claude Code entry — single line: @AGENTS.md
├── README.md              # Human-facing runbook (quick start, daily workflow)
├── log.md                 # Append-only timeline: ingest / query / schema / lint / scaffold
├── raw/                   # Human-owned sources; LLM read-only after ingest
│   ├── articles/          # Hand-saved articles (markdown)
│   ├── clippings/         # Obsidian Web Clipper output (main entry)
│   ├── images/            # Screenshots/images + same-name .md sidecar metadata
│   ├── pdfs/              # PDFs + same-name .md sidecar metadata
│   ├── notes/             # Loose notes, meeting fragments
│   └── personal/          # ★ User-authored writing — first-class source
├── wiki/                  # LLM-curated knowledge layer
│   ├── index.md           # Content-oriented index (graph-excluded)
│   ├── overview.md        # High-level summary + Health Dashboard
│   ├── QUESTIONS.md       # Open-question queue
│   ├── sources/           # type:source — one page per raw source
│   ├── entities/          # type:entity — people, orgs, products, works, papers
│   ├── concepts/          # type:concept — ideas, frameworks, techniques (uses aliases)
│   ├── synthesis/         # type:synthesis — cross-source / cross-concept analysis
│   └── templates/         # Page templates (source/entity/concept/synthesis) the LLM copies
├── outputs/               # Non-markdown query products (slides, charts, lint reports, exports)
└── scripts/
    └── lint.py            # 9-check wiki linter (stdlib only)
```

### What's inside this repo

This is the skill itself, not a KB. Skills load from `~/.claude/skills/<name>/`, so the layout here is:

```
karpathy-llm-wiki-creator/
├── SKILL.md               # Scaffold instructions the LLM follows
├── README.md              # This file
├── LICENSE
└── templates/             # Files copied verbatim into each new KB on scaffold
    ├── AGENTS.md  CLAUDE.md  README.md  log.md  gitignore
    ├── wiki/{index,overview,QUESTIONS}.md
    ├── wiki/templates/{source,entity,concept,synthesis}.md
    └── scripts/lint.py
```

## License

[MIT](LICENSE)
