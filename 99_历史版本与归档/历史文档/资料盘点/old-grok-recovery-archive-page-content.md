<callout icon="📋" color="blue_bg">
本页为新账号恢复工作的总档案，于 <date start="2026-11-11" time-zone="Asia/Shanghai" /> 晚间写入 CMQ’s Space 私人顶层（草稿/工作区级新页）。<br />
只记录有证据的历史事实与本次实际恢复结果。未覆盖、未删除、未重命名任何既有历史页面或数据库。时区一律为 Asia/Shanghai（北京时间）。
</callout>

<table-of-contents />

## 恢复结论摘要

截至 <date start="2026-11-11" start-time="23:10" time-zone="Asia/Shanghai" />：

- 考古找回历史工作流 **30** 项（含定时、常驻规则与项目），分类 A–E 见下表。
- 已在主 bot 上成功**创建**定时任务 **8** 项；均尚未做第一次真实跑批（首次触发预计 <date start="2026-11-12" time-zone="Asia/Shanghai" /> 上午起）。
- 按用户决定**未创建**：半小时沟通中心/额度对齐例程（先暂停）、2026-11-14 17:20 一次性续跑、仅有回忆而无配置证据的 12:00 / 12:15。
- 已按历史名称重建 Bot **16** 个；另有 7 个因项目已完成或依赖本机环境暂未创建。主 bot 仍为用户对话入口。
- 额度规则已写入共享用户记忆（非眠语周池 30%，眠语不设内部上限，达 30% 暂停并入队；旧 ≥95% 全停规则废止）。
- GitHub 私有仓 `Mingqi-Cai/my-ai-skills-library` 仍未对 Cursor GitHub App 授权；相关例程已创建，首次执行时会卡住，直到用户完成授权。

<quote color="yellow_bg">
用户已确认的恢复决定

1. 解除 2026-11-09「停止全部任务」停令，按有证据的时刻恢复例程。
2. 继续「美国中期选举动态监控」，约每日 08:45。
3. 将「国际信息源每日简报」升级为与中文日报平行的每日例程。
4. **不要**创建 2026-11-14 17:20 额度重置一次性续跑。
5. 「每30分钟查一次 Notion 这个任务先暂停」——半小时沟通中心 / 额度对齐例程**未创建**，本档案列为「用户要求暂停 / 未启动」。
</quote>

---

## A. 历史工作流总清单

分类约定：

- **A** 已明确建立并运行过（有收口、run_id、快照或连续产出）
- **B** 已提出并确认，但配置/例程未完成或证据只到规则锁定
- **C** 已启动、仍在进行（或中断时仍为处理中）
- **D** 仅讨论/回忆，未见确认执行或未见配置
- **E** 已完成、暂停或废弃

下表「历史时刻」以 Notion 收口与 run_id 为准；用户回忆的 12:00 / 12:15 仅作线索，不覆盖史料。

