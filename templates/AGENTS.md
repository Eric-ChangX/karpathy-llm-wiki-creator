# AGENTS.md — Personal Knowledge Base 运维手册

本仓库是一个 **LLM Wiki**：由 LLM（Codex / Claude / 其它 agent）维护、由用户策划的个人知识库。

> 本文件是 schema 的 **canonical source**。`CLAUDE.md` 是 stub，仅指向本文件——所有结构规则只在这里改。

- 用户负责：sourcing、提问、确定方向、判断重点。
- LLM 负责：阅读 `raw/` 来源，写入与维护 `wiki/` 页面，更新 `index.md` 和 `log.md`，保持交叉引用一致。

本文件是 schema，用户和 LLM 共同演化它。

---

## 语言

- 主语言：**中文**。
- 专有名词、技术词、产品名、人名、文献原标题保留英文原文，**不翻译**（例：LLM、Obsidian、Memex、GPT-4o、RAG、Tolkien Gateway）。
- 引用原文时保留原文语言。
- 上述规则同时适用于 wiki 页面、log、index、与用户的对话回复。

---

## 目录结构

```
.
├── AGENTS.md       # 本文件，canonical schema
├── CLAUDE.md       # Claude Code 入口，单行 @AGENTS.md import（不要删）
├── index.md        # wiki 目录索引（content-oriented）
├── log.md          # 时间线日志（chronological, append-only）
├── raw/            # 原始来源，只读
│   └── assets/     # 图片等附件（Obsidian Web Clipper 输出位置）
├── wiki/           # LLM 生成与维护的页面
│   └── sources/    # 每篇来源对应一篇 source page
├── outputs/        # 非 markdown 的 query 产物（slides, charts, tables 等）
└── scripts/        # 辅助脚本（search、lint、ingest helper 等）
```

- `raw/` **ingest 之后永不修改**（含改名、移动、删除），是 source of truth。Web Clipper 落盘那一刻的命名是允许整理的；一旦在 wiki 中被引用即冻结。
- `wiki/` 根目录平铺 entity / concept / self / topic 页面，用 frontmatter 的 `type` 字段区分类型，不再分子目录（保持 Obsidian wikilink 简洁）。
- `wiki/sources/` 是唯一的特殊子目录，因为 source page 数量增长最快。
- `outputs/` 存放非 markdown 形态的 query 产物：Marp slide deck（`.md`，但用于演示）、matplotlib chart（`.png` / `.svg`）、CSV / Excel 对比表、HTML canvas 等。文件名规范：`YYYY-MM-DD_kind_短标题.ext`（`kind` ∈ `{slides, chart, table, export}`）。在相关 wiki 页面里引用：图片/PDF 等用嵌入语法 `![[outputs/2026-04-26_chart_xxx.png]]`，markdown / slide deck 用跳转语法 `[[outputs/2026-04-26_slides_xxx]]`。避免产物孤立于 wiki 之外。
- `scripts/` 存放为这个 wiki 服务的辅助脚本——搜索（如自建简易 search 或 qmd 包装）、lint helper、批量重命名、ingest 自动化等。**不是工程代码**，按需新增。每个脚本第一行写一句话说明用途。

---

## 页面 frontmatter

### entity / concept / self / topic 页面

```yaml
---
type: entity | concept | self | topic
created: 2026-04-26
updated: 2026-04-26
sources:
  - "[[2026-04-26_短标题]]"   # 该页面引用了哪些 source page
tags: []
---
```

### source 页面（`wiki/sources/`）

source page 描述的是「某一份 raw 来源」本身，frontmatter 不同：

```yaml
---
type: source
created: 2026-04-26
updated: 2026-04-26
raw: "raw/2026-04-26_短标题.md"   # 对应的 raw 文件相对路径
original_url:                      # 原文 URL（如有）
author:                            # 原作者（如有）
published:                         # 原文发布日期（如有）
captured: 2026-04-26                # 抓取/落盘日期
tags: []
---
```

source page **不写 `sources:` 字段**——它自己就是 source。

### 通用约定

