# 视频辅助与人物记录

每个角色保存一张主基准图与记录。文字用于追踪，图像才是视觉锚点。以下为历史日韩轻修图人物示例；年龄、性别、风格和妆容均随所选人物，不是 Skill 的通用默认：

```yaml
character_id: fictional-selfie-001
synthetic: true
apparent_age: 27
identity_anchor: character-anchor.png
appearance:
  face: soft oval face, gently rounded chin
  eyes: dark brown almond eyes, subtle eyelid asymmetry
  nose: straight medium-width bridge, rounded tip
  lips: medium-full muted pink lips
  hair: dark chocolate brown, collarbone length, off-center part, face-framing layers
  skin: light-medium, neutral-warm undertone
wardrobe: oatmeal crew-neck cotton T-shirt
locked: face geometry, hairline, apparent age, skin undertone
variable: setting, lighting, camera viewpoint, small expression
finish: light-social-retouch
makeup: daily
beauty_mark: none
```

不把默认肤色或五官施加到用户选定的其他人物。如果增加痣或雀斑，先在基准图确认位置再保持一致，不为“真实”随机加点。

无论单人还是多人物，每个人都有自己的身份锚点。跨场景或图生视频保留这个人的修图强度、妆容设计、唇部质地和痣的位置，避免逐帧在不同妆容之间跳变。露少量上牙的微笑也可作首帧，但比闭口多了牙齿一致性检查；需要稳妥的首轮微动测试时优先使用闭口版本。

## 首帧选择

正面或小角度、眼口无遮挡、正常闭嘴或轻微微笑，优先于大笑露齿、强逆光和发丝盖眼。保留全下巴、头顶与部分肩膀，避免轻微移动即裁头。留白按目标平台决定，不把眼在上三分之一当强制条件。

口播需另行提供台词与口型要求；静态闭口参考不能保证牙齿和口腔一致。大侧脸、快速转头、举手跨脸需要额外参考或单独测试。

## 可用图生视频动作 prompt

```text
Use the supplied selfie as the exact starting frame. Keep the same adult character, facial proportions, hairline, clothing, room and lighting throughout. A short quiet handheld selfie moment: subtle natural breathing, one relaxed blink, a tiny shift of gaze toward the lens and a barely perceptible closed-mouth smile. Keep the head upright and frontal, eyes level, without sideways head tilt or camera roll. Minimal natural handheld drift, no zoom or camera orbit, no new objects, no hands crossing the face. Preserve consistent facial structure, skin detail, hair volume and background geometry over time. One continuous shot, no cuts, no text.
```

首轮可尝试约 4–5 秒；实际时长、帧率和尺寸使用平台已支持的参数。讲话时替换上面的闭口动作并补短台词，不叠加矛盾要求。

## 视频验收

实际出视频后检查首帧、中段、末帧和运动最大帧：眼距、鼻形、下颌是否漂移，牙齿是否突变，发丝/肤质是否闪烁，衣领和背景线条是否扭曲，手是否异常。先减少运动、简化场景，再用原始锚点准备首帧。

未生成视频就标注“视频候选首帧＋动作 prompt，尚未验证时间一致性”，不用静态真实感证明视频稳定。