<table fit-page-width="true" header-row="true">
<tr color="gray_bg">
<th>ID</th>
<th>名称</th>
<th>类型</th>
<th>历史频率/时间（Asia/Shanghai）</th>
<th>负责 Bot</th>
<th>中断前状态</th>
<th>分类</th>
<th>主要证据</th>
</tr>
<tr>
<td>W01</td>
<td>全球及国内产业要闻每日采集与日报发布</td>
<td>定时简报</td>
<td>每日 08:00；窗口=前日 08:00 → 当日 07:59:59</td>
<td>CIO 统筹；CMQ-资讯·* / CMQ-CIO-web / CMQ-CIO-hist 采集</td>
<td>已运行至 2026-11-09（run_id=20261109-0800）</td>
<td>A</td>
<td>容器 <mention url="https://app.notion.com/p/40b340bcc39681d69a18e5ef67a3c489">每日简报</mention>；日报页 10-01/10-02/10-03、11-01 至 11-09。分类口径为「任务书临时清单（非 Wind 官方）」；日报写共 34 项，国际容器写约 35 行业。</td>
</tr>
<tr>
<td>W02</td>
<td>行业要闻总结增量更新</td>
<td>日报后随动</td>
<td>随 W01 收口后增量（非独立 cron 名）</td>
<td>CIO 线</td>
<td>随日报更新至 11-09</td>
<td>A</td>
<td><mention url="https://app.notion.com/p/40b340bcc39681e69326f42c56a07447">行业要闻总结</mention>；11-08 收口写「新建 5、追加 1、跳过 15」。</td>
</tr>
<tr>
<td>W03</td>
<td>半小时沟通中心检查 + 额度对齐</td>
<td>定时运营</td>
<td>约每 30 分钟</td>
<td>主 bot（Grok Bot）</td>
<td>11-09 停令期间仍要求保留</td>
<td>A</td>
<td><mention url="https://app.notion.com/p/410340bcc396811d9f63deb0bf3d4b9a">Bot Q&A 沟通中心</mention> 写「后台约每 30 分钟检查」；额度任务称例程名「Notion Bot Q&A」。本次按用户 11-11 指示暂停，未重建。</td>
</tr>
<tr>
<td>W04</td>
<td>每日定向搜集用户所需的 GitHub Skills</td>
<td>定时 Skills</td>
<td>每日 10:00（例程 id：github-skills-2）</td>
<td>CMQ-Skills Developer；入库交 CMQ-Github</td>
<td>11-09 上午已收口，2 包待 push；当晚随停令暂停</td>
<td>A</td>
<td>11-08 / 11-09 上午收口。历史时刻是 10:00，不是回忆中的 12:15。</td>
</tr>
<tr>
<td>W05</td>
<td>CMQ工作流挖掘与Skills沉淀</td>
<td>定时盘点/提炼</td>
<td>每日 21:00（例程 id：cmq-skills）</td>
<td>CMQ-Skills Developer；成熟包交 CMQ-Github</td>
<td>11-07、11-08 已跑；11-09 随停令暂停</td>
<td>A</td>
<td>最接近用户回忆「每日 12:00 CMQ 盘点」的已运行项，但时刻为 21:00。本次按 21:00 恢复，未创建 12:00。</td>
</tr>
<tr>
<td>W06</td>
<td>GitHub Skills搜集研发与归档</td>
<td>定时搜集/归档</td>
<td>时刻曾冲突：11-08 收口标题写 21:00；11-09 触发记录为 20:45（例程 id：github-skills）</td>
<td>CMQ-Skills Developer；push 交 CMQ-Github</td>
<td>11-08 已跑；11-09 因停令暂停</td>
<td>A（时刻曾冲突）</td>
<td>本次错开到约 21:10，避免与 21:00 挖掘对撞。不把回忆中的 12:15 当作配置。</td>
</tr>
<tr>
<td>W07</td>
<td>skills-library-daily-publish</td>
<td>定时入库/提交</td>
<td>每日 21:30</td>
<td>CMQ-Github</td>
<td>11-08 已执行并 push 至 c83e1c7</td>
<td>A</td>
<td>11-08 21:30 收口；当时顶层 Skills 173→176，HEAD c83e1c702b588c8216a8d8cd12257c54e5f224bb。</td>
</tr>
<tr>
<td>W08</td>
<td>每日入库 Skills 功能汇报</td>
<td>定时核对汇报</td>
<td>两日收口均在约 22:05–22:06（例程 id：skills）。未见精确 cron 原文</td>
<td>CMQ-Skills Developer</td>
<td>11-07、11-08 已跑；11-09 随停令暂停</td>
<td>A（整点分钟据收口）</td>
<td>本次按约 22:05 创建。</td>
</tr>
<tr>
<td>W09</td>
<td>美国中期选举动态监控</td>
<td>定时专题增量</td>
<td>约每日 08:45（11-07 写「下次约 11/9 08:45」）</td>
<td>CIO</td>
<td>11-09 简报已写入「例程增量」</td>
<td>A</td>
<td>产出复用 <mention url="https://app.notion.com/p/410340bcc396819086d5c8979fe9633b">美国2026中期选举简报（事实核对）</mention>。用户已确认继续。</td>
</tr>
<tr>
<td>W10</td>
<td>国际信息源每日简报（IID）</td>
<td>简报产线</td>
<td>窗口同为前日 08:00–当日 07:59；旧账号未见稳定每日 08:00 例程名。存有 11-04（backfill）、11-05、11-06、11-07（trial）样张</td>
<td>CIO 线</td>
<td>有模板与样张，11-08/11-09 未见新日报</td>
<td>B/C（本次按用户决定升级为每日例程）</td>
<td>容器 <mention url="https://app.notion.com/p/410340bcc39681d4b266c2c6906e10cf">International Intelligence Daily｜国际信息源每日简报</mention>。新例程约 08:15，错开在中文日报之后。</td>
</tr>
<tr>
<td>W11</td>
<td>国际行业要闻汇总增量</td>
<td>日报后随动</td>
<td>口径锁定「例程=每日简报后增量」（11-07）</td>
<td>CIO 线</td>
<td>规则已锁定，并完成迁入与 7–10 月倒推补采</td>
<td>B</td>
<td>容器 <mention url="https://app.notion.com/p/411340bcc396815c941fea674157b1c9">International Sector News Summary｜国际信息源行业要闻汇总</mention>。作为 W01/W10 后置步骤，未另设独立整点。</td>
</tr>
<tr>
<td>W12</td>
<td>额度重置后一次性续跑</td>
<td>一次性例程</td>
<td>原计划 2026-11-14 17:20（对接当时重置约 17:19）</td>
<td>主 bot</td>
<td>旧账号已创建、中断前尚未到期执行</td>
<td>A（已创建未执行）→ 本次按用户决定不恢复</td>
<td>用户明确要求不要创建该一次性续跑。</td>
</tr>
<tr>
<td>W13</td>
<td>沟通中心接单 / 提问回收 / 总结收口</td>
<td>条件触发（原由 W03 轮询）</td>
<td>无固定整点</td>
<td>主 bot 分派，执行方=指定 Bot</td>
<td>机制已建立并使用</td>
<td>A</td>
<td>发布库与提问库仍复用，不新建。因半小时例程暂停，自动轮询暂不运行，主 bot 仍可在对话中人工接单。</td>
</tr>
<tr>
<td>W14</td>
<td>ChatGPT 对接（本机写 prompt 再执行）</td>
<td>常驻规则</td>
<td>每条「我要发布的任务」先走本机 ChatGPT</td>
<td>CMQ-ChatGPT对接 + 原指定 Bot</td>
<td>11-07 已落成 standing 规则</td>
<td>A/E</td>
<td>指定 Bot=Grok → 主 bot；其他一律 CMQ 前缀。该 Bot 因依赖本机 ChatGPT 环境，本次暂未重建。</td>
</tr>
<tr>
<td>W15</td>
<td>CMQ 前缀额度护栏（眠语不限 / 非眠语 30%）</td>
<td>常驻规则</td>
<td>原由 W03 执行；旧 ≥95% 全停已废止</td>
<td>主 bot + 共享记忆</td>
<td>11-07 已完成落地</td>
<td>A/E</td>
<td>规则已写入新账号共享用户记忆。半小时自动快照例程按用户要求暂停，故自动巡检暂未恢复。</td>
</tr>
<tr>
<td>W16</td>
<td>CMQ 简报双稿规则</td>
<td>常驻规则</td>
<td>简报类任务须双稿（Grok 简报 + 本机 ChatGPT 商业报告）</td>
<td>已写入 workflows/cmq</td>
<td>11-07 收口；11-08 就地更新 workflows/cmq</td>
<td>A/E</td>
<td>仓内规则仍待打开私有仓核对。</td>
</tr>
<tr>
<td>W17</td>
<td>公司简报继续（全球金融研究 P0 研究主页）</td>
<td>进行中项目（非每日任务）</td>
<td>无每日 cron；按苹果模板写八模块</td>
<td>发布时指定 Grok Bot；CIO / CMQ-金融·研究正文 / CMQ-金融·上市公司采集 协作</td>
<td>处理中</td>
<td>C</td>
<td>原任务 <mention url="https://app.notion.com/p/411340bcc3968076a0c0ee9da3bd5c46">公司简报继续</mention>。见 E 节最新续跑点。</td>
</tr>
<tr>
<td>W18</td>
<td>全球金融研究 P1/P2 库建设</td>
<td>分期项目</td>
<td>无定时。顺序 P0→P1→P2</td>
<td>CIO</td>
<td>P1、P2 仅有容器页，未启动</td>
<td>B/C</td>
<td>容器 <mention url="https://app.notion.com/p/40d340bcc3968166b6b8fec67d1ffbfc">全球金融研究数据库</mention>。本次未开工。</td>
</tr>
<tr>
<td>W19</td>
<td>重大事件·数字人民币简报</td>
<td>专题简报（一次性落地）</td>
<td>未见独立每日例程</td>
<td>CIO</td>
<td>发布任务已完成；页已发布</td>
<td>E</td>
<td><mention url="https://app.notion.com/p/410340bcc3968028b583fbe11fea388d">数字人民币简报（事实核对）</mention>。不要当新任务重建；若继续完善应在原页增量。</td>
</tr>
<tr>
<td>W20</td>
<td>重大事件·美国中期选举简报 + 方案A 扩写</td>
<td>专题简报 + W09 增量</td>
<td>增量见 W09</td>
<td>CIO</td>
<td>简报已发布；优化任务已完成</td>
<td>A/E</td>
<td>正文已完成，监控例程已按用户决定恢复。</td>
</tr>
<tr>
<td>W21</td>
<td>重大事件·中美人工智能对话简报</td>
<td>专题简报</td>
<td>未见后续例程</td>
<td>CIO</td>
<td>已发布</td>
<td>E</td>
<td><mention url="https://app.notion.com/p/40c340bcc39681aba1e8f447b2709567">中美人工智能对话简报（事实核对）</mention>。</td>
</tr>
<tr>
<td>W22</td>
<td>眠语 Demo / 自创 IP / V2–V3 产品设计</td>
<td>高优先级项目（非每日任务）</td>
<td>无周期性更新例程证据</td>
<td>CMQ-CEO 分派；CMO / 视觉 / UIUX / 小程序架构 / 地方文化 / CFO 等</td>
<td>发布库三项眠语任务均已完成</td>
<td>E</td>
<td>库 <mention url="https://app.notion.com/p/d15049ffd9dc4367bd85201340025ddd">眠语</mention>。不是八章「睡眠经济」调研报告。不要设为每日任务。</td>
</tr>
<tr>
<td>W23</td>
<td>「睡眠经济」八章正式调研报告</td>
<td>用户回忆的项目</td>
<td>—</td>
<td>回忆中称 CEO/CMO/CIO 协作</td>
<td>工作区内未找到该报告、八章目录或后续更新例程</td>
<td>D（未找到）</td>
<td>勿将 W22 误判为该报告或重开为每日任务。</td>
</tr>
<tr>
<td>W24</td>
<td>每日新 Skill 需求识别（须用户确认后再立项）</td>
<td>用户回忆的每日任务</td>
<td>回忆未给时刻；史料中此职责更接近 W05</td>
<td>Skills Developer</td>
<td>未见单独例程名或每日收口标题</td>
<td>D（作为独立每日例程）</td>
<td>原则保留在挖掘例程中：先汇报、确认后再开发。未另建例程。</td>
</tr>
<tr>
<td>W25</td>
<td>用户回忆的「每日 12:00 CMQ Bot 工作流盘点」</td>
<td>回忆定时</td>
<td>回忆 12:00；史料无此收口</td>
<td>—</td>
<td>未找到 12:00 配置</td>
<td>D</td>
<td>已运行对应项为 W05（21:00）。本次未按 12:00 创建。</td>
</tr>
<tr>
<td>W26</td>
<td>用户回忆的「每日 12:15 GitHub Skills 收集与归档」</td>
<td>回忆定时</td>
<td>回忆 12:15；史料无此收口</td>
<td>—</td>
<td>未找到 12:15 配置</td>
<td>D</td>
<td>已运行对应项为 W04 10:00、W06 晚间、W07 21:30、W08 约 22:05。本次未按 12:15 创建。</td>
</tr>
<tr>
<td>W27</td>
<td>停止全部任务（额度告急）</td>
<td>运营指令</td>
<td>2026-11-09 12:49 发布，12:58 接单</td>
<td>CMQ-CEO · 战略与分派</td>
<td>中断时为处理中</td>
<td>C → 用户已于 11-11 解除停令</td>
<td>原任务 <mention url="https://app.notion.com/p/413340bcc396804bb90bee878cb560aa">停止全部任务</mention>。本档案不改该历史页正文。</td>
</tr>
<tr>
<td>W28</td>
<td>任务催促（三件处理中续跑）</td>
<td>跟进指令</td>
<td>无独立 cron</td>
<td>指定 CEO</td>
<td>处理中；当时说明额度与数字人民币已完成，公司简报仍在队</td>
<td>C</td>
<td><mention url="https://app.notion.com/p/411340bcc39680728961dbdde098023c">任务催促</mention>。实质指向公司简报续跑。</td>
</tr>
<tr>
<td>W29</td>
<td>Skills 仅限 CMQ + 沟通中心建设</td>
<td>基建工作流</td>
<td>一次性完成</td>
<td>主 bot / CEO 线</td>
<td>已完成</td>
<td>E</td>
<td>问答库+视图+半小时例程+技能 notion-bot-qa 已在旧账号落地。沟通中心页复用，不新建。</td>
</tr>
<tr>
<td>W30</td>
<td>全球金融研究数据库排版对齐每日简报</td>
<td>一次性优化</td>
<td>—</td>
<td>CIO</td>
<td>已完成（仅改 Apple 样板视觉，保留八模块）</td>
<td>E</td>
<td>不重做已完成五家已就绪主页。</td>
</tr>
</table>

