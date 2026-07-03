# 输出契约

## visual-breakdown.md

必须包含四张表：资源判断表、Logo 判断表、源视口几何表、关键颜色映射表。

资源判断表：

```text
区域 | 类型 | 处理方式 | 输出 | 状态
```

每一行都要能解释为什么这么处理。遇到不确定内容，写 `needs-review`。

Logo 判断表：

```text
Logo 区域 | 类型(simple-mark/brand-lockup) | 处理方式 | 字标是否自定义 | 状态
```

`brand-lockup` 默认整块裁切保真。除非能准确临摹母图里的字标、比例、字距和颜色，否则不要拆成 SVG 图形 + 系统字体文字。

源视口几何表：

```text
区域 | 原图位置/尺寸 | HTML 实现策略 | 状态
```

至少覆盖画布/外框、主导航、顶部栏、Hero、主要卡片网格、底部区域和主要间距。

关键颜色映射表：

```text
Token | 原图区域 | 取样颜色 | 页面用途 | 状态
```

关键背景、文字、边框、品牌色、按钮/胶囊色都必须有来源；主观微调用 `derived` 标记。

## asset-manifest.json

推荐结构：

```json
{
  "source": "source/original.png",
  "source_viewport": {
    "type": "desktop",
    "width": 1440,
    "height": 1024,
    "strategy": "desktop-first"
  },
  "assets": [
    {
      "id": "hero-bg",
      "type": "image",
      "path": "assets/images/hero-bg.webp",
      "bbox": [0, 0, 1440, 720],
      "crop_padding": "24px",
      "css_fit": "contain",
      "method": "crop-webp",
      "usage": "hero background",
      "status": "confirmed"
    }
  ]
}
```

`bbox` 使用 `[x, y, width, height]`，单位是原图像素。复杂插画、产品图和角色图推荐记录 `crop_padding`、`css_fit` 和边界检查结论。

Logo 资产推荐补充：

```json
{
  "id": "logo",
  "type": "brand-lockup",
  "path": "assets/logos/logo-lockup.png",
  "bbox": [0, 0, 240, 96],
  "method": "crop-png",
  "usage": "brand logo lockup",
  "status": "confirmed",
  "notes": "完整品牌组合整块裁切，避免字标失真"
}
```

## text-map.json

推荐结构：

```json
{
  "items": [
    {
      "id": "hero-title",
      "text": "校对后的标题",
      "role": "h1",
      "bbox": [120, 80, 620, 160],
      "font_size": 48,
      "font_weight": 700,
      "color": "#111111",
      "confidence": "medium",
      "status": "confirmed"
    }
  ]
}
```

不确定文字用 `needs-review`。HTML 里不要写未确认文字，除非同时在页面或报告中标注待确认。

## font-map.json

推荐结构：

```json
{
  "primary_sans": {
    "font_family": "Noto Sans SC",
    "usage": "正文、按钮、导航",
    "reason": "接近视觉稿里的现代无衬线中文风格",
    "source": "Google Fonts",
    "license": "OFL",
    "status": "verified"
  }
}
```

字体只记录可公开商用的开源字体；不确定许可证时不要下载。

## tokens/tokens.css

至少包含：

```css
:root {
  --font-sans: system-ui, sans-serif;
  --color-bg: #ffffff;
  --color-text-primary: #111111;
  --space-1: 4px;
  --radius-card: 8px;
}
```

只把实际 HTML 会使用的值放进 token。颜色证据层可以很全，CSS token 不必全部收录。

关键颜色 token 必须能在 `colors/color-map.json` 或 `visual-breakdown.md` 的关键颜色映射表里找到来源。

## qa/compare-report.md

必须说明：

- 源视口截图是否完成。
- 另一端截图是否完成。
- 哪些点与母图一致。
- 哪些点存在明显偏差。
- 裁切资产是否有贴边、缺角、主体被容器裁掉。
- Logo 是否被正确分类；brand-lockup 是否保持整体比例、字重、字距、基线和 slogan 位置。
- 关键颜色是否来自原图取样，是否存在明显漂移。
- 源视口关键几何是否接近原图，包括外框、导航、Hero、卡片网格、间距和圆角。
- 哪些点需要用户确认。
- 哪些点 v1 暂不处理。
