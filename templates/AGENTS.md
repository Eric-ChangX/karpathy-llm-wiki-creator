# AGENTS.md — Personal Knowledge Base 运维手册

本仓库是一个 **LLM Wiki**：由 LLM（Codex / Claude / 其它 agent）维护、由用户策划的个人知识库。

> 本文件是 schema 的 **canonical source**。`CLAUDE.md` 是 Claude Code 入口（`@AGENTS.md` import）；所有结构规则只在这里改。

- 用户负责：sourcing、提问、确定方向、判断重点。
- LLM 负责：阅读 `raw/` 来源，维护 `wiki/` 页面，更新 `wiki/index.md` 与 `wiki/log.md`，保持交叉引用一致。

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
├── AGENTS.md              # 本文件，canonical schema
├── CLAUDE.md              # Claude Code 入口（单行 @AGENTS.md import；不要删）
├── README.md              # 人类入口，介绍这个 KB 的领域和用法
├── raw/                   # 原始来源，人类所有，LLM 只读
│   ├── articles/          # 手动保存的文章（markdown）
│   ├── clippings/         # Obsidian Web Clipper 剪藏（主入口）
│   ├── images/            # 截图、图片 + 同名 sidecar 元数据
│   ├── pdfs/              # PDF + 同名 sidecar 元数据
│   ├── notes/             # 随手记录
│   └── personal/          # ★ 用户自己写的文章、报告、笔记（一等公民来源）
├── wiki/                  # LLM 完全拥有
│   ├── index.md           # 内容目录索引（content-oriented）
│   ├── overview.md        # 高层综述 + Health Dashboard
│   ├── QUESTIONS.md       # 开放问题队列
│   ├── log.md             # 行为流水线：grep-friendly ingest / query 历史
│   ├── sources/           # 每篇 raw 来源对应一篇 source page
│   ├── concepts/          # 概念、框架、技术、模式
│   ├── entities/          # 人物、组织、产品、作品、论文
│   ├── synthesis/         # 跨来源、跨概念的综合分析
│   └── templates/         # 页面模板（LLM 创建新页时套用）
├── outputs/               # 非 markdown 的 query 产物（slides, charts, tables, lint 报告等）
└── scripts/
    └── lint.py            # 9 项 wiki 健康检查
```

### 各目录规则

- **`raw/` ingest 之后永不修改**（含改名、移动、删除），是 source of truth。Web Clipper 落盘那一刻的整理是允许的；一旦在 wiki 中被引用即冻结。
  - 子目录是组织方式，不是行为约束。LLM 跨子目录读；用户存放时按内容类型放对应子目录。
  - **`personal/` 是用户自己写的素材**（投资笔记、分析报告、个人思考），与外部来源同等待遇，可以被 ingest 成 source page。
  - **`pdfs/` 与 `images/` 必须配同名 `.md` sidecar metadata**，否则 LLM 很难稳定理解上下文：
    - PDF 例：`raw/pdfs/company_report.pdf` + `raw/pdfs/company_report.md`。
    - 图片例：`raw/images/product_screenshot.png` + `raw/images/product_screenshot.md`。
    - sidecar `.md` 是 ingest 入口；source page 的 `raw:` 指向 sidecar `.md`，sidecar 再记录实际二进制文件名。
    - sidecar 至少写：标题、文件名、来源/URL（如有）、抓取日期、为什么保存、图片/PDF 内容简述、希望 LLM 关注的 angle。
- **`wiki/` 按 type 分子目录**：
  - `wiki/sources/` — type:source
  - `wiki/entities/` — type:entity
  - `wiki/concepts/` — type:concept
  - `wiki/synthesis/` — type:synthesis
  - 其他子目录均不允许。新增 type 必须先改本 schema。
- **`wiki/templates/`** 存放页面模板（`source.md` / `entity.md` / `concept.md` / `synthesis.md`），LLM 创建新页时套用。模板不参与 lint 的 wikilink / orphan 检查。
- **`wiki/index.md` / `overview.md` / `QUESTIONS.md` / `log.md`** 是 wiki 根的 meta 页面：
  - frontmatter 只需 `graph-excluded: true`（让 Obsidian graph view 不把它们当节点）。
  - 没有 `type` 字段，不参与 type-vs-子目录检查。
  - `log.md` 是**行为流水线**：grep-friendly 地累积每次 ingest / query / schema / lint / scaffold 操作，append-only。详见下文「log.md 行格式」。
- **`outputs/`** 是 bucket，不分子目录。文件名规范：`YYYY-MM-DD_kind_短标题.ext`（`kind` ∈ `{slides, chart, table, export, lint, query}`）。在相关 wiki 页面引用：图片/PDF 用 `![[outputs/2026-04-26_chart_xxx.png]]`，markdown / slide deck 用 `[[outputs/2026-04-26_slides_xxx]]`。
- **`scripts/`** 存放为这个 wiki 服务的辅助脚本。`lint.py` 是必备的；其他按需新增（搜索、批量重命名、ingest 自动化等）。每个脚本第一行写一句话说明用途。

---

## 页面 frontmatter

### entity / concept / synthesis 页面

```yaml
---
type: entity | concept | synthesis
created: 2026-04-26
updated: 2026-04-26
sources:
  - "[[2026-04-26_短标题]]"   # 该页面引用了哪些 source page
