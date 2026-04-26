# claude-skills

Personal collection of [Claude Code](https://claude.com/claude-code) / Claude Agent SDK skills.

Skills are self-contained instruction packs that Claude loads on demand when a user request matches the skill's trigger description. See [Anthropic's skills repo](https://github.com/anthropics/skills) for the official format.

## Skills in this repo

| Skill | Purpose |
|---|---|
| [llm-wiki-scaffold](llm-wiki-scaffold/) | Initialize a new LLM Wiki knowledge base (Karpathy-style: `raw/` + `wiki/` + `index.md` + `log.md`, Obsidian-friendly). |

## Installing locally

Skills are loaded from `~/.claude/skills/<skill-name>/`. To install one from this repo:

```bash
# Linux / macOS
cp -r llm-wiki-scaffold ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse llm-wiki-scaffold $env:USERPROFILE\.claude\skills\
```

After copying, restart Claude Code (or just open a new session) — the skill will appear in the available-skills list.

## Layout per skill

```
<skill-name>/
├── SKILL.md         # frontmatter (name/version/description) + instructions
├── templates/       # static files the skill copies into the user's workspace (optional)
├── references/      # background knowledge the skill loads on demand (optional)
└── scripts/         # helper scripts the skill invokes (optional)
```

`SKILL.md`'s `description` field is what Claude reads to decide when to trigger the skill — keep it specific and example-rich.

## License

MIT — see [LICENSE](LICENSE).
