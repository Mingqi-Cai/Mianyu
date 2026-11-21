# 2026-11-20 recut-2146 独立总装说明

时间：2026-11-20 22:56 Asia/Shanghai
执行：CMQ-Demo · HTML制作，按 CMQ-CEO 派单只写本目录。
用字从 /workspace/mianyu-ip-names/OFFICIAL-NAMES.txt 复制（SHA-256 9fc86faedf76772f1efc710edcef76da0ef68938debfe1f086b5bd55900c0269）。本包角色为第 4 个正式 IP「泊泊」。

## 边界

- 只写入：`/workspace/mianyu-demo/20261120-html-interactive-bobo-recut-2146/`
- 未写入被污染快照 `/workspace/mianyu-demo/20261120-html-interactive-bobo/`
- 未改 `/workspace/mianyu-demo/20261120-html-interactive-bobo-night-rev/`（夜间收光观感已锁定）
- 未改 Design 修订包、恢复包或任何已终验正本
- 未入仓，未合并 PR #1。本包不是新的官方 IP 正本，也不是 21:46 入库目标替换件。用户看过并确认前，泊泊包一律不入仓。

## 文本（哈希保持 21:46 终验，未改一字）

来源：`/workspace/mianyu-demo/20261120-html-interactive-bobo-restore-2146/`

- `CHANGE.md` → SHA-256 e95e0e5984c9ab39a35d56fbee4928e7e881380d1237c8dbc57b7c519e5d27ba
- `prototype/index.html` → SHA-256 998e82fd05c120b4f6f6033165105dbe2e5a715594df1e3952e6acf709be2a9c
- `prototype/assets/styles.css` → SHA-256 c1d24146543e37600755ac2dc64b1cc3315dc8a8ff9413f2b694431462864ffc

未改这三份文本，因此也未把本说明写入 CHANGE.md。

## 角色切图（只用这一张）

`prototype/assets/bobo-figure.png` 从
`/workspace/mianyu-ip-system-finals/2026-11-20-屏内换皮素材-bobo-recut-2146/assets/bobo-figure.png`
原样拷入。SHA-256 4aef69898d6f525b977ea7b8ac0f3a3b0cb5e99bb2c96b382190cc04c213ae38，1010×737，760517 字节。
未使用丢失的 63477364…，也未使用 21:54 成稿 67ca03c3…。未把 Design 包的 previews/ 拷入页面素材。

## 其他未污染资产

只读拷贝自被污染快照目录中仍保持 21:46 终验或随影盏副本一并存在、且未被 21:54 总装改写的文件：

- `prototype/assets/app.js` → SHA-256 b3430c3d7a68a173064acdc8877c0a08b5963dc565c700128fa0c338b660abe4（终验，未改）
- `prototype/assets/bobo-frame.jpg` → SHA-256 46007d733e5faf3c9e457c4ed3b37e687c6c18fd0130a0aa11d56256861779f6
- `prototype/assets/insert-a.png` / `insert-b.png`（21:46 包原有插片，见 ASSETS.txt）
- `prototype/assets/room-night.jpg`、`yingzhan-figure.png`、`yingzhan-wall.jpg`
- 21:46 及更早的说明与验收记录：README.md、architecture 等、ceo-acceptance-20261120-bobo.md、verify-20261120-bobo/ 等

未拷贝：快照中已污染的 index.html、styles.css、CHANGE.md、bobo-figure.png；21:54 新增的 bobo-insert-a.png、bobo-insert-a@2x.png、bobo-wall.jpg、SOURCE.txt、ASSETS.txt、verify-20261120-bobo-assemble/；night-rev 的任何文件；走查截图占位图。

说明：`verify-20261120-bobo/` 是 21:46 验收时的历史截图（当时角色为已丢失的试切图），不能当作本 recut 切图的观感证据。本包自检放在 `verify-20261120-bobo-recut-2146/`。

## Skills 检索

执行前已查个人 Skills 库 SKILLS_INDEX.md（GitHub：Mingqi-Cai/my-ai-skills-library）。采用：

- `engineering-workflow/verification-before-completion`：完成前须留下可核对证据
- `frontend-engineering/frontend-visual-qa`：对已渲染首页与落位帧做视觉走查

`testing-automation/webapp-testing` 依赖 Playwright Python，本环境沿用既有 Chrome + puppeteer-core 的 file:// 验证，不新装 Playwright。未使用 `design/web-artifacts-builder`。未新开发 Skill。

## 自检（2026-11-20 22:57 Asia/Shanghai）

入口：`prototype/index.html`（file://）。脚本：`/tmp/mianyu-verify/shot-recut-2146.js`（Chrome + puppeteer-core）。证据：`verify-20261120-bobo-recut-2146/`。

- 无控制台错误、无 pageerror。
- 主页图为 `assets/bobo-frame.jpg`，自然尺寸 1152×864；不是 night-rev 的 bobo-home。
- 角色图为 `assets/bobo-figure.png`，自然尺寸 1010×737。
- 两插片槽为 `assets/insert-a.png` / `assets/insert-b.png`。`.skin-bobo .actor-inserts` 与 `.actor-eyes` 按 21:46 CSS 为 `display: none`（未叠影盏头插与假眼）。因此 medal 相对位置无法按可见矩形量，这是 21:46 文本原样，不是本轮改 CSS。
- `.skin-bobo .palm-glow` 按 21:46 CSS 为 opacity 0.35。
- 落位后角色宽 276px，bottom 197.75px（对应 21:46 `bottom: 24%`），场景底 `room-night.jpg`。
- 页面无 `.actor-glow-img`，未带入 night-rev 光晕图。
- 被污染快照、night-rev、Design recut 包、恢复包的目录树哈希与开工前一致。

本包仍不入仓，请验收后转主 bot 给用户看。