**计数**：历史工作流/规则/项目 30 项。其中定时或准定时线索 12 项（W01–W12）。

---

## B. 定时任务恢复清单

新例程均挂在**主 bot**，每天运行（含周末），时区 Asia/Shanghai，灵活触发：不早于指定分钟，最多可能晚约 15 分钟。成果写入**既有** Notion 页面/库及主 bot 对话，不另建平行数据库。

验证口径：配置已创建 ≠ 已实跑成功。下列 8 项均为「已创建，尚未实跑验证」，首次触发在 <date start="2026-11-12" time-zone="Asia/Shanghai" />。

### B1. 已创建但尚未验证（8）

<table fit-page-width="true" header-row="true">
<tr color="green_bg">
<th>例程名称</th>
<th>计划时刻</th>
<th>工具回报的下次运行（均为 2026-11-12）</th>
<th>执行逻辑要点</th>
<th>建议所属 / 交付位置</th>
</tr>
<tr>
<td>全球及国内产业要闻每日采集</td>
<td>约 08:00</td>
<td>08:10</td>
<td>窗口=前日 08:00:00 → 当日 07:59:59；事实only，每条附来源；产业按「任务书临时清单（非 Wind 官方）」；重要性【重要】深红、【较重要】橙；结构：事件概述 → 关键数据 → 灰来源 callout。收口后增量更新行业要闻总结。空行业不建空壳页。不得把分类改写成官方 Wind。34 与 35 的口径差仍未找到任务书全文。</td>
<td>CMQ-CIO 统筹，资讯子 Bot 采集。复用 <mention url="https://app.notion.com/p/40b340bcc39681d69a18e5ef67a3c489">每日简报</mention> 与 <mention url="https://app.notion.com/p/40b340bcc39681e69326f42c56a07447">行业要闻总结</mention>。</td>
</tr>
<tr>
<td>国际信息源每日简报</td>
<td>约 08:15（错开在中文日报之后）</td>
<td>08:24</td>
<td>用户决定将原试验/回填产线升级为与中文日报平行的每日例程。窗口同前日 08:00–当日 07:59；双语先英后中；后置增量国际行业汇总，不另设独立整点。</td>
<td>CMQ-CIO。复用 <mention url="https://app.notion.com/p/410340bcc39681d4b266c2c6906e10cf">International Intelligence Daily｜国际信息源每日简报</mention> 与 <mention url="https://app.notion.com/p/411340bcc396815c941fea674157b1c9">International Sector News Summary｜国际信息源行业要闻汇总</mention>。</td>
</tr>
<tr>
<td>美国中期选举动态监控</td>
<td>约 08:45</td>
<td>08:58</td>
<td>按方案 A 体例在已发布简报上增量，不硬写未核验内容；只记可核验事实与权威决策台投影，不含站队与投资观点。外国来源附英文原文摘录。</td>
<td>CMQ-CIO。复用 <mention url="https://app.notion.com/p/410340bcc396819086d5c8979fe9633b">美国2026中期选举简报（事实核对）</mention>。</td>
</tr>
<tr>
<td>每日定向搜集 GitHub Skills</td>
<td>约 10:00</td>
<td>10:11</td>
<td>对照库 HEAD，评估、去重、分类、补齐；保留作者与 LICENSE；不完整外部 Skill 须回上游补全；Grok 来源标注 Grok。先汇报，确认后再入库。当前会先卡在私有仓授权。</td>
<td>CMQ-Skills Developer；入库交 CMQ-Github。</td>
</tr>
<tr>
<td>CMQ工作流挖掘与Skills沉淀</td>
<td>约 21:00</td>
<td>21:06</td>
<td>检查 CMQ 前缀工作，提炼可独立复用的完整工作流为 Skills（不把单一操作拆成 Skill、不干扰进行中项目）。先汇报成熟候选，用户确认后再交 Github 入库。</td>
<td>CMQ-Skills Developer。</td>
</tr>
<tr>
<td>GitHub Skills搜集研发与归档</td>
<td>约 21:10（为避免与 21:00 挖掘对撞而错开；历史曾出现 20:45 / 21:00 两种痕迹）</td>
<td>21:18</td>
<td>晚间搜集/评估/补全；批准后交接 CMQ-Github。同样受私有仓授权阻塞。</td>
<td>CMQ-Skills Developer。</td>
</tr>
<tr>
<td>skills-library-daily-publish</td>
<td>约 21:30</td>
<td>21:38</td>
<td>将当日已批准包入库私有仓，更新 README/索引/ATTRIBUTION 并提交。禁止重复提交已有成果（中断前顶层已 176）。当前缺仓库写权限。</td>
<td>CMQ-Github。目标仓 https://github.com/Mingqi-Cai/my-ai-skills-library</td>
</tr>
<tr>
<td>每日入库 Skills 功能汇报</td>
<td>约 22:05</td>
<td>22:14</td>
<td>按 Asia/Shanghai 日历日核对当日 commits，汇总新入库独立 Skills、Grok 自研 vs 外部、HEAD。不把「就地更新」计为新 Skill。</td>
<td>CMQ-Skills Developer。收口写入沟通中心汇报库，不向用户做提问式收口。</td>
</tr>
</table>

