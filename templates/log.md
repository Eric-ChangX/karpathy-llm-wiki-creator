# Log

时间线日志，append-only。每条以 `## [YYYY-MM-DD] <op> | <title>` 开头，便于 grep：

```bash
grep "^## \[" log.md | tail -10
```

`<op>` ∈ `{ingest, query, lint, schema, scaffold}`。

---

## [{{DATE}}] scaffold | initial scaffold for {{DOMAIN}}

由 `karpathy-llm-wiki-creator` skill 创建：

- 目录：`raw/{articles,clippings,images,pdfs,notes,personal}/`、`wiki/{sources,concepts,entities,synthesis,templates}/`、`outputs/`、`scripts/`
- 文件：`AGENTS.md`、`CLAUDE.md`（@AGENTS.md import）、`README.md`、`log.md`、`wiki/index.md`、`wiki/overview.md`、`wiki/QUESTIONS.md`、`wiki/templates/{source,entity,concept,synthesis}.md`、`scripts/lint.py`
- 领域：{{DOMAIN}}
- 用途：个人 Knowledge Base，使用 Obsidian 浏览
- 下一步：把第一篇 raw 文件放进 `raw/<某子目录>/`，然后说「ingest」开始首次摄入
