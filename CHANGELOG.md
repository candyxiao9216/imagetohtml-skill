# 变更记录

## 0.1.1 - 2026-07-03

### 调整

- 增强裁切规则：复杂插画和产品图必须保留主体、阴影、装饰和安全留白。
- 调整 Logo 策略：简单清晰的 Logo 可手写 SVG，复杂或不确定的 Logo 继续占位并标记。
- 增加源视口几何记录、关键颜色来源映射和 QA 偏差检查要求。
- 为 `crop_asset.py` 增加 `--pad` 和 `--pad-percent` 参数。

## 0.1.0 - 2026-07-02

首个公开版本。

### 新增

- 发布 `imagetohtml` Codex Skill。
- 支持单张视觉稿图片转结构化静态 HTML。
- 提供图片检查、颜色采样、资产裁切和截图 QA 辅助脚本。
- 提供视觉资产处理规则和输出契约参考文档。
- 提供 `requirements.txt` 记录脚本依赖和最低版本。
- 在 README 中补充最小验证命令和发布前检查清单。

### 输出

- HTML / CSS。
- 可复用 assets。
- `tokens/tokens.css`。
- `asset-manifest.json`。
- `text-map.json`。
- `font-map.json`。
- `qa/compare-report.md`。

### 边界

- 不支持多页站点。
- 不凭空重绘复杂或不确定的 Logo。
- 不承诺像素级复刻。