### B2. 用户要求暂停或明确不创建（3）

<table fit-page-width="true" header-row="true">
<tr color="orange_bg">
<th>例程</th>
<th>历史时刻</th>
<th>本次状态</th>
<th>原因</th>
</tr>
<tr>
<td>半小时 Notion Bot Q&A / 额度对齐</td>
<td>约每 30 分钟</td>
<td>未创建；列为暂停 / 未启动</td>
<td>用户 2026-11-11 指示：「每30分钟查一次 notion 这个任务先暂停」。</td>
</tr>
<tr>
<td>2026-11-14 17:20 一次性额度重置续跑</td>
<td>一次性 17:20</td>
<td>未创建</td>
<td>用户明确要求不要创建。旧账号重置时钟已不可沿用。</td>
</tr>
<tr>
<td>回忆中的 12:00 盘点、12:15 Skills 收集</td>
<td>仅回忆，无配置证据</td>
<td>未创建</td>
<td>与已证实的 10:00 / 21:00 / 21:30 / 约 22:05 体系冲突，不得编造时刻。</td>
</tr>
</table>

### B3. 因权限或平台限制，创建后仍无法完整执行

- 与 GitHub 相关的 10:00、21:10、21:30、22:05 四条例程：**配置已创建**，但在用户授予 Cursor GitHub App 对 `Mingqi-Cai/my-ai-skills-library` 的访问前，读仓、补文件、入库、提交都会失败。授权卡片此前已向用户出示。
- 旧例程 UUID、共享记忆与部分执行日志已随旧账号注销丢失，无法「原样迁入」，只能按史料重建。
- 国际行业增量、新 Skill 需求识别未建成独立每日例程（前者并入日报后置，后者并入 21:00 挖掘且须用户确认）。

