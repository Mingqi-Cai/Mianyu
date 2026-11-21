# 泊泊 recut-2146 独立总装包 · CEO 终验记录

时间：2026-11-20 23:12 Asia/Shanghai  
执行：CMQ-CEO  
入口：`/workspace/mianyu-demo/20261120-html-interactive-bobo-recut-2146/prototype/index.html`

## 结论

**终验通过。** 同意验收「通过」结论。无新增挡验收项。请主 bot 明早转用户看。用户看到之前，本切图、本总装、night-rev、被污染快照均不入仓。不合并 PR #1。本包不是新的官方 IP 正本，不覆盖已终验设计正本。

本包是 21:46 终验文本 + 依官方 V3 残存展示帧补做的屏内切图，与 night-rev 分轨。主页仍为官方亮底棚拍帧，屏内角色落在 `room-night.jpg` 上，未按 night-rev 观感标准评判。

## 路径

- 切图包：`/workspace/mianyu-ip-system-finals/2026-11-20-屏内换皮素材-bobo-recut-2146/`
- 切图：`.../assets/bobo-figure.png`（SHA-256 `4aef69898d6f525b977ea7b8ac0f3a3b0cb5e99bb2c96b382190cc04c213ae38`，1010×737 RGBA，760517 字节）
- 总装：`/workspace/mianyu-demo/20261120-html-interactive-bobo-recut-2146/`
- 验收记录与走查截图：`/workspace/mianyu-demo/20261120-html-interactive-bobo-recut-2146/verify-20261120-recut-2146-accept/`（`ACCEPT.md`、`report.json`、01–19 走查截图、绿底切图取证）

关键帧：`01-home.png`、`03-seated.png`、`03b-seated-actor-crop.png`、`figure-on-green.png`、`crop-mat-left-on-green.png`、`17-end.png`。

## 哈希复核（与验收走查前后及派单要求一致）

| 文件 | SHA-256 |
|---|---|
| CHANGE.md | e95e0e5984c9ab39a35d56fbee4928e7e881380d1237c8dbc57b7c519e5d27ba |
| prototype/index.html | 998e82fd05c120b4f6f6033165105dbe2e5a715594df1e3952e6acf709be2a9c |
| prototype/assets/styles.css | c1d24146543e37600755ac2dc64b1cc3315dc8a8ff9413f2b694431462864ffc |
| prototype/assets/app.js | b3430c3d7a68a173064acdc8877c0a08b5963dc565c700128fa0c338b660abe4 |
| prototype/assets/bobo-figure.png | 4aef69898d6f525b977ea7b8ac0f3a3b0cb5e99bb2c96b382190cc04c213ae38 |
| prototype/assets/bobo-frame.jpg | 46007d733e5faf3c9e457c4ed3b37e687c6c18fd0130a0aa11d56256861779f6 |
| prototype/assets/insert-a.png | 4f606d490b3e18f077e87d6696b745adcb96726f23ccd90fdfb5259220c119f2 |
| prototype/assets/insert-b.png | 1ebd7be87646be19fe07a5a0e92478445acd0a70539718b4f0c2424e3e32e1c3 |

角色图不是丢失的 63477364…，也不是 21:54 的 67ca03c3…。

## 目视与隔离

- 主页为官方 V3 残存展示帧（亮底棚拍），首发角色为泊泊，标注屏内 Demo、非真机 AR。
- 垫面左侧为完整圆角弧；行李箱与垫面之间地面湾为透明。丢失试切图那种左侧白块未再现。
- 结束页写明「不是医疗或心理咨询产品」。源码去掉注释后无 `getUserMedia` 调用。可见文案无疗效、助眠、哄睡宣称。
- 被污染快照 `/workspace/mianyu-demo/20261120-html-interactive-bobo/` 关键文件 mtime 仍为 21:54，未被改写。night-rev 关键文件 mtime 仍为 22:09–22:19，未被改写。未入仓。

包内 `ceo-acceptance-20261120.md` 是另一套已终验互动 Demo 的历史拷贝，不代表本包终验。本文件才是 recut-2146 的 CEO 终验记录。

## 残留（不挡终验，无新增项）

1. 官方帧已切到行李箱左缘；
2. 提手金属间隙有极小原背景色；
3. 垫面右侧外缘可见约 1–3 像素级偏紧或锯齿；
4. 行李箱与垫面窄缝仍可见少许原台面色；
5. 开麦说明面板较高，挡住角色下沿；
6. 确认只能整帧轻倾，不能单独让牌耳转动；
7. 靠近无法先做「眼转向窗」；
8. 语音为模拟；
9. 无 V4 专包。
