# 视觉资产处理规则

## 分类

| 类型 | 默认格式 | 默认处理 |
| --- | --- | --- |
| 照片、背景图 | WebP | 大块裁切，保留视觉完整性 |
| 复杂插画 | WebP/PNG | 大块裁切，避免强行矢量化 |
| 简单图标 | SVG | 优先用图标库或手写 SVG |
| 定制图标 | SVG/PNG | 能重绘才 SVG；不确定先 PNG 占位 |
| Logo | SVG/PNG | 简单清晰的手写 SVG；复杂或不确定的 PNG 占位 |
| 文字 | HTML 文本 | OCR 后校对 |
| 按钮、卡片、圆角、阴影 | CSS | 不裁图 |
| 简单几何和渐变 | CSS | 不裁图 |

## 混合裁切原则

- 大块裁切：hero 背景、复杂插画、复杂纹理、产品图。
- 单独裁切：logo 占位、人物主体、可复用装饰、产品局部。
- 不裁切：普通文字、按钮、卡片、边框、阴影、圆角、纯色背景、简单渐变、简单几何。
- 只要某个元素会在 HTML 中重复使用，优先单独资产化。
- 只要某个元素只是视觉稿里的一次性局部纹理，优先保留在大块图片里。

## 裁切边界规则

- 复杂插画、产品图和角色图以可见主体为内框，再向四周加安全留白。
- 安全留白优先级：普通资产至少 8px 或 3%；Hero、产品大图、带阴影资产至少 24px 或 5%；遇到原图边界时可以贴边，但必须记录原因。
- 裁切必须包含视觉上属于该资产的阴影、反光、底座、叶片、装饰点和其他附属元素。
- 如果裁切后主体、阴影或装饰贴边、缺角、被截断，资产状态必须是 `needs-review`，不能写 `confirmed`。
- 独立插画和产品图在 CSS 中默认使用 `object-fit: contain`，不要用固定容器加 `overflow:hidden` 裁掉主体。
- 照片缩略图可以使用 `object-fit: cover`，但前提是原图本身就是局部照片或用户可接受头像/缩略图裁切。

## Logo SVG 规则

- 简单、清晰、低风险的 Logo 可以手写 SVG，输出到 `assets/logos/logo-full.svg` 或内联 SVG。
- 手写 SVG 只能还原母图里可见的形状、比例和颜色，不得凭想象补全品牌细节。
- 复杂、模糊、带精细纹理或品牌识别不确定的 Logo 先用 PNG 占位，并在 `asset-manifest.json` 标记 `needs-svg-redraw` 或 `needs-review`。

## 命名

- 图片：`assets/images/<area>-<purpose>.webp`
- 插画：`assets/illustrations/<subject>.webp`
- 图标：`assets/icons/<meaning>.svg`
- Logo：`assets/logos/logo-temp.png`、`assets/logos/logo-full.svg`
- 字体：`assets/fonts/<family-name>.<ext>`

## 状态字段

`asset-manifest.json` 里的资产状态只使用这些值：

- `confirmed`：可以直接用于 HTML，包括已按母图手写且自检通过的简单 SVG。
- `needs-review`：内容、边界、用途或质量需要用户确认。
- `needs-svg-redraw`：当前是位图占位，后续需要人工重绘 SVG。
- `deferred`：v1 暂不处理，但已记录。

## 禁止事项

- 不把整张视觉稿作为页面背景来伪装 HTML。
- 不把普通文字裁成图片。
- 不凭想象重绘 Logo。
- 不强行把复杂 AI 插画转成 SVG。
- 不为了“资产化”把页面切成大量不可维护碎片。
