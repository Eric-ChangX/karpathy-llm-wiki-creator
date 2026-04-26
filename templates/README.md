# Personal Knowledge Base

这是一个 LLM Wiki：人类负责收集来源、提出问题、判断重点；LLM 负责把来源整理成可累积的 `wiki/` 页面，并维护索引、交叉引用、开放问题和日志。

日常使用时，把这个目录当成 Obsidian vault 打开。人类主要看 `wiki/overview.md` 和 `wiki/index.md`，LLM 主要按 `AGENTS.md` 的规则维护内容。

## 快速开始

1. 把新材料放进 `raw/` 的合适子目录。
2. 对文件名做一次简单整理，尽量包含日期和短标题。
3. 对 LLM 说：`ingest raw/clippings/2026-04-26_xxx.md，重点关注……`
4. LLM 会先和你确认 angle，再更新 `wiki/sources/`、相关 `wiki/entities/` / `wiki/concepts/` / `wiki/synthesis/`、`wiki/index.md`、`wiki/QUESTIONS.md` 和 `log.md`。
5. 你 review LLM 写出的 wiki 页面，要求它补充、删减或改重点。
6. 跑 `py scripts/lint.py`，确认 9 项机械检查通过。
7. 用 git 提交这一轮变更。

## raw/ 怎么放

`raw/` 是人类拥有的原始来源。LLM 可以读取，但 ingest 之后不要再改名、移动或删除，因为 `wiki/sources/` 会引用它。

- `raw/clippings/`：Obsidian Web Clipper 剪藏，日常最主要入口。适合网页文章、博客、文档页。
- `raw/articles/`：手动保存或整理过的文章 markdown。适合你自己从网页、邮件、聊天记录中清理出的长文。
- `raw/pdfs/`：PDF 文件和同名 sidecar metadata。例：`report.pdf` 必须配 `report.md`，ingest 时让 LLM 读 `report.md`。
- `raw/images/`：截图、图片和同名 sidecar metadata。例：`screenshot.png` 必须配 `screenshot.md`，说明图片来源、内容和保存原因。
- `raw/notes/`：临时想法、会议碎片、随手记录。适合还没成文但值得进入知识库的材料。
- `raw/personal/`：你自己写的文章、分析报告、投资笔记、长期思考。这里的内容是一等公民来源，不比外部文章低一等。

PDF/图片的 sidecar `.md` 至少写清楚：标题、实际文件名、来源或 URL、抓取日期、为什么保存、内容简述、希望 LLM 关注的 angle。

## wiki/ 怎么读

`wiki/` 是 LLM 维护的知识层。建议人类少量手改，更多通过“让 LLM 修改”的方式维护一致性。

- `wiki/overview.md`：高层综述和 Health Dashboard。第一次进入先看这里。
- `wiki/index.md`：内容目录。提问和浏览时从这里找入口。
- `wiki/QUESTIONS.md`：开放问题队列。记录还缺来源、暂时无法判断或值得继续追踪的问题。
- `wiki/sources/`：每个 raw 来源对应一篇 source page，记录出处、要点、关键引用和本次 angle。
- `wiki/entities/`：人物、组织、产品、作品、论文等。
- `wiki/concepts/`：概念、框架、技术、模式等。
- `wiki/synthesis/`：跨来源、跨概念的综合判断、比较、路线图和阶段性结论。
- `wiki/templates/`：LLM 创建页面时用的模板，不作为知识内容阅读。

## 日常工作流

### Ingest 新来源

把来源放到 `raw/` 后，告诉 LLM 文件路径和你关心的 angle。不要只说“处理一下”，最好说清楚为什么保存它，例如：

```text
ingest raw/clippings/2026-04-26_llm-wiki.md。重点关注它对个人知识库结构、human/LLM 分工和 query 归档的启发。
```

LLM 应该先确认 angle，再动手写。完成后，你重点检查三件事：source page 有没有抓住原文重点，相关 entity/concept/synthesis 页有没有误解，`wiki/index.md` 是否能让未来的你找回这条材料。

### Query 提问

直接问问题即可。LLM 会先读 `wiki/overview.md` 和 `wiki/index.md`，再读相关页面，必要时回到 `raw/` 核对。

如果一次回答有长期价值，让 LLM 归档：markdown 综合结论通常放到 `wiki/synthesis/`；图表、slides、CSV、lint 报告等放到 `outputs/`，并从相关 wiki 页面链接过去。

### Lint 健康检查

每次 ingest 后建议跑：

```powershell
py scripts/lint.py
```

需要保存报告时跑：

```powershell
py scripts/lint.py --write
```

lint 只做机械检查：断链、孤儿页、frontmatter、type、source raw、outputs 引用、index 缺漏、log 格式、页面位置。矛盾、过时结论和研究缺口仍需要 LLM 在 query 或专门 review 时判断。

### Git 维护

建议每次完整 ingest 或 schema 调整后提交一次：

```powershell
git status
git add .
git commit -m "ingest: short title"
```

提交前先跑 lint。`raw/` 里的来源也应该进 git，除非包含敏感或过大的文件。

## 哪些文件可以手改

- 可以手改：`raw/` 中尚未 ingest 的文件、`README.md`、有意识要演化规则时的 `AGENTS.md`。
- 谨慎手改：`wiki/` 页面。更推荐让 LLM 按你的反馈改，这样它会同步更新 index、questions 和 log。
- 不要改：已 ingest 的 `raw/` 文件路径和文件名。
- 不要随手改：`log.md`。它是 append-only 时间线，schema/ingest/query/lint 的重要记录应追加，不应重写历史。

## Schema

所有结构规则在 [AGENTS.md](AGENTS.md)。Claude Code 通过 [CLAUDE.md](CLAUDE.md) 的 `@AGENTS.md` import 自动加载同一份规则。

修改 schema 时，必须同步在 [log.md](log.md) 追加一条 `schema` 记录。
