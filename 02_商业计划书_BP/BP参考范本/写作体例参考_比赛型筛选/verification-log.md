# 核验日志

核验时点：2026-11-13 00:45–00:50（Asia/Shanghai，UTC+8）。  
方法：对原始文件链接用 `curl` 实测 HTTP 状态、Content-Type、下载字节数；PDF 用 `pdfinfo` 核对页数；PPTX 用文件魔数与内部 `ppt/slides/slideN.xml` 统计幻灯页数，并抽取幻灯可见文字以确认是完整路演稿而非空模板。部分站点声明式 User-Agent 为 `Mozilla/5.0` 或 Chrome 兼容 UA。  
判定规则：只有 HTTP 200 且确认为可直接阅读的完整 PDF / PPT / PPTX（或完整 HTML 幻灯）的创业项目型 BP 或赛事路演，才进入筛选清单。招股书、年报、研报、普通企业介绍、教程/空白模板、仅封面或证书、需登录/付费才能看全文、目录页无直链、密码保护无法打开、不完整重建稿，一律不进筛选清单。第三方转存须在记录中标明。

---

## 一、进入筛选清单的已核验文件

### 1. 探旅中轴（PPT + 计划书终版，合订 PDF）

- **为何判定是真正创业比赛 BP/路演，而不是招股书/年报/研报/简介**：文面首页为「青创北京」2025 年「挑战杯」「青砺基层」专项赛；前半为路演幻灯（政策/行业背景、调研、痛点、解决方案、核心技术、小程序、商业模式、营销、竞品、财务与融资、团队、展望），后半为带完整「目录」的书面计划书（第一至十章另加附录）。不是监管披露文件，也不是一页封面或新闻稿。
- **URL（干净原始文件链接）**：https://raw.githubusercontent.com/KarlHeinrich-jpg/Business-Plan-and-PPT/main/%E6%8E%A2%E6%97%85%E4%B8%AD%E8%BD%B4ppt%2B%E8%AE%A1%E5%88%92%E4%B9%A6%E7%BB%88%E7%89%88.pdf
- **来源说明**：GitHub 仓库 https://github.com/KarlHeinrich-jpg/Business-Plan-and-PPT （仓库 README 称为「完整项目案例」之一）。**第三方汇编/转存，非挑战杯官网或高校官方首发件。**
- **命令与结果**：
  - `curl -sL`：HTTP 200，`Content-Type: application/octet-stream`，下载 23,964,711 字节。
  - `pdfinfo`：PDF，110 页，Producer/Creator 标为 PPDDFF，未加密。
- **完整性**：通过。可提取书面计划书完整目录；路演部分部分图表为图片，文字层有缺失，但不影响确认是完整合订稿。
- **是否转存**：是（第三方 GitHub）。本地副本：`files/探旅中轴-ppt与计划书终版.pdf`。
- **结论**：通过，列入筛选清单 A 类（兼作 C/文旅体验参考）。

### 2. 辛庄「研」选，「莓」好童行（校赛合订 PDF）

- **为何判定是真正创业比赛 BP/路演**：文面首页为「青创北京」2026 年「挑战杯」首都大学生创业计划竞赛——「揭榜挂帅」机制专项赛，参赛赛道「青砺基层」社会治理专项赛，选题「榜单18—探索兴寿镇辛庄村多元业态发展」；文件名标明「校赛」。前半路演、后半书面计划书（第一至九章，含商业模式、B/C 端收入、财务、风险、团队、社会价值）。不是招股书或简介。
- **URL**：https://raw.githubusercontent.com/KarlHeinrich-jpg/Business-Plan-and-PPT/main/%E8%BE%9B%E5%BA%84%E2%80%9C%E7%A0%94%E2%80%9D%E9%80%89%EF%BC%8C%E2%80%9C%E8%8E%93%E2%80%9D%E5%A5%BD%E7%AB%A5%E8%A1%8C%E2%80%94%E2%80%94AI%E8%B5%8B%E8%83%BD%E7%9A%84%E4%BA%B2%E5%AD%90%E7%A0%94%E5%AD%A6%E6%96%87%E6%97%85%E5%AF%BC%E8%A7%88%E5%B9%B3%E5%8F%B0%E6%A0%A1%E8%B5%9B.pdf
- **来源说明**：同上 GitHub 仓库。**第三方汇编/转存，非赛事官网首发。** 文件自身标明为校赛/专项赛选题，本轮未在挑战杯官网交叉核到该项目的获奖公示。
- **命令与结果**：
  - `curl -sL`：HTTP 200，`application/octet-stream`，59,200,973 字节。
  - `pdfinfo`：PDF，113 页，未加密。
