#!/usr/bin/env python3
"""Wiki 健康检查 — 对照 AGENTS.md schema 跑 9 项机械检查。

用法:
    py scripts/lint.py           # Windows: 输出到 stdout
    py scripts/lint.py --write   # Windows: 同时写到 outputs/<YYYY-MM-DD>_lint_<short>.md

stdlib only。无外部依赖。
"""
import argparse
import ast
import datetime
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

# Windows 默认 GBK 控制台无法直接输出 ✓ / ✗ 这类字符；强制 stdout/stderr UTF-8。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
OUTPUTS = ROOT / "outputs"
LOG = ROOT / "log.md"

TYPE_DIR = {
    "source": "sources",
    "entity": "entities",
    "concept": "concepts",
    "synthesis": "synthesis",
}
META_FILES = {"index.md", "overview.md", "QUESTIONS.md"}
WIKILINK_RE = re.compile(r'(!?)\[\[([^\]|#]+?)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]')
LOG_HEADING_RE = re.compile(r'^## \[(\d{4}-\d{2}-\d{2})\] (\w+) \| (.+)$')
VALID_OPS = {"ingest", "query", "lint", "schema", "scaffold"}
REQUIRED_FRONTMATTER = {
    "source": ["type", "created", "updated", "raw", "captured"],
    "entity": ["type", "created", "updated"],
    "concept": ["type", "created", "updated"],
    "synthesis": ["type", "created", "updated"],
}


def parse_frontmatter(text):
    """Minimal YAML-ish parser handling scalars, empty values, and simple lists."""
    if not (text.startswith("---\n") or text.startswith("---\r\n")):
        return None, text
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return None, text
    end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end == -1:
        return None, text
    fm = {}
    current_list = None
    for line in lines[1:end]:
        if not line.strip():
            continue
        if line.startswith((" ", "\t")):
            stripped = line.strip()
            if stripped.startswith("- ") and current_list is not None:
                current_list.append(stripped[2:].strip().strip("\"'"))
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip()
        v = v.strip()
        if v == "[]":
            fm[k] = []
            current_list = None
        elif v.startswith("[") and v.endswith("]"):
            fm[k] = parse_inline_list(v)
            current_list = None
        elif v == "":
            fm[k] = []
            current_list = fm[k]
        else:
            fm[k] = v.strip("\"'")
            current_list = None
    return fm, "\n".join(lines[end + 1:])


def parse_inline_list(value):
    """Parse a small YAML-style inline list such as ["A", "B"]."""
    try:
        parsed = ast.literal_eval(value)
    except Exception:
        parsed = [part.strip().strip("\"'") for part in value.strip("[]").split(",")]
    if not isinstance(parsed, list):
        return []
    return [str(item).strip() for item in parsed if str(item).strip()]


def collect_wiki_pages():
    """Return dict: wiki-relative page id → page metadata."""
    pages = {}
    if not WIKI.exists():
        return pages
    for md in WIKI.rglob("*.md"):
        rel = md.relative_to(WIKI)
        if md.name in META_FILES and len(rel.parts) == 1:
            continue
        if rel.parts[0] == "templates":
            continue
        text = md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        info = {
            "path": md,
            "rel_to_wiki": rel,
            "rel_to_root": md.relative_to(ROOT),
            "frontmatter": fm,
            "body": body,
            "raw_text": text,
        }
        key = rel.with_suffix("").as_posix()
        pages[key] = info
    return pages


def strip_code_fences(text):
    """Remove ``` fenced blocks AND `inline` code so wikilinks inside examples are not counted."""
    out = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    text = "\n".join(out)
    return re.sub(r"`[^`\n]*`", "", text)


def collect_all_wikilinks():
    """Scan all .md (except outputs/ and templates/) for [[X]] / ![[X]] references.

    Returns dict: target_string → list of {source, is_embed}.
    Targets keep their literal form including any subdir prefix.
    Links inside ``` code fences are ignored — schema docs use them as examples.
    """
    refs = defaultdict(list)
    skip_dirs = {"outputs", ".git", ".obsidian", "node_modules"}
    for md in ROOT.rglob("*.md"):
        rel_parts = md.relative_to(ROOT).parts
        if any(p in skip_dirs for p in rel_parts):
            continue
        if len(rel_parts) >= 2 and rel_parts[0] == "wiki" and rel_parts[1] == "templates":
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except Exception:
            continue
        text = strip_code_fences(text)
        for m in WIKILINK_RE.finditer(text):
            embed_marker, target = m.group(1), m.group(2).strip()
            refs[target].append({"source": md, "is_embed": embed_marker == "!"})
    return refs


