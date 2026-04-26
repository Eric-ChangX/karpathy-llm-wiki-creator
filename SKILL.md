---
name: karpathy-llm-wiki-creator
version: 2.2.0
description: "在指定路径下初始化一个新的 LLM Wiki 知识库（Karpathy 风格：raw/ 不动 + wiki/ 按 type 分子目录累积综合 + wiki/ 内 index/overview/QUESTIONS/log 四个 meta 页（log 是 grep-friendly 行为流水线）+ lint.py 9 项健康检查 + 人类 runbook README + PDF/图片 sidecar 元数据规则 + frontmatter aliases 跨语言别名 + Obsidian 友好）。当用户说『新建一个知识库』『初始化一个 LLM Wiki』『为 X 领域开一个 wiki』『scaffold 一个新知识库』时使用。每个 KB 一个领域（飞书、AI、个人项目等各自独立）。本 skill 只负责脚手架，不导入任何 raw 内容。"
---

# Karpathy LLM Wiki Creator

参考 Andrej Karpathy 提出的「LLM Wiki」工作流：原始来源 immutable，LLM 在上面累积综合页面，index 导航 + log 记录演化。

为新领域知识库创建标准 scaffold。每个领域独立一个目录，互不干扰。

## 使用前提

- 已有 git 可用（`git --version`）。
- 用户已选好或会指定一个**新的目录路径**（不要往已有 KB 里覆盖）。
- Python 3 可用（`py --version` / `python3 --version`）—— `scripts/lint.py` 用到。

## 步骤

### 1. 与用户确认目标

简短问清：

- **目录路径**（绝对路径，例如 `E:/Knowledge bases/AI/`）。如果路径已存在且非空，停下来确认是否覆盖。
- **领域名**（一句话，例如「飞书 / Lark 生态」「AI 研究」「个人健康」）——用于初始 commit message、`log.md` 第一条、以及 `README.md` 标题，**不写入 AGENTS.md**（schema 保持领域无关）。

不要问颜色、tags 等细节。Schema 是领域无关的，用户后续 ingest 第一篇来源时再自然发散。

### 2. 创建目录树

```
<target>/
├── AGENTS.md              # canonical schema
├── CLAUDE.md              # @AGENTS.md import（Claude Code 入口）
├── README.md              # 人类入口（标题含领域名）
├── .gitignore
├── raw/
│   ├── articles/          # 手动保存的文章
│   ├── clippings/         # Web Clipper 主入口
│   ├── images/            # 截图、图片
│   ├── pdfs/              # PDF + 元数据
│   ├── notes/             # 随手记录
│   └── personal/          # ★ 用户自己写的素材
├── wiki/
│   ├── index.md           # 内容目录索引（meta）
│   ├── overview.md        # 高层综述 + Health Dashboard（meta）
│   ├── QUESTIONS.md       # 开放问题队列（meta）
│   ├── log.md             # 行为流水线：grep-friendly ingest/query 历史（meta）
│   ├── sources/           # type:source 页面
│   ├── concepts/          # type:concept 页面
│   ├── entities/          # type:entity 页面
│   ├── synthesis/         # type:synthesis 页面
│   └── templates/         # source.md / entity.md / concept.md / synthesis.md
├── outputs/               # 非 markdown 产物（slides, charts, lint 报告等）
└── scripts/
    └── lint.py            # 9 项 wiki 健康检查
```

每个**没有自带文件的空目录**放一个 `.gitkeep`（必须的：raw 的 6 个子目录、wiki/sources、wiki/concepts、wiki/entities、wiki/synthesis、outputs/）。`wiki/templates/` 因为有 4 个 .md 模板文件，不需要 .gitkeep。

### 3. 复制模板文件

从本 skill 的 `templates/` 目录读取并写入 target。模板树与目标树映射：

| 模板路径 | 目标路径 | 占位符替换 |
|---|---|---|
| `templates/AGENTS.md` | `<target>/AGENTS.md` | 无 |
| `templates/CLAUDE.md` | `<target>/CLAUDE.md` | 无 |
| `templates/README.md` | `<target>/README.md` | 无（runbook 已领域无关） |
| `templates/wiki/log.md` | `<target>/wiki/log.md` | `{{DATE}}` → 今日日期（YYYY-MM-DD），`{{DOMAIN}}` → 领域名 |
| `templates/gitignore` | `<target>/.gitignore` | 无（注意目标文件名带点） |
| `templates/wiki/index.md` | `<target>/wiki/index.md` | 无 |
| `templates/wiki/overview.md` | `<target>/wiki/overview.md` | 无 |
| `templates/wiki/QUESTIONS.md` | `<target>/wiki/QUESTIONS.md` | 无 |
| `templates/wiki/templates/source.md` | `<target>/wiki/templates/source.md` | 无 |
| `templates/wiki/templates/entity.md` | `<target>/wiki/templates/entity.md` | 无 |
| `templates/wiki/templates/concept.md` | `<target>/wiki/templates/concept.md` | 无 |
| `templates/wiki/templates/synthesis.md` | `<target>/wiki/templates/synthesis.md` | 无 |
| `templates/scripts/lint.py` | `<target>/scripts/lint.py` | 无 |

读取模板用 `Read`，写入用 `Write`。**不要**把 `{{DATE}}` / `{{DOMAIN}}` 占位符留在最终文件里。

### 4. 初始 commit

```bash
cd <target>
git init
git add -A
git commit -m "scaffold: initial LLM Wiki for <DOMAIN>"
```

如果 git 用户未配置，用 `git -c user.name=... -c user.email=...` 一次性传入（不要全局改 config）。

### 5. 验证

```bash
py scripts/lint.py
```

预期输出：「共 0 项问题」，9 项全部 ✓，exit 0。如果失败说明 scaffold 有问题，先排查再交给用户。

### 6. 报告

向用户输出：

- 目标路径与首个 commit 的 short hash。
- lint 验证结果。
- 提示下一步：
  - 把第一篇 raw 文件放进 `raw/<对应子目录>/`（多数情况是 `raw/clippings/`），然后说「ingest」。
  - schema 在 [AGENTS.md](AGENTS.md)，演化都改这一个文件并在 `log.md` 记 `schema` 操作。

## 不要做

- **不要**自动给新 KB 添加 Obsidian vault 配置（`.obsidian/`）——让用户在 Obsidian 里 Open as vault 时自动生成。
- **不要**在 AGENTS.md 里写领域专属规则（飞书术语、AI 标签等）。Schema 跨领域复用。
- **不要**预先创建任何 wiki 内容页（entity / concept / synthesis / source）。第一次 ingest 时再生成。`wiki/templates/*.md` 是模板（LLM 创建新页时套用），不算内容页。
- **不要**把已有领域 KB 的内容复制过去。每个 KB 从空开始。

## Schema 演化反向同步

如果用户在某个具体 KB 中迭代了 AGENTS.md schema 并希望沉淀回 skill：

1. 用户明确说「把这条规则同步到 skill 模板」。
2. 把改动手工同步到 `templates/AGENTS.md`（以及 `templates/wiki/templates/` 下的页面模板，如有相关变化）。
3. 如果 schema 变化影响 lint 行为（type 枚举、必填字段、子目录约束），同步更新 `templates/scripts/lint.py`。
4. **不要**自动监听或定期同步——schema 变更需要人工判断是否真的通用。
