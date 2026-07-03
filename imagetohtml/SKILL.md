---
name: imagetohtml
description: Use when Codex needs to convert a single visual mockup image (PNG/JPG/WebP) into a maintainable static HTML page with reusable visual assets, extracted design tokens, OCR-reviewed text, responsive source-viewport-first layout, and screenshot QA. Trigger for requests like image to HTML, visual mockup to HTML, extract visual assets from a generated design, or turn an AI-generated design image into web assets.
---

# Imagetohtml

## 目标

把一张视觉稿图片，翻译成可维护的静态 HTML 小项目。不要把整张图铺成背景，也不要追求像素级复刻；目标是保留视觉语言，同时沉淀可复用资产、文字、布局和设计 token。

## 硬规则

- 原图是母图。除非用户明确要求，不重新生成、重画或改写 logo、插画、人物、构图、表情、动作、风格。
- v1 只处理单张视觉稿图片；多页、多状态、多端完整设计系统不在默认范围内。
- 文字必须转成 HTML 真文字。OCR 只是初稿，必须人工/模型对照母图校对。
- Logo 先分类：`simple-mark`（纯几何、扁平、无自定义字标）才可手写 SVG；`brand-lockup`（图形 + wordmark 品牌字标/中文/slogan 组合）默认整块裁切保真。用户明确要求矢量但无法准确临摹时，标记 `needs-vector-redraw`，不要用系统字体近似替代自定义字标后标记 `confirmed`。
- 图标优先 SVG 化；常见图标优先使用项目已有图标库或 lucide。
- 图片、复杂插画、复杂纹理用 PNG/WebP 资产；按钮、卡片、边框、圆角、阴影、纯色和简单渐变用 CSS。
- 复杂插画、产品图和角色资产裁切必须保留主体、阴影、装饰元素和安全留白；贴边、缺角或被容器裁掉时，不得标记为 `confirmed`。
- 页面结构使用语义化 HTML，不用全局绝对定位拼截图。
- 响应式以原图设备为优先：桌面图桌面优先，手机图手机优先；另一端只保证不溢出、不重叠、顺序合理、视觉风格延续。
- QA 必须生成截图和人工对比报告，并检查裁切遮挡、颜色漂移和源视口关键几何；不要把像素 diff 作为 v1 硬验收。

## 输出结构

```text
imagetohtml-output/
  source/
    original.png
  assets/
    images/
    icons/
    illustrations/
    logos/
    fonts/
  colors/
    raw-colors.json
    palette.png
    color-map.json
  tokens/
    tokens.css
  visual-breakdown.md
  asset-manifest.json
  text-map.json
  font-map.json
  index.html
  qa/
    source-viewport.png
    alternate-viewport.png
    compare-report.md
```

## 工作流

1. 复制母图到 `source/original.png`。
2. 运行 `scripts/inspect_image.py` 获取尺寸、比例、设备推断和基础元信息。
3. 写 `visual-breakdown.md`，逐区判断每个视觉元素应该裁图、SVG 化、CSS 复刻还是转成真文字，并记录源视口关键几何。
4. 做 OCR 初提取，写 `text-map.json`；对照母图校对，不确定内容标 `needs-review`。
5. 匹配相似开源字体，写 `font-map.json`；必须记录来源、许可证和用途。
6. 运行 `scripts/sample_colors.py` 生成颜色证据层；完整颜色统计只作为证据，不等于全部进入 CSS token。
7. 按混合裁切规则运行 `scripts/crop_asset.py` 提取图片、插画、Logo 占位等资产；复杂插画优先加安全留白。
8. 写 `asset-manifest.json`，记录每个资产的来源区域、用途、处理方式和待确认项。
9. 写 `tokens/tokens.css`，包含字体、颜色、字号、间距、圆角、阴影等实际页面会用到的 token；关键颜色必须能追溯到 `colors/color-map.json`。
10. 写 `index.html` 和必要 CSS。先按源视口几何锁定外框、网格、卡片、间距和主要图片区域，再做语义化结构。
11. 运行 `scripts/qa_screenshot.py` 截源视口和另一端视口。
12. 写 `qa/compare-report.md`，列出一致点、主要偏差、待用户确认和暂不处理项；必须单列裁切遮挡、颜色和源视口几何检查。

