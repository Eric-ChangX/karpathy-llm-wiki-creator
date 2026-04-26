---
name: llm-wiki-scaffold
version: 1.0.0
description: "在指定路径下初始化一个新的 LLM Wiki 知识库（Karpathy 风格：raw/ 不动 + wiki/ 累积综合 + index.md 导航 + log.md 时间线 + Obsidian 友好）。当用户说『新建一个知识库』『初始化一个 LLM Wiki』『为 X 领域开一个 wiki』『scaffold 一个新知识库』时使用。每个 KB 一个领域（飞书、AI、个人项目等各自独立）。本 skill 只负责脚手架，不导入任何 raw 内容。"
---

# LLM Wiki Scaffold

为新领域知识库创建标准 scaffold。每个领域独立一个目录，互不干扰。

## 使用前提

- 已有 git 可用（`git --version`）。
- 用户已选好或会指定一个**新的目录路径**（不要往已有 KB 里覆盖）。

## 步骤

### 1. 与用户确认目标

简短问清：

- **目录路径**（绝对路径，例如 `E:/Knowledge bases/AI/`）。如果路径已存在且非空，停下来确认是否覆盖。
- **领域名**（一句话，例如「飞书 / Lark 生态」「AI 研究」「个人健康」）——只用于初始 commit message 和 log 第一条，**不写入 AGENTS.md**（schema 保持领域无关）。

不要问颜色、tags 等细节。Schema 是领域无关的，用户后续 ingest 第一篇来源时再自然发散。

### 2. 创建目录树

```
<target>/
├── AGENTS.md
├── CLAUDE.md
├── index.md
├── log.md
├── .gitignore
├── raw/
│   └── assets/
├── wiki/
│   └── sources/
├── outputs/
└── scripts/
```

每个空目录放一个 `.gitkeep`（否则 git 不会跟踪）。

### 3. 复制模板文件

从本 skill 的 `templates/` 目录读取并写入到 target：

| 模板源 | 目标文件 | 替换 |
|---|---|---|
| `templates/AGENTS.md` | `<target>/AGENTS.md` | 无（完全领域无关） |
| `templates/CLAUDE.md` | `<target>/CLAUDE.md` | 无 |
| `templates/index.md` | `<target>/index.md` | 无 |
| `templates/log.md` | `<target>/log.md` | `{{DATE}}` → 今日日期（YYYY-MM-DD），`{{DOMAIN}}` → 用户给的领域名 |
| `templates/gitignore` | `<target>/.gitignore` | 无（注意目标文件名带点） |

读取模板时用 `Read`，写入用 `Write`。**不要**把 `{{DATE}}` 等占位符留在最终文件里。

### 4. 初始 commit

```bash
cd <target>
git init
git add -A
git commit -m "scaffold: initial LLM Wiki for <DOMAIN>"
```

如果 git 用户未配置，用 `git -c user.name=... -c user.email=...` 一次性传入（不要全局改 config）。

### 5. 报告

向用户输出：

- 目标路径与首个 commit 的 short hash。
- 提示下一步：把第一篇 raw 文件放进 `raw/`，然后说「ingest」即可。
- 提醒：所有结构规则在 [AGENTS.md](AGENTS.md)，schema 演化都改这一个文件。

## 不要做

- **不要**自动给新 KB 添加 Obsidian vault 配置（`.obsidian/`）——让用户在 Obsidian 里 Open as vault 时自动生成。
- **不要**在 AGENTS.md 里写领域专属规则（飞书术语、AI 标签等）。Schema 跨领域复用。
- **不要**预先创建任何 wiki 页面或 source page。第一次 ingest 时再生成。
- **不要**把已有领域 KB 的内容复制过去。每个 KB 从空开始。

## Schema 演化反向同步

如果用户在某个具体 KB 中迭代了 AGENTS.md schema 并希望沉淀回 skill：

1. 用户明确说「把这条规则同步到 skill 模板」。
2. 把改动手工同步到 `templates/AGENTS.md`。
3. **不要**自动监听或定期同步——schema 变更需要人工判断是否真的通用。
