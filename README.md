# ImageToHTML Skill

![Version](https://img.shields.io/badge/version-0.1.3-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Codex Skill](https://img.shields.io/badge/Codex-Skill-black)
![ShowNowAI](https://img.shields.io/badge/by-ShowNowAI-orange)

ImageToHTML Skill 是一个 Codex Skill，用于把单张视觉稿图片转换成结构化静态 HTML 项目。

由 ShowNowAI 出品。

它不是“把整张图铺成背景”的截图复刻工具。它会尽量把视觉稿拆成可维护的 HTML、CSS、assets、design tokens、文字映射、字体映射、颜色证据和截图 QA 报告。

## Quick Start

从 GitHub 安装：

```text
$skill-installer install https://github.com/candyxiao9216/imagetohtml-skill/tree/main/imagetohtml
```

安装后重启 Codex，然后直接用自然语言启动：

```text
使用 $imagetohtml 把这张视觉稿图片转成结构化静态 HTML。
```

## 这是什么

ImageToHTML Skill 是一套面向 Codex 的视觉稿转 HTML 工作流，包含：

- 面向 Agent 的 Skill 指令。
- 视觉资产处理规则。
- 输出文件契约。
- 图片检查、颜色采样、资产裁切和截图 QA 脚本。
- `asset-manifest.json`、`text-map.json`、`font-map.json` 等结构化记录。

## 能做什么 / 不能做什么

能做：

- 单张视觉稿图片转静态 HTML。
- 将普通文字转成 HTML 真文字。
- 裁切复杂图片、插画和完整品牌 Logo 组合；simple-mark（简单独立图形标识）可手写 SVG。
- 生成颜色证据层、设计 token、最终截图颜色反向 QA 和截图报告。
- 对关键局部区域做单独验收，避免照片主体、组合插画或局部卡片失真后被误判通过。
- 按源视口优先做基础响应式适配。

不能做：

- 不生成多页站点或完整设计系统。
- 不凭空重绘复杂、模糊或品牌识别不确定的 Logo。
- 不把 brand-lockup（完整品牌 Logo 组合）拆成近似图形和系统字体后当作完成。
- 不强行把复杂插画 SVG 化。
- 不承诺像素级 diff 复刻。
- 不替用户确认字体、品牌或私有素材授权。

## 运行环境

基础使用需要：

- Codex。
- Python 3。

脚本依赖：

```bash
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
```

最小验证：

```bash
python3 -m py_compile imagetohtml/scripts/*.py
```

## 使用示例

基础转换：

```text
使用 $imagetohtml 把这张视觉稿图片转成结构化静态 HTML。
```

指定输出目录：

```text
使用 $imagetohtml 把这张图转成 HTML，输出到 outputs/landing-page-html。
```

强调母图边界：

```text
使用 $imagetohtml 转 HTML。simple-mark（简单独立图形标识）可以手写 SVG；brand-lockup（完整品牌 Logo 组合）优先整块裁切保真，不要用系统字体近似替代自定义字标。
```

强调关键区域：

```text
使用 $imagetohtml 转 HTML。请把我圈出的区域作为 critical-region 单独验收；组合插画要按 composition-group 处理，照片缩略图不能裁掉主体。
```

## 输出结构

默认输出结构：

```text
imagetohtml-output/
  source/original.png
  assets/
  colors/
  tokens/tokens.css
  visual-breakdown.md
  asset-manifest.json
  text-map.json
  font-map.json
  index.html
  qa/
    color-check.json
```

这些是生成产物，不是 Skill 本体。

## 目录结构

```text
imagetohtml-skill/
  imagetohtml/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
  README.md
  CHANGELOG.md
  LICENSE
  requirements.txt
```

Codex 真正读取的是 `imagetohtml/` 目录；本 README 用于 GitHub 首页和人工理解。ShowNowAI 作为出品方信息保留在 README 和仓库描述中，不改变 `$imagetohtml` 的调用方式。

## 发布前检查

```bash
quick_validate.py imagetohtml
python3 -m py_compile imagetohtml/scripts/*.py
find . -name '.DS_Store'
rg --glob '!README.md' "/Users|Miyo|米芽|secret|api_key|password|ghp_|AKIA|sk-[A-Za-z0-9]{20,}" .
```

`quick_validate.py` 来自 Codex 的 skill-creator 工具；如果本机没有该命令，可先跳过这一项，但发布前应至少完成脚本编译和敏感内容扫描。

## 版本与更新

查看 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

本项目使用 MIT License，详见 [LICENSE](LICENSE)。

## 问题反馈

如果遇到安装、触发、输出结构或 QA 截图问题，请通过 GitHub Issues 提交。
