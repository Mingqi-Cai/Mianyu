# recut-2146 独立总装包 · 走查验收记录

时间：2026-11-20 23:09 Asia/Shanghai  
执行：CMQ-Demo · 验收  
入口：`/workspace/mianyu-demo/20261120-html-interactive-bobo-recut-2146/prototype/index.html`  
证据目录：`/workspace/mianyu-demo/20261120-html-interactive-bobo-recut-2146/verify-20261120-recut-2146-accept/`

## 结论

**通过。** 无新增挡验收项。

本包是 21:46 终验文本 + 新切图 `bobo-figure.png`（SHA-256 `4aef69898d6f525b977ea7b8ac0f3a3b0cb5e99bb2c96b382190cc04c213ae38`，1010×737）的分轨总装，不是夜间收光包。主页仍为官方 V3 残存展示帧（亮底棚拍），屏内角色为该帧去底切图落在 `room-night.jpg` 上。未按 night-rev 的光晕/收光标准评判。

走查前后哈希均与要求一致。未改 `prototype/`，未写入被污染快照 `/workspace/mianyu-demo/20261120-html-interactive-bobo/`，未改 night-rev，未入仓，未合并 PR #1。包内 `ceo-acceptance-20261120.md` 是从影盏包拷来的历史记录，不代表本包终验。

## 哈希（走查前、走查后均一致）

| 文件 | SHA-256 |
|---|---|
| CHANGE.md | e95e0e5984c9ab39a35d56fbee4928e7e881380d1237c8dbc57b7c519e5d27ba |
| prototype/index.html | 998e82fd05c120b4f6f6033165105dbe2e5a715594df1e3952e6acf709be2a9c |
| prototype/assets/styles.css | c1d24146543e37600755ac2dc64b1cc3315dc8a8ff9413f2b694431462864ffc |
| prototype/assets/app.js | b3430c3d7a68a173064acdc8877c0a08b5963dc565c700128fa0c338b660abe4 |
| prototype/assets/bobo-figure.png | 4aef69898d6f525b977ea7b8ac0f3a3b0cb5e99bb2c96b382190cc04c213ae38 |
| prototype/assets/bobo-frame.jpg | 46007d733e5faf3c9e457c4ed3b37e687c6c18fd0130a0aa11d56256861779f6 |

角色图不是丢失的 63477364…，也不是 21:54 的 67ca03c3…。两插片槽为 21:46 原有 `insert-a.png` / `insert-b.png`；`.skin-bobo` 下 `.actor-inserts` 与 `.actor-eyes` 为 `display: none`，页面无 `.actor-glow-img`。

## 走查路径与结果

环境：系统 Chrome + puppeteer-core，`file://`，视口 430×920、deviceScaleFactor 2，截 `#phone`。脚本：`/tmp/mianyu-verify/walk-recut-2146-accept.js`（不写入 prototype）。

第一轮：开始今晚 → 点场景落位 → 换个位置（仅一次，其后不再出现该按钮）→ 再落位 → 就在这儿 → 躲猫猫 S4/S5（「算了，回来吧」）→ 回位「它回来了」→ 插片确认 → 开始静默沟通 → 开麦试试看（模拟）→ 确认 / 靠近 / 闲聊 / 晚安 → 今晚就到这儿 → 结束页。

第二轮：就在这儿后在 S5 点击藏处，标题为「找到了」。

仪器检查全部通过：无控制台或 pageerror；`app.js` 去掉注释后无 `getUserMedia` / `mediaDevices` 调用，运行时钩子零次；语音文案为「不真开麦」「模拟，未接真麦克风」；结束页写明「不是医疗或心理咨询产品」；可见文案无疗效、助眠、哄睡宣称。

截图：`01-home.png` … `19-found-by-click.png`，另有落位角色裁切 `03b-seated-actor-crop.png`。切图取证：`figure-on-green.png`、`crop-mat-left-on-green.png`、`crop-mat-right-on-green.png`、`crop-suitcase-mat-gap-on-green.png`、`crop-handle-on-green.png`、`figure-cut-metrics.json`。

## 垫面左侧（重点）

绿底合成与落位实拍均显示：垫面左侧是完整圆角弧，行李箱下方与垫面左侧之间为透明（绿底透过），**未见丢失试切图那种左侧白块**。

## 残留清单

下列均为派单已列或 21:46 既有残留，本轮核到，**不挡验收**，无新增项。

**本轮切图（与派单已知残留一致，不预设必须不通过）：**

1. 官方帧本身已切到行李箱左缘（绿底可见行李箱左侧贴齐画布，`opaque_bbox.x = 0`）。
2. 提手金属间隙可见极小原背景色（绿底提手裁切；计量约 133 个近奶油色不透明像素，体量很小）。
3. 垫面右侧外缘可见约 1–3 像素级偏紧/锯齿（`crop-mat-right-on-green.png`）。
4. 行李箱底边与垫面之间的窄缝仍可见少许原台面色（`crop-suitcase-mat-gap-on-green.png`、`03b-seated-actor-crop.png`）。

**21:46 既有残留：**

5. 开麦说明面板较高，挡住角色下沿（`10-mic-explain.png`）。
6. 确认只能整帧轻倾，不能单独让牌耳转动（21:46 文本原样，无独立牌耳层）。
7. 靠近无法先做「眼转向窗」（`13-intent-near.png` 面部仍正视；官方帧无独立眼层，且假眼层为 hidden）。
8. 语音为模拟，不是真机识别（沿用已终验口径；源码与运行时均未调用 `getUserMedia`）。
9. 目前没有泊泊 V4 专包；主页仍用官方 V3 残存展示帧。

另：中段回位、插片确认、闲聊暖光闪的瞬时动画在静帧中不易单独定格；关光收尽后的在场静帧未另做定格页（`16-outro.png` 为关光过程中的在场帧）。以上亦不挡验收。

## Skills

执行前已查个人 Skills 库 `SKILLS_INDEX.md`（Mingqi-Cai/my-ai-skills-library）。采用：

- `engineering-workflow/verification-before-completion`（A）：结论前先跑走查并保留证据
- `frontend-engineering/frontend-visual-qa`（A，仅审计）：实际打开截图与绿底切图做视觉核对，未改实现

`testing-automation/webapp-testing`（B）依赖 Playwright Python，本环境未安装，沿用本 Demo 既有系统 Chrome + puppeteer-core、`file://` 走查。未新开发 Skill。

请 CEO 终验后再交主 bot 转用户看。用户确认前不入仓。
