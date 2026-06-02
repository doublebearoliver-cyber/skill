# 方伟投资视角 Skill

基于公众号「方伟看十年」52 篇原文 + 群聊实时更新蒸馏的 Mavis Agent Skill。

## 安装（首次）

```bash
# 克隆到本地 Mavis skills 目录（公开仓库，无需 token）
git clone https://github.com/doublebearoliver-cyber/skill.git \
  ~/.mavis/agents/mavis/skills/fangwei-perspective

# 验证安装成功
ls ~/.mavis/agents/mavis/skills/fangwei-perspective/SKILL.md
```

安装完成后重启 Mavis 或刷新 skill 列表即可使用。

## 更新

```bash
cd ~/.mavis/agents/mavis/skills/fangwei-perspective
git pull
```

## 多平台支持

本仓库同时输出以下平台的适配版本，**内容与 Mavis Skill 完全一致**，由 `convert.py` 自动生成：

| 平台 | 文件 | 使用方式 |
|------|------|---------|
| **Mavis** | `fangwei-perspective/SKILL.md` | 放入 `~/.mavis/agents/<agent>/skills/` |
| **Claude Code** | `exports/claude.md` | 放入项目 `.claude/` 目录 |
| **OpenAI GPTs** | `exports/gpts-instructions.txt` | 复制到 Assistant 的 Instructions 字段 |
| **Cursor / Codex** | `exports/cursorrules` | 放入项目根目录 |
| **Coze** | `exports/coze-prompt.txt` | 复制到 Bot 的提示词中 |

### 各平台详细说明

**Claude Code**
```bash
# 在项目目录中
mkdir -p .claude/commands
cp exports/claude.md .claude/commands/fangwei.md
```

**OpenAI GPTs**
打开 https://chat.openai.com/gpts/edit → 粘贴 `exports/gpts-instructions.txt` 的全部内容到 Instructions。

**Cursor / Codex**
将 `exports/cursorrules` 的全部内容粘贴到项目的 `.cursorrules` 文件。

**Coze**
打开 Coze Bot 编辑页面 → 粘贴 `exports/coze-prompt.txt` 的全部内容到提示词。

## 重新生成多平台文件

如果修改了 `SKILL.md`，重新运行转换脚本：

```bash
python3 convert.py
```

## 触发方式

- "用方伟的视角分析 X"
- "方伟会怎么看"
- "fangwei perspective"
- "以方伟思路评估这家公司"

## 核心内容

| 模块 | 内容 |
|------|------|
| 分析框架 | "1"（企业的核心）、进入壁垒、Fact vs Opinion、质量 vs 数量等 10 个框架 |
| 出海质量 | 真全球化 vs 假全球化，直营 vs 代理商判断标准 |
| 反共识点 | 14 条主流观点 vs 方伟反共识 |
| 近期判断 | 腾讯、英伟达、拼多多、美团等具体持仓观点（2026年5-6月） |
| 引用原文 | 52 篇公众号文章的 reference 文件 |

## 版本

- **v1.2.0** — 新增视频号 vs 抖音"产品 vs 流量"框架、短视频竞争格局判断
