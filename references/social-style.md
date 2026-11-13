# 可选预设：轻度日韩网感与三档妆容

本文件只在用户选择日韩网感/可爱轻修图方向时加载。它不是核心 Skill 的唯一审美；其它方向按人物与当前请求设计。三档配方只是起点，需再按 makeup-adaptation.md 的落点、眼睑与天然唇形适配。

## 修图与妆容分开

选中日韩网感时，`light-social-retouch` 对应此前用户“降低约 5%–10% 真实感”的主观方向：轻度磨去粗糙与斑驳，肤色过渡更柔和，唇部、眉睫更精致，保留摄影光影、成年比例与个体差异。这不是百分比控制或已校准量表，不向图像 API 杜撰 `realism=0.9`。

可切换 `natural` 回到自然肤质；该模式不叠加轻修图。提高妆容强度不必同步提高磨皮、缩鼻或放大眼睛。

风格模块（创作预设，不是对某国所有人的定义）：

```text
Korean-inspired social-feed beauty finish: clean luminous satin complexion, softly polished midtones, fresh restrained pink tones and neatly separated lashes. Gently idealized and cute, with subtle editorial retouching.
```

```text
Japanese-inspired social-feed beauty finish: translucent soft satin complexion, gentle warm color, softly diffused cheek color and an airy approachable mood. Gently idealized and cute, with subtle editorial retouching.
```

保留之前确认的亲近感：`both eyes directly engaged with the lens, a tender attentive gaze as if looking at her boyfriend behind the camera`。头部统一端正，亲近感通过眼神和不同嘴角的微笑表达。

## 妆容模块

| 档位 | 需要能看出的差别 |
|---|---|
| light 淡妆 | 薄底妆、极浅上眼影、轻眉睫、薄唇釉，腮红很少 |
| daily 日常妆 | 有晕染的玫瑰棕/蜜桃眼影、细内眼线、分明睫毛、轻腮红、润泽唇釉 |
| glam 浓妆 | 更完整底妆、清楚的眼影层次和细翘眼线、较强睫毛、克制修容高光、莓玫瑰唇色，仍可甜美微笑 |

英文可直接使用：

```text
Very light makeup: sheer satin base, softly brushed brows, a faint peach-beige wash on the upper lids, delicate lash definition and thin rosy lip glaze. Minimal blush; the face remains fresh and understated.
```

```text
Everyday date makeup: light even satin base, softly blended rose-taupe upper-lid shadow, fine brown tightlining, separated lashes, gentle peach-rose blush and a translucent rose lip lacquer. Visible but restrained.
```

```text
Polished full social-media makeup: an even satin base with fine residual skin detail, softly blended mauve-brown eye shadow, precise fine winged liner, defined individual lashes, controlled cheek highlight, softly sculpted cheeks and a glossy muted berry-rose lip. Clearly stronger than daily makeup, while the expression remains sweet and approachable.
```

## 多样性变量

| 层次 | 变化方式 | 复用时 |
|---|---|---|
| 脸型与骨相 | 圆椭圆、心形、柔方、长椭圆、柔菱形；颊部饱满度、下颌宽度、下巴长度 | 固定，不因“可爱”全部变成同一 V 脸 |
| 眉眼鼻口 | 眼型/眼距/眼睑/眼尾、鼻梁和鼻尖、口宽与唇形、眉弧 | 固定基本比例，妆容只改变视觉表现 |
| 头姿 | 正头、正面、双眼水平、下巴中性、镜头无倾斜 | 固定默认，不随机侧歪 |
| 微笑 | 小幅对称闭口、轻微单边嘴角、唇微开露窄窄上牙、少量上牙的温暖笑 | 可变，露齿需检查牙龈、牙齿数量和嘴角 |
| 头发 | 短/中/长；刘海/侧分/无刘海；自然黑深棕或奶茶棕、灰棕、铜棕、玫瑰棕染发 | 个人基准固定，需要换发型时明确记录版本 |
| 痣 | 无痣为常见选项；部分角色有一个极小眼角痣或上颊痣 | 身份特征，位置固定，不能每张随机换边 |
| 妆容 | light/daily/glam，与发色和表情独立组合 | 可变，不改变原始肤色或面部几何 |

痣用图像坐标说明，例如“画面右侧眼睛的外眼角下方”；非镜像正面图对应人物自己的左侧。镜像自拍需要相应翻转，不能把画面左右与人物左右混用。痣只给部分角色，避免全部同位置或额外生成雀斑/污点。

## 风格验收

整图看亲近、偏可爱、像轻修图后的社交照片；放大仍有鼻唇和眼睑结构，不像塑料或绘画。三档妆容在眼影/眼线/睫毛/唇色上可区分。人物身份差异应在看脸时成立，不能靠背景、染发或文件编号解释为“不重复”。