- **完整性**：通过。可提取完整书面目录与 B/C 端收入等正文；路演部分同样有图文混排导致的文字层缺失。
- **是否转存**：是。本地副本：`files/辛庄研选-AI赋能亲子研学文旅导览平台-校赛.pdf`。
- **结论**：通过，列入筛选清单 A 类（兼作 C 类 IP/文创参考）。

### 3. 「竞赛云」项目策划（第三届「互联网+」大赛）

- **为何判定是真正创业比赛 BP**：封面与页眉写明「第三届互联网+创新创业大赛」「“竞赛云”项目策划」，主体为淄博中天互联信息科技有限公司；目录含执行概要、公司概况、产品与服务、市场分析、商业模式、竞争分析、财务分析、融资计划及发展战略、风险分析。是项目型书面 BP，不是招股书、年报或教程模板。
- **URL**：https://jxxy.sdut.edu.cn/_upload/article/files/c8/df/7275eae344f583730887e1cf40f4/89d2ad00-5e8e-4123-b50a-6bcabb58d5d7.pdf
- **来源说明**：山东理工大学机械工程学院官方站点「挑战杯互联网+作品参考」列表页 https://jxxy.sdut.edu.cn/2019/0404/c4331a279022/page.htm （页面发布于 2019-04-04；附件 Last-Modified: 2019-04-04）。高校官方转载的参赛/教学参考件，**不是教育部大赛官网首发**；本轮未核到该项目的国赛获奖等级，不以「金奖」称呼。
- **命令与结果**：
  - `curl -sI` / `curl -sL`：HTTP 200，`Content-Type: application/pdf`，`Content-Length` / 下载 3,756,874 字节。
  - `pdfinfo`：PDF，49 页，Creator: WPS Office，Author: Mac，未加密。
- **完整性**：通过。目录与各章正文可提取。
- **是否转存**：否（高校官网直链）。本地副本：`files/竞赛云-第三届互联网+项目策划.pdf`。
- **结论**：通过，列入筛选清单 A 类。

### 4. 遥智边疆（路演 + 书面计划书合订 PDF）

- **为何判定是真正创业比赛 BP/路演**：首页为「青创北京」2026 年「挑战杯」首都大学生创业计划竞赛，赛道「青智未来」；前 16 页为路演幻灯，自约第 17 页起为书面「计划书」完整目录（第一至十二章）。不是招股书或一页证书。需同时记下质量问题：书面部分「图目录」出现「上海洪水易发性区位图」「SHAP value」等与边疆遥感主题明显不符的条目，存在模板残留或拼装痕迹，但不改变「这是一份赛事计划书合订稿」的文件类型判断。
- **URL**：https://raw.githubusercontent.com/KarlHeinrich-jpg/Business-Plan-and-PPT/main/581002-%E9%81%A5%E6%99%BA%E8%BE%B9%E7%96%86%E2%80%94%E2%80%94%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0_%E6%84%9F%E8%A7%A3%E8%AF%91%E5%B9%B3%E5%8F%B0-%E9%A1%B9%E7%9B%AE%E4%BD%9C%E5%93%81-89b09fad%20(1).pdf
- **来源说明**：同上 GitHub 仓库。**第三方汇编/转存。** 文中负责人作「XXX」脱敏。仓库另提供书面预览版（见下条），不另计一份范本。
- **命令与结果**：
  - `curl -sL`：HTTP 200，`application/octet-stream`，19,574,991 字节。
  - `pdfinfo`：PDF，88 页，未加密。
- **完整性**：通过（合订完整可打开）。质量瑕疵见上，评价时须写明。
- **是否转存**：是。本地副本：`files/遥智边疆-深度学习与群智能遥感解译平台-项目作品.pdf`。
- **结论**：通过，列入筛选清单 A 类。

### 4b. 遥智边疆书面计划书预览版（同一项目，不单独计入筛选条数）

- **URL**：https://raw.githubusercontent.com/KarlHeinrich-jpg/Business-Plan-and-PPT/main/%E5%8F%AF%E7%BC%96%E8%BE%91%E7%89%88%E6%9C%AC%E6%A8%A1%E6%9D%BF/%E9%A1%B9%E7%9B%AE%E5%8D%81%E4%B8%89-pdf.pdf
- **命令与结果**：HTTP 200，`application/octet-stream`，2,668,721 字节；`pdfinfo`：PDF，73 页，Creator/Producer: Microsoft Word 2021。封面为「遥智边疆……计划书」，赛道组别「青智未来」，负责人「xxx」。
- **结论**：作为第 4 项的书面版对照件保留，不另开筛选序号。本地副本：`files/遥智边疆-商业计划书预览版.pdf`。

### 5. 地脉灵犀（路演 PPTX）