## 资源判断表

开始写 HTML 前，必须先写一张表：

```text
区域 | 类型 | 处理方式 | 输出 | 状态
Hero 背景 | 复杂图片 | 裁切 WebP，保留主体和安全留白 | assets/images/hero-bg.webp | confirmed
Logo | 品牌标识 | simple-mark 可 SVG；brand-lockup 整块裁切保真；不确定则待矢量重绘 | assets/logos/logo-full.svg 或 logo-lockup.png | confirmed / needs-vector-redraw
标题 | 文本 | OCR 校对后写入 HTML | text-map.json / index.html | confirmed
按钮 | UI 组件 | CSS 复刻 | tokens.css / index.html | confirmed
功能图标 | 图标 | lucide 或 SVG 替换 | assets/icons/ | needs-review
```

详细规则见 `references/asset-rules.md` 和 `references/output-contract.md`。

## 源视口几何

开始写 HTML 前，必须记录关键尺寸和布局关系，例如画布、外框、侧栏、顶部栏、Hero、卡片网格、底部区域、主要间距和圆角。

```text
区域 | 原图位置/尺寸 | HTML 实现策略 | 状态
App 外框 | x,y,w,h | width/max-width/padding/border-radius | confirmed
侧栏 | x,y,w,h | fixed/flex-basis | confirmed
Hero | x,y,w,h | grid/flex + image safe area | confirmed
卡片网格 | 列数/列宽/间距 | CSS grid tracks/gap | confirmed
```

## 字体策略

- 按视觉稿匹配相似开源字体，而不是宣称识别出原字体。
- 只允许使用可公开商用的开源字体。
- 中文字体和英文字体可以分开匹配。
- 必须在 `font-map.json` 记录 `font_family`、`usage`、`reason`、`source`、`license`、`status`。
- 如果字体来源或许可证不确定，状态必须是 `needs-review`，不要下载或内嵌。

## 颜色策略

- 先保留完整颜色采样/统计证据层：`colors/raw-colors.json` 和 `colors/palette.png`。
- 再写 `colors/color-map.json`，说明主要颜色来自哪些区域，并记录 token、采样区域、原图颜色、页面用途和状态。
- `tokens/tokens.css` 可以使用细碎颜色，但不要为了显得系统化而制造大量无意义 token。
- 重复使用或有语义角色的颜色优先进入 token；一次性局部颜色可以写局部 CSS，并在 `color-map.json` 标来源。
- 如果为了对比度或可读性微调颜色，必须在 `color-map.json` 标记为 derived，不要把主观调色写成原图取样。

## 响应式策略

- 先根据原图尺寸、长宽比和 UI 结构判断 `source_viewport`：desktop、mobile、tablet、poster、square 或 `needs-review`。
- 设备判断不能只看像素宽度；高分辨率导出图、放大截图或设计稿可能超过常见设备宽度，需要结合状态栏、导航形态、内容密度和画面比例判断。
- 源视口是第一验收对象，必须按几何记录尽量还原视觉层级、布局和比例；不要把满幅画布误缩成居中的小容器。
- 另一端只要求：无横向溢出、无重叠、信息顺序合理、视觉风格延续。
- 除非用户明确要求，不把另一端适配扩展成完整重设计或多断点设计系统。

## QA 报告格式

`qa/compare-report.md` 使用以下结构：

```markdown
# 对比报告

## 源视口
- 原图尺寸：
- 截图尺寸：
- 结论：

## 一致点
-

## 主要偏差
-

## 裁切/遮挡检查
-

## Logo 核对
-

## 颜色核对
-

## 源视口几何核对
-

## 待用户确认
-

## 暂不处理
-

## 另一端检查
-
```

## 脚本

- `scripts/inspect_image.py`：读取图片尺寸、比例、模式和源视口推断。
- `scripts/sample_colors.py`：生成颜色统计 JSON 和色板 PNG。
- `scripts/crop_asset.py`：按坐标裁切资产并可转 PNG/WebP。
- `scripts/qa_screenshot.py`：用 Playwright 截取 HTML 页面视口截图。

脚本是辅助工具。视觉分层、字体选择、资产取舍和 QA 判断必须由 Codex 明确写出依据。
