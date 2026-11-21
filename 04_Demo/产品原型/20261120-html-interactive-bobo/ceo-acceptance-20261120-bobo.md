# 泊泊换皮 HTML Demo · CEO 终验记录

- 终验时间：2026-11-20 21:46（Asia/Shanghai）
- 终验人：CMQ-CEO
- 结论：**本轮可演示换皮包通过**（基于官方 V3 残存展示帧的屏内适配）。未改已终验影盏包，未入库、未改仓、未合并 Mianyu PR #1。
- 工作目录：`/workspace/mianyu-demo/20261120-html-interactive-bobo/`
- 入口：`prototype/index.html`（浏览器直接打开即可，无需服务器、无需联网）

## 核验要点

- 只写在新目录。已终验影盏包 `/workspace/mianyu-demo/20261120-html-interactive/` 关键文件哈希与入库时一致：`prototype/index.html` 为 `3d2603e8fc4df7aa0705a4de90e756aa27f858078c44b316b4d18ab1637fa92c`，`ceo-acceptance-20261120.md` 为 `839efafd0e8f30f1765de105d384a75fe11ad3faec140ee1ea0dcac214b085b0`。
- 本目录中 `ceo-acceptance-20261120.md` 是从影盏包拷来的历史记录，不代表本轮泊泊终验；本轮以本文件为准。
- 主页原图 `prototype/assets/bobo-frame.jpg` 与官方 V3 残存展示帧 `/workspace/mianyu-five-ip-images/04-泊泊-V3残存展示帧.jpg` 字节一致，SHA-256 `46007d733e5faf3c9e457c4ed3b37e687c6c18fd0130a0aa11d56256861779f6`。屏内角色为同一帧去底裁切 `bobo-figure.png`（SHA-256 `6347736443eabf32fa339392af02ad8c5c5ea1e30e90d370cc933756d90ecde1`），未见新绘改形。影盏头上插片与假眼已在 `.skin-bobo` 下隐藏。
- 文案为首发角色泊泊；可运行入口 `prototype/index.html` 与 `assets/app.js` 用字正确。代码中 `getUserMedia` 仅出现在注释，未调用，语音为模拟。走查 `verify-20261120-bobo/`（01–12）控制台无报错，路径可走通：开始今晚 → 落位 → 躲猫猫（含「算了，回来吧」）→ 回位与插片确认 → 开麦说明（模拟）→ 意图按钮 → 关光结束。
- 本目录 `CHANGE.md` 在 21:45 补充：当前图为官方 V3 残存帧的版式适配；若后续有不改形的屏内成稿，只在本目录替换后再做视觉复核。

本轮关键文件 SHA-256（2026-11-20 21:46 记录）：

- `CHANGE.md`：`e95e0e5984c9ab39a35d56fbee4928e7e881380d1237c8dbc57b7c519e5d27ba`
- `prototype/index.html`：`998e82fd05c120b4f6f6033165105dbe2e5a715594df1e3952e6acf709be2a9c`
- `prototype/assets/app.js`：`b3430c3d7a68a173064acdc8877c0a08b5963dc565c700128fa0c338b660abe4`
- `prototype/assets/styles.css`：`c1d24146543e37600755ac2dc64b1cc3315dc8a8ff9413f2b694431462864ffc`

## 已记录残留（不挡本轮通过）

- 去底后，行李箱与垫面之间在深色场景里可能见到一小块原图台面色，垫面外缘偶有轻毛边。
- 确认只能整帧轻倾，不能单独让牌耳转动；靠近无法先做「眼转向窗」（无单独表情层，也未新绘）。
- 开麦说明面板仍较高，可能挡住角色下沿。
- 语音仍为模拟；目前没有泊泊 V4 专包。

## 入库

本包先留在本地。是否写入眠语导入分支，须经主 bot 转交用户确认后再做；不得覆盖影盏 20261120 包与 20261112 静态原型正本，不得合并 PR #1。入库时不要把 `SOURCE.txt` 原样写入仓库（其中含工作约束），应另写 `SOURCE.md`。