tags: []
aliases: []                     # 跨语言别名，例：["Memex", "memex", "记忆延伸"]
---
```

### source 页面（`wiki/sources/`）

source page 描述「某一份 raw 来源」本身，frontmatter 不同：

```yaml
---
type: source
created: 2026-04-26
updated: 2026-04-26
raw: "raw/clippings/2026-04-26_短标题.md"   # 对应 raw 入口文件的相对路径，必填；PDF/图片写 sidecar .md
original_url:                                # 原文 URL（如有）
author:                                      # 原作者（如有）
published:                                   # 原文发布日期（如有）
captured: 2026-04-26                          # 抓取/落盘日期
tags: []
aliases: []
---
```

source page **不写 `sources:` 字段**——它自己就是 source。

### 通用约定

- 正文中链接其它页面用 Obsidian wikilink `[[页面名]]`，便于 graph view。
  - 同名歧义时用 `[[concepts/Foo]]` 这种带子目录的形式消歧。
- `type` 字段值：`source` / `entity` / `concept` / `synthesis`。
  - `entity` —— 人物、组织、产品、作品、论文。
  - `concept` —— 概念、框架、技术、模式。
  - `synthesis` —— 跨来源、跨概念、跨 entity 的综合分析（旧 schema 中的 `topic`）。
- `aliases` 字段记录跨语言别名（中英文、缩写、笔误常见拼法），让 lint 与搜索能定位同一概念的不同写法。

---

## 三个核心 Operations

### 1. Ingest（摄入新来源）

用户把新文件放入 `raw/<某子目录>/` 并要求处理时：

1. 读全文。带图片的 markdown 先读文本，再按需 `Read` 配套图片获得额外上下文。
2. **先和用户简短对齐 angle 与重点**，再动手写。
3. 按「命名约定」在 `wiki/sources/` 创建 source page。同日同主题须加来源简称区分，避免覆盖。可以从 `wiki/templates/source.md` 起手。
4. 扫 `wiki/index.md`，找出受影响的 entity / concept / synthesis 页面：
   - 已存在 → 更新内容，标注与旧观点的一致 / 矛盾。
   - 应存在但缺失 → 新建到对应子目录（`wiki/entities/`、`wiki/concepts/`、`wiki/synthesis/`），起手用对应模板。
5. 更新 `wiki/index.md`（新增条目或修改简介）。
6. 若有未解问题，登记到 `wiki/QUESTIONS.md`。
7. 在 `wiki/log.md` 追加一条 `ingest` 记录。

一次 ingest 通常触动 5–15 个页面。

### 2. Query（提问）

用户提问时：

1. 先读 `wiki/overview.md` 与 `wiki/index.md` 定位相关页面。
2. 读相关页面，必要时回到 `raw/` 原文核对。
3. 综合回答，**每个事实都带 `[[页面名]]` 或原文引用**。
4. **关键**：若答案本身有积累价值，主动询问是否归档：
   - markdown 形态（comparison、新关联、综合判断）→ 通常落到 `wiki/synthesis/`。
   - 非 markdown 形态（slide deck / chart / table / canvas）→ 落到 `outputs/`，按上文 `outputs/` 约定使用 `![[outputs/...]]` 或 `[[outputs/...]]` 在相关 wiki 页面引用。
5. 发现的新 open question 进 `wiki/QUESTIONS.md`。
6. 重要 query 在 `wiki/log.md` 留一条；琐碎可省。

### 3. Lint（健康检查）

通过 `py scripts/lint.py`（Windows）或 `python scripts/lint.py`（其它环境）执行，**只输出报告，不自动改 wiki**。9 项机械检查：

1. **断链**：`[[X]]` / `![[X]]` 找不到对应文件。
2. **孤儿页**：wiki 页面没有任何 inbound link。
3. **frontmatter 缺失/必填字段**：根据 type 校验必填字段。
4. **type 字段非法**：type 不在 `{source, entity, concept, synthesis}`。
5. **source page raw 字段完整性**：source page 必须有 `raw` 字段且对应文件存在。
6. **outputs 引用断链**：`![[outputs/X]]` / `[[outputs/X]]` 落不到真实文件。
7. **index.md 缺漏**：wiki 页存在但 `wiki/index.md` 没列。
8. **wiki/log.md 行格式**：`##` 标题不匹配 `## [YYYY-MM-DD] <op> | <title>` 或 op 非法。
9. **页面位置错**：type 与所在子目录不匹配（如 type:concept 不在 `wiki/concepts/`）。

