#!/usr/bin/env python3
"""
方伟投资视角 Skill — 多平台转换脚本
将 SKILL.md 转换为各平台可用格式：
  - claude.md        Claude Code 项目指令
  - gpts-instructions.txt  OpenAI GPTs Assistant 指令
  - cursorrules      Cursor / Codex 项目规则
  - coze-prompt.txt  Coze Bot 提示词

用法：python3 convert.py
"""

import re
from pathlib import Path

SKILL_PATH = Path(__file__).parent / "fangwei-perspective" / "SKILL.md"
OUT_DIR = Path(__file__).parent / "exports"


# ─── 解析 SKILL.md ───────────────────────────────────────────────────────────

def parse_skill(path):
    raw = path.read_text(encoding="utf-8")

    # 去掉 frontmatter (---...---)
    raw = re.sub(r"^---\n.*?\n---\n", "", raw, flags=re.DOTALL)

    # 按 ## 标题分割（保留标题行，去掉 leading ##）
    pattern = re.compile(r"(?=\n## )", flags=re.MULTILINE)
    parts = pattern.split(raw)
    parts = [p for p in parts if p.strip()]

    sections = {}
    for part in parts:
        m = re.match(r"\n## (.+?)\n(.*)", part, flags=re.DOTALL)
        if m:
            title = m.group(1).strip()
            content = m.group(2).strip()
            sections[title] = content
    return sections


# ─── 各平台生成器 ────────────────────────────────────────────────────────────

def to_claude_md(sections: dict) -> str:
    """Claude Code 项目级指令（settings.json 中加载）"""
    role = sections.get("你是谁", "")
    stance = sections.get("核心立场（必须保持）", "")
    frameworks = sections.get("第二章：核心思维框架", "")
    template = sections.get("第三章：分析输出模板", "")
    anti = sections.get("第四章：反共识点", "")
    recent = sections.get("第四章附：近期具体判断（来自群聊，2026年5-6月）", "")
    dna = sections.get("第五章：表达 DNA", "")
    boundary = sections.get("第六章：边界（不回答的问题）", "")
    refs = sections.get("引用文章速查（52 篇）", "")

    # 精简核心框架（提取框架名+关键引用）
    framework_lines = []
    in_framework = False
    for line in frameworks.split("\n"):
        if re.match(r"^### 框架 \d+：", line):
            framework_lines.append(line)
            in_framework = True
        elif in_framework and line.startswith("**"):
            framework_lines.append(line)
        elif in_framework and not line.strip():
            in_framework = False

    out = []
    out.append("# 方伟投资视角 — Claude Code 指令")
    out.append("")
    out.append(role.strip())
    out.append("")
    out.append("## 核心立场")
    out.append(_condense(stance))
    out.append("")
    out.append("## 思维框架（摘要）")
    out.append(_condense("\n".join(framework_lines[:12])))
    out.append("")
    out.append("## 分析模板（使用时引用）")
    out.append(_condense(template))
    out.append("")
    out.append("## 表达 DNA")
    out.append(_condense(dna))
    out.append("")
    out.append("## 边界（不回答）")
    out.append(_condense(boundary))
    out.append("")
    out.append("## 反共识速查")
    out.append(_condense(anti))
    out.append("")
    out.append("## 近期判断（2026年5-6月）")
    out.append(_condense(recent))

    return "\n".join(out)


def to_gpts_instructions(sections: dict) -> str:
    """OpenAI GPTs / Assistant instructions"""
    role = sections.get("你是谁", "")
    stance = sections.get("核心立场（必须保持）", "")
    frameworks = sections.get("第二章：核心思维框架", "")
    template = sections.get("第三章：分析输出模板", "")
    anti = sections.get("第四章：反共识点", "")
    recent = sections.get("第四章附：近期具体判断（来自群聊，2026年5-6月）", "")
    dna = sections.get("第五章：表达 DNA", "")
    boundary = sections.get("第六章：边界（不回答的问题）", "")

    out = []
    out.append(role.strip())
    out.append("")
    out.append("## 核心立场（必须保持）")
    out.append(_condense(stance))
    out.append("")
    out.append("## 分析框架（10个）")
    out.append(_condense(_extract_frameworks(frameworks)))
    out.append("")
    out.append("## 分析模板")
    out.append(_condense(template))
    out.append("")
    out.append("## 反共识点（14条）")
    out.append(_condense(anti))
    out.append("")
    out.append("## 近期具体判断（2026年5-6月）")
    out.append(_condense(recent))
    out.append("")
    out.append("## 表达 DNA")
    out.append(_condense(dna))
    out.append("")
    out.append("## 边界")
    out.append(_condense(boundary))
    out.append("")
    out.append("你扮演方伟，以第一人称「我」给出分析，不自报家门，直接切入。")

    return "\n".join(out)


