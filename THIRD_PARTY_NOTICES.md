# 第三方来源与改动说明

AIGC Character Sheet（Persona Blueprint 工作流）以根目录 [LICENSE](LICENSE) 中的 MIT 许可发布。以下第三方版权与许可继续独立保留。

本 Skill 的整体目标、既有自拍/视频流程、正头直视与无文字偏好来自当前用户。人物设计规则及部分代码/案例融合自：

- 项目：[南鸢·人像角色设定师](https://github.com/nuyoah-ai-works/nuyoah-portrait-character-designer)
- 版本：v0.2.1；本次阅读的仓库提交：[99b9a2c90e5b09507c6a61b5c27b9e2740ddb63d](https://github.com/nuyoah-ai-works/nuyoah-portrait-character-designer/tree/99b9a2c90e5b09507c6a61b5c27b9e2740ddb63d)
- Copyright (c) 2026 南鸢 nuyoah。
- 第三方代码/文档原 MIT 许可完整保留于 [licenses/nuyoah-MIT.txt](licenses/nuyoah-MIT.txt)。版权说明仅用于来源归属，绝不作为图片中的署名要求。

## 融合范围

scripts/check_design.py 改写自原 scripts/check_design.py：保留 16 规范轴、六组差异、全阵容逐对比较、锁定与输入验证；增加骨相计划非空检查、六项妆容合同、正头/直视/无文字属性锁，允许 identity 模式保留部分已知轴而不补未知项。程序不判断骨相语义、prompt 质量或图像识别。

references/character-structure.md、makeup-adaptation.md、design-contract.md 融合原结构、妆容和合同规则，按本项目任务重新编排。整体核心从日韩批量脸库调整为人物设计与复用；批量和日韩风格改为可选模块。

references/integrated-prompts.md 保留并改写原 examples/real-cases.md 的四份完整案例：唐风、窗边、校园露齿与校园自然状态。已删除所有手写作者署名要求，将闭眼/偏头部分调整为当前的正头直视，不复制第三方参考图片。原案例和改写版的验证状态分别说明，不冒充本轮已生成图像。

参考图库的初轮视觉观察仍见 [references/source-analysis.md](references/source-analysis.md)，不声称获得图库原始 prompt。


## 本项目后续固化内容

assets/approved-portraits 与 assets/approved-character-sheet 为本项目实际生成、用户认可后保存的独立虚构人像和角色设定表，不是第三方图库或南鸢项目原图。新增 workflow 合同、六表情设定表模板及服装输入流程来自本用户要求；不将来源版权文字画进图片。

examples/ 下的三套人脸与设定表同样由本项目实际生成，分别包含自然活力、日韩轻甜与知性复古方向。人物和服装在本次示例中由用户委托助手选择，实际提示词及输入关系保留在各自 character.json；不包含第三方图库原图或私人上传的服装参考。生成示例的许可范围及平台条款边界见 README.md。