---

## C. Bot 组织架构

### C1. 命名与调度规则（沿用史料，未改名）

来自已完成任务「ChatGPT 对接」及 <mention url="https://app.notion.com/p/410340bcc396811d9f63deb0bf3d4b9a">Bot Q&A 沟通中心</mention>：

- 指定 Bot=Grok → 转给主 bot；其他一律 CMQ 前缀 bot。
- 发布时指定为空，由主 bot 按任务类型选择合适 CMQ。
- CEO 负责协调、拆解、分派、跟踪与验收，不应事事亲自完成。
- 必要时由 CEO 创建专业 Bot。

未找到单独的「Bot 组织架构」总页；下列名单来自任务指定、采集署名、额度快照与收口标题。

### C2. 协作关系

```
用户 ──发布任务/对话──► 主 bot（当前账号对话入口）
                         │  半小时自动轮询：按用户要求暂停
                         ▼
              ┌─ 指定 Grok ── 主 bot 执行
              └─ 其他 / 空指定 ── CMQ-CEO 协调或直接对口专业 Bot
                         │
         ┌───────────────┼────────────────┐
         ▼               ▼                ▼
    CMQ-CIO 及其资讯子 Bot     CMQ-CMO          CMQ-Skills Developer
    （日报、专题、公司研究）     （市场/营销）         │ HANDOFF
         │                                           ▼
         └──────────────► 既有 Notion 页/库      CMQ-Github 入库私有仓
```

