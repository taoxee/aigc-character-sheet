# 内部结构记录与逐对检查

程序采用南鸢 MIT 检查器的 16 个规范轴、六个独立组，并增加当前项目的骨相字段、六项妆容和正头/直视/无文字合同。完整来源见 THIRD_PARTY_NOTICES.md。检查只读输入，不联网、不生图。

`python3 <skill-dir>/scripts/check_design.py PLAN.json`

复杂任务才需要内部 JSON；不要让用户填写或默认展示。可通过 plan_cast.py 得到完整示例：

```bash
python3 <skill-dir>/scripts/plan_cast.py --count 3 --makeup daily --same-makeup --out-dir <empty-directory>
```

输出的 design-plan.json 即可交给检查器；manifest.jsonl 是逐人记录，不能直接冒充 PLAN.json。

## 记录结构

- `schema_version: 1` 为设计合同版本，和逐人 manifest 的版本分开。
- `request` 保留本轮请求文本、mode=text/image、explicit_image_request。布尔值只是执行者判断，不是用户授权证据；脚本不能理解引用与否定。
- `roster_goal` 为 single / distinct / identity / related。
- `characters` 每人含 id、axes、attributes；原创含 bone_plan，妆容含六项 makeup，完整 prompt 可另存。
- `locks` 与每人的 `locks` 是轴值锁定；`attribute_locks` 可锁肤色、年龄、痣、发色等非轴值。
- `reference_axes` 为已知身份基线。identity 模式允许部分记录，但角色 axes 必须与此基线完全一致，不增加未知轴。图像锚点和未编码的外观仍要人工比较。
- `same_makeup: true` 时六项 makeup 合同逐字段完全一致，比例适配放在 makeup_adaptation，不混进合同。

规范轴的键和值以 scripts/check_design.py 的 AXES 为准。近义词先归一化；数组、多值、未知轴、重复 JSON 键均不能绕过检查。低/中/高是创作参照，不是测量值。

## 实际检查

不同脸模式要求完整 16 轴，比较全阵容每一对，而非仅前后邻居。六组中至少四组改变，且 face/eyes/nose 至少两组改变；同组多个轴至多算一次。肤色、痣、发型、妆容不加结构差异分。

identity 模式只核对已有基线与锁定，不为了通过不同脸门槛改变身份。single/related 可保留部分未知结构。未知参考没有完整轴时，不编造轴值去套 distinct。

每人 attributes 明确 `head_roll_degrees: 0`、`camera_roll_degrees: 0`、`gaze: direct`、`visible_text: false`、`watermark: false`。它们是目标，不是从图片测得的实际角度或内容。

原创 bone_plan 写 brow_socket、cheek_transition、jaw_chin、soft_tissue。程序只检查字段存在且非空，不判断描述是否自洽、是否真的进入 prompt。固定脸编辑默认不强求新增 bone_plan，避免编造未知深度。

## 仍须语义与成图检查

骨相的高低、宽度、前后关系是否冲突，妆容适配有没有改天然结构，prompt 是否含隐性署名、闭眼或歪头要求，程序都不能全面理解。合成 prompt 后须逐项复核当前硬约束。

实际成图还需检查五官、牙齿、眼神、妆容落点、痣位置、头姿、画面文字和近似同脸。PASS 不能转写成“身份识别准确率”或“不同脸成功率”。发现重复应调整自由结构重做；锁定空间不足或两轮修复仍失败就说明缺口，不降低门槛伪装通过。


## 完整工作流的附加合同

完整人物制作可加入 workflow 对象，格式见 [workflow.md](workflow.md)。程序会检查人脸认可记录、服装 provided/none 的明确选择，以及最终产物为角色设定表；它不能证明消息摘要真实或图片确实存在/符合要求，执行者仍须核对实际输入。只做人脸/文字局部任务不要求伪造整条工作流。

设定表的六表情是同一人物变体，不能作为 distinct 阵容去拉开骨相；侧面/背面不适用正面直视目标。按各视图职责做图像复核，不把所有面板套进同一 gaze=direct 单人目标。
