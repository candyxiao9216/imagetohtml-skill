# 视觉资产处理规则

## 分类

| 类型 | 默认格式 | 默认处理 |
| --- | --- | --- |
| 照片、背景图 | WebP | 大块裁切，保留视觉完整性 |
| 复杂插画 | WebP/PNG | 大块裁切，避免强行矢量化 |
| 简单图标 | SVG | 优先用图标库或手写 SVG |
| 定制图标 | SVG/PNG | 能重绘才 SVG；不确定先 PNG 占位 |
| Logo | SVG/PNG | simple-mark 可手写 SVG；brand-lockup 默认整块裁切保真 |
| 文字 | HTML 文本 | OCR 后校对 |
| 按钮、卡片、圆角、阴影 | CSS | 不裁图 |
| 简单几何和渐变 | CSS | 不裁图 |

## 混合裁切原则

- 大块裁切：hero 背景、复杂插画、复杂纹理、产品图。
- 单独裁切：logo 占位、人物主体、可复用装饰、产品局部。
- 不裁切：普通文字、按钮、卡片、边框、阴影、圆角、纯色背景、简单渐变、简单几何。
- 只要某个元素会在 HTML 中重复使用，优先单独资产化。
- 只要某个元素只是视觉稿里的一次性局部纹理，优先保留在大块图片里。
- 只要主体、装饰、底座、背景或边框共同构成一个视觉语义单元，按 `composition-group` 处理，不要只裁主体。

## 裁切边界规则

- 复杂插画、产品图和角色图以可见主体为内框，再向四周加安全留白。
- 安全留白优先级：普通资产至少 8px 或 3%；Hero、产品大图、带阴影资产至少 24px 或 5%；遇到原图边界时可以贴边，但必须记录原因。
- 裁切必须包含视觉上属于该资产的阴影、反光、底座、叶片、装饰点和其他附属元素。
- 如果裁切后主体、阴影或装饰贴边、缺角、被截断，资产状态必须是 `needs-review`，不能写 `confirmed`。
- 独立插画和产品图在 CSS 中默认使用 `object-fit: contain`，不要用固定容器加 `overflow:hidden` 裁掉主体。
- 照片缩略图可以使用 `object-fit: cover`，但前提是原图本身就是局部照片或用户可接受头像/缩略图裁切。

## 组合区域规则

- `composition-group` 指主体、装饰、底座、背景、边框或局部留白共同构成的视觉语义单元。
- 组合区域优先整组裁切保真；如果拆成多个资产，必须记录每个子资产的相对位置和 CSS 还原方式。
- 装饰爱心、叶片、光点、底座、内框、局部背景和主体之间的留白关系属于组合区域的一部分，不能因为“主体已裁切”而丢掉。
- 如果组合区域被拆散后视觉关系明显变化，状态必须是 `needs-review`，不能写 `confirmed`。

## 照片缩略图规则

- 照片缩略图裁切必须保留人脸、手部、食物、动作主体和关键上下文。
- 不默认使用 `object-fit: cover`；只有母图本来就是局部缩略图，或裁切不会损失关键主体时才使用。
- 如果需要缩略图尺寸小于原裁切区域，优先扩大资产裁切框，再用 `object-fit: contain` 或调整 `object-position` 保留主体。
- 人脸、手、食物或动作主体被截断时，资产状态必须是 `needs-review`。

## Logo 规则

- `simple-mark` 指纯几何、扁平、无渐变阴影、无自定义字标的简单标识；这类标识可以手写 SVG，输出到 `assets/logos/logo-full.svg` 或内联 SVG。
- `brand-lockup` 指图形 + wordmark 品牌字标/中文/slogan 的组合标识；默认整块裁切为 PNG/WebP 保真，不拆成“近似图形 + 系统字体文字”。
- 手写 SVG 只能还原母图里可见的形状、比例和颜色，不得凭想象补全品牌细节。
- 自定义 wordmark、中文品牌字、slogan 的字重、字距、基线或字体特征无法准确还原时，不得用系统字体替代后标记 `confirmed`。
- 低分辨率、模糊、带渐变/阴影、带体积感或品牌识别不确定的 Logo 先用整块裁切保真，并在 `asset-manifest.json` 标记 `needs-vector-redraw` 或 `needs-review`。
- 用户明确要求矢量输出但当前只能近似时，应输出裁切占位 + `needs-vector-redraw`，不要交付会改变品牌识别的“伪矢量版”。

## Logo QA

- 核对整体宽高、图形与字标比例、字重、字距、基线、颜色、slogan 位置和透明/阴影效果。
- 任何一项明显偏离母图时，Logo 资产不能标记 `confirmed`。

## 命名

- 图片：`assets/images/<area>-<purpose>.webp`
- 插画：`assets/illustrations/<subject>.webp`
- 图标：`assets/icons/<meaning>.svg`
- Logo：`assets/logos/logo-lockup.png`、`assets/logos/logo-temp.png`、`assets/logos/logo-full.svg`
- 字体：`assets/fonts/<family-name>.<ext>`

## 状态字段

`asset-manifest.json` 里的资产状态只使用这些值：

- `confirmed`：可以直接用于 HTML，包括已按母图手写且自检通过的简单 SVG。
- `needs-review`：内容、边界、用途或质量需要用户确认。
- `needs-svg-redraw`：当前是位图占位，后续需要人工重绘 SVG。
- `needs-vector-redraw`：当前保留裁切位图，后续需要人工矢量重绘。
- `deferred`：v1 暂不处理，但已记录。

## 禁止事项

- 不把整张视觉稿作为页面背景来伪装 HTML。
- 不把普通文字裁成图片。
- 不凭想象重绘 Logo。
- 不把 brand-lockup 拆成近似图形和系统字体后当作完成。
- 不强行把复杂 AI 插画转成 SVG。
- 不为了“资产化”把页面切成大量不可维护碎片。