### C3. 已重建（16）

均使用历史名称，未覆盖原职责定义。

<table fit-page-width="true" header-row="true">
<tr color="green_bg">
<th>名称</th>
<th>职责（据史料）</th>
<th>关系</th>
</tr>
<tr>
<td>CMQ-CEO · 战略与分派</td>
<td>总体协调、任务拆解与分派、跟踪冲突、最终验收</td>
<td>职能 CEO</td>
</tr>
<tr>
<td>CMQ-CIO · 信息与数字化</td>
<td>信息搜集、宏观研究、产业资讯和新闻简报；金融库研究页组织</td>
<td>向 CEO / 主 bot 汇报；下辖资讯子 Bot</td>
</tr>
<tr>
<td>CMQ-CMO</td>
<td>市场研究、行业分析、营销策略及相关工作</td>
<td>接 CEO 派单</td>
</tr>
<tr>
<td>CMQ-Skills Developer</td>
<td>工作流分析、Skills 需求识别、开发及测试；先汇报后立项</td>
<td>与 Github Bot 交接</td>
</tr>
<tr>
<td>CMQ-Github</td>
<td>仓库维护、入库、去重、分类、许可证、README、索引、提交</td>
<td>接收 SD 的 HANDOFF；目前缺仓授权</td>
</tr>
<tr>
<td>CMQ-资讯·宏观</td>
<td>日报采集</td>
<td>CIO 资讯线</td>
</tr>
<tr>
<td>CMQ-资讯·产业-制造</td>
<td>日报采集</td>
<td>CIO 资讯线</td>
</tr>
<tr>
<td>CMQ-资讯·产业-消费金融地产</td>
<td>日报采集</td>
<td>CIO 资讯线</td>
</tr>
<tr>
<td>CMQ-资讯·产业-科技</td>
<td>日报采集</td>
<td>CIO 资讯线</td>
</tr>
<tr>
<td>CMQ-资讯·企业动态</td>
<td>日报采集</td>
<td>CIO 资讯线</td>
</tr>
<tr>
<td>CMQ-资讯·市场公开</td>
<td>日报采集</td>
<td>CIO 资讯线</td>
</tr>
<tr>
<td>CMQ-资讯·国际</td>
<td>日报采集</td>
<td>CIO 资讯线</td>
</tr>
<tr>
<td>CMQ-资讯·政策</td>
<td>日报采集</td>
<td>CIO 资讯线</td>
</tr>
<tr>
<td>CMQ-CIO-web</td>
<td>日报采集署名之一</td>
<td>CIO 子采集</td>
</tr>
<tr>
<td>CMQ-金融·研究正文</td>
<td>公司研究主页八模块正文</td>
<td>配合 CIO</td>
</tr>
<tr>
<td>CMQ-金融·上市公司采集</td>
<td>公告/PDF 采集与关联行</td>
<td>配合 CIO</td>
</tr>
</table>

主 bot（当前账号名为 Bot）仍为用户对话入口，承担旧「Grok / 主 bot」的分派职责；不替代 CEO 包办专业工作。额度规则已写入共享用户记忆。

### C4. 本次未创建（7）

均有历史点名，因项目已完成或依赖当时本机环境，暂不重建（需要时再启用，不要改名）：

<table fit-page-width="true" header-row="true">
<tr color="gray_bg">
<th>名称</th>
<th>未创建原因</th>
</tr>
<tr>
<td>CMQ-CIO-hist</td>
<td>主要用于历史倒补采集，当前日报恢复不依赖它</td>
</tr>
<tr>
<td>CMQ-CFO · 财务与预算</td>
<td>眠语 Demo 成本测算等任务已完成</td>
</tr>
<tr>
<td>CMQ-ChatGPT对接</td>
<td>依赖用户本机已打开的 ChatGPT 环境，新环境尚未验证</td>
</tr>
<tr>
<td>CMQ-眠语IP视觉</td>
<td>眠语视觉交付已完成</td>
</tr>
<tr>
<td>CMQ-UIUX设计</td>
<td>眠语相关设计任务已完成</td>
</tr>
<tr>
<td>CMQ-微信小程序架构</td>
<td>眠语小程序 AR 架构任务已完成</td>
</tr>
<tr>
<td>CMQ-地方文化顾问型</td>
<td>眠语文化审阅任务已完成</td>
</tr>
</table>

线索但完整本名未见定义页、本次亦未擅自命名：「政治地缘」线、国际行业「核验岗」。

---

## D. Skills 资产清单