- 正文中链接其它页面用 Obsidian wikilink `[[页面名]]`，便于 graph view。
- `type` 字段含义：
  - `source` —— `wiki/sources/` 中的来源页。
  - `entity` —— 人物、组织、地点、产品、作品。
  - `concept` —— 想法、框架、术语、模型。
  - `self` —— 关于用户本人（目标、价值观、习惯、状态）。
  - `topic` —— 跨多个 entity / concept 的领域综合页。

---

## 三个核心 Operations

### 1. Ingest（摄入新来源）

用户把新文件放入 `raw/` 并要求处理时：

1. 读全文。若是带图片的 markdown，先读文本，再按需 `Read` `raw/assets/` 中的图片获得额外上下文。
2. **先和用户简短对齐 angle 与重点**，再动手写。
3. 按下文「命名约定」在 `wiki/sources/` 创建 source page：原文出处、要点、关键引用、用户当前 angle 下的重点。同日同主题须按命名约定加来源简称区分，避免覆盖。
4. 扫 `index.md`，找出受影响的 entity / concept / self / topic 页面：
   - 已存在 → 更新内容，标注与旧观点的一致 / 矛盾。
   - 应存在但缺失 → 新建。
5. 更新 `index.md`（新增条目或修改简介）。
6. 在 `log.md` 追加一条 `ingest` 记录。

一次 ingest 通常触动 5–15 个页面。

### 2. Query（提问）

用户提问时：

1. 先读 `index.md` 找相关页面。
2. 读相关页面，必要时回到 `raw/` 原文核对。
3. 综合回答，**每个事实都带 `[[页面名]]` 或原文引用**。
4. **关键**：若答案本身有积累价值，主动询问是否归档：
   - markdown 形态（comparison、新关联、综合判断）→ 新建 wiki 页面。
   - 非 markdown 形态（slide deck / chart / table / canvas）→ 落到 `outputs/`，按上文 `outputs/` 约定使用 `![[outputs/...]]`（图片/PDF 嵌入）或 `[[outputs/...]]`（markdown / slide deck 跳转）在相关 wiki 页面引用。
5. 重要 query 在 `log.md` 留一条；琐碎可省。

### 3. Lint（健康检查）

用户主动要求时执行，**只输出报告，不自动改 wiki**：

- **矛盾**：不同页面对同一事实给出冲突说法。
- **过时**：旧结论被新来源推翻但未更新。
- **孤儿**：没有任何 inbound link 的页面。
- **缺口**：被频繁提及但缺独立页面的概念。
- **断链**：`[[...]]` 指向不存在的页面。
- **下一步**：值得深入的问题、值得搜索的来源。

---

## 命名约定

- source page 文件名：`YYYY-MM-DD_短标题.md`，便于按时间排序。
  - 同日同主题冲突时，加来源简称区分：`2026-04-26_OpenAI_blog.md` / `2026-04-26_OpenAI_techcrunch.md`。再不够就追加 `-2`。
- entity / concept / self / topic 文件名：用主题名作为文件名，**同一概念全仓库统一一种写法**（避免 `OpenAI` 与 `openai` 并存）。
- 英文专名原样进文件名，不加引号，不翻译。

---

## log.md 行格式

每条以 `## [YYYY-MM-DD] <op> | <title>` 开头，便于 grep：

```bash
grep "^## \[" log.md | tail -10
```

`<op>` ∈ `{ingest, query, lint, schema, scaffold}`。

---

## 协作约定

- **Ingest 前先和用户对齐 angle 再动手写**，不要直接长篇大论地填页面。
- 大的结构变动（新增分类、改命名规范）改本文件并在 `log.md` 记一条 `schema` 操作。`CLAUDE.md` 是 stub，不要在那里写实质规则。
- 不批量 refactor wiki，**单点演进**优先。
- 不在 `raw/` 中的内容写入 wiki 时必须标注「推理」或「外部知识」，区分于一手来源。
- 此 schema 持续与用户共同演化；当某条规则反复被违反或反复被绕过，提出修订方案。
