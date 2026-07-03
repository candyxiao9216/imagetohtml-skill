# 变更记录

## 0.1.3 - 2026-07-03

### 调整

- 增加 `critical-region` 关键局部区域验收要求。
- 增加 `composition-group` 资产规则，避免只裁主体而丢失装饰、底座、内框和局部留白。
- 收紧照片缩略图规则，要求保留人脸、手部、食物、动作主体和关键上下文。
- 新增 `check_render_colors.py`，对母图和最终截图的关键区域均色做反向核对，并检测源视口截图尺寸是否一致。
- 调整 `qa_screenshot.py`：默认只截视口，显式传 `--full-page` 才截长图。

## 0.1.2 - 2026-07-03

### 调整

- 收紧 Logo 策略：simple-mark 才可手写 SVG，brand-lockup 默认整块裁切保真。
- 禁止将完整品牌 Logo 组合拆成近似图形和系统字体后标记为完成。
- 增加 Logo QA 要求：核对整体比例、字重、字距、基线、颜色和 slogan 位置。

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