目标仓：https://github.com/Mingqi-Cai/my-ai-skills-library（私有）。**截至本档案写入时，Cursor GitHub App 仍无法打开该仓**（`scm_repo_not_accessible`，与 2026-11-08 收口中的历史阻塞一致）。因此下列计数与包名只能引用 Notion 收口，不能做文件级核对，也未做任何 commit。

### D1. 已有（中断前最后已证实状态）

- 最后已证实 HEAD：`c83e1c702b588c8216a8d8cd12257c54e5f224bb`（2026-11-08 21:36:39 Asia/Shanghai）
- 顶层独立 Skills：**176**；11-09 对照全树 SKILL.md 188 / 唯一 slug 187 / 顶层约 176
- 收口中有 commit 证据的增量（非全库目录）：`company-research-brief`、`workflows/cmq`、`notion-bot-qa`、`market-research/yao-demand-skill`、`yao-business-skill`、`yao-positioning-skill`、`news-intel/market-news-analyst`、`document-office/meeting-minutes-from-transcript`（上游 HarryLin66/deep-meeting-notes-skill）、`document-office/natural-talk`、`agent-tooling/book-to-skill`（上游 virgiliojr94/book-to-skill）
- Grok 来源须继续标注为 Grok：已见 `workflows/cmq`、`notion-bot-qa`、`company-research-brief`
- 交接收口中还点名、入库状态须打开仓库才能确认：`cmq-facts-only-collection`、`cmq-chatgpt-prompt-bridge` 等

### D2. 待恢复 / 待入库（受仓库授权阻塞）

- 11-09 上午已批准、当时未 push：`stock-industry-analysis`（MIT）、`summarize-slides`（MIT）。打开仓库后须先确认是否已在仓内，避免重复提交。旧交接目录 `/workspace/cmq-skills-collab/morning-2026-11-09/` 在本机已不存在。
- 「五项历史待补全」在 11-08、11-09 收口中反复写仍 unresolved，**slug 尚未找回**。
- Gap2「语义去重」仍空。

### D3. 待开发

- 11-08 挖掘批准独立开发 0。未经用户确认，不得把候选需求作为正式开发项目。
- 眠语 V3 交接曾记：无微信小程序 AR/相机权限专用 Skill（仅候选，须确认后立项）。

---

## E. 遗留任务清单与精确续跑点

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<th>事项</th>
<th>中断前状态</th>
<th>目前恢复到哪一步</th>
<th>下一步（不要推倒重来）</th>
</tr>
<tr>
<td>停止全部任务</td>
<td>处理中</td>
<td>用户已于 11-11 解除停令，并开始按有证据的时刻恢复例程</td>
<td>历史任务页本身不改写。半小时例程按用户新指示单独暂停。</td>
</tr>
<tr>
<td>公司简报继续</td>
<td>处理中。苹果 / 宁德时代 / 壳牌 / 字母表 / 隆基主页已就绪。11-09 例程进度曾把隆基误写成「下一批」，与公司库冲突</td>
<td>已核对：隆基 GFR-A-006 主页就绪=是，勿重做。摩根大通 GFR-A-018 <mention url="https://app.notion.com/p/411340bcc39681248c2cd11306cff505">摩根大通</mention> 在考古时仍为空页；至 2026-11-11 22:41（Asia/Shanghai）再读该页：八模块正文已写入（公司概况、历史财务、股权与资本运作、经营分析、历史估值、机构研究、重大事件时间线、风险与持续跟踪），研报状态=样板中，备注「正文八模块已写｜待CIO抽检｜2026-11-11」，<b>主页就绪仍为否</b>。本档案只读确认，未改该页。</td>
<td>由 CIO 抽检摩根大通八模块，通过后再勾选主页就绪。不要从空页重写，也不要重做已就绪的五家。P0 其余公司与 P1/P2 仍未启动。</td>
</tr>
<tr>
<td>额度上限规则落地</td>
<td>旧账号已完成（30% / 眠语不限；废止 ≥95%）</td>
<td>规则已写入新账号共享用户记忆。自动半小时巡检按用户要求未重建</td>
<td>不必重开规则讨论。用户若恢复巡检，再创建半小时例程即可。</td>
</tr>
<tr>
<td>重大事件 / 数字人民币简报</td>
<td>发布任务已完成，页已发布（检索截止 2026-11-07）</td>
<td>未新建第二份简报，未覆盖原页。未见独立每日例程</td>
<td>若需继续完善，在原页增量并先确认是否设例程。</td>
</tr>
<tr>
<td>美国中期选举监控</td>
<td>简报已发布，11-09 有例程增量</td>
<td>每日约 08:45 例程已创建，待 11-12 首次实跑</td>
<td>在原简报页增量，不另建页。</td>
</tr>
<tr>
<td>Skills 待入库 / 待补全</td>
<td>2 包待 push；5 项待补全 slug 未知；四条例程曾被暂停</td>
<td>相关每日例程已重建，但私有仓仍不可访问；本机交接目录已丢失</td>
<td>用户先授予 GitHub App 访问权，再只读核对 HEAD 与是否已入库，然后补全或提交。</td>
</tr>
<tr>
<td>GFR P1 / P2</td>
<td>未启动</td>
<td>未开工；容器复用</td>
<td>P0 验收完成后再启动，不提前另建库。</td>
</tr>
<tr>
<td>睡眠经济八章调研报告</td>
<td>用户回忆项目</td>
<td>工作区未找到报告或定期更新例程。眠语是另一个已完成的产品/IP 项目</td>
<td>不设每日任务，不重开八章项目，除非用户另有来源。</td>
</tr>
<tr>
<td>中文日报缺页</td>
<td>最后完整日为 2026-11-09</td>
<td>08:00 例程已创建，待 11-12 起续写当日页</td>
<td>在既有「每日简报」容器下按日新增，不补造已缺失日期的「伪历史」页，除非用户要求补采。</td>
</tr>
</table>

