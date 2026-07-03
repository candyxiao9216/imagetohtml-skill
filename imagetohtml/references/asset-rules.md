# 视觉资产处理规则

## 分类

| 类型 | 默认格式 | 默认处理 |
| --- | --- | --- |
| 照片、背景图 | WebP | 大块裁切，保留视觉完整性 |
| 复杂插画 | WebP/PNG | 大块裁切，避免强行矢量化 |
| 简单图标 | SVG | 优先用图标库或手写 SVG |
| 定制图标 | SVG/PNG | 能重绘才 SVG；不确定先 PNG 占位 |
| Logo | PNG 占位，后续 SVG | v1 不自动重绘 |
| 文字 | HTML 文本 | OCR 后校对 |
| 按钮、卡片、圆角、阴影 | CSS | 不裁图 |
| 简单几何和渐变 | CSS | 不裁图 |

## 混合裁切原则

- 大块裁切：hero 背景、复杂插画、复杂纹理、产品图。
- 单独裁切：logo 占位、人物主体、可复用装饰、产品局部。
- 不裁切：普通文字、按钮、卡片、边框、阴影、圆角、纯色背景、简单渐变、简单几何。
- 只要某个元素会在 HTML 中重复使用，优先单独资产化。
- 只要某个元素只是视觉稿里的一次性局部纹理，优先保留在大块图片里。

## 命名

- 图片：`assets/images/<area>-<purpose>.webp`
- 插画：`assets/illustrations/<subject>.webp`
- 图标：`assets/icons/<meaning>.svg`
- Logo：`assets/logos/logo-temp.png`、`assets/logos/logo-full.svg`
- 字体：`assets/fonts/<family-name>.<ext>`

## 状态字段

`asset-manifest.json` 里的资产状态只使用这些值：

- `confirmed`：可以直接用于 HTML。
- `needs-review`：内容、边界、用途或质量需要用户确认。
- `needs-svg-redraw`：当前是位图占位，后续需要人工重绘 SVG。
- `deferred`：v1 暂不处理，但已记录。

## 禁止事项

- 不把整张视觉稿作为页面背景来伪装 HTML。
- 不把普通文字裁成图片。
- 不自动重绘 logo。
- 不强行把复杂 AI 插画转成 SVG。
- 不为了“资产化”把页面切成大量不可维护碎片。