def page_aliases(info):
    """All link forms that should resolve to this page: stem, subdir/stem, and aliases."""
    forms = {info["rel_to_wiki"].stem}
    if len(info["rel_to_wiki"].parts) > 1:
        forms.add(info["rel_to_wiki"].with_suffix("").as_posix())
    fm = info["frontmatter"] or {}
    aliases = fm.get("aliases", [])
    if isinstance(aliases, str):
        aliases = parse_inline_list(aliases) if aliases.startswith("[") else [aliases]
    for alias in aliases or []:
        alias = str(alias).strip()
        if alias:
            forms.add(alias)
    return forms


# ---------- 9 checks ----------

def check_1_broken_wikilinks(pages, references):
    """[[X]] / ![[X]] target where no matching page/output exists, or a bare target is ambiguous."""
    findings = []
    target_map = defaultdict(list)
    for info in pages.values():
        for alias in page_aliases(info):
            target_map[alias].append(info)
    # also include meta files at wiki root
    for name in ("index", "overview", "QUESTIONS"):
        target_map[name].append({"rel_to_root": WIKI / f"{name}.md"})
    for target, ref_list in sorted(references.items()):
        if target.startswith("outputs/") or target.startswith("outputs\\"):
            continue
        if target in target_map:
            if "/" not in target and "\\" not in target and len(target_map[target]) > 1:
                matches = ", ".join(
                    i["rel_to_root"].as_posix() for i in target_map[target]
                )
                for ref in ref_list:
                    findings.append(
                        f"  - `[[{target}]]` in {ref['source'].relative_to(ROOT).as_posix()} "
                        f"存在歧义，可匹配: {matches}"
                    )
            continue
        for ref in ref_list:
            findings.append(f"  - `[[{target}]]` in {ref['source'].relative_to(ROOT).as_posix()}")
    return findings


def check_2_orphan_pages(pages, references):
    """Wiki page with no inbound [[X]] from anywhere."""
    findings = []
    inbound = set(references.keys())
    for name, info in sorted(pages.items()):
        forms = page_aliases(info)
        if not (forms & inbound):
            findings.append(f"  - {info['rel_to_root'].as_posix()}")
    return findings


def check_3_frontmatter(pages):
    """Every wiki page must have frontmatter with required fields per type."""
    findings = []
    for name, info in sorted(pages.items()):
        fm = info["frontmatter"]
        if fm is None:
            findings.append(f"  - {info['rel_to_root'].as_posix()}: 缺 frontmatter")
            continue
        t = fm.get("type")
        required = REQUIRED_FRONTMATTER.get(t, REQUIRED_FRONTMATTER["entity"])
        missing = [k for k in required if k not in fm]
        if missing:
            findings.append(f"  - {info['rel_to_root'].as_posix()}: 缺字段 {missing}")
    return findings


def check_4_invalid_type(pages):
    """type field must be in TYPE_DIR keys."""
    findings = []
    valid = set(TYPE_DIR.keys())
    for name, info in sorted(pages.items()):
        fm = info["frontmatter"] or {}
        t = fm.get("type")
        if t and t not in valid:
            findings.append(f"  - {info['rel_to_root'].as_posix()}: type='{t}' 非法 (允许: {sorted(valid)})")
    return findings


def check_5_source_raw_integrity(pages):
    """type:source must have raw field; raw file must exist."""
    findings = []
    for name, info in sorted(pages.items()):
        fm = info["frontmatter"] or {}
        if fm.get("type") != "source":
            continue
        raw_path = fm.get("raw")
        if not raw_path:
            findings.append(f"  - {info['rel_to_root'].as_posix()}: 缺 raw 字段")
            continue
        full = ROOT / raw_path
        if not full.exists():
            findings.append(f"  - {info['rel_to_root'].as_posix()}: raw='{raw_path}' 文件不存在")
    return findings


def check_6_outputs_broken_refs(references):
    """outputs/ 引用必须落到真实文件；尝试常见扩展名。"""
    findings = []
    exts = ("", ".md", ".png", ".svg", ".jpg", ".jpeg", ".pdf", ".html", ".csv", ".xlsx")
    for target, ref_list in sorted(references.items()):
        if not target.startswith("outputs/"):
            continue
        if any((ROOT / (target + e)).exists() for e in exts):
            continue
        for ref in ref_list:
            embed = "!" if ref["is_embed"] else ""
            findings.append(f"  - `{embed}[[{target}]]` in {ref['source'].relative_to(ROOT).as_posix()}")
    return findings