- **为何判定是真正创业比赛路演，而不是空模板或招股书**：PPTX 内 18 页幻灯首页为「地脉灵犀」「青创北京」2026 年「挑战杯」首都大学生创业计划竞赛，赛道「青智未来」，副题「多尺度天空地一体化地貌智能监测预警系统」；后续为痛点、方案、技术、应用验证、社会价值、团队、展望。是赛事路演稿。书面计划书在同一仓库中为 `.docx`（约 40 页，仓库 README 自称），**本轮筛选标准不接受 DOC/DOCX 作为「已核验完整文件」，故书面版未列入筛选清单**。本项仅作为完整路演 PPTX 收录。18 页中未见完整的收入模型/融资页，商业论证弱于书面 BP。
- **URL**：https://raw.githubusercontent.com/KarlHeinrich-jpg/Business-Plan-and-PPT/main/%E5%8F%AF%E7%BC%96%E8%BE%91%E7%89%88%E6%9C%AC%E6%A8%A1%E6%9D%BF/%E9%A1%B9%E7%9B%AE14PPT5.10.pptx
- **来源说明**：同上 GitHub。**第三方汇编/转存。** 团队与指导教师信息部分脱敏；文中自述竞赛经历未经官网交叉核验，评价时不得当成已证实奖项。
- **命令与结果**：
  - `curl -sL`：HTTP 200，`application/octet-stream`，72,955,966 字节。
  - 文件魔数 `PK\x03\x04`（ZIP/OOXML）；内部 `ppt/slides/slide1.xml`–`slide18.xml` 共 18 页，可提取全文。
- **完整性**：路演 PPTX 完整可打开；书面 BP 因格式不符未核验进清单。
- **是否转存**：是。本地副本：`files/地脉灵犀-青创北京2026挑战杯路演PPT.pptx`。
- **结论**：通过（仅路演），列入筛选清单 A 类，不作深入研究首推。

### 6. Buffer Seed Pitch Deck（早期融资路演）

- **为何判定是真正早期创业路演，而不是招股书或简介**：这是 Buffer 创始团队后来公开的约 2011 年种子轮融资幻灯（2013 年发博说明）。13 页完整 PDF，主题为产品、牵引、商业模式与融资，属于早期创业 deck。行业是社交媒体内容排期工具，不是大学生比赛 BP。官方入口是博文而非文件首发站；可通读的 PDF 为第三方转存。
- **官方博文（文章，不是独立完整文件）**：https://buffer.com/resources/the-slide-deck-we-used-to-raise-half-a-million-dollars/  
  `curl -sI`（声明式 UA）：HTTP 200，`text/html; charset=utf-8`。
- **已核验完整 PDF（须标明非官方转存）**：https://southfloridainvestorsocialclub.com/wp-content/uploads/2025/01/buffer-seed-round-deck-130506180753-phpapp01.pdf
- **命令与结果**：
  - `curl -sI` / `curl -sL`：HTTP 200，`Content-Type: application/pdf`，6,584,037 字节。
  - `pdfinfo`：13 页；Creator: Apple Keynote 5.3；Producer: Mac OS X 10.8.2 Quartz PDFContext；CreationDate: 2013-05-07 05:34:48 CST。与旧页记录一致，本轮复测仍通过。
- **完整性**：通过（13 页完整 deck）。
- **是否转存**：是（第三方站点）。本地副本：`files/Buffer-seed-round-deck.pdf`。
- **结论**：通过，列入筛选清单 B 类；英文补充，不进入 3—5 份深入研究推荐。

---

## 二、已实测但未通过 / 不进入筛选清单的记录

（详见 `rejected.md`，此处保留核验数据。）

### 茅台学院「第七届中国国际互联网+全国金奖-陈昊」附件

- 列表页：https://mtxy.edu.cn/xzbm/jwc/sjjx/xkjs704/20240313/20240313_678304.shtml （HTTP 200，HTML）
- 文件：https://mtxy.edu.cn/visit/1cf7016bfb758a07246329c7187672aa84c40a497da4108b10726a651230f58c.pdf
- `curl -sI`：HTTP 200，`Content-Type: application/pdf;charset=UTF-8`，`Content-Length: 3013573`。
- 下载 3,013,573 字节。`pdfinfo`：**仅 1 页**，Title「1-1高教金奖」，Creator: CorelDRAW，CreationDate: 2022-05-07。是奖状/展示单页，不是完整 BP。**舍弃。**

### 南昌航空大学「互联网+项目计划书（全）」

