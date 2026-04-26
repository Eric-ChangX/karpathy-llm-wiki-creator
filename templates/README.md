# Personal Knowledge Base — {{DOMAIN}}

LLM Wiki，按 [Andrej Karpathy](https://karpathy.bearblog.dev/) 提出的 LLM Wiki 思路组织：

- `raw/` 是原始来源，**ingest 后冻结**
- `wiki/` 是 LLM 维护的综合页面，按 type 分子目录
- `wiki/index.md` 是内容目录，`wiki/overview.md` 是高层综述
- `log.md` 是时间线日志（ingest / query / schema / lint / scaffold）

## 用法

- **Ingest 新来源**：把文件放进 `raw/<某子目录>/`，告诉 LLM「ingest 这个」。
- **提问**：直接问，LLM 会从 `wiki/index.md` 入口检索。
- **Lint**：`py scripts/lint.py` 跑 9 项健康检查；`--write` 同时落到 `outputs/`。

## Schema

所有结构规则在 [AGENTS.md](AGENTS.md)（canonical）。Claude Code 通过 [CLAUDE.md](CLAUDE.md) 一行 `@AGENTS.md` import 自动加载。

修改 schema 必须改 AGENTS.md 并在 [log.md](log.md) 记一条 `schema` 操作。

## 由 [karpathy-llm-wiki-creator](https://github.com/Eric-ChangX/karpathy-llm-wiki-creator) skill 创建

可在 Claude Code 中通过这个 skill 为新领域快速建立同样结构的 KB。
