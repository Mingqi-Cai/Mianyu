# 被丢掉或未纳入的链接及原因

核验时点：2026-11-13 00:45–00:50（Asia/Shanghai，UTC+8）。详细命令与状态码见 `verification-log.md`。

## 一、已打开但不符合「完整创业比赛/早期创业 BP 或路演」标准

| 名称或来源 | 链接 | 原因 |
| --- | --- | --- |
| 茅台学院「第七届中国国际互联网+全国金奖-陈昊」PDF | https://mtxy.edu.cn/visit/1cf7016bfb758a07246329c7187672aa84c40a497da4108b10726a651230f58c.pdf | HTTP 200，PDF，3,013,573 字节，**仅 1 页**，标题为「1-1高教金奖」，属奖状/展示单页，不是完整 BP。 |
| 南昌航空大学「互联网+项目计划书（全）」页及附件图 | 页面 https://csc.nchu.edu.cn/xzzx/hlw/content_85505 ；图 https://csc.nchu.edu.cn/upload/cxcy/contentmanage/article/file/2020/06/11/“互联网”大学生创新创业大赛项目计划书（全）(1)_new.png | 页面 HTTP 200，但无 PDF/PPT 直链；附件为 PNG（118,625 字节）。不能标为已核验完整文件。 |
| CourierKyn《挑战杯项目规划.pdf》 | https://raw.githubusercontent.com/CourierKyn/challenge-cup/master/%E6%8C%91%E6%88%98%E6%9D%AF%E9%A1%B9%E7%9B%AE%E8%A7%84%E5%88%92.pdf | HTTP 200，约 140 KB PDF，但加密，`pdfinfo` 报 Incorrect password，无法阅读。 |
| dlu-edu《plan.doc》（挑战杯辽宁省二等奖，仓库自述） | https://raw.githubusercontent.com/dlu-edu/Venture-Contest/master/plan.doc | HTTP 200，1,588,736 字节，但是 `.doc`，不符合本轮文件类型标准。 |
| zhongrongzhao 仓库「互联网+项目模板.docx」 | https://github.com/zhongrongzhao/-Internet-plus-students-innovation-and-Entrepreneurship-Competition | 仓库只有模板 DOCX，不是填好的真实项目 BP。 |
| 哈尔滨理工大学挑战杯「创业（商业）计划书」PDF | https://youth.hrbust.edu.cn/_upload/article/files/6c/21/5eaa2efc4cd0b624bfe189a9ad55/5f2d6ae0-a2e9-47f1-899b-76633e915ffe.pdf | 检索摘要显示为带占位符的参考模板；本轮 curl 失败（http_code=000）。即使可打开也不应作为真实项目 BP。 |
| Airbnb 种子 deck 教学重建稿（NCSU） | https://sites.ced.ncsu.edu/design-and-pitch/wp-content/uploads/sites/13/2020/05/Pitch-Example-Air-BnB-PDF.pdf | HTTP 200，PDF，12 页，文面为 Business Insider 转 PowerPoint 的教学重建，不完整原件。旧页已判不完整，本轮复测维持。 |
| Airbnb 种子 deck 重建稿（GenPPT） | https://media.genppt.com/pitch-decks/airbnb/airbnb-pitch-deck-2009.pdf | HTTP 200，PDF，11 页，第三方重建，不完整。 |
| KarlHeinrich 仓库中的 PPT 设计模板（科技蓝 / 石破天金 / 蓝白色医疗） | 见 https://github.com/KarlHeinrich-jpg/Business-Plan-and-PPT 的 `ppt模板/` 目录 | 视觉模板，不是真实项目 BP/路演。 |
| 武汉传媒学院、四川大学、内蒙古师范大学、兰州理工等「商业计划书参考模板」 | 例如 http://cxcyxy.whmc.edu.cn/info/1091/2592.htm 、https://jwc.scu.edu.cn/__local/9/9C/67/0185A06B4C4868922989B61B0FB_2321F471_18DF03.pdf 等 | 「怎么写 BP」或空白/示范提纲，不是真实项目完整稿。 |

## 二、类型排除：招股书、年报、监管演示、普通企业介绍（旧页已有，本轮不再包装成比赛 BP）

旧页 https://app.notion.com/p/416340bcc39681dea02bc9cc1467fd08 已定稿，必须保留不覆盖。下列文件在旧页中或曾作为范本，**本轮按纠正口径一律不进入新筛选清单、也不进入推荐**：

- 泡泡玛特港交所招股书（中英文 PDF）
- Casper Sleep、Airbnb、Funko、Bilibili、名创优品等 Form 424B4
- Sonder 投资者/交易演示（SEC HTML 幻灯）

Airbnb 种子轮 14 页原件本轮仍未找到；仅有上述不完整重建稿。Buffer 种子 deck 因属于真实早期创业路演、且完整可开，按新标准重新评估后进入 **B 类筛选**（英文补充），但不进入深入研究推荐。

11-07 财务底稿页 https://app.notion.com/p/411340bcc396814a9b16de9c7b11419c 不是范本，本轮未改。

## 三、需登录、付费、网盘或仅有目录/新闻，不得标为已核验完整文件

- 百度文库、豆丁、道客巴巴、人人文库、原创力文档、夸克文档上的「文创 IP / 夜间经济 / 旅游创业计划书」等：预览或 VIP，无可靠全文直链。
- 给力资源网、哇哈网盘、经管之家资源帖、B 站「国奖计划书+PPT 资料包」、飞书分享帖等：网盘/付费合集，无本轮可直接打开的公开 PDF。
- 教育部或省赛「获奖名单」PDF、高校金奖新闻稿：名单或报道，不是项目 BP。
- 常州大学「征集国赛金奖项目素材」通知：是内部征集，不附已公开 BP。
- mikenote/homekeeping 等仓库：计划书指向蓝奏网盘，不是可直接核验的公开 PDF。

## 四、待浏览器核验（本执行环境无浏览器，不猜测内容）

下列地址有希望或页面存在，但本轮无法在无浏览器条件下确认「完整可下载的 BP 原件」，故不进筛选清单：

- 南昌航空大学下载中心相关栏目（若页面另有需登录或动态加载的附件）：https://csc.nchu.edu.cn/xzzx/hlw/content_85505 及其挑战杯栏目 https://csc.nchu.edu.cn/xzzx/tzbcyjh/content_88146
- Front Series A 官方博文与 SlideShare 嵌入页（旧页曾记 SlideShare 为 Challenge 页、Medium 403）：https://front.com/blog/inside-fronts-series-a-slide-deck 、https://www.slideshare.net/slideshow/front-series-a-deck-64596550/64596550
- 山东理工大学同一「作品参考」页上的 ZIP / PPTX（本轮只核验了其中一份直链 PDF「竞赛云」；ZIP 内是否还有完整 BP 需解压前先下载并逐份核验，本轮未拆包以免把未读文件算进清单）：https://jxxy.sdut.edu.cn/2019/0404/c4331a279022/page.htm
- 各类文库/网盘详情页，若后续改用浏览器仍须找到直链 PDF/PPT 并做同样 curl 核验，才能升级为「已核验」。

## 五、检索中见到但明确不采用的信息

- 仓库或路演中团队「自述金奖/特等奖/市赛奖」：未经赛事官网或高校获奖公示交叉核验的，评价中不得写成已证实奖项。
- 遥智边疆书面计划书「图目录」与主题不符的条目：作为质量局限记录，不因此把文件改称为「假文件」，但也不掩盖问题。