def to_cursorrules(sections: dict) -> str:
    """Cursor / Codex .cursorrules"""
    role = sections.get("你是谁", "")
    stance = sections.get("核心立场（必须保持）", "")
    frameworks = sections.get("第二章：核心思维框架", "")
    template = sections.get("第三章：分析输出模板", "")
    anti = sections.get("第四章：反共识点", "")
    recent = sections.get("第四章附：近期具体判断（来自群聊，2026年5-6月）", "")
    dna = sections.get("第五章：表达 DNA", "")
    boundary = sections.get("第六章：边界（不回答的问题）", "")

    out = []
    out.append("# 方伟投资视角 — Cursor / Codex 项目规则")
    out.append("")
    out.append("## 角色定义")
    out.append(role.strip())
    out.append("")
    out.append("## 核心立场")
    out.append(_condense(stance))
    out.append("")
    out.append("## 10大思维框架")
    out.append(_condense(_extract_frameworks(frameworks)))
    out.append("")
    out.append("## 分析模板")
    out.append(_condense(template))
    out.append("")
    out.append("## 反共识点")
    out.append(_condense(anti))
    out.append("")
    out.append("## 近期判断（2026年5-6月）")
    out.append(_condense(recent))
    out.append("")
    out.append("## 表达规则")
    out.append(_condense(dna))
    out.append("")
    out.append("## 不回答的问题")
    out.append(_condense(boundary))
    out.append("")
    out.append("以第一人称「我」回答，直接给出分析结论，不自报家门。")

    return "\n".join(out)


def to_coze_prompt(sections: dict) -> str:
    """Coze Bot 提示词（结构化分块）"""
    role = sections.get("你是谁", "")
    stance = sections.get("核心立场（必须保持）", "")
    frameworks = sections.get("第二章：核心思维框架", "")
    template = sections.get("第三章：分析输出模板", "")
    anti = sections.get("第四章：反共识点", "")
    recent = sections.get("第四章附：近期具体判断（来自群聊，2026年5-6月）", "")
    dna = sections.get("第五章：表达 DNA", "")
    boundary = sections.get("第六章：边界（不回答的问题）", "")

    out = []
    out.append("【角色定义】")
    out.append(role.strip())
    out.append("")
    out.append("【必须遵守的核心立场】")
    out.append(_condense(stance))
    out.append("")
    out.append("【分析框架】")
    out.append(_condense(_extract_frameworks(frameworks)))
    out.append("")
    out.append("【分析模板】")
    out.append(_condense(template))
    out.append("")
    out.append("【反共识点速查】")
    out.append(_condense(anti))
    out.append("")
    out.append("【近期判断（2026年5-6月）】")
    out.append(_condense(recent))
    out.append("")
    out.append("【表达风格】")
    out.append(_condense(dna))
    out.append("")
    out.append("【禁止回答】")
    out.append(_condense(boundary))
    out.append("")
    out.append("【开场白】以「我」的第一人称直接给出投资分析，不自报家门，不说「我是AI」。")

    return "\n".join(out)


# ─── 辅助函数 ────────────────────────────────────────────────────────────────

def _condense(text: str) -> str:
    """精简文本：去掉多余空行、表格md格式、过长引用"""
    lines = text.split("\n")
    result = []
    blank_count = 0
    for line in lines:
        stripped = line.strip()
        # 跳过纯表格分隔行
        if re.match(r"^\|[-| :]+\|$", stripped):
            continue
        # 跳过空标题行
        if stripped in ["## 1. 这家公司在解决什么需求？", "## 2. 这家公司的「1」是什么？",
                         "## 3. 护城河——真的是进入壁垒吗？", "## 4. 出海质量（如适用）",
                         "## 5. 利润质量", "## 6. 我倾向于……"]:
            continue
        if stripped:
            blank_count = 0
            result.append(stripped)
        else:
            blank_count += 1
            if blank_count <= 1:
                result.append("")
    return "\n".join(result)


def _extract_frameworks(text: str) -> str:
    """提取框架标题和核心引用，跳过详细展开"""
    lines = text.split("\n")
    result = []
    for i, line in enumerate(lines):
        # 框架标题行
        if re.match(r"^### 框架 \d+：", line):
            result.append(line)
        # 下一行如果是"核心原则"或引号开头，保留
        elif result and i > 0 and lines[i-1].startswith("### 框架"):
            if line.startswith("**") and "：" in line:
                result.append(line)
            elif line.startswith('>'):
                result.append(line)
    return "\n".join(result)


# ─── 主逻辑 ────────────────────────────────────────────────────────────────

def main():
    print("📖 解析 SKILL.md...")
    sections = parse_skill(SKILL_PATH)
    print(f"   解析到 {len(sections)} 个章节")

    OUT_DIR.mkdir(exist_ok=True)

    generators = [
        ("claude.md", to_claude_md),
        ("gpts-instructions.txt", to_gpts_instructions),
        ("cursorrules", to_cursorrules),
        ("coze-prompt.txt", to_coze_prompt),
    ]

    for filename, generator in generators:
        content = generator(sections)
        out_path = OUT_DIR / filename
        out_path.write_text(content, encoding="utf-8")
        lines = len(content.split("\n"))
        print(f"   ✅ {filename} ({lines} 行)")

    print(f"\n🎉 输出目录：{OUT_DIR.relative_to(Path(__file__).parent)}")


if __name__ == "__main__":
    main()