加 `--write` 同时把报告落到 `outputs/<YYYY-MM-DD>_lint_<short>.md`。

非机械的检查（矛盾、过时结论、缺口、深入方向）由 LLM 在 query 时人工提示。

---

## 命名约定

- source page 文件名：`YYYY-MM-DD_短标题.md`，便于按时间排序。
  - 同日同主题冲突时，加来源简称区分：`2026-04-26_OpenAI_blog.md` / `2026-04-26_OpenAI_techcrunch.md`。再不够就追加 `-2`。
- entity / concept / synthesis 文件名：用主题名作为文件名，**同一概念全仓库统一一种写法**（避免 `OpenAI` 与 `openai` 并存）；备用写法进 `aliases:` frontmatter。
- 英文专名原样进文件名，不加引号，不翻译。
- 文件**必须放对应子目录**：source→`wiki/sources/`，entity→`wiki/entities/`，concept→`wiki/concepts/`，synthesis→`wiki/synthesis/`。

---

## log.md 行格式

`wiki/log.md` 是**行为流水线**——以 grep-friendly 格式累积 ingest / query / schema / lint / scaffold 历史。每条以 `## [YYYY-MM-DD] <op> | <title>` 开头：

```bash
grep "^## \[" wiki/log.md | tail -10            # 最近 10 条
grep "^## \[2026-04\]" wiki/log.md              # 某月
grep "^## \[.*\] ingest " wiki/log.md           # 只看 ingest
```

`<op>` ∈ `{ingest, query, lint, schema, scaffold}`。append-only：错条用新条目修订/翻案，不重写历史。

---

## 协作约定

- **Ingest 前先和用户对齐 angle 再动手写**，不要直接长篇大论地填页面。
- 大的结构变动（新增分类、改命名规范）改本文件并在 `wiki/log.md` 记一条 `schema` 操作。`CLAUDE.md` 不要写实质规则。
- 不批量 refactor wiki，**单点演进**优先。
- 不在 `raw/` 中的内容写入 wiki 时必须标注「推理」或「外部知识」，区分于一手来源。
- 此 schema 持续与用户共同演化；当某条规则反复被违反或反复被绕过，提出修订方案。