---

## F. 恢复日志

所有时间均为 Asia/Shanghai。

<table fit-page-width="true" header-row="true">
<tr color="gray_bg">
<th>时间</th>
<th>操作</th>
<th>结果 / 验证</th>
<th>问题</th>
</tr>
<tr>
<td>2026-11-11 约 22:00–22:28</td>
<td>第一阶段考古：检索授权 Notion 工作区（CMQ’s Space）全部私人顶层项；查询发布任务 14 条、BOT总结性汇报 137 条、重大事件 3 条、公司主库 6 家；尝试列出并打开 GitHub 账号 Mingqi-Cai 的仓库</td>
<td>写成清单文件（仅在执行机，非本页）：`/workspace/old-grok-recovery/phase1-inventory.md`。本阶段当时未改任何 Notion 历史页、未 commit</td>
<td>GitHub App 看不到私有仓；本机无历史工作目录；12:00/12:15 无配置证据；行业任务书 34 vs 35 全文未找到</td>
</tr>
<tr>
<td>2026-11-11 晚间（父代理执行恢复）</td>
<td>按用户决定解除 11-09 停令；按历史名称创建 16 个 CMQ Bot；将额度规则写入共享用户记忆；在主 bot 上创建 8 条每日例程（含周末、Asia/Shanghai、灵活触发）</td>
<td>Bot 16 个已创建。例程 8 条配置成功，工具回报下次运行均在 2026-11-12（08:10、08:24、08:58、10:11、21:06、21:18、21:38、22:14）。<b>尚未做第一次真实跑批</b>，不能仅凭配置页面认定执行成功</td>
<td>GitHub 相关例程仍会因仓授权失败。国际日报从试验产线升级为每日例程，属用户明确授权后的恢复，而非旧账号已稳定运行的 08:00 cron</td>
</tr>
<tr>
<td>2026-11-11（用户指示）</td>
<td>用户要求：「每30分钟查一次 notion 这个任务先暂停」；并已先决定不创建 11-14 17:20 一次性续跑、不创建无证据的 12:00/12:15</td>
<td>半小时例程未创建；11-14 续跑未创建；12:00/12:15 未创建</td>
<td>沟通中心自动轮询与额度快照暂缺；额度规则目前只存在于共享记忆，没有半小时自动执行器</td>
</tr>
<tr>
<td>2026-11-11 22:41</td>
<td>为写入本档案，只读复核 <mention url="https://app.notion.com/p/411340bcc39681248c2cd11306cff505">摩根大通</mention> 页（未编辑）</td>
<td>确认八模块正文已在，状态为「待CIO抽检」，主页就绪仍为否。据此更新续跑点，不再写「空页待写满」</td>
<td>该公司库 SQL 复核因 Notion「Query Data Source」额度用尽未执行，改用单页 fetch。未改该页</td>
</tr>
<tr>
<td>2026-11-11 约 23:10</td>
<td>在授权工作区新建本页《旧 Grok 账号工作流恢复总档案》，作为私人顶层新页；不嵌套在每日简报、全球金融研究或眠语容器内</td>
<td>本页创建成功即完成本步。创建过程只新增这一页</td>
<td>例程实跑验证留待 11-12；Skills 文件树仍待 GitHub 授权</td>
</tr>
</table>

### 仍待验证（不能提前标「恢复成功」）

1. 8 条例程能否在指定时区准时启动，并完整跑完。
2. 日报、国际日报、中期选举增量是否写回既有 Notion 位置、格式是否仍为事实 only + 原分类口径。
3. GitHub 授权后：读仓、去重、补全五项未知 slug、2 包是否需入库、提交是否成功。
4. 失败时是否留下真实收口，而不是静默失败。
5. 是否出现重复触发或循环触发（尤其 21:00 / 21:10 / 21:30 / 22:05 四条相近例程）。

### 仍未完成或无法恢复

- 私有仓文件树与五项待补全名单
- 旧例程 UUID 与旧账号记忆（只能重建，不能迁回）
- 半小时沟通中心例程（用户暂停）
- 11-14 17:20 一次性续跑（用户不创建）
- 12:00 / 12:15（无历史配置证据）
- 八章睡眠经济报告（未找到）
- 行业「任务书临时清单」全文（34 vs 35）
- ChatGPT 本机桥接及 7 个未建专业 Bot
- GFR P1/P2 未启动

本页为新建档案，不替代、不修改上述任何历史页面或数据库。
