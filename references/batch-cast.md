# 可选：多人物与批量规划

人物设计是核心。单人或同脸修改不需要运行本脚本；用户明确要角色阵容/批量时才调用。脚本使用 Python 3 标准库，不联网、不出图。

```bash
python3 <skill-dir>/scripts/plan_cast.py --count 5 --style natural --makeup daily --same-makeup --out-dir <empty-directory>
```

新版默认 count=1、自然人像，不再自动规划三十人或默认日韩可爱。命令参数：

- `--style natural|korean|japanese|editorial|retro|custom|mixed`。mixed 明确表示混合日韩；custom 需 `--style-prompt`。预设不限制手工设计可用的其它风格。
- `--finish auto|natural|light-social-retouch|editorial`。auto 按所选风格决定；风格和肤质整理分开。
- `--makeup none|light|daily|glam|mixed`。`--same-makeup` 要求一个固定档位，不能和 mixed 并用。六项妆容合同固定，按眼睑/天然唇形补比例适配。
- `--makeup-goal keep-shape|soften|uplift|widen` 选择视觉目标；不能因目标自动改变骨架或天然眼角。same-makeup 模式只使用 keep-shape 做比例适配；其它目标先重写共享合同，避免每人的边缘/方向被暗中改成另一套妆。
- `--subject` 和 `--age` 覆盖人物方向与成年年龄。默认只写成年虚构角色，不强制女性；性别呈现、身份与用途应按当前请求给出。更复杂人物优先手工设计合同。
- `--hair mixed|short|medium|long`、`--image-type face|selfie`、`--mole-frequency 0..1` 控制造型，均不计入不同脸分数。
- `--seed` 只控制文字规划；`--batch-id` 控制编号；输出目录需为空，不覆盖结果。
- `--request-text` 保存本轮原始请求，供语义复核；未提供时只记录“按脚本参数规划”，不假装知道原话。Skill 执行者应在合同里保留真实请求。
- `--exclude-manifest` 可重复指定 v5 规范轴 JSONL，跨批也按全体逐对差异排除。旧版只有自然语言的记录不能可靠自动映射规范轴，应先人工迁移或做图像比较；脚本会明确拒绝，不默默假装已去重。
- `--max-attempts` 约束每人候选尝试次数；空间不足会失败，不降低差异门槛。

输出 manifest.jsonl、逐人中文完整 prompt、design-plan.json、check-report.json、summary.json。manifest 版本是 2，内部检查合同版本是 1，二者不要混用。新规范轴与旧版 seed 方案不同，不承诺沿用原批次的同一人物；旧文件保留。

## 不同脸检查

face/jaw/eyes/nose/lips/brows 六组，所有人物对至少四组改变，其中 face/eyes/nose 至少两组改变；跨批排除也比较规范轴，不只比较完全相同的字符串。头姿固定正头，双眼水平，直视镜头，无文字署名水印。

骨相描述按三区和软组织单独记录，妆容按眼睑与本轮目标适配；程序仍不理解全部骨相语义或图片。不把随机词不同、文件哈希不同、头发/妆容/痣不同当作实际不同脸。

## 实际出图是另一阶段

只有当前请求要求图片才调用图像工具，逐人独立生成；每个新人物不能引用上一人的脸。工具规则按当前环境执行，不自动换付费 API。

通过的个人图才成为该角色 identity_anchor。记录实际尺寸、状态、完成数与失败数；没出图的保持 planned。近似同脸时调整自由结构重做，保留旧文件；两轮仍失败说明缺口。实际批量中间中断时续做未完成项，不整批重来。

大批全体两两约束可能使可行空间不足。优先满足明确人数与用户锁定；无法同时满足就交付已完成计划和限制，不能把“至少四组”改成更低还声称通过。图片的视觉去重仍需单独执行。
