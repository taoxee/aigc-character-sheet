# 来源与视觉反推

观察日期：2026-11-11。初轮查看中长发面部分区首屏与 `f01dd5f818e` 放大图；后续按用户要求查看短发首屏及两张放大图。不是全站逐张分析。

## 短发与轻修图方向的补充

[短发筛选页](https://photoai.life/portrait/#hair=%E3%82%B7%E3%83%A7%E3%83%BC%E3%83%88)当时显示 433 张。首屏可见不同发色、刘海和微笑方式。放大查看 [f02977ebdcb](https://photoai.life/portrait/img/f02977ebdcb.png)：层次短波波头、浅棕发、微露上牙、柔和肤色与轻腮红；以及 [f03337617f6](https://photoai.life/portrait/img/f03337617f6.png)：深色波波头、细碎侧刘海、闭口微笑、不同的眼口轮廓。

“可爱、轻度社交平台修图感”是结合这些可见效果和用户偏好作出的风格解释，不能据此断言原图实际用过某个修图软件。大批次中控制头姿、笑容、自然/染发、眼角痣和三档妆容，是用户要求的扩展，并未声称逐张确认全站都包含这些组合。原始 prompt 仍未获得。

用户将目标调整为在可用的自然人像基础上降低约 5%–10% 原生态真实感；本 Skill 将其解释为轻度肤质与色彩整理，不是测得的真实感百分比。

## 页面事实

- [指定页面](https://photoai.life/portrait/#hair=%E3%82%BB%E3%83%9F%E3%83%AD%E3%83%B3%E3%82%B0)：`セミロング` 对应中长发，当时筛选显示 154 张。面部分区用于正面、纯色背景脸部参考，另有造型分区。页面标示素材为 AI 虚构人物、CC0。
- [原作者页面](https://ai-portrait-gallery.pages.dev/)：生成提示词与案例限其 LINE 社群公开，图片元数据已经移除。本次未加入社群，未取得原始 prompt、模型、checkpoint、LoRA、采样器或 seed。
- 放大观察：[f01dd5f818e](https://photoai.life/portrait/img/f01dd5f818e.png)，页面显示 1122×1402 PNG。首屏缩略图对照：[f029a34a679](https://photoai.life/portrait/img/f029a34a679.png)、[f041ee5b0fd](https://photoai.life/portrait/img/f041ee5b0fd.png)、[f042429bfb7](https://photoai.life/portrait/img/f042429bfb7.png)、[f0457e14faa](https://photoai.life/portrait/img/f0457e14faa.png)。后四张只比较发型、表情和色调，未逐张放大检查。

## 从图像推断

| 可见特征 | 重建用语 | 边界 |
|---|---|---|
| 正面、头肩、居中、接近视线高度 | centered front-facing head-and-shoulders portrait, eye-level | 实际镜头未知 |
| 浅灰到灰青的均匀背景 | pale cool gray seamless background | 仅描述颜色与形态 |
| 柔和脸部明暗，下巴浅影 | broad soft frontal light, gentle shadow under chin | 无法确认窗户/软箱及尺寸 |
| 眉眼鼻唇清晰、皮肤较均匀 | natural facial proportions, light everyday makeup, restrained skin texture | 真实年龄、族裔不可由此确认；人物设定是创作选择 |
| 发丝层次，刘海/发色变化 | collarbone-length layered hair, separated strands | 具体发型随样本变化 |
| 闭口微笑或平静表情 | relaxed expression, small closed-mouth smile | 不强制所有人物同一表情 |

## 网站风格 prompt（原创推断）

```text
A photorealistic front-facing head-and-shoulders portrait of a fictional adult woman, centered at eye level, looking directly into the lens. Collarbone-length layered dark brown hair with fine loose strands framing the face. Relaxed small closed-mouth smile, light everyday makeup, natural facial proportions. Soft broad frontal illumination with gentle shadows under the chin, pale cool gray uniform background, restrained contrast and neutral color. Clear individual hair strands, realistic eyes and lips, subtle skin texture at portrait distance. Complete hair silhouette and shoulders in frame, simple unobtrusive clothing, portrait 4:5. One photograph, no text, no watermark, no beauty-filter skin, no exaggerated eyes.
```

此段重建画面语言，不能保证复现某张图库人物。局部毛孔、轻微不对称、家居背景和手机视角是为模拟自拍新增的设计，不能称为网站原始提示词内容。

从参考照转自拍时保留人物几何、发际线和发型；替换灰背景、手机机位、生活光线与皮肤处理。持续使用同一参考图比每次独立复述外貌更有利于同脸，效果仍取决于工具。

Skill 不打包或批量转载图库。本次交付样图是新生成的独立虚构角色，不是网站原图。
