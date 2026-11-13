# 公开示例：三套人脸与角色设定表

这三套是本项目实际生成的成年虚构人物，分别使用自己的 face.png 作为设定表唯一身份图像输入，不交叉借用另外两位人物。风格、服装及人物由用户明确委托助手选择；用户之后整体认可效果，不补写逐张人脸批准记录。

| 人物 | 基准脸 | 最终设定表 | 完整记录 |
| --- | --- | --- | --- |
| 自然活力 | [face.png](../examples/01-natural/face.png) | [character-sheet.png](../examples/01-natural/character-sheet.png) | [character.json](../examples/01-natural/character.json) |
| 日韩轻甜 | [face.png](../examples/02-social/face.png) | [character-sheet.png](../examples/02-social/character-sheet.png) | [character.json](../examples/02-social/character.json) |
| 知性复古 | [face.png](../examples/03-vintage/face.png) | [character-sheet.png](../examples/03-vintage/character-sheet.png) | [character.json](../examples/03-vintage/character.json) |

每份 character.json 包含骨相计划、五官轴、六项妆容、服装、实际执行的人脸 prompt 与 sheet_prompt、图像尺寸、参考输入和 PNG 的 SHA-256。它是执行记录，不是 check_design.py 的完整输入合同；需要做合同检查时按 design-contract.md 的 schema 整理。

静态检查可见：每张表包含正侧背全身三视图、三列两行六表情、必要服装细节和七色色板。正面与表情图正头直视；侧面与背面维持真实方向，无可见文字水印。妆容跟随各自脸型，不依靠改妆制造表情。

自然款较宽轮廓与细长眼型、日韩款较短轮廓与开放眼型、复古款偏长脸与颧鼻层次形成可见区别。克制的难过与不满表情仍可能较接近。侧背、身体和未显示的下装属于设计补全；这些结果没有经过生物特征评分、真实解剖验证或视频连续性测试。

复用风格可以读对应 prompt，但新人物不默认引用样例脸。用户选中具体人物时再查看并实际传入该人物的 face.png。仅在编辑设定表版式时才把对应 character-sheet.png 作为编辑目标。