def check_7_index_completeness(pages):
    """每个 wiki 页都应在 wiki/index.md 出现。"""
    findings = []
    index_path = WIKI / "index.md"
    if not index_path.exists():
        return [f"  - wiki/index.md 不存在"]
    text = strip_code_fences(index_path.read_text(encoding="utf-8"))
    indexed = {m.group(2).strip() for m in WIKILINK_RE.finditer(text)}
    for name, info in sorted(pages.items()):
        if not (page_aliases(info) & indexed):
            findings.append(f"  - {info['rel_to_root'].as_posix()} 未出现在 index.md")
    return findings


def check_8_log_format():
    """log.md 的 ## 标题必须匹配 `## [YYYY-MM-DD] op | title`，op 在合法集合内。"""
    findings = []
    if not LOG.exists():
        return [f"  - log.md 不存在"]
    text = LOG.read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines(), 1):
        if not line.startswith("## "):
            continue
        m = LOG_HEADING_RE.match(line)
        if not m:
            findings.append(f"  - log.md:{i}: 「{line[:60]}」格式错")
            continue
        op = m.group(2)
        if op not in VALID_OPS:
            findings.append(f"  - log.md:{i}: op='{op}' 不在 {sorted(VALID_OPS)}")
    return findings


def check_9_page_in_wrong_subdir(pages):
    """type:X 页面必须放在 wiki/<TYPE_DIR[X]>/ 下。"""
    findings = []
    for name, info in sorted(pages.items()):
        fm = info["frontmatter"] or {}
        t = fm.get("type")
        if t not in TYPE_DIR:
            continue
        expected = TYPE_DIR[t]
        rel_parts = info["rel_to_wiki"].parts
        actual_subdir = rel_parts[0] if len(rel_parts) > 1 else None
        if actual_subdir != expected:
            findings.append(f"  - {info['rel_to_root'].as_posix()}: type={t} 应在 wiki/{expected}/")
    return findings


CHECKS = [
    ("1. 断链 (broken wikilinks)", check_1_broken_wikilinks, ("pages", "references")),
    ("2. 孤儿页 (orphan pages)", check_2_orphan_pages, ("pages", "references")),
    ("3. frontmatter 缺失/必填字段", check_3_frontmatter, ("pages",)),
    ("4. type 字段非法", check_4_invalid_type, ("pages",)),
    ("5. source page raw 字段完整性", check_5_source_raw_integrity, ("pages",)),
    ("6. outputs/ 引用断链", check_6_outputs_broken_refs, ("references",)),
    ("7. index.md 缺漏", check_7_index_completeness, ("pages",)),
    ("8. log.md 行格式", check_8_log_format, ()),
    ("9. 页面位置错 (type vs 子目录)", check_9_page_in_wrong_subdir, ("pages",)),
]


def run_lint():
    pages = collect_wiki_pages()
    references = collect_all_wikilinks()
    ctx = {"pages": pages, "references": references}
    results = []
    for name, fn, args in CHECKS:
        kwargs = {a: ctx[a] for a in args}
        results.append((name, fn(**kwargs)))
    return results


def render_report(results):
    today = datetime.date.today().isoformat()
    total = sum(len(f) for _, f in results)
    lines = [
        f"# Wiki Lint Report — {today}",
        "",
        f"_共 {total} 项问题_",
        "",
    ]
    for name, findings in results:
        n = len(findings)
        status = "✓" if n == 0 else f"✗ {n} 条"
        lines.append(f"## {name} — {status}")
        if findings:
            lines.extend(findings)
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Wiki 9-check lint")
    parser.add_argument("--write", action="store_true", help="同时写到 outputs/")
    args = parser.parse_args()

    results = run_lint()
    report = render_report(results)
    print(report)
    if args.write:
        OUTPUTS.mkdir(exist_ok=True)
        today = datetime.date.today().isoformat()
        h = hashlib.md5(report.encode("utf-8")).hexdigest()[:6]
        out = OUTPUTS / f"{today}_lint_{h}.md"
        out.write_text(report, encoding="utf-8")
        print(f"\n→ 写入 {out.relative_to(ROOT).as_posix()}", file=sys.stderr)
    total = sum(len(f) for _, f in results)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
