# 变更记录

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
- 不自动重绘 logo。
- 不承诺像素级复刻。
