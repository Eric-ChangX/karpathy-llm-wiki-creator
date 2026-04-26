---
graph-excluded: true
---

# Log

**行为流水线**——以 grep-friendly 格式记录 ingest / query 历史（含 schema / lint / scaffold 操作）。append-only。每条以 `## [YYYY-MM-DD] <op> | <title>` 开头，便于按 op、按日期、按主题反查：

```bash
grep "^## \[" wiki/log.md | tail -10            # 最近 10 条
grep "^## \[2026-04\]" wiki/log.md              # 某月
grep "^## \[.*\] ingest " wiki/log.md           # 只看 ingest
```

`<op>` ∈ `{ingest, query, lint, schema, scaffold}`。

---

## [{{DATE}}] scaffold | initial scaffold for {{DOMAIN}}

由 `karpathy-llm-wiki-creator` skill 创建：

- 目录：`raw/{articles,clippings,images,pdfs,notes,personal}/`、`wiki/{sources,concepts,entities,synthesis,templates}/`、`outputs/`、`scripts/`
- 文件：`AGENTS.md`、`CLAUDE.md`（@AGENTS.md import）、`README.md`、`wiki/index.md`、`wiki/overview.md`、`wiki/QUESTIONS.md`、`wiki/log.md`、`wiki/templates/{source,entity,concept,synthesis}.md`、`scripts/lint.py`
- 领域：{{DOMAIN}}
- 用途：个人 Knowledge Base，使用 Obsidian 浏览
- 下一步：把第一篇 raw 文件放进 `raw/<某子目录>/`，然后说「ingest」开始首次摄入