- 页面 https://csc.nchu.edu.cn/xzzx/hlw/content_85505 ：HTTP 直连 `http` 得到空响应；`https` `curl -sL` 为 HTTP 200，31,258–34,261 字节 HTML。正文未见 PDF/DOC 附件，仅见图片：https://csc.nchu.edu.cn/upload/cxcy/contentmanage/article/file/2020/06/11/“互联网”大学生创新创业大赛项目计划书（全）(1)_new.png
- 该 PNG：`curl -sI` HTTP 200，`Content-Type: image/png`，`Content-Length: 118625`。不是可直接阅读的完整 PDF/PPT。**不进筛选清单**（未完全核验全文）。

### CourierKyn / 挑战杯项目规划.pdf

- https://raw.githubusercontent.com/CourierKyn/challenge-cup/master/%E6%8C%91%E6%88%98%E6%9D%AF%E9%A1%B9%E7%9B%AE%E8%A7%84%E5%88%92.pdf
- HTTP 200，`application/octet-stream`，139,982 字节，文件头 `%PDF-1.6`。
- `pdfinfo` / `pdftotext`：**Incorrect password**，无法打开阅读。**舍弃。**

### dlu-edu / Venture-Contest `plan.doc`

- https://raw.githubusercontent.com/dlu-edu/Venture-Contest/master/plan.doc
- HTTP 200，`application/octet-stream`，1,588,736 字节。仓库说明为挑战杯辽宁省二等奖。
- 格式为 `.doc`，不符合本轮「PDF 或 PPT/PPTX/完整 HTML 幻灯」标准。**不进筛选清单**，记入缺口/未纳入。

### zhongrongzhao / 互联网+项目模板.docx

- 仓库页 HTTP 200：https://github.com/zhongrongzhao/-Internet-plus-students-innovation-and-Entrepreneurship-Competition
- 可见文件为「互联网+项目模板.docx」，是模板不是填好的项目 BP。**舍弃。**

### 哈尔滨理工大学「挑战杯创业（商业）计划书」PDF

- https://youth.hrbust.edu.cn/_upload/article/files/6c/21/5eaa2efc4cd0b624bfe189a9ad55/5f2d6ae0-a2e9-47f1-899b-76633e915ffe.pdf
- 检索摘要显示为带占位符的参考模板。本轮 `curl -sL` 对该 URL **失败（http_code=000，0 字节）**，未能复测页数。按「未通过核验」处理，且即使可打开也属模板，不进筛选。

### Airbnb 种子 deck 重建稿（旧页已判不完整，本轮复测）

1. https://sites.ced.ncsu.edu/design-and-pitch/wp-content/uploads/sites/13/2020/05/Pitch-Example-Air-BnB-PDF.pdf  
   HTTP 200，`application/pdf`，862,121 字节，**12 页**，文面为教学用重建稿，不足典型引述的 14 页原件。**不进筛选。**
2. https://media.genppt.com/pitch-decks/airbnb/airbnb-pitch-deck-2009.pdf  
   HTTP 200，`application/pdf`，4,509,019 字节，**11 页**，Title 自称 Airbnb Pitch Deck (2009)，属第三方重建。**不进筛选。**

### 旧页中的招股书 / 年报 / 投资者演示（本轮不再作为比赛 BP 推荐，也不进入新筛选清单）

以下链接在旧页已核验为完整监管文件或路演，但类型不符合本轮口径，本轮不重复下载，仅登记「类型排除」：

- 泡泡玛特 HKEX 招股书（中英文 PDF）
- Casper / Airbnb / Funko / Bilibili / 名创优品 Form 424B4（SEC HTML）
- Sonder 投资者演示 HTML（SEC，图像幻灯）

### 其他检索命中但未当作已核验完整文件的来源

- 百度文库、豆丁、道客巴巴、人人文库、原创力文档、夸克文档等：预览页或需登录/付费，**不得标为已核验可直接阅读的完整文件**。
- 网盘合集页（如 gforce.com.cn、waha.cc、经管之家资源帖、B 站「国奖资料包」）：无公开直链 PDF，或为收费/网盘。
- 大量高校「计划书模板 / 参考模板」页面（武汉传媒学院、四川大学、内蒙古师范大学、兰州理工等）：是写作模板，不是真实项目 BP。
- 茅台学院金奖新闻页本身、教育部获奖名单 PDF：名单或证书，不是项目 BP。

---

## 三、命令备忘（本轮实际使用的核心命令形态）

```bash
curl -sI -A "Mozilla/5.0 ..." --max-time 20 "<URL>"
curl -sL -A "Mozilla/5.0 ..." --max-time 60 -o <file> -w "http_code=%{http_code} content_type=%{content_type} size=%{size_download}\n" "<URL>"
pdfinfo <file>
pdftotext -layout -f 1 -l 12 <file> -
# PPTX：检查 PK 魔数，枚举 ppt/slides/slideN.xml
```

未使用浏览器。需浏览器才能确认全文的条目已列入「待浏览器核验」，不猜测内容。
