# 已认可案例：白底六表情角色设定表

用户在查看本次六表情新版设定表后要求固化。以下保留当时实际执行的 prompt 与输入角色，作为可复用案例，不将这位人物、26岁年龄、蓝衣白裤或日韩修图设为全 Skill 默认。

包内文件位于 `../assets/approved-character-sheet/`（相对本文件）：

- character-base-v1.png：已选定的人物身份图，后续换场景优先使用它。
- character-reference-sheet-v1.png：当时编辑输入的四表情旧版，作为历史输入保留。
- character-reference-sheet-v2-six-expressions.png：已认可的新版成图。
- manifest.json：文件角色、六表情顺序、SHA-256 和来源范围。

未来新建角色使用通用 character-sheet.md 模板，不直接把此人物的脸和衣服作为新角色输入。复用这位人物时，先查看原始身份图；编辑当前设定表时再将新版设定表作为编辑目标。仅重现当时执行过程时才需要旧版。

实际结果为 1774×887 的白底写实设定表，包含完整三视图、六表情、服装细节和七色色板，无可见文字水印。难过表情是克制的低落，没有明显泪水。侧背、身体与下装是新增设计，不能当作正面照已证实的结构；本次未测试动态连续性。

下面的英文是原样执行记录；通用任务仍默认按用户语言给 prompt。

# 六表情角色设定表：实际提示词

工具：内置 image_gen。输入 1：character-base-v1.png，人物身份参考；输入 2：character-reference-sheet-v1.png，上一版设定表和编辑目标。输出：character-reference-sheet-v2-six-expressions.png。保留原版。

表情按从左到右、从上到下排列：平静、浅笑、开心大笑、惊讶、轻微不满、难过。正面表情均正头、直视镜头；侧面和背面维持三视图所需方向。其余服装、细节和七色色板沿用上一版。

```text
Use case: identity-preserve.
Image 1 is the approved identity portrait. Image 2 is the previous character reference sheet and the edit/layout target. Create one revised official-style realistic character reference sheet of this exact same fictional adult woman, expanding the FACIAL EXPRESSION DETAIL section from four portraits to EXACTLY SIX clearly different expressions.

Keep the original woman's face geometry, apparent age 26, eyelids, eye spacing, nose, lips, natural asymmetry, tiny beauty mark on her right upper cheek (viewer-left in frontal portraits), skin tone, dark brown collarbone-length layered hair, delicate peach-rose daily makeup and rose lip glaze. Keep the lightly polished photographic finish. Do not replace her with a new or generic face.

Use a wide LANDSCAPE 2:1 sheet on pure white with an organized grid, thin pale-gray separators, comfortable gutters and margins. Increase the space given to the six expression close-ups so eyebrow, eyelid, cheek and mouth changes are easy to inspect. Do not squeeze six tiny faces into the old four-face area.

UPPER LEFT, approximately 45% of the width: retain three full-body standing views FRONT / TRUE LEFT-FACING SIDE PROFILE / BACK, equal height and consistent ground baseline. Preserve body proportions, pose, hairstyle, exact existing sky-blue long-sleeve fine-knit crewneck sweater with rib cuffs/hem, ivory straight-leg jeans and off-white plain low-top sneakers. Entire heads and shoes visible. No new equipment, jewelry or accessories. Front view upright with direct camera gaze; profile and back remain genuine profile and back, not turned toward the viewer.

UPPER RIGHT, approximately 55% of the width: a LARGE, evenly aligned 3-column by 2-row grid of exactly SIX face-and-neck close-ups, all at the same scale, front-facing with head upright, eyes directed to the camera, no sideways tilts. Frame each face large, complete chin, hair framing and a little neckline, consistent lighting and makeup. Same person in every panel. In reading order:
1. CALM NEUTRAL: brows and cheeks relaxed, lips gently closed, steady natural gaze.
2. FRIENDLY SMALL SMILE: corners of lips gently raised, slight cheek lift, a narrow glimpse of upper front teeth, tender engaged eyes.
3. JOYFUL LAUGH: clearly wider genuine smile with upper teeth visible, raised cheeks and gentle lower-lid compression, eyes remain open toward the camera. Not the same small smile as panel 2.
4. SURPRISE: brows visibly raised, upper lids more open, lips softly rounded in a small open O; believable mild surprise, no cartoon eye enlargement.
5. MILD ANNOYANCE: inner brows lowered and slightly drawn together, subtly tense lower lids, lips pressed together, a restrained displeased look. No smile and no head turn.
6. SADNESS: inner brows raised with outer brows soft, slightly drooping mouth corners and relaxed parted lips, a subdued vulnerable expression, eyes still directed to the viewer; no dramatic tears or running makeup.
These are six distinct facial muscle configurations, not six similar smiling photos. Preserve facial structure through the changes; do not change identity, eye color, hairstyle or cosmetics to imply an emotion.

BOTTOM STRIP: retain three neat material/detail insets for sweater neckline knit, cuff/hem and jeans pocket with sneaker silhouette; retain a clear row of SEVEN coordinated color chips for dark brown hair, warm-neutral skin beige, peach blush, rose lip glaze, sky blue knit, ivory denim and off-white shoes. Arrange these below the large views without overlap or excessive empty space.

Realistic skin and soft studio illumination, crisp facial details, fine restrained texture. No grain, gray-brown mottling, repeated texture veil or plastic skin. No visible text, labels, numbers, letters, captions, handwritten signature, watermark, logos or decorative frames. Expression names above describe the design only and must not be printed. One integrated multi-panel reference sheet.
```

