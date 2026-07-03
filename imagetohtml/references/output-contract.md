# 输出契约

## visual-breakdown.md

必须包含一张资源判断表：

```text
区域 | 类型 | 处理方式 | 输出 | 状态
```

每一行都要能解释为什么这么处理。遇到不确定内容，写 `needs-review`。

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
      "method": "crop-webp",
      "usage": "hero background",
      "status": "confirmed"
    }
  ]
}
```

`bbox` 使用 `[x, y, width, height]`，单位是原图像素。

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

## qa/compare-report.md

必须说明：

- 源视口截图是否完成。
- 另一端截图是否完成。
- 哪些点与母图一致。
- 哪些点存在明显偏差。
- 哪些点需要用户确认。
- 哪些点 v1 暂不处理。
