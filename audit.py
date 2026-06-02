#!/usr/bin/env python3
"""
方伟 Skill 更新质量检查脚本
每次 skill 更新后，运行此脚本对比新旧版本，生成评审报告。
"""

import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime

SKILL_PATH = Path(__file__).parent / "fangwei-perspective" / "SKILL.md"

def get_git_prev(skill_path):
    """获取 skill 文件的上一版本内容"""
    skill_rel = str(skill_path.relative_to(Path(__file__).parent))
    try:
        result = subprocess.run(
            ["git", "show", f"HEAD~1:{skill_rel}"],
            capture_output=True, text=True, cwd=Path(__file__).parent, timeout=10
        )
        return result.stdout if result.returncode == 0 else None
    except Exception:
        return None

def check_structure(content: str) -> dict:
    """检查结构完整性"""
    checks = {
        "角色定义": bool(re.search(r"方伟", content)),
        "核心立场": bool(re.search(r"买股票就是买公司|产品经理|长期主义|不懂不碰|屁股影响脑袋", content)),
        "分析框架": len(re.findall(r"框架 \d+", content)),
        "分析模板": bool(re.search(r"分析输出模板|需求.*Save Time|Kill Time", content)),
        "反共识点": bool(re.search(r"反共识", content)),
        "表达DNA": bool(re.search(r"第一人称|自嘲|结论先行", content)),
        "边界说明": bool(re.search(r"不适用于|不回答|太难了", content)),
        "引用速查": bool(re.search(r"引用文章速查|references/\d+\.md", content)),
        "近期判断": bool(re.search(r"2026|腾讯|英伟达|拼多多|美团", content)),
    }
    return checks

def check_consistency(content: str) -> dict:
    """检查内部一致性"""
    issues = []

    # 检查反共识条数是否一致
    anti_table = re.findall(r"^\|\s*\d+\s*\|", content, re.MULTILINE)
    # 检查反共识表格标题行数
    anti_header = re.search(r"## 第四章.*反共识", content)
    if anti_table:
        count_in_text = len(re.findall(r"主流观点.*方伟反共识", content, re.DOTALL))
        issues.append(f"反共识表格行数：{len(anti_table)}")

    # 检查框架编号是否连续
    framework_nums = re.findall(r"框架 (\d+)", content)
    if framework_nums:
        expected = list(range(1, len(framework_nums) + 1))
        actual = [int(n) for n in framework_nums]
        if sorted(actual) != expected:
            issues.append(f"框架编号不连续：找到 {actual}，期望 {expected}")

    # 检查是否有空表格行
    empty_table_rows = len(re.findall(r"\|[ ]*\|[ ]*\|", content))
    if empty_table_rows > 0:
        issues.append(f"发现 {empty_table_rows} 行空表格行")

    return {"issues": issues, "pass": len(issues) == 0}

def count_stats(content: str) -> dict:
    """统计基本信息"""
    lines = content.split("\n")
    chars = len(content)
    tables = len(re.findall(r"\|.*\|", content))
    quotes = len(re.findall(r"> ", content))
    headers = len(re.findall(r"^#{1,3} ", content, re.MULTILINE))

    # 估算字数（去掉 markdown 语法）
    plain = re.sub(r"\[.*?\]\(.*?\)|[#*|`>\[\]|]", "", content)
    words = len(plain.split())

    return {
        "总行数": len(lines),
        "总字符": chars,
        "估算中文字数": words,
        "表格行数": tables,
        "引用行数": quotes,
        "标题数": headers,
    }

def generate_report(old_content, new_content):
    old_stats = count_stats(old_content)
    new_stats = count_stats(new_content)
    new_structure = check_structure(new_content)
    consistency = check_consistency(new_content)

    print("=" * 60)
    print("  方伟 Skill 更新评审报告")
    print(f"  生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    print("\n📊 内容规模变化")
    for key in old_stats:
        delta = new_stats[key] - old_stats[key]
        sign = "+" if delta > 0 else ""
        print(f"  {key}：{old_stats[key]} → {new_stats[key]}  ({sign}{delta})")

    print("\n✅ 结构完整性检查")
    all_pass = True
    for item, ok in new_structure.items():
        status = "✅" if ok else "❌"
        if not ok:
            all_pass = False
        print(f"  {status} {item}")
    if not all_pass:
        print("  ⚠️  有结构缺失，请检查")

    print("\n🔍 内部一致性检查")
    if consistency["pass"]:
        print("  ✅ 无明显一致性问题")
    else:
        for issue in consistency["issues"]:
            print(f"  ⚠️  {issue}")

    print("\n📋 评审结论")
    if old_content is None:
        print("  ℹ️  首次版本，无历史对比")
        print("  → 请人工检查：内容是否准确表达了方伟的思维框架")
        return

    # 内容变化检测
    added_sections = []
    removed_sections = []

    old_headers = set(re.findall(r"^## (.+)$", old_content, re.MULTILINE))
    new_headers = set(re.findall(r"^## (.+)$", new_content, re.MULTILINE))
    for h in new_headers - old_headers:
        added_sections.append(h)
    for h in old_headers - new_headers:
        removed_sections.append(h)

    if added_sections:
        print("  ➕ 新增章节：")
        for s in added_sections:
            print(f"     · {s}")
    if removed_sections:
        print("  ➖ 减少章节：")
        for s in removed_sections:
            print(f"     · {s}")

    if not added_sections and not removed_sections:
        print("  ℹ️  章节结构无变化，内容在现有章节内更新")

    print("\n💡 建议人工核查点：")
    print("  1. 新增内容是否符合方伟原意？（引用原文/群聊为依据）")
    print("  2. 更新后是否有事实性错误？（人名/公司名/数据/引用）")
    print("  3. 各平台导出文件（exports/）是否正常生成？")
    print("  4. 反共识点的逻辑是否自洽？")

    print("\n" + "=" * 60)


def main():
    if not SKILL_PATH.exists():
        print(f"❌ 找不到 SKILL.md：{SKILL_PATH}")
        sys.exit(1)

    new_content = SKILL_PATH.read_text(encoding="utf-8")
    old_content = get_git_prev(SKILL_PATH)

    generate_report(old_content, new_content)

    # 如果有 exports，也检查一下
    exports_dir = Path(__file__).parent / "exports"
    if exports_dir.exists():
        export_files = list(exports_dir.glob("*"))
        print(f"\n📁 exports 目录：{len(export_files)} 个文件")
        for f in sorted(export_files):
            lines = len(f.read_text(encoding="utf-8").split("\n"))
            print(f"   {f.name} ({lines} 行)")


if __name__ == "__main__":
    main()
