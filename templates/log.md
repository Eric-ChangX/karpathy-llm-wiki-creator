# Log

时间线日志，append-only。每条以 `## [YYYY-MM-DD] <op> | <title>` 开头，便于 grep：

```bash
grep "^## \[" log.md | tail -10
```

`<op>` ∈ `{ingest, query, lint, schema, scaffold}`。

---

## [{{DATE}}] scaffold | initial scaffold for {{DOMAIN}}

由 `karpathy-llm-wiki-creator` skill 创建：

- 目录：`raw/`、`raw/assets/`、`wiki/`、`wiki/sources/`、`outputs/`、`scripts/`
- 文件：`AGENTS.md`（canonical schema）、`CLAUDE.md`（stub）、`index.md`、`log.md`、`.gitignore`
- 领域：{{DOMAIN}}
- 用途：个人 Knowledge Base，使用 Obsidian 浏览
- 下一步：把第一篇 raw 文件放进 `raw/`，然后说「ingest」开始首次摄入
