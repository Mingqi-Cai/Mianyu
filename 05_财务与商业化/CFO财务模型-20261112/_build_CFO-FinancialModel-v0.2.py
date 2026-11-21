#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build 眠语财务模型 v0.2.

另存交付，不覆盖 v0.1 的 xlsx、测算说明或 _build_CFO-FinancialModel-v0.1.py。
不改 00-统一参数口径-20261112.md，不改 Notion。
唯一输入在参数台；关键结果为 Excel 公式（英语函数名、逗号分隔）。
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.comments import Comment
from pathlib import Path

OUT_XLSX = Path("/workspace/mianyu-cfo/CFO-FinancialModel-眠语财务模型v0.2-20261112.xlsx")

THIN = Border(
    left=Side(style="thin", color="B0B0B0"),
    right=Side(style="thin", color="B0B0B0"),
    top=Side(style="thin", color="B0B0B0"),
    bottom=Side(style="thin", color="B0B0B0"),
)
FILL_HEADER = PatternFill("solid", fgColor="1F4E79")
FILL_SECTION = PatternFill("solid", fgColor="2E75B6")
FILL_INPUT = PatternFill("solid", fgColor="FFF2CC")
FILL_FORMULA = PatternFill("solid", fgColor="DDEBF7")
FILL_PENDING = PatternFill("solid", fgColor="F8CBAD")
FILL_GAP = PatternFill("solid", fgColor="FCE4D6")
FILL_NOTE = PatternFill("solid", fgColor="E2EFDA")
FILL_TITLE = PatternFill("solid", fgColor="0D1B2A")
FILL_WHITE = PatternFill("solid", fgColor="FFFFFF")
FILL_GREY = PatternFill("solid", fgColor="F2F2F2")
FILL_PURPLE = PatternFill("solid", fgColor="E2D5F1")
FILL_REF = PatternFill("solid", fgColor="DEEBF7")

FONT_WHITE = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
FONT_WHITE_LG = Font(name="Calibri", bold=True, color="FFFFFF", size=16)
FONT_TITLE = Font(name="Calibri", bold=True, size=14, color="1F4E79")
FONT_H = Font(name="Calibri", bold=True, size=11, color="1F4E79")
FONT_N = Font(name="Calibri", size=10)
FONT_B = Font(name="Calibri", size=10, bold=True)
FONT_SM = Font(name="Calibri", size=9, italic=True, color="666666")
FONT_WARN = Font(name="Calibri", size=10, bold=True, color="C65911")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)

YUAN = "#,##0"
YUAN2 = "#,##0.00"
WAN = "0.000"
PCT = "0.00%"

SRC_COST = (
    "已验收 Cost：CFO-Cost-成本拆分-20261112.xlsx；"
    "CFO-验收与裁决-COST-20261112.md；"
    "统一口径 / 2026-11-07 Notion 定稿页（只读）"
    "https://app.notion.com/p/411340bcc396814a9b16de9c7b11419c"
)
SRC_REV = (
    "已验收 Revenue：CFO-Revenue-收入测算准备-20261112.xlsx；"
    "CFO-验收-REV-20261112.md"
)
SRC_BENCH = (
    "已复验通过 Benchmark v1.1：CFO-Benchmark-行业基准-20261112-v1.1.xlsx；"
    "CFO-验收-BENCH-v1.1-20261112.md（禁止引用第一版分项或已作废中值差）"
)
SRC_MODEL = (
    "CFO-验收与裁决-MODEL-v0.1-20261112.md；"
    "CFO-验收-AUDIT-MODEL-v0.1-20261112.md（同意有条件通过，展示层交 v0.2 修正）"
)
DATE_EST = "估算日 2026-11-07"
DATE_NOW = "2026-11-12"
NATURE_EST = "已有底稿估算 / 待询价"
CALIBER_ONEOFF = "CNY 元；一次性；含税口径未拆，待询价，非合同价，非用户已锁定；期间云与认证年费不计入一次性打包"
SCOPE_A = "A 当前 Demo"


def style_header_row(ws, row, start, end):
    for col in range(start, end + 1):
        c = ws.cell(row, col)
        c.fill = FILL_HEADER
        c.font = FONT_WHITE
        c.alignment = CENTER
        c.border = THIN


def style_input(c, num=False, fmt=None):
    c.fill = FILL_INPUT
    c.font = FONT_N
    c.alignment = CENTER if num else LEFT
    c.border = THIN
    if num:
        c.number_format = fmt or YUAN


def style_formula(c, num=True, pending=False, fmt=None):
    c.fill = FILL_GAP if pending else FILL_FORMULA
    c.font = FONT_N
    c.alignment = CENTER
    c.border = THIN
    if num:
        c.number_format = fmt or YUAN


def style_text(c, fill=None):
    c.fill = fill or FILL_GREY
    c.font = FONT_N
    c.alignment = LEFT
    c.border = THIN


def style_pending_empty(c):
    c.fill = FILL_PENDING
    c.font = FONT_N
    c.alignment = CENTER
    c.border = THIN


def section_bar(ws, row, text, start=1, end=8):
    ws.merge_cells(start_row=row, start_column=start, end_row=row, end_column=end)
    c = ws.cell(row, start, text)
    c.fill = FILL_SECTION
    c.font = FONT_WHITE
    c.alignment = LEFT
    for col in range(start, end + 1):
        ws.cell(row, col).fill = FILL_SECTION
        ws.cell(row, col).border = THIN
        ws.cell(row, col).font = FONT_WHITE


def cur_lo(c, e, g):
    return f'=IF($C$3="精益",{c},IF($C$3="基准",{e},IF($C$3="完整",{g},"")))'


def cur_hi(d, f, h):
    return f'=IF($C$3="精益",{d},IF($C$3="基准",{f},IF($C$3="完整",{h},"")))'


def if_blank(src):
    """Keep a blank source blank (do not coerce empty to 0)."""
    return f'=IF({src}="","",{src})'


def product2(a, b):
    return f'=IF(COUNT({a},{b})<2,"",{a}*{b})'


def product3(a, b, c):
    return f'=IF(COUNT({a},{b},{c})<3,"",{a}*{b}*{c})'


def sum_if_any(*cells):
    listed = ",".join(cells)
    return f'=IF(COUNT({listed})=0,"",SUM({listed}))'



def set_widths(ws, widths):
    for col, w in widths.items():
        ws.column_dimensions[col].width = w


def build_params(wb):
    ws = wb.active
    ws.title = "01_参数台"
    ws.sheet_properties.tabColor = "1F4E79"
    ws.freeze_panes = "A10"
    ws.row_dimensions[1].height = 22
    set_widths(ws, {
        "A": 16, "B": 46, "C": 14, "D": 14, "E": 14, "F": 14,
        "G": 14, "H": 14, "I": 14, "J": 14, "K": 14, "L": 42,
        "M": 36, "N": 28, "O": 28, "P": 22, "Q": 22,
    })

    ws.merge_cells("A1:Q1")
    ws["A1"] = "眠语财务模型 v0.2 · 参数台（全部可调输入集中本表；请勿在其他表改数）"
    ws["A1"].font = FONT_WHITE_LG
    ws["A1"].fill = FILL_TITLE
    ws["A1"].alignment = LEFT
    for col in range(1, 18):
        ws.cell(1, col).fill = FILL_TITLE
        ws.cell(1, col).font = FONT_WHITE_LG

    ws.merge_cells("A2:Q2")
    ws["A2"] = (
        "单号 CFO-20261112-MODEL-v0.2｜财务准备 / 非正式 BP｜默认展示档=基准（旧稿建议首选，用户尚未锁定）｜"
        "已并入已验收 Cost / Revenue / Benchmark v1.1｜改 C3/C4/C5 或黄色输入格，成本、现金流、盈亏平衡随公式联动｜"
        "空参数保持空白，不以 0 冒充已测算"
    )
    ws["A2"].font = FONT_WHITE
    ws["A2"].fill = FILL_SECTION
    ws["A2"].alignment = LEFT
    for col in range(1, 18):
        ws.cell(2, col).fill = FILL_SECTION

    # ---- controls ----
    ws["A3"] = "当前档位"
    ws["A3"].font = FONT_B
    ws["C3"] = "基准"
    style_input(ws["C3"], num=False)
    ws.merge_cells("D3:Q3")
    ws["D3"] = "待确认：用户尚未锁定档位。三档均可切换，不得视为已定案。"
    ws["D3"].font = FONT_SM

    ws["A4"] = "完整档是否含02可选"
    ws["A4"].font = FONT_B
    ws["C4"] = "否"
    style_input(ws["C4"], num=False)
    ws.merge_cells("D4:Q4")
    ws["D4"] = "默认不含。H4：02/04 不进精益/基准；完整为可选。纳入后分项求和可能高于旧稿头条，但不得自动抬高头条（已裁决）。"
    ws["D4"].font = FONT_SM

    ws["A5"] = "完整档是否含04可选"
    ws["A5"].font = FONT_B
    ws["C5"] = "否"
    style_input(ws["C5"], num=False)
    ws.merge_cells("D5:Q5")
    ws["D5"] = "默认不含。同上。"
    ws["D5"].font = FONT_SM

    dv_tier = DataValidation(type="list", formula1='"精益,基准,完整"', allow_blank=False)
    dv_tier.error = "请选择 精益 / 基准 / 完整"
    dv_tier.errorTitle = "档位"
    dv_tier.prompt = "选择当前测算档位"
    dv_tier.showDropDown = False
    ws.add_data_validation(dv_tier)
    dv_tier.add(ws["C3"])

    dv_yn = DataValidation(type="list", formula1='"是,否"', allow_blank=False)
    dv_yn.error = "请选择 是 / 否"
    dv_yn.errorTitle = "开关"
    dv_yn.showDropDown = False
    ws.add_data_validation(dv_yn)
    dv_yn.add(ws["C4"])
    dv_yn.add(ws["C5"])

    ws["A6"] = "货币"
    ws.merge_cells("C6:Q6")
    ws["C6"] = "CNY 元（表内统一用元；摘要万元=元/10000，为公式；非金额行不换算万元）"
    ws["C6"].font = FONT_N

    ws["A7"] = "控制区说明"
    ws.merge_cells("C7:Q7")
    ws["C7"] = (
        "黄色=输入；蓝色=公式；橙色=待确认/留空；紫底=非现金对照。每一笔数字含来源、口径、适用范围、性质、日期。"
        "差额已裁决：单独列示、禁止衬平、禁止虚拟补差行。官方 19.9 元/月（P-003）只作对照，不改总包。"
    )
    ws["C7"].font = FONT_SM

    # ---- A-stage cost ----
    section_bar(ws, 9, "A. A阶段成本参数（一次性，元；Cost 已验收编码 A01–A08 / PACK / GAP；沿用 2026-11-07 旧稿区间，待询价）", 1, 17)

    headers = [
        "参数ID", "参数名称", "精益_下限", "精益_上限", "基准_下限", "基准_上限",
        "完整_下限", "完整_上限", "当前_下限", "当前_上限", "单位",
        "来源", "口径", "适用范围", "性质", "日期", "待确认",
    ]
    for i, h in enumerate(headers, 1):
        ws.cell(10, i, h)
    style_header_row(ws, 10, 1, 17)

    # rows 11-18 items: (id, name, c,d,e,f,g,h, unit, caliber_extra, scope_extra)
    items = [
        ("A01", "工程包", 12000, 25000, 25000, 50000, 50000, 90000, "元", "", SCOPE_A),
        ("A02", "IP美术（完整档为五皮）", 3000, 8000, 8000, 15000, 35000, 55000, "元", "完整档为五皮，不得把五皮价叠进精益/基准", SCOPE_A),
        ("A03", "UI/UX", 0, 7000, 10000, 20000, 20000, 40000, "元", "精益下沿 0 表示旧稿允许该档不单列规范 UI 外包", SCOPE_A),
        ("A04", "互动文案", 0, 2000, 2000, 6000, 8000, 15000, "元", "精益下沿 0 表示旧稿允许 Bot 补策划文案", SCOPE_A),
        ("A05", "云+认证一次性", 400, 800, 2000, 5000, 5000, 10000, "元", "一次性，不与 Demo 期持续月费/认证年费串口径；与期间费用是否重叠待确认（Cost P6）", SCOPE_A),
        ("A06", "测试", 0, 2000, 4000, 7000, 11000, 23000, "元", "精益下沿允许自测为 0；官方免费时长对照见 P-007/P-008，不改本行", SCOPE_A),
        ("A07", "02可选（仅完整）", 0, 0, 0, 0, 15000, 50000, "元", "仅完整可选，精益/基准为 0（H4）；当前列仅当完整且 C4=是 才纳入分项合计；纳入不得自动抬高头条", "A 当前 Demo；仅完整可选"),
        ("A08", "04可选（仅完整）", 0, 0, 0, 0, 5000, 20000, "元", "仅完整可选，精益/基准为 0（H4）；当前列仅当完整且 C5=是 才纳入；纳入不得自动抬高头条", "A 当前 Demo；仅完整可选"),
    ]
    for i, (pid, name, c, d, e, f, g, h, unit, extra, scope) in enumerate(items):
        r = 11 + i
        ws.cell(r, 1, pid).font = FONT_B
        ws.cell(r, 2, name)
        for col, val in zip(range(3, 9), [c, d, e, f, g, h]):
            ws.cell(r, col, val)
            style_input(ws.cell(r, col), num=True)
        if pid == "A07":
            ws.cell(r, 9, '=IF(AND($C$3="完整",$C$4="是"),G17,0)')
            ws.cell(r, 10, '=IF(AND($C$3="完整",$C$4="是"),H17,0)')
        elif pid == "A08":
            ws.cell(r, 9, '=IF(AND($C$3="完整",$C$5="是"),G18,0)')
            ws.cell(r, 10, '=IF(AND($C$3="完整",$C$5="是"),H18,0)')
        else:
            ws.cell(r, 9, cur_lo(f"C{r}", f"E{r}", f"G{r}"))
            ws.cell(r, 10, cur_hi(f"D{r}", f"F{r}", f"H{r}"))
        style_formula(ws.cell(r, 9))
        style_formula(ws.cell(r, 10))
        ws.cell(r, 11, unit)
        ws.cell(r, 12, SRC_COST)
        cal = CALIBER_ONEOFF + (("；" + extra) if extra else "")
        ws.cell(r, 13, cal)
        ws.cell(r, 14, scope)
        ws.cell(r, 15, NATURE_EST)
        ws.cell(r, 16, DATE_EST)
        ws.cell(r, 17, "是：待询价")
        for col in (1, 2, 11, 12, 13, 14, 15, 16, 17):
            style_text(ws.cell(r, col), FILL_GREY if col not in (1, 2) else FILL_WHITE)
        ws.cell(r, 1).font = FONT_B
        ws.cell(r, 1).border = THIN
        ws.cell(r, 2).border = THIN

    # row 19 SUM-SWITCH
    r = 19
    ws.cell(r, 1, "SUM-SWITCH")
    ws.cell(r, 2, "分项求和（主预算：A01–A06 + 按开关计入的 A07/A08）")
    ws.cell(r, 3, "=SUM(C11:C16)+0")
    ws.cell(r, 4, "=SUM(D11:D16)+0")
    ws.cell(r, 5, "=SUM(E11:E16)+0")
    ws.cell(r, 6, "=SUM(F11:F16)+0")
    ws.cell(r, 7, '=SUM(G11:G16)+IF($C$4="是",G17,0)+IF($C$5="是",G18,0)')
    ws.cell(r, 8, '=SUM(H11:H16)+IF($C$4="是",H17,0)+IF($C$5="是",H18,0)')
    ws.cell(r, 9, "=SUM(I11:I18)")
    ws.cell(r, 10, "=SUM(J11:J18)")
    for col in range(3, 11):
        style_formula(ws.cell(r, col))
    ws.cell(r, 11, "元")
    ws.cell(r, 12, SRC_COST + "；公式结果")
    ws.cell(r, 13, "公式：分项下限/上限分别求和；02/04 仅当完整且开关为「是」时计入；不替代 PACK 头条")
    ws.cell(r, 14, SCOPE_A)
    ws.cell(r, 15, "公式结果（非新估算）")
    ws.cell(r, 16, "跟随分项")
    ws.cell(r, 17, "是：与头条可能有差额")
    for col in (1, 2, 11, 12, 13, 14, 15, 16, 17):
        style_text(ws.cell(r, col))
    ws.cell(r, 1).font = FONT_B

    # row 20 PACK headline — hardcoded alignment, not formula from sum
    r = 20
    ws.cell(r, 1, "PACK")
    ws.cell(r, 2, "旧稿头条一次性合计（与 11-07 底稿硬对齐，验收锚点；不随 02/04 开关抬高）")
    for col, val in zip(range(3, 9), [25000, 55000, 55000, 110000, 110000, 220000]):
        ws.cell(r, col, val)
        style_input(ws.cell(r, col), num=True)
    ws.cell(r, 9, cur_lo("C20", "E20", "G20"))
    ws.cell(r, 10, cur_hi("D20", "F20", "H20"))
    style_formula(ws.cell(r, 9))
    style_formula(ws.cell(r, 10))
    ws.cell(r, 11, "元")
    ws.cell(r, 12, SRC_COST + "；统一口径第4条")
    ws.cell(r, 13, "CNY 元；一次性总预算区间；待询价，非合同价；用户尚未锁定档位；对外合计与仍需现金主口径用本行，不以分项加总替代")
    ws.cell(r, 14, SCOPE_A)
    ws.cell(r, 15, NATURE_EST)
    ws.cell(r, 16, DATE_EST)
    ws.cell(r, 17, "是：待询价，档位未锁定")
    for col in (1, 2, 11, 12, 13, 14, 15, 16, 17):
        style_text(ws.cell(r, col))
    ws.cell(r, 1).font = FONT_B

    # row 21 GAP
    r = 21
    ws.cell(r, 1, "GAP")
    ws.cell(r, 2, "差额（旧稿头条 − 分项求和）。已裁决：单独列示，禁止虚拟行或改头条衬平。无来源不得编造补差行。")
    for col, formula in zip(range(3, 11), [
        "=C20-C19", "=D20-D19", "=E20-E19", "=F20-F19",
        "=G20-G19", "=H20-H19", "=I20-I19", "=J20-J19",
    ]):
        ws.cell(r, col, formula)
        style_formula(ws.cell(r, col), pending=True)
    ws.cell(r, 11, "元")
    ws.cell(r, 12, SRC_MODEL + "；" + SRC_COST + "；差额来自 2026-11-07 底稿本身（定稿写明「总表已打包防双计」），不是本模型算错")
    ws.cell(r, 13, (
        "已裁决归类：精益 +9,600–+10,200、基准 +4,000–+7,000 视为未归类余量，不是已确认可开支成本包；"
        "完整不含 02/04 为 −19,000–−13,000，含 02+04 为 −39,000–−83,000，对外仍以头条 11–22 万为锚，"
        "不得把分项上限加总当作完整档预算。分项对照口径可并列，不替代主口径。"
    ))
    ws.cell(r, 14, SCOPE_A)
    ws.cell(r, 15, "公式结果 / 已裁决：单独列示禁止衬平")
    ws.cell(r, 16, "跟随公式")
    ws.cell(r, 17, "否：已裁决，只列示不衬平")
    for col in (1, 2, 11, 12, 13, 14, 15, 16, 17):
        style_text(ws.cell(r, col), FILL_GAP)
    ws.cell(r, 1).font = FONT_B

    # row 22 SUM-A01-08 always include 02+04 for 完整对照
    r = 22
    ws.cell(r, 1, "SUM-A01-08")
    ws.cell(r, 2, "分项求和（完整档对照：始终含 02+04；精益/基准的 02/04 仍为 0）")
    ws.cell(r, 3, "=SUM(C11:C18)")
    ws.cell(r, 4, "=SUM(D11:D18)")
    ws.cell(r, 5, "=SUM(E11:E18)")
    ws.cell(r, 6, "=SUM(F11:F18)")
    ws.cell(r, 7, "=SUM(G11:G18)")
    ws.cell(r, 8, "=SUM(H11:H18)")
    ws.cell(r, 9, '=IF($C$3="完整",SUM(G11:G18),SUM(I11:I16))')
    ws.cell(r, 10, '=IF($C$3="完整",SUM(H11:H18),SUM(J11:J16))')
    for col in range(3, 11):
        style_formula(ws.cell(r, col))
    ws.cell(r, 11, "元")
    ws.cell(r, 12, "公式对照")
    ws.cell(r, 13, "仅展示完整档含全部可选时的分项合计，不替代头条验收锚点，也不自动抬高 PACK")
    ws.cell(r, 14, SCOPE_A)
    ws.cell(r, 15, "公式结果")
    ws.cell(r, 16, "跟随分项")
    ws.cell(r, 17, "是：对照用")
    for col in (1, 2, 11, 12, 13, 14, 15, 16, 17):
        style_text(ws.cell(r, col))
    ws.cell(r, 1).font = FONT_B

    # ---- B. period costs ----
    section_bar(ws, 24, "B. Demo 期持续费用与周期（元；不计入一次性头条合计）", 1, 17)
    for i, h in enumerate(headers, 1):
        ws.cell(25, i, h)
    style_header_row(ws, 25, 1, 17)

    # 26 OPEX_M
    r = 26
    ws.cell(r, 1, "OPEX_M")
    ws.cell(r, 2, "Demo期月度持续")
    for col, val in zip(range(3, 9), [100, 300, 200, 400, 400, 800]):
        ws.cell(r, col, val)
        style_input(ws.cell(r, col), num=True)
    ws.cell(r, 9, cur_lo("C26", "E26", "G26"))
    ws.cell(r, 10, cur_hi("D26", "F26", "H26"))
    style_formula(ws.cell(r, 9))
    style_formula(ws.cell(r, 10))
    ws.cell(r, 11, "元/月")
    ws.cell(r, 12, SRC_COST)
    ws.cell(r, 13, "CNY 元/月；Demo 期持续；另加认证年费；待询价；不计入一次性 PACK。官方基础套餐现价 19.9 元/月（P-003）只作对照，不改本行、不改总包（Benchmark T-010）。")
    ws.cell(r, 14, "A 当前 Demo；Demo 期")
    ws.cell(r, 15, NATURE_EST)
    ws.cell(r, 16, DATE_EST)
    ws.cell(r, 17, "是：待询价")
    for col in (1, 2, 11, 12, 13, 14, 15, 16, 17):
        style_text(ws.cell(r, col))
    ws.cell(r, 1).font = FONT_B

    # 27 CERT_Y
    r = 27
    ws.cell(r, 1, "CERT_Y")
    ws.cell(r, 2, "认证年费（基准/完整按精益同额占位，维持待确认）")
    for col in range(3, 9):
        ws.cell(r, col, 300)
        style_input(ws.cell(r, col), num=True)
    ws.cell(r, 9, cur_lo("C27", "E27", "G27"))
    ws.cell(r, 10, cur_hi("D27", "F27", "H27"))
    style_formula(ws.cell(r, 9))
    style_formula(ws.cell(r, 10))
    ws.cell(r, 11, "元/年")
    ws.cell(r, 12, SRC_COST + "；对照 Benchmark P-001 / T-001（不升格）")
    ws.cell(r, 13, (
        "CNY 元/年；旧稿仅对精益写明 300 元/年，基准与完整写「+认证」，本表按同额占位，不是已确认同价（Cost/MODEL 裁决维持待确认）。"
        "P-001：官方为微信认证 300 元/次（不一定支付：企业可对公打款验证），官方未把「每年」写成小程序口径。"
    ))
    ws.cell(r, 14, SCOPE_A)
    ws.cell(r, 15, "已有底稿估算 / 待确认占位（基准、完整）")
    ws.cell(r, 16, DATE_EST)
    ws.cell(r, 17, "是：占位待确认，不升格")
    for col in (1, 2, 11, 12, 13, 14, 15, 16, 17):
        style_text(ws.cell(r, col), FILL_PENDING)
    ws.cell(r, 1).font = FONT_B

    # 28 WEEKS
    r = 28
    ws.cell(r, 1, "WEEKS")
    ws.cell(r, 2, "开发周期（公历周）")
    for col, val in zip(range(3, 9), [3, 4, 4, 6, 6, 10]):
        ws.cell(r, col, val)
        style_input(ws.cell(r, col), num=True, fmt="0")
    ws.cell(r, 9, cur_lo("C28", "E28", "G28"))
    ws.cell(r, 10, cur_hi("D28", "F28", "H28"))
    style_formula(ws.cell(r, 9), fmt="0")
    style_formula(ws.cell(r, 10), fmt="0")
    ws.cell(r, 11, "周")
    ws.cell(r, 12, SRC_COST)
    ws.cell(r, 13, "公历周（7 天）。人天按 1 人×1 工作日，不得把日历周直接当 7 人天。本行不是金额，现金流万元列不得对本行做 /10000。")
    ws.cell(r, 14, SCOPE_A)
    ws.cell(r, 15, NATURE_EST)
    ws.cell(r, 16, DATE_EST)
    ws.cell(r, 17, "是")
    for col in (1, 2, 11, 12, 13, 14, 15, 16, 17):
        style_text(ws.cell(r, col))
    ws.cell(r, 1).font = FONT_B

    # 29 DAYS_M
    r = 29
    ws.cell(r, 1, "DAYS_M")
    ws.cell(r, 2, "月换算分母（示意：周×7÷本参数）")
    ws.cell(r, 3, 30)
    style_input(ws.cell(r, 3), num=True, fmt="0")
    ws.cell(r, 9, "=C29")
    ws.cell(r, 10, "=C29")
    style_formula(ws.cell(r, 9), fmt="0")
    style_formula(ws.cell(r, 10), fmt="0")
    ws.cell(r, 11, "天/月")
    ws.cell(r, 12, "本模型设定（非旧稿原文）")
    ws.cell(r, 13, "仅用于把开发周数示意折成月数，付款节奏未约定，非合同安排。本行不是金额。")
    ws.cell(r, 14, "A 当前 Demo；示意")
    ws.cell(r, 15, "待确认假设")
    ws.cell(r, 16, DATE_NOW)
    ws.cell(r, 17, "是")
    for col in (1, 2, 11, 12, 13, 14, 15, 16, 17):
        style_text(ws.cell(r, col))
    ws.cell(r, 1).font = FONT_B

    # ---- C. cash, rates, bot ----
    section_bar(ws, 31, "C. 已发生现金、人天费率锚点、Bot 非现金（不得从仍需现金扣减）", 1, 17)

    def simple_param(r, pid, name, value, unit, source, caliber, scope, nature, date, pending, empty=False, fill=None, fmt=None):
        ws.cell(r, 1, pid).font = FONT_B
        ws.cell(r, 2, name)
        if empty:
            ws.cell(r, 3).value = None
            style_pending_empty(ws.cell(r, 3))
        else:
            ws.cell(r, 3, value)
            style_input(ws.cell(r, 3), num=True, fmt=fmt)
            if fill:
                ws.cell(r, 3).fill = fill
        ws.cell(r, 11, unit)
        ws.cell(r, 12, source)
        ws.cell(r, 13, caliber)
        ws.cell(r, 14, scope)
        ws.cell(r, 15, nature)
        ws.cell(r, 16, date)
        ws.cell(r, 17, pending)
        for col in (1, 2, 11, 12, 13, 14, 15, 16, 17):
            style_text(ws.cell(r, col), FILL_PURPLE if fill == FILL_PURPLE else FILL_GREY)
        ws.cell(r, 1).font = FONT_B
        ws.cell(r, 1).border = THIN
        ws.cell(r, 2).border = THIN

    simple_param(
        32, "CASH_SPENT", "已发生现金", 0, "元", SRC_COST,
        "估算；有票据后回填。仍需现金主口径=PACK 头条合计−已发生（见现金流表）。Bot 不得填进本格。",
        SCOPE_A, "已有底稿估算（H8）", DATE_EST, "是：待票据回填",
    )
    simple_param(33, "P-RATE-L", "人天费率_低（折算非雇佣）", 550, "元/人天", SRC_COST,
                 "仅折算锚点（H5），不得用其倒推已确认人天或代替分项报价", SCOPE_A, NATURE_EST, DATE_EST, "是")
    simple_param(34, "P-RATE-M", "人天费率_中（折算非雇佣）", 830, "元/人天", SRC_COST,
                 "仅折算锚点（H5）", SCOPE_A, NATURE_EST, DATE_EST, "是")
    simple_param(35, "P-RATE-H", "人天费率_高（折算非雇佣）", 1290, "元/人天", SRC_COST,
                 "仅折算锚点（H5）", SCOPE_A, NATURE_EST, DATE_EST, "是")
    simple_param(36, "P-OUT-L", "外包加成经验_下限", 1200, "元/人天", SRC_COST,
                 "外包加成经验区间，待询价，非雇佣工资", SCOPE_A, NATURE_EST, DATE_EST, "是")
    simple_param(37, "P-OUT-H", "外包加成经验_上限", 2000, "元/人天", SRC_COST,
                 "外包加成经验区间，待询价，非雇佣工资", SCOPE_A, NATURE_EST, DATE_EST, "是")
    simple_param(38, "P-BOT-LO", "Bot替代价值_下限（非现金）", 50000, "元", SRC_COST,
                 "非现金；不可入账为已节省，不得从仍需现金直接扣减",
                 "附注，不进入 A 现金主表合计", "已有底稿估算 / 待询价", DATE_EST, "是",
                 fill=FILL_PURPLE)
    ws["C38"].fill = FILL_PURPLE
    simple_param(39, "P-BOT-HI", "Bot替代价值_上限（非现金）", 120000, "元", SRC_COST,
                 "非现金；不可入账为已节省，不得从仍需现金直接扣减",
                 "附注，不进入 A 现金主表合计", "已有底稿估算 / 待询价", DATE_EST, "是",
                 fill=FILL_PURPLE)
    ws["C39"].fill = FILL_PURPLE

    # ---- D. B/C/D totals (keep C42-C47 addresses) ----
    section_bar(ws, 41, "D. B/C/D 阶段区间（Cost 已验收粗区间；旧稿情景，待专项复核；严禁混入 A）", 1, 17)
    simple_param(42, "B-TOTAL-LO", "B产品验证_下限", 20000, "元", SRC_COST,
                 "旧稿情景区间，待专项复核；不得混入 A 合计或 A 现金流", "B 产品验证",
                 "已有底稿估算 / 待专项复核", DATE_EST, "是")
    simple_param(43, "B-TOTAL-HI", "B产品验证_上限", 80000, "元", SRC_COST,
                 "旧稿情景区间，待专项复核；不得混入 A", "B 产品验证",
                 "已有底稿估算 / 待专项复核", DATE_EST, "是")
    simple_param(44, "C-TOTAL-LO", "C商业试点_下限", 50000, "元", SRC_COST,
                 "旧稿情景区间，待专项复核；不得混入 A", "C 商业试点",
                 "已有底稿估算 / 待专项复核", DATE_EST, "是")
    simple_param(45, "C-TOTAL-HI", "C商业试点_上限", 300000, "元", SRC_COST,
                 "旧稿情景区间，待专项复核；不得混入 A", "C 商业试点",
                 "已有底稿估算 / 待专项复核", DATE_EST, "是")
    simple_param(46, "D-TOTAL-L", "D规模化_下限", 500000, "元", SRC_COST,
                 "旧稿为 ¥500,000–数百万+；上限未给出单一数字，见 D-TOTAL-H（C47）留空",
                 "D 规模化；若上硬件则供应链单列",
                 "已有底稿估算 / 待专项复核", DATE_EST, "是")
    # C47 MUST remain empty (not 0)
    simple_param(47, "D-TOTAL-H", "D规模化_上限（旧稿未给单一数字）", None, "（旧稿：数百万+，本格留空）", SRC_COST,
                 "旧稿表述为「数百万+」，本格留空，不倒推上限，不以 0 冒充已测算",
                 "D 规模化", "待确认（旧稿无单一上限）", DATE_EST, "是：留空不编造",
                 empty=True)
    ws["K47"] = "（旧稿：数百万+，本格留空）"
    style_text(ws["K47"], FILL_PENDING)

    return ws


def _meta(ws, r, unit, source, caliber, scope, nature, date, pending, fill=FILL_GREY):
    ws.cell(r, 11, unit)
    ws.cell(r, 12, source)
    ws.cell(r, 13, caliber)
    ws.cell(r, 14, scope)
    ws.cell(r, 15, nature)
    ws.cell(r, 16, date)
    ws.cell(r, 17, pending)
    for col in (1, 2, 11, 12, 13, 14, 15, 16, 17):
        style_text(ws.cell(r, col), fill)
    ws.cell(r, 1).font = FONT_B
    ws.cell(r, 1).border = THIN
    ws.cell(r, 2).border = THIN


def empty_input(ws, r, col=3):
    ws.cell(r, col).value = None
    style_pending_empty(ws.cell(r, col))


def build_params_rest(ws):
    """Revenue, Benchmark pointers, and Cost B/C/D detail — all after C47 to keep addresses stable."""

    # ---- E. Revenue (accepted, values blank) ----
    section_bar(
        ws, 49,
        "E. 收入模式参数（已并入已验收 Revenue；全部待研究，不是已确定商业决策；缺参数留空，禁止填入看起来合理的虚数，不以 0 冒充）",
        1, 17,
    )
    rev_headers = [
        "参数ID", "参数名称", "数值（可调，当前留空则保持空白）", "（预留）", "（预留）",
        "（预留）", "（预留）", "（预留）", "（预留）", "（预留）", "单位",
        "来源", "口径", "适用范围", "性质", "日期", "待确认",
    ]
    for i, h in enumerate(rev_headers, 1):
        ws.cell(50, i, h)
    style_header_row(ws, 50, 1, 17)

    # G-04 has a structural default 12; others empty
    def rev_row(r, pid, name, unit, caliber, qid, value=None, nature="待确认假设 / 待研究", date=DATE_NOW):
        ws.cell(r, 1, pid)
        ws.cell(r, 2, name)
        if value is None:
            empty_input(ws, r, 3)
            pending = f"是：空，禁止倒推（{qid}）"
        else:
            style_input(ws.cell(r, 3, value), num=True, fmt="0")
            pending = f"结构约定，不是收入预测（{qid}）"
        _meta(ws, r, unit, SRC_REV, caliber, "待研究情景，非已确定商业决策", nature, date, pending,
              FILL_NOTE if value is not None else FILL_PENDING)

    rev_row(51, "G-04", "测算期月数", "个公历月",
            "仅结构约定（公历一年=12 个月），不是已有或已预测的 12 个月收入；可改，改后须注明",
            "Q-01", value=12, nature="结构约定", date=DATE_NOW)
    rev_row(52, "G-05", "含税口径（1=含税，0=未税）", "0/1",
            "未确认。空则收入结果不得标注含税或未税", "Q-02")
    rev_row(53, "G-06", "平台或渠道扣点率", "小数（1=100%）",
            "未确认。空则净收入公式输出空白，不把空扣点当作 0。官方对照见 P-011 至 P-018，不自动填入本格（未决定通道与档位）",
            "Q-03")
    rev_row(54, "G-07", "单均变动成本（获客+履约等，可选）", "元/单位",
            "未确认。空则不扣变动成本，也不把空值当 0 去倒推单位贡献。不得擅自填入经验获客成本（CAC 本轮留空）",
            "Q-19")

    section_bar(ws, 56, "E1. A. 小程序/AR 互动（待研究方向）——项目制 / 年框 / 可选 C 端", 1, 17)
    a_rows = [
        (57, "A-01", "B端单项目或 Campaign 单价", "元/项目", "驱动 A1=A-01×A-02。无 PO/签约不得填已定项目数或签约额。", "Q-05"),
        (58, "A-02", "测算期内 B 端项目数", "个", "驱动 A1。立项号不等于采购单。", "Q-05"),
        (59, "A-03", "B端年框单价", "元/份", "驱动 A2=A-03×A-04。须与 A1 防双计。", "Q-06"),
        (60, "A-04", "测算期内年框份数", "份", "驱动 A2。", "Q-06"),
        (61, "A-05", "C端付费用户数", "人", "驱动 A3=A-05×A-06×A-07。不可默认存在可填用户量。", "Q-07"),
        (62, "A-06", "C端人均单价（每次或每期）", "元/人", "驱动 A3。不得按助眠疗效定价。", "Q-07"),
        (63, "A-07", "C端人均付费次数（测算期内）", "次/人", "驱动 A3。匿名开放聊天路径已判暂不可行，不得按聊天订阅填本线。", "Q-07"),
    ]
    for args in a_rows:
        rev_row(*args)

    section_bar(ws, 65, "E2. B. IP 内容与数字产品（待研究方向）——季包 / 可选订阅", 1, 17)
    for args in [
        (66, "B-01", "内容季包或内容包单价", "元/包", "驱动 B1=B-01×B-02。国内客单价本轮未核验到可引用公开价；国际起价不可直接当国内锚。", "Q-08"),
        (67, "B-02", "测算期内售出包数", "包", "驱动 B1。", "Q-08"),
        (68, "B-03", "C端订阅单价（每期）", "元/人/期", "驱动 B2=B-03×B-04×B-05。不宜把单独 ToC 月订阅作为唯一假设。", "Q-09"),
        (69, "B-04", "订阅用户数", "人", "驱动 B2。", "Q-09"),
        (70, "B-05", "人均订阅期数（测算期内）", "期/人", "驱动 B2。", "Q-09"),
    ]:
        rev_row(*args)

    section_bar(ws, 72, "E3. C. 授权联名（待研究方向）——授权金 / 分成 / 联名项目", 1, 17)
    for args in [
        (73, "C-01", "授权金（按份或按年）", "元/份", "驱动 C1=C-01×C-02。目前无已谈成授权，全部待确认。", "Q-10"),
        (74, "C-02", "授权合约或份数", "份", "驱动 C1。", "Q-10"),
        (75, "C-03", "按销售分成比例", "小数（1=100%）", "驱动 C2=C-03×C-04。不得用行业口头通例填数。", "Q-10"),
        (76, "C-04", "分成基数（对方相关销售额）", "元", "驱动 C2。不得用行业总盘充当分成基数。", "Q-10"),
        (77, "C-05", "联名项目单价（非授权金）", "元/项目", "驱动 C3=C-05×C-06。须与 A/D 项目款防双计。", "Q-11"),
        (78, "C-06", "联名项目数", "个", "驱动 C3。", "Q-11"),
    ]:
        rev_row(*args)

    section_bar(ws, 80, "E4. D. 酒店文旅（待研究方向；酒店重要但非唯一；本阶段不以规模化部署为已定收入）", 1, 17)
    for args in [
        (81, "D-01", "单店期间服务费或年费", "元/店", "驱动 D1=D-01×D-02。须有签约主体+可执行门店才算验证。", "Q-13"),
        (82, "D-02", "付费门店数", "家", "驱动 D1。严禁把 Hilton 稿称 2400+（P-020）或其他连锁规模填入本格。", "Q-13"),
        (83, "D-03", "试点项目款（按项目）", "元/项目", "驱动 D2=D-03×D-04。与 D1 可能描述同一合同，须防双计。", "Q-13"),
        (84, "D-04", "试点项目数", "个", "驱动 D2。", "Q-13"),
        (85, "D-05", "主题房可分成溢价（每间夜）", "元/间夜", "驱动 D3=D-05×D-06×D-07。媒体口径不可当作本项目溢价。", "Q-14"),
        (86, "D-06", "可分成间夜数", "间夜", "驱动 D3。", "Q-14"),
        (87, "D-07", "溢价分成比例（归本项目）", "小数（1=100%）", "驱动 D3。", "Q-14"),
    ]:
        rev_row(*args)

    section_bar(ws, 89, "E5. E. 衍生品与线下体验（待研究方向；硬件量产不是本轮已定投入）", 1, 17)
    for args in [
        (90, "E-01", "衍生品平均单价", "元/件", "驱动 E1=E-01×E-02。目前无可靠销量与定价。", "Q-16"),
        (91, "E-02", "衍生品销量", "件", "驱动 E1。", "Q-16"),
        (92, "E-03", "线下体验或票务单价", "元/人次", "驱动 E2=E-03×E-04。文旅动线工程不是本项目本体。", "Q-17"),
        (93, "E-04", "线下体验人次", "人次", "驱动 E2。", "Q-17"),
    ]:
        rev_row(*args)

    ws.merge_cells("A95:Q95")
    ws["A95"] = (
        "收入公式见 04 表：A1=A-01×A-02；A2=A-03×A-04；A3=A-05×A-06×A-07；"
        "B1=B-01×B-02；B2=B-03×B-04×B-05；C1=C-01×C-02；C2=C-03×C-04；C3=C-05×C-06；"
        "D1=D-01×D-02；D2=D-03×D-04；D3=D-05×D-06×D-07；E1=E-01×E-02；E2=E-03×E-04。"
        "必要因子为空则结果为空白。净收入仅在 G-06 已填时计算。不要把本区空白解读为收入为 0。"
    )
    ws["A95"].font = FONT_SM
    ws["A95"].alignment = LEFT

    # ---- F. Benchmark v1.1 (reference, not cost drivers) ----
    section_bar(
        ws, 97,
        "F. 行业基准对照参数（已复验 Benchmark v1.1；引用须带参数 ID；官方价目只作对照，不改 PACK 总包，不自动写入收入或认证年费）",
        1, 17,
    )
    for i, h in enumerate([
        "参数ID", "参数名称", "低值", "高值", "中值（公式，非官方档位）",
        "（预留）", "（预留）", "（预留）", "（预留）", "（预留）", "单位",
        "来源", "口径", "适用范围", "性质", "日期", "待确认/限制",
    ], 1):
        ws.cell(98, i, h)
    style_header_row(ws, 98, 1, 17)

    # P-001 to P-020. mid formula only when both ends numeric.
    # Values from Benchmark v1.1 可引用参数. P-019 has no amount. P-020 low=2400, high empty.
    bench = [
        # r, id, name, lo, hi, unit, caliber, scope, nature, limit, mid_ok
        (99, "P-001", "微信小程序认证服务费", 300, 300, "元/次",
         "官方接入指南（更新 2026-07-28）：企业可对公打款或选择微信认证。300 元只对应选择「微信认证」的路径，不一定支付。官方未把「每年」写成小程序口径。",
         "仅当拟用主体选择「微信认证」时可比；不自动改 CERT_Y 占位，不升格为已确认年费",
         "事实", "对照用，不改总包；认证是否年缴见 T-001", True),
        (100, "P-002", "微信公众号/服务号认证费（对照，非小程序本页）", 300, 300, "元/次",
         "腾讯客服 FAQ：每次 300 元，认证成功后一年内有效。对象是公众号/服务号，不是小程序。",
         "仅作对照，说明「300 元、一年有效」出处属于公众号/服务号",
         "事实", "部分可比，不写入 CERT_Y", True),
        (101, "P-003", "微信云开发基础套餐（现价）", 19.9, 19.9, "元/月",
         "官方计费说明（更新 2026-10-26）「三、基础套餐」：现价 19.9 元/月（原价 39 元/月），每月 40,000 资源点。页上未见「5 折长期有效」或套餐调价「提前 3 个月」。",
         "使用微信云开发且选择基础套餐的小程序。只作对照，不改 OPEX_M，不改 PACK 总包。",
         "事实", "官方 19.9 元/月只作对照，不改总包", True),
        (102, "P-004", "微信云开发基础套餐（原价，对照）", 39, 39, "元/月",
         "同一官方计费文档列示的基础套餐原价。现价见 P-003。P-004 适用范围旧表述易让人把活动截止日通知规则误接到套餐价，Benchmark 残留已披露，本表仅作原价对照。",
         "同 P-003，对照促销结束后的目录价上限",
         "事实", "对照用，不改总包", True),
        (103, "P-005", "微信云开发免费环境（活动截止）", 0, 0, "元/环境·活动期",
         "官方「二、免费体验活动」：发布后到期日变为上线后第 15 天；活动至 2026-12-31。页上「提前 3 个月通知」只约束活动截止日若调整，不是套餐调价承诺。跨过该日不得再按 0 元假设。",
         "Demo/未发布或刚发布 15 天内、且活动仍有效。过期后改用付费套餐。",
         "事实", "有截止日期，过期不得按 0 假设", True),
        (104, "P-006", "微信云开发资源点单价", 0.001, 0.001, "元/资源点",
         "官方计费：1000 资源点 = 1 元，即 0.001 元/点。",
         "云开发按量计费部分",
         "事实", "对照用", True),
        (105, "P-007", "微信 MiniTest 每周免费测试时长", 150, 150, "分钟/周·每小程序",
         "官方《免费测试时长使用说明》（更新 2026-08-21）只明确每周 150 分钟。页上未见「每周一 00:00 刷新、未使用作废」。",
         "使用微信云测 / MiniTest 的小程序测试。A 阶段精益档可优先用免费额度。",
         "事实", "非金额；不改 A06 测试分项", True),
        (106, "P-008", "微信 MiniTest 一次性额外免费时长", 100, 100, "分钟/项目·一次",
         "官方文档：可申请一次额外 100 分钟，有效期 30 天，每个项目限一次。",
         "同 P-007，一次性补充，不可当作每周常态额度",
         "事实", "非金额；不改 A06", True),
        (107, "P-009", "微信云测 WeTest 专有云真机（不足 10 台）", 1600, 1600, "元/月·台",
         "官方文档（更新 2026-08-21）：专有云小于 10 台时，1600 元/月/台。",
         "需要独占真机云的测试需求。不是 MiniTest 免费时长的默认升级项。精益档测试上限 2,000 元只够约一台一个月。",
         "事实", "部分可比，不改 A06", True),
        (108, "P-010", "微信云测 WeTest 专有云真机（不少于 10 台）", 1400, 1400, "元/月·台",
         "同一官方文档：不少于 10 台时，1400 元/月/台。",
         "同 P-009，规模档。A 阶段几乎用不到 10 台门槛。",
         "事实", "部分可比，不改 A06", True),
        (109, "P-011", "微信小程序虚拟支付·Android/鸿蒙/Windows 主动支付（当前优惠）", 0.01, 0.01, "比率（成交额）",
         "官方虚拟支付开发指南（更新 2026-10-29）：工具/社交/文娱-非微短剧等，当前优惠 1%。属收入侧可变成本，不是 CAC。",
         "若在小程序内对虚拟商品发起主动支付且类目符合该表。不自动写入 G-06。",
         "事实", "部分可比；优惠档与标准档须分列", True),
        (110, "P-012", "微信小程序虚拟支付·Android/鸿蒙/Windows 主动支付（标准费率）", 0.1, 0.1, "比率（成交额）",
         "同 P-011 官方表的标准费率 10%。",
         "同 P-011。优惠结束或恢复标准档时对照。不自动写入 G-06。",
         "事实", "部分可比", True),
        (111, "P-013", "微信小程序虚拟支付·订阅（首笔当前优惠 / 后续标准）", 0.01, 0.1, "比率（成交额）",
         "同一官方表：首笔当前优惠 1%，后续 10%。低值=首笔优惠，高值=后续标准。中值是算术平均，不是官方档位；测算必须按笔拆开。",
         "若启用小程序订阅支付且类目符合该表。禁止用中值 0.055 当费率。",
         "事实", "中值不是官方档位", True),
        (112, "P-014", "微信小程序虚拟支付·iOS（当前，全部为苹果佣金）", 0.12, 0.12, "比率（成交额）",
         "同一官方表：iOS 当前优惠 12%，全部为苹果佣金。与 App Store 中国店 12% 数字相同、合同不同，禁止加总。",
         "微信小程序内 iOS 端虚拟支付。不自动写入 G-06。",
         "事实", "部分可比；不得与 P-017 加总", True),
        (113, "P-015", "微信小程序虚拟支付·iOS（标准费率）", 0.17, 0.17, "比率（成交额）",
         "同一官方表标准费率 17%，其中 12% 为苹果佣金。",
         "同 P-014，优惠恢复后的对照。",
         "事实", "部分可比", True),
        (114, "P-016", "App Store 中国大陆店面佣金（2026-03-15 起，标准档）", 0.25, 0.25, "比率（成交额）",
         "Apple Developer 官方新闻（2026-03-12）：自 2026-03-15 起，中国大陆店标准 IAP 及付费应用 25%（此前 30%）。",
         "在中国大陆 App Store 上架的付费应用或 IAP。本阶段主路径是微信小程序，本行仅在讨论独立 App 时对照。",
         "事实", "部分可比", True),
        (115, "P-017", "App Store 中国大陆店面佣金（小企业计划/迷你应用/订阅满一年后续订）", 0.12, 0.12, "比率（成交额）",
         "同一官方新闻：符合相应计划时 12%（此前 15%）。与 P-014 数字相同、合同不同，禁止加总。",
         "需符合相应计划资格。中国店不要误用全球 15%（P-018）。",
         "事实", "部分可比；不得与 P-014 加总", True),
        (116, "P-018", "App Store Small Business Program 佣金（全球计划规则）", 0.15, 0.15, "比率（成交额）",
         "Apple 官方计划页：符合条件者佣金 15%；年 proceeds 不超过 100 万美元。中国大陆店现行档以 P-017 的 12% 为准。",
         "原生 App Store 全球计划规则对照。",
         "事实", "中国店现行以 P-017 为准", True),
        (117, "P-019", "Hilton × Calm：客房内免费提供内容（案例事实，非费率）", None, None, "—（非金额）",
         "Hilton 官方新闻稿（2025-01-21）：独家合作，2025-03 起内容进入 Connected Room，住客通过客房电视使用，稿件写明无需订阅。授权费未披露。",
         "仅作为「酒店场景下，住客免费、内容进入客房系统」的公开案例。不要当金额驱动，不要填无来源的授权单价。",
         "事实", "案例事实，非费率；金额留空", False),
        (118, "P-020", "Hilton Connected Room 覆盖酒店数（案例事实，稿称下界）", 2400, None, "家（稿称 more than，下界）",
         "同一官方新闻稿：more than 2,400 hotels globally。表中 2,400 只作下界。规模不可外推。严禁把本数填入 D-02 付费门店数。",
         "说明该合作接入的是已规模化部署的客房系统，不是单店试点基数。规模不可比。",
         "事实", "不可比（规模）；高值留空；禁止写入 D-02", False),
    ]

    for r, pid, name, lo, hi, unit, caliber, scope, nature, limit, mid_ok in bench:
        ws.cell(r, 1, pid)
        ws.cell(r, 2, name)
        if lo is None:
            empty_input(ws, r, 3)
        else:
            fmt = PCT if unit.startswith("比率") else (YUAN2 if isinstance(lo, float) and lo < 100 else YUAN)
            if pid in ("P-006",):
                fmt = "0.000"
            if pid in ("P-007", "P-008", "P-020"):
                fmt = "0"
            style_input(ws.cell(r, 3, lo), num=True, fmt=fmt)
            # Benchmark values are 对照: keep yellow but comment they should not feed PACK
        if hi is None:
            empty_input(ws, r, 4)
        else:
            fmt = PCT if unit.startswith("比率") else (YUAN2 if isinstance(hi, float) and hi < 100 else YUAN)
            if pid in ("P-006",):
                fmt = "0.000"
            if pid in ("P-007", "P-008"):
                fmt = "0"
            style_input(ws.cell(r, 4, hi), num=True, fmt=fmt)
        if mid_ok:
            ws.cell(r, 5, f'=IF(AND(ISNUMBER(C{r}),ISNUMBER(D{r})),(C{r}+D{r})/2,IF(ISNUMBER(C{r}),C{r},IF(ISNUMBER(D{r}),D{r},"")))')
            style_formula(ws.cell(r, 5), fmt=ws.cell(r, 3).number_format or YUAN)
        else:
            # still a formula, but blank if either side missing as appropriate
            ws.cell(r, 5, f'=IF(AND(ISNUMBER(C{r}),ISNUMBER(D{r})),(C{r}+D{r})/2,IF(ISNUMBER(C{r}),C{r},IF(ISNUMBER(D{r}),D{r},"")))')
            style_formula(ws.cell(r, 5), num=False)
        _meta(ws, r, unit, SRC_BENCH + f"；参数ID {pid}；访问日 2026-11-12", caliber, scope, nature, "访问日 2026-11-12", limit, FILL_REF)
        if pid == "P-013":
            ws.cell(r, 15, "事实（中值列不是官方档位）")

    ws.merge_cells("A120:Q120")
    ws["A120"] = (
        "本节为对照参数，不进入 02/03 的 A 阶段合计或仍需主口径，也不自动写入 G-06 或 CERT_Y。"
        "禁止使用 Benchmark 第一版分项或已作废的中值差（−8,350 / −15,000 / −22,000）。"
        "结构校验请用本模型 GAP（头条−分项，上下限分列），与已裁决口径一致。"
        "CAC / 留存本轮无过核验数字，保持留空（Benchmark 获客与留存表 / T-005）。"
    )
    ws["A120"].font = FONT_SM
    ws["A120"].alignment = LEFT

    # ---- G. Cost B/C/D details (appendix only) ----
    section_bar(
        ws, 122,
        "G. B/C/D 情景分项（Cost 已验收；仅附录 06 引用；严禁进入 02/03/00/05 的 A 合计或现金流）",
        1, 17,
    )
    for i, h in enumerate([
        "参数ID", "参数名称", "下限（元）", "上限（元）", "", "", "", "", "", "", "单位/周期",
        "来源", "口径", "适用范围", "性质", "日期", "待确认",
    ], 1):
        ws.cell(123, i, h)
    style_header_row(ws, 123, 1, 17)

    def bcd_row(r, pid, name, lo, hi, unit, caliber, scope, note):
        ws.cell(r, 1, pid)
        ws.cell(r, 2, name)
        if lo is None:
            empty_input(ws, r, 3)
        else:
            style_input(ws.cell(r, 3, lo), num=True)
        if hi is None:
            empty_input(ws, r, 4)
        else:
            style_input(ws.cell(r, 4, hi), num=True)
        _meta(ws, r, unit, SRC_COST, caliber, scope, "已有底稿估算 / 待询价 / 待专项复核", DATE_EST, note)

    bcd_row(124, "B-DEV", "B · 迭代开发", 15000, 50000, "一次性情景（约）",
            "B 情景分项，待专项复核；不得混入 A；不得当作已批准的 A 之外研发预算",
            "B 仅情景", "是：仅附录")
    bcd_row(125, "B-REC", "B · 招募礼品访谈", 5000, 20000, "一次性情景（约）",
            "验证期招募，不是规模化 CAC；不得混入 A",
            "B 仅情景", "是：仅附录")
    bcd_row(126, "B-RPT", "B · 分析报告", 3000, 10000, "一次性情景（约）",
            "B 情景分项；不得混入 A",
            "B 仅情景", "是：仅附录")
    # B item sum and gap vs B-TOTAL
    ws.cell(127, 1, "B-CHECK")
    ws.cell(127, 2, "B 分项算术（B-DEV+B-REC+B-RPT）")
    ws.cell(127, 3, "=SUM(C124:C126)")
    ws.cell(127, 4, "=SUM(D124:D126)")
    style_formula(ws.cell(127, 3))
    style_formula(ws.cell(127, 4))
    _meta(ws, 127, "元", "公式（Cost B-CHECK）",
          "校验用，不替代 B-TOTAL，不计入 A。分项低 23,000 高于粗区间低 20,000，差额 3,000 已披露，不编造调平项（Cost P11）",
          "B 仅情景", "公式结果", DATE_EST, "是：差额已披露不衬平")

    ws.cell(128, 1, "B-GAP")
    ws.cell(128, 2, "B 分项算术 − B 粗区间（B-TOTAL）")
    ws.cell(128, 3, "=IF(OR(C127=\"\",C42=\"\"),\"\",C127-C42)")
    ws.cell(128, 4, "=IF(OR(D127=\"\",C43=\"\"),\"\",D127-C43)")
    style_formula(ws.cell(128, 3), pending=True)
    style_formula(ws.cell(128, 4), pending=True)
    _meta(ws, 128, "元", "公式（Cost B-GAP）",
          "低列预期 3,000；高列预期 0。不改写 B-TOTAL，不编造调平项。",
          "B 仅情景", "公式结果", DATE_EST, "是：Cost P11")

    bcd_row(129, "C-PROD", "C · 产品增量（Marker/渠道包）", 20000, 80000, "一次性情景（约）",
            "C 情景分项；不得混入 A；不是 A 的 02/04",
            "C 仅情景", "是：仅附录")
    bcd_row(130, "C-MAT", "C · 台卡物料", 5000, 30000, "一次性情景（约）",
            "C 情景分项；酒店台卡后置，不进 A 主预算",
            "C 仅情景", "是：仅附录")
    bcd_row(131, "C-OPS", "C · 驻场运营（月级）", 10000, 50000, "元/月（情景）",
            "月级期间费用，不是一次性；试点月数未确认，不自动乘月，也不与 C-PROD/C-MAT/C-TOTAL 直接相加",
            "C 仅情景", "是：月数待确认，不自动相乘")

    bcd_row(132, "D-SW", "D · 软件中台/客服（首年感）", 200000, 800000, "首年感；上沿旧稿「20–80 万+」，高列只取写出的 80 万",
            "情景；「+」未量化列入待确认；不得混入 A",
            "D 仅情景", "是：上沿+未量化")
    bcd_row(133, "D-MKT", "D · 市场推广", 100000, None, "下沿 10 万；上沿「数百万」，高列留空",
            "情景；上沿不是单一数字，禁止编造；不得混入 A；不是已确定获客预算",
            "D 仅情景", "是：高列留空不编造")
    bcd_row(134, "D-HW", "D · 硬件量产模具+首批", None, None, "旧稿：常数十万起；明示非现行 Demo 战略",
            "红线后置：不列为本轮必须完成或已确定投入；低/高均留空，不把「数十万起」写成预算数；不得混入 A",
            "D 仅情景 / 红线后置", "是：低/高均留空")

    ws.merge_cells("A136:Q136")
    ws["A136"] = (
        "G 区与 C42:C47 粗区间仅供 06_附录BCD 引用。00/02/03/05 公式不得引用 C42:C47 或 C124:D134。"
        "D-TOTAL-H（C47）、D-MKT 上限（D133）、D-HW（C134:D134）必须保持空白，展示层须用 IF(源=\"\",\"\",源)，不得显示为 0。"
    )
    ws["A136"].font = FONT_SM
    ws["A136"].alignment = LEFT

    ws.auto_filter.ref = "A10:Q22"
    ws.sheet_view.showGridLines = False
    return ws


def build_cover(wb):
    ws = wb.create_sheet("00_封面", 0)
    ws.sheet_properties.tabColor = "0D1B2A"
    set_widths(ws, {"A": 42, "B": 22, "C": 22, "D": 16, "E": 16, "F": 42, "G": 28})
    ws.row_dimensions[1].height = 24
    ws.merge_cells("A1:G1")
    ws["A1"] = "眠语财务模型 v0.2"
    ws["A1"].font = FONT_WHITE_LG
    ws["A1"].fill = FILL_TITLE
    for col in range(1, 8):
        ws.cell(1, col).fill = FILL_TITLE
        ws.cell(1, col).font = FONT_WHITE_LG

    ws.merge_cells("A2:G2")
    ws["A2"] = (
        "财务准备测算｜非正式 BP 正文｜单号 CFO-20261112-MODEL-v0.2｜"
        "交 CMQ-CFO 第一次验收｜本文件未自审通过｜不直接交 CEO、不请用户拍板"
    )
    ws["A2"].font = FONT_WHITE
    ws["A2"].fill = FILL_SECTION
    for col in range(1, 8):
        ws.cell(2, col).fill = FILL_SECTION

    meta = [
        (4, "版本", "v0.2（并入已验收 Cost / Revenue / Benchmark v1.1；修正 v0.1 展示残留；不覆盖 v0.1）"),
        (5, "日期", "2026-11-12（Asia/Shanghai）；旧稿数字估算日 2026-11-07；基准对照访问日 2026-11-12"),
        (6, "口径文件（只读，未改）", "/workspace/mianyu-cfo/00-统一参数口径-20261112.md"),
        (7, "已验收输入", "Cost 成本拆分与 COST 裁决；Revenue 收入测算准备与 REV 验收；Benchmark v1.1 与 BENCH v1.1 复验；MODEL v0.1 裁决与 AUDIT 有条件通过"),
        (8, "成本底稿（只读，未改）", "https://app.notion.com/p/411340bcc396814a9b16de9c7b11419c"),
        (9, "产品口径", "A 当前 Demo：微信小程序 AR（点按平面落位 → 预设偏移躲猫猫 → 一次轻互动），先通霁霁，屏内同玩法必达。真遮挡/人体跟随/暗房满血 6DoF/硬件不做进 A 阶段主预算。"),
        (10, "定位红线", "低唤醒夜间陪伴搭子；不是儿童哄睡、医疗助眠或依赖 AI 长对话的虚拟陪伴。不宣传未验证助眠疗效。"),
    ]
    for r, k, v in meta:
        ws.cell(r, 1, k).font = FONT_B
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
        ws.cell(r, 2, v).font = FONT_N
        ws.cell(r, 2).alignment = LEFT

    ws["A12"] = "颜色约定"
    ws["A12"].font = FONT_B
    ws["B12"] = "黄色格子 = 可调输入（请只改这些）"
    ws["D12"] = "蓝色格子 = 公式结果（不要覆盖）"
    ws["F12"] = "橙色格子 = 待确认 / 留空 / 已裁决差额列示"
    ws["B12"].fill = FILL_INPUT
    ws["D12"].fill = FILL_FORMULA
    ws["F12"].fill = FILL_PENDING

    ws.merge_cells("A14:G14")
    ws["A14"] = "使用方法"
    ws["A14"].font = FONT_B
    ws.merge_cells("A15:G16")
    ws["A15"] = (
        "1. 在「01_参数台」C3 切换 精益 / 基准 / 完整（默认基准仅作展示，不是已锁定）。"
        "2. 完整档如需把 02/04 可选纳入分项合计，将 C4/C5 改为「是」；纳入不得自动抬高头条 PACK。"
        "3. 修改任一分项上下限或一个收入参数后，02/03/04/05 及封面摘要会按公式重算。"
        "4. 收入参数现在为空：04/05 结果应显示为空白，不会倒推出量或单价，也不把空值显示为 0。"
        "5. B/C/D 只在附录，不进入 A 的合计与现金流主表。D 上限参数为空时附录必须显示空白而非 0。"
        "6. 万元列只对金额行作 ÷10000；开发周期与示意月数不换算万元。"
        "7. 引用行业基准必须带参数 ID；官方 19.9 元/月（P-003）只作对照，不改总包。"
    )
    ws["A15"].font = FONT_N
    ws["A15"].alignment = LEFT

    ws.merge_cells("A18:G18")
    ws["A18"] = "当前档摘要（全部为公式，随参数台联动）"
    ws["A18"].font = FONT_WHITE
    ws["A18"].fill = FILL_SECTION
    for col in range(1, 8):
        ws.cell(18, col).fill = FILL_SECTION
        ws.cell(18, col).font = FONT_WHITE

    for i, h in enumerate(["指标", "下限（元）", "上限（元）", "下限（万元）", "上限（万元）", "口径", "待确认"], 1):
        ws.cell(19, i, h)
    style_header_row(ws, 19, 1, 7)

    def cover_row(r, name, lo, hi, caliber, pending, wan=True):
        ws.cell(r, 1, name).font = FONT_B
        ws.cell(r, 1).border = THIN
        ws.cell(r, 2, lo)
        ws.cell(r, 3, hi)
        style_formula(ws.cell(r, 2), num=isinstance(lo, str) and lo.startswith("=") and "C3" not in lo)
        style_formula(ws.cell(r, 3), num=True)
        if wan:
            ws.cell(r, 4, f'=IF(B{r}="","",B{r}/10000)')
            ws.cell(r, 5, f'=IF(C{r}="","",C{r}/10000)')
            style_formula(ws.cell(r, 4), fmt=WAN)
            style_formula(ws.cell(r, 5), fmt=WAN)
        style_text(ws.cell(r, 6, caliber))
        style_text(ws.cell(r, 7, pending), FILL_PENDING)

    ws.cell(20, 1, "当前档位").font = FONT_B
    ws.cell(20, 1).border = THIN
    ws["B20"] = "='01_参数台'!C3"
    style_formula(ws["B20"], num=False)
    style_text(ws["F20"], FILL_GREY)
    ws["F20"] = "默认展示=基准（旧稿建议首选）"
    style_text(ws["G20"], FILL_PENDING)
    ws["G20"] = "是：用户尚未锁定"

    cover_row(21, "旧稿头条一次性合计（验收锚点 / 主口径）",
              "='01_参数台'!I20", "='01_参数台'!J20",
              "与 11-07 底稿硬对齐；待询价；不随 02/04 开关抬高", "是")
    cover_row(22, "分项求和（主预算，含开关控制的02/04）",
              "='01_参数台'!I19", "='01_参数台'!J19",
              "公式求和；对照口径，不替代头条", "是")
    cover_row(23, "差额（头条−分项；已裁决：单独列示，禁止衬平）",
              "='01_参数台'!I21", "='01_参数台'!J21",
              "正差=未归类余量（非已确认成本包）；负差不得用分项加总抬高头条。来自 11-07 底稿，不是算错。",
              "否：已裁决，只列示")
    cover_row(24, "已发生现金",
              "='01_参数台'!C32", "='01_参数台'!C32",
              "H8 估算，待票据", "是")
    cover_row(25, "仍需一次性（主口径=头条−已发生）",
              "='03_现金流'!B8", "='03_现金流'!C8",
              "主口径：与旧稿头条对齐；不扣 Bot", "是")
    cover_row(26, "仍需一次性（对照=分项求和−已发生）",
              "='03_现金流'!B10", "='03_现金流'!C10",
              "对照口径，非验收替代", "是")
    cover_row(27, "Demo期月度持续",
              "='01_参数台'!I26", "='01_参数台'!J26",
              "待询价；另加认证年费；P-003 的 19.9 元/月只作对照，不改本行", "是")
    cover_row(28, "认证年费（占位，维持待确认）",
              "='01_参数台'!I27", "='01_参数台'!J27",
              "基准/完整是否同 300 待确认；P-001 为 300 元/次对照，不升格为已确认年费", "是")

    ws.merge_cells("A30:G31")
    ws["A30"] = (
        "工作表：00 封面｜01 参数台｜02 A阶段成本拆分｜03 现金流｜04 收入与收支结构｜05 盈亏平衡｜"
        "06 附录BCD｜07 待确认清单｜08 假设H1-H8｜09 基准对照。"
        "关键结果栏均为公式。未确认假设未写成事实。本工作簿不覆盖 2026-11-07 Notion 定稿页，亦不覆盖 v0.1 文件。"
        "测算说明：/workspace/mianyu-cfo/CFO-FinancialModel-测算说明-v0.2-20261112.md。"
        "本件未自审。"
    )
    ws["A30"].font = FONT_SM
    ws["A30"].alignment = LEFT
    ws.sheet_view.showGridLines = False
    ws.row_dimensions[15].height = 78
    ws.row_dimensions[23].height = 36
    return ws


def build_cost_split(wb):
    ws = wb.create_sheet("02_A阶段成本拆分")
    ws.sheet_properties.tabColor = "2E75B6"
    set_widths(ws, {c: 16 for c in "ABCDEFGHI"})
    ws.column_dimensions["A"].width = 42
    ws.column_dimensions["J"].width = 48
    ws.column_dimensions["K"].width = 28

    ws.merge_cells("A1:K1")
    ws["A1"] = "A 阶段成本拆分（全部公式链接参数台；B/C/D 不在本表；差额已裁决单独列示，禁止衬平，无虚拟补差行）"
    ws["A1"].font = FONT_WHITE_LG
    ws["A1"].fill = FILL_TITLE
    for col in range(1, 12):
        ws.cell(1, col).fill = FILL_TITLE
        ws.cell(1, col).font = FONT_WHITE

    ws["A2"] = "当前档位"
    ws["B2"] = "='01_参数台'!C3"
    style_formula(ws["B2"], num=False)
    ws["C2"] = "完整档含02"
    ws["D2"] = "='01_参数台'!C4"
    style_formula(ws["D2"], num=False)
    ws["E2"] = "完整档含04"
    ws["F2"] = "='01_参数台'!C5"
    style_formula(ws["F2"], num=False)
    ws.merge_cells("G2:K2")
    ws["G2"] = "分项与头条均来自参数台；02/04 仅完整且开关为「是」才纳入分项合计；纳入不得自动抬高头条。单位：元。"
    ws["G2"].font = FONT_SM

    headers = ["分项", "精益_下限", "精益_上限", "基准_下限", "基准_上限",
               "完整_下限", "完整_上限", "当前_下限", "当前_上限", "公式说明", "待确认"]
    for i, h in enumerate(headers, 1):
        ws.cell(4, i, h)
    style_header_row(ws, 4, 1, 11)

    rows = [
        (5, "A01 工程包", 11, "参数台 A01 行", "是：待询价"),
        (6, "A02 IP美术", 12, "参数台 A02 行；完整档为五皮", "是：待询价"),
        (7, "A03 UI/UX", 13, "参数台 A03 行", "是：待询价"),
        (8, "A04 互动文案", 14, "参数台 A04 行", "是：待询价"),
        (9, "A05 云+认证一次性", 15, "参数台 A05 行；与期间费用是否重叠待确认", "是：待询价"),
        (10, "A06 测试", 16, "参数台 A06 行；官方免费时长对照见 P-007/P-008，不改本行", "是：待询价"),
        (11, "A07 02可选（按开关计入当前列）", 17, "当前列已按 C4 开关；精益/基准列显示 0（H4）", "是：待询价"),
        (12, "A08 04可选（按开关计入当前列）", 18, "当前列已按 C5 开关；精益/基准列显示 0（H4）", "是：待询价"),
    ]
    for r, name, pr, note, pend in rows:
        ws.cell(r, 1, name).font = FONT_B
        ws.cell(r, 1).border = THIN
        # C-J of param: C=3 ... J=10  -> B-I of this sheet
        letters = ["C", "D", "E", "F", "G", "H", "I", "J"]
        for i, let in enumerate(letters, 2):
            ws.cell(r, i, f"='01_参数台'!{let}{pr}")
            style_formula(ws.cell(r, i))
        style_text(ws.cell(r, 10, note))
        style_text(ws.cell(r, 11, pend), FILL_PENDING)

    def link_row(r, name, pr, note, pend, pending_fill=False):
        ws.cell(r, 1, name).font = FONT_B
        ws.cell(r, 1).border = THIN
        for i, let in enumerate(["C", "D", "E", "F", "G", "H", "I", "J"], 2):
            ws.cell(r, i, f"='01_参数台'!{let}{pr}")
            style_formula(ws.cell(r, i), pending=pending_fill)
        style_text(ws.cell(r, 10, note), FILL_GAP if pending_fill else FILL_GREY)
        style_text(ws.cell(r, 11, pend), FILL_PENDING if not pending_fill else FILL_GAP)

    link_row(13, "SUM-SWITCH 分项求和（主预算）", 19,
             "参数台第19行：A01–A06 + 开关控制的 A07/A08", "是：与头条可能有差额")
    link_row(14, "PACK 旧稿头条一次性合计（验收锚点 / 主口径）", 20,
             "必须与旧稿 2.5–5.5 / 5.5–11 / 11–22 万元区间一致；不随 02/04 开关抬高",
             "是：待询价，档位未锁定")
    link_row(15, "GAP 差额（头条−分项；已裁决单独列示，禁止衬平）", 21,
             "正差=未归类余量，不是已确认可开支成本包；负差=分项高于头条，不得把分项加总当作完整档预算。禁止虚拟行衬平。",
             "否：已裁决，只列示", pending_fill=True)
    link_row(16, "SUM-A01-08 分项求和（完整对照：始终含02+04）", 22,
             "仅对照，不替代头条验收锚点", "是：对照用")

    ws.merge_cells("A18:K19")
    ws["A18"] = (
        "差额归类（可溯源至 Cost / MODEL v0.1 裁决与 2026-11-07 底稿「总表已打包防双计」，不是本模型算错；无虚拟补差行）："
        "精益分项 15,400–44,800 vs 头条 25,000–55,000，差额 +9,600–+10,200，视为未归类余量，不是已确认可开支成本包；"
        "基准分项 51,000–103,000 vs 头条 55,000–110,000，差额 +4,000–+7,000，同为未归类余量；"
        "完整（不含02/04）分项 129,000–233,000 vs 头条 110,000–220,000，差额 −19,000–−13,000；"
        "完整（含02+04）分项 149,000–303,000 vs 同一头条 110,000–220,000，差额 −39,000–−83,000。"
        "对外与验收仍以头条 11–22 万为锚，不得把分项上限加总当作完整档预算；纳入 02/04 不得自动抬高头条，须另行决策。"
        "上列差额由公式重算，改参数台分项后以公式为准。未自行改旧稿头条，也未编造补差行。"
    )
    ws["A18"].font = FONT_SM
    ws["A18"].alignment = LEFT
    ws["A18"].fill = FILL_GAP
    ws.row_dimensions[18].height = 36
    ws.row_dimensions[19].height = 36
    ws.sheet_view.showGridLines = False
    return ws


def build_cashflow(wb):
    ws = wb.create_sheet("03_现金流")
    ws.sheet_properties.tabColor = "548235"
    set_widths(ws, {c: 16 for c in "ABCDEFGHIJK"})
    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["F"].width = 56
    ws.column_dimensions["G"].width = 16

    ws.merge_cells("A1:K1")
    ws["A1"] = "现金流：已发生 vs 仍需；一次性 vs 月度持续（A 阶段；不混入 B/C/D；不扣 Bot 替代价值）"
    ws["A1"].font = FONT_WHITE_LG
    ws["A1"].fill = FILL_TITLE
    for col in range(1, 12):
        ws.cell(1, col).fill = FILL_TITLE
        ws.cell(1, col).font = FONT_WHITE

    ws["A2"] = "当前档位"
    ws["B2"] = "='01_参数台'!C3"
    style_formula(ws["B2"], num=False)
    ws.merge_cells("C2:K2")
    ws["C2"] = "主口径「仍需一次性」= 旧稿头条合计 − 已发生现金。分项口径并列表对照。万元列只对金额行换算。"
    ws["C2"].font = FONT_SM

    for i, h in enumerate(["项目", "下限（元或原单位）", "上限（元或原单位）", "下限（万元）", "上限（万元）", "口径 / 公式", "待确认"], 1):
        ws.cell(4, i, h)
    style_header_row(ws, 4, 1, 7)

    def cash_row(r, name, lo, hi, note, pending=False, wan=True, fmt=YUAN, wan_note_blank=False):
        ws.cell(r, 1, name).font = FONT_B
        ws.cell(r, 1).border = THIN
        ws.cell(r, 1).alignment = LEFT
        ws.cell(r, 2, lo)
        style_formula(ws.cell(r, 2), pending=pending, fmt=fmt)
        ws.cell(r, 3, hi)
        style_formula(ws.cell(r, 3), pending=pending, fmt=fmt)
        if wan:
            ws.cell(r, 4, f'=IF(OR(B{r}="",B{r}="-"),"",B{r}/10000)')
            ws.cell(r, 5, f'=IF(OR(C{r}="",C{r}="-"),"",C{r}/10000)')
            style_formula(ws.cell(r, 4), pending=pending, fmt=WAN)
            style_formula(ws.cell(r, 5), pending=pending, fmt=WAN)
        else:
            # v0.2 fix: do NOT divide weeks/months by 10000. Leave 万元 columns blank.
            ws.cell(r, 4, '=""')
            ws.cell(r, 5, '=""')
            style_formula(ws.cell(r, 4), num=False)
            style_formula(ws.cell(r, 5), num=False)
            ws.cell(r, 4).alignment = CENTER
            ws.cell(r, 5).alignment = CENTER
        style_text(ws.cell(r, 6, note), FILL_GAP if pending else FILL_GREY)
        style_text(ws.cell(r, 7, "是" if not wan_note_blank else "是（非金额行）"), FILL_PENDING)

    cash_row(5, "已发生现金", "='01_参数台'!C32", "='01_参数台'!C32",
             "H8：≈0，估算；有票据后回填参数台 C32")
    cash_row(6, "旧稿头条一次性合计（PACK）", "='01_参数台'!I20", "='01_参数台'!J20",
             "验收锚点，随当前档联动，不随 02/04 开关抬高")
    cash_row(7, "分项求和（主预算 SUM-SWITCH）", "='01_参数台'!I19", "='01_参数台'!J19",
             "公式求和，随档位与 02/04 开关联动")
    cash_row(8, "仍需一次性（主口径=头条−已发生）", "=B6-B5", "=C6-C5",
             "仍需现金=上列三档（口径原文）。改档位或已发生现金后联动。不扣 Bot。")
    cash_row(9, "差额（头条−分项；已裁决单独列示，禁止衬平）", "='01_参数台'!I21", "='01_参数台'!J21",
             "已裁决：正差=未归类余量（非已确认成本包）；负差不得用分项加总抬高头条。来自 11-07 底稿，不是算错。",
             pending=True)
    cash_row(10, "仍需一次性（对照=分项−已发生）", "=B7-B5", "=C7-C5",
             "对照口径，不替代主口径与旧稿硬对齐")
    cash_row(11, "Bot替代价值（非现金，不扣减）", "='01_参数台'!C38", "='01_参数台'!C39",
             "非现金；不可入账为已节省，未从第8/10行扣减")
    cash_row(12, "Demo期月度持续", "='01_参数台'!I26", "='01_参数台'!J26",
             "元/月；不计入一次性头条；P-003 的 19.9 元/月只作对照，不改本行")
    cash_row(13, "认证年费（占位，维持待确认）", "='01_参数台'!I27", "='01_参数台'!J27",
             "元/年；基准/完整是否同 300 待确认；P-001 为 300 元/次对照，不升格")

    # v0.2 MUST: weeks and months — wan=False
    cash_row(14, "开发周期（公历周）", "='01_参数台'!I28", "='01_参数台'!J28",
             "公历周；非 7 人天。本行不是金额：万元列留空，不对周数做 /10000（v0.2 已改正 v0.1 残留）。",
             wan=False, fmt="0", wan_note_blank=True)
    cash_row(15, "示意月数（周×7÷换算分母）",
             "=IF(OR('01_参数台'!I28=\"\",'01_参数台'!I29=0),\"\",'01_参数台'!I28*7/'01_参数台'!I29)",
             "=IF(OR('01_参数台'!J28=\"\",'01_参数台'!J29=0),\"\",'01_参数台'!J28*7/'01_参数台'!J29)",
             "示意折月，付款节奏未约定，待确认。本行不是金额：万元列留空，不对月数做 /10000（v0.2 已改正 v0.1 残留）。",
             wan=False, fmt="0.00", wan_note_blank=True)

    # B16/C16 fractional months (kept) + B17/C17 ROUNDUP alignment (v0.2 suggestion)
    cash_row(16, "示意：持续费用合计（分数月口径＝月度×示意月数＋年费）",
             '=IF(OR(B12="",B15=""),"",B12*B15+B13)',
             '=IF(OR(C12="",C15=""),"",C12*C15+C13)',
             "示意，非合同付款安排。本行用分数月。未计入营收（收入参数为空，不以 0 充当流入）。")
    cash_row(17, "示意：持续费用合计（整月口径＝月度×ROUNDUP(示意月数,0)＋年费）",
             '=IF(OR(B12="",B15=""),"",B12*ROUNDUP(B15,0)+B13)',
             '=IF(OR(C12="",C15=""),"",C12*ROUNDUP(C15,0)+C13)',
             "示意，非合同付款安排。与下方 1–12 月示意月度串（用 ROUNDUP 决定是否计整月月度）同一取整口径，便于对照。与第16行的差额来自分数月 vs 向上取整整月，不是主口径错误。")

    ws.merge_cells("A19:K19")
    ws["A19"] = (
        "示意月度流出（非合同节奏，待确认）。一次性按期初一次流出；月度按月；年费放在第 1 月。"
        "无收入流入（参数为空，不编造营收）。列示 1–12 月；仅在 ROUNDUP(示意月数) 范围内计月度。"
        "第16行（分数月）与本串加总（整月）允许不同，差额来源已在第17行对照列出。两行都不是付款计划，也不回写头条或仍需主口径。"
    )
    ws["A19"].font = FONT_SM
    ws["A19"].alignment = LEFT
    ws.row_dimensions[19].height = 36

    for i, h in enumerate(["月序", "一次性_下限", "一次性_上限", "月度_下限", "月度_上限",
                           "年费_下限", "年费_上限", "当月合计_下限", "当月合计_上限",
                           "累计_下限", "累计_上限"], 1):
        ws.cell(21, i, h)
    style_header_row(ws, 21, 1, 11)

    for m in range(1, 13):
        r = 21 + m
        ws.cell(r, 1, m)
        style_formula(ws.cell(r, 1), num=True, fmt="0")
        if m == 1:
            ws.cell(r, 2, "=$B$8")
            ws.cell(r, 3, "=$C$8")
            ws.cell(r, 6, "=$B$13")
            ws.cell(r, 7, "=$C$13")
        else:
            ws.cell(r, 2, "=0")
            ws.cell(r, 3, "=0")
            ws.cell(r, 6, "=0")
            ws.cell(r, 7, "=0")
        ws.cell(r, 4, f'=IF($B$15="","",IF({m}<=ROUNDUP($B$15,0),$B$12,0))')
        ws.cell(r, 5, f'=IF($C$15="","",IF({m}<=ROUNDUP($C$15,0),$C$12,0))')
        ws.cell(r, 8, f'=IF(OR(B{r}="",D{r}="",F{r}=""),"",B{r}+D{r}+F{r})')
        ws.cell(r, 9, f'=IF(OR(C{r}="",E{r}="",G{r}=""),"",C{r}+E{r}+G{r})')
        if m == 1:
            ws.cell(r, 10, f"=H{r}")
            ws.cell(r, 11, f"=I{r}")
        else:
            ws.cell(r, 10, f'=IF(OR(J{r-1}="",H{r}=""),"",J{r-1}+H{r})')
            ws.cell(r, 11, f'=IF(OR(K{r-1}="",I{r}=""),"",K{r-1}+I{r})')
        for c in range(1, 12):
            style_formula(ws.cell(r, c))

    # verification: sum of series opex+cert should match row 17 (whole-month)
    ws.merge_cells("A35:K35")
    ws["A35"] = (
        "校验（公式，非主口径）：示意串「月度+年费」加总下限=SUM(D22:D33)+SUM(F22:F33)，应与第17行下限一致（整月口径）。"
        "本表不含 B/C/D 支出，不含编造的收入流入。改参数台档位、头条、已发生现金、月度或年费后，本表公式全部联动。"
        "示意月度串不是付款计划。"
    )
    ws["A35"].font = FONT_SM
    ws["A35"].alignment = LEFT

    ws["A36"] = "示意串月度+年费加总_下限（整月）"
    ws["B36"] = '=IF(OR(B12="",B15=""),"",SUM(D22:D33)+SUM(F22:F33))'
    style_formula(ws["B36"])
    ws["C36"] = "示意串月度+年费加总_上限（整月）"
    ws["D36"] = '=IF(OR(C12="",C15=""),"",SUM(E22:E33)+SUM(G22:G33))'
    style_formula(ws["D36"])
    ws["E36"] = "与第17行差额_下限（应为0）"
    ws["F36"] = '=IF(OR(B17="",B36=""),"",B36-B17)'
    style_formula(ws["F36"])
    ws["G36"] = "与第17行差额_上限（应为0）"
    ws["H36"] = '=IF(OR(C17="",D36=""),"",D36-C17)'
    style_formula(ws["H36"])

    ws.sheet_view.showGridLines = False
    return ws


def build_revenue(wb):
    ws = wb.create_sheet("04_收入与收支结构")
    ws.sheet_properties.tabColor = "C65911"
    set_widths(ws, {"A": 18, "B": 36, "C": 28, "D": 22, "E": 22, "F": 22, "G": 22, "H": 28, "I": 24, "J": 40})
    ws.merge_cells("A1:J1")
    ws["A1"] = (
        "收入与不同模式收支结构（已并入已验收 Revenue 参数 ID；全部待研究，非已确定商业决策；"
        "参数未到则结果留空，不以 0 冒充已测算）"
    )
    ws["A1"].font = FONT_WHITE
    ws["A1"].fill = FILL_TITLE
    for col in range(1, 11):
        ws.cell(1, col).fill = FILL_TITLE
        ws.cell(1, col).font = FONT_WHITE

    ws.merge_cells("A2:J2")
    ws["A2"] = (
        "输入全部在参数台 E 区（G-04:G-07、A-01:E-04）。必要因子为空时公式输出空白。"
        "净收入=毛收入×(1−G-06)，仅当 G-06 已填；不把空扣点当作 0。"
        "G-07 为空时不扣变动成本，也不把空值当 0 去填单位贡献。"
        "五种模式当前均为待研究方向。确认前不要把汇总行当作可对外引用的收入预测（须先排除双计）。"
    )
    ws["A2"].font = FONT_SM
    ws["A2"].alignment = LEFT
    ws.row_dimensions[2].height = 36

    # general params display
    ws["A4"] = "通用参数（公式引用，空则空）"
    ws["A4"].font = FONT_H
    for i, h in enumerate(["参数ID", "名称", "数值", "单位", "状态"], 1):
        ws.cell(5, i, h)
    style_header_row(ws, 5, 1, 5)
    generals = [
        (6, "G-04", "测算期月数", "C51", "个公历月"),
        (7, "G-05", "含税口径", "C52", "0/1"),
        (8, "G-06", "平台或渠道扣点率", "C53", "小数"),
        (9, "G-07", "单均变动成本（可选）", "C54", "元/单位"),
    ]
    for r, pid, name, cell, unit in generals:
        ws.cell(r, 1, pid)
        ws.cell(r, 2, name)
        ws.cell(r, 3, if_blank(f"'01_参数台'!{cell}"))
        style_formula(ws.cell(r, 3), num=False)
        if pid == "G-06":
            ws.cell(r, 3).number_format = PCT
        elif pid == "G-04":
            ws.cell(r, 3).number_format = "0"
        else:
            ws.cell(r, 3).number_format = YUAN2
        ws.cell(r, 4, unit)
        ws.cell(r, 5, f'=IF(C{r}="","待确认：参数为空","已填（仍属待研究/结构约定）")')
        style_formula(ws.cell(r, 5), num=False)
        style_text(ws.cell(r, 1))
        style_text(ws.cell(r, 2))
        style_text(ws.cell(r, 4))

    # mode blocks
    # We'll list line items starting row 11
    headers = ["模式/子线", "公式说明", "毛收入（公式）", "净收入（公式，须G-06）",
               "因子1", "因子2", "因子3", "状态"]
    ws.merge_cells("A11:H11")
    ws["A11"] = "分模式测算（全部公式；空则空）"
    ws["A11"].font = FONT_WHITE
    ws["A11"].fill = FILL_SECTION
    for col in range(1, 9):
        ws.cell(11, col).fill = FILL_SECTION
        ws.cell(11, col).font = FONT_WHITE
    for i, h in enumerate(headers, 1):
        ws.cell(12, i, h)
    style_header_row(ws, 12, 1, 8)

    # Helper to add a product line. factors are param cells like '01_参数台'!C57
    def line(r, title, desc, factors, fmt=YUAN):
        ws.cell(r, 1, title).font = FONT_B
        ws.cell(r, 1).border = THIN
        ws.cell(r, 2, desc)
        style_text(ws.cell(r, 2))
        if len(factors) == 2:
            ws.cell(r, 3, product2(factors[0], factors[1]))
        else:
            ws.cell(r, 3, product3(factors[0], factors[1], factors[2]))
        style_formula(ws.cell(r, 3), fmt=fmt)
        ws.cell(r, 4, f'=IF(OR(C{r}="",\'01_参数台\'!C53=""),"",C{r}*(1-\'01_参数台\'!C53))')
        style_formula(ws.cell(r, 4), fmt=fmt)
        for i, f in enumerate(factors):
            ws.cell(r, 5 + i, if_blank(f))
            style_formula(ws.cell(r, 5 + i), num=False)
        ws.cell(r, 8, f'=IF(C{r}="","待确认：参数为空，未测算","已按输入试算（仍属待研究情景）")')
        style_formula(ws.cell(r, 8), num=False)

    def subtotal(r, title, children):
        ws.cell(r, 1, title).font = FONT_B
        ws.cell(r, 1).border = THIN
        ws.cell(r, 2, "全空则空，不把空当 0")
        style_text(ws.cell(r, 2))
        cells = [f"C{c}" for c in children]
        ws.cell(r, 3, sum_if_any(*cells))
        style_formula(ws.cell(r, 3))
        ws.cell(r, 4, f'=IF(OR(C{r}="",\'01_参数台\'!C53=""),"",C{r}*(1-\'01_参数台\'!C53))')
        style_formula(ws.cell(r, 4))
        ws.cell(r, 8, f'=IF(C{r}="","待确认：参数为空，未测算","已按输入试算（仍属待研究情景；加总前须排除双计）")')
        style_formula(ws.cell(r, 8), num=False)

    P = "'01_参数台'"
    line(13, "A1 项目制", "A-01×A-02", [f"{P}!C57", f"{P}!C58"])
    line(14, "A2 年框", "A-03×A-04（须与 A1 防双计）", [f"{P}!C59", f"{P}!C60"])
    line(15, "A3 C端", "A-05×A-06×A-07", [f"{P}!C61", f"{P}!C62", f"{P}!C63"])
    subtotal(16, "A 小程序/AR互动 小计", [13, 14, 15])

    line(18, "B1 内容包", "B-01×B-02", [f"{P}!C66", f"{P}!C67"])
    line(19, "B2 订阅", "B-03×B-04×B-05", [f"{P}!C68", f"{P}!C69", f"{P}!C70"])
    subtotal(20, "B IP内容与数字产品 小计", [18, 19])

    line(22, "C1 授权金", "C-01×C-02", [f"{P}!C73", f"{P}!C74"])
    line(23, "C2 分成", "C-03×C-04", [f"{P}!C75", f"{P}!C76"])
    line(24, "C3 联名项目", "C-05×C-06（须与 A/D 防双计）", [f"{P}!C77", f"{P}!C78"])
    subtotal(25, "C 授权联名 小计", [22, 23, 24])

    line(27, "D1 单店年费/服务费", "D-01×D-02（禁止把 P-020 的 2400 填入 D-02）", [f"{P}!C81", f"{P}!C82"])
    line(28, "D2 试点项目款", "D-03×D-04（须与 D1 防双计）", [f"{P}!C83", f"{P}!C84"])
    line(29, "D3 主题房溢价分成", "D-05×D-06×D-07", [f"{P}!C85", f"{P}!C86", f"{P}!C87"])
    subtotal(30, "D 酒店文旅 小计", [27, 28, 29])

    line(32, "E1 衍生品", "E-01×E-02", [f"{P}!C90", f"{P}!C91"])
    line(33, "E2 线下体验", "E-03×E-04", [f"{P}!C92", f"{P}!C93"])
    subtotal(34, "E 衍生品与线下体验 小计", [32, 33])

    subtotal(36, "五种模式毛收入合计", [16, 20, 25, 30, 34])
    ws["B36"] = "全空则空。确认前不要把本行当作可对外引用的收入预测（须先排除双计）。"
    style_text(ws["B36"], FILL_GAP)

    ws["A37"] = "万元摘要（仅当合计非空）"
    ws["C37"] = '=IF(C36="","",C36/10000)'
    style_formula(ws["C37"], fmt=WAN)
    ws["D37"] = '=IF(D36="","",D36/10000)'
    style_formula(ws["D37"], fmt=WAN)
    ws["E37"] = "万元=元/10000，不改变表内「元」主口径"
    style_text(ws["E37"])

    ws.merge_cells("A39:J39")
    ws["A39"] = (
        "获客成本、税费、渠道分成等：G-06/G-07 当前为空，不编造。官方抽成对照见 09 表 P-011 至 P-018，不自动写入 G-06。"
        "不要把本表空白解读为收入为 0。模式名称与驱动因子来自已验收 Revenue（CFO-验收-REV-20261112.md）。"
    )
    ws["A39"].font = FONT_SM
    ws["A39"].alignment = LEFT
    ws.sheet_view.showGridLines = False
    return ws


def build_breakeven(wb):
    ws = wb.create_sheet("05_盈亏平衡")
    ws.sheet_properties.tabColor = "833C0C"
    set_widths(ws, {c: 16 for c in "ABCDEFGHIJKLM"})
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 28
    ws.column_dimensions["C"].width = 22

    ws.merge_cells("A1:M1")
    ws["A1"] = (
        "盈亏平衡（必须写明：相对哪一档成本、哪一收入模式/子线、哪些固定/变动成本；"
        "缺收入参数留空，禁止倒推看起来合理的数）"
    )
    ws["A1"].font = FONT_WHITE
    ws["A1"].fill = FILL_TITLE
    for col in range(1, 14):
        ws.cell(1, col).fill = FILL_TITLE
        ws.cell(1, col).font = FONT_WHITE

    ws["A3"] = "相对成本档位（随参数台 C3 联动，不是已锁定档位）"
    ws["B3"] = "='01_参数台'!C3"
    style_formula(ws["B3"], num=False)
    ws.merge_cells("C3:F3")
    ws["C3"] = "本表所有「所需量/所需单价」均相对这一档计算，三档可切换。"
    ws["C3"].font = FONT_SM

    ws["A4"] = "固定成本口径A：仍需一次性_主口径（PACK头条−已发生）下限"
    ws["B4"] = "='03_现金流'!B8"
    style_formula(ws["B4"])
    ws["C4"] = "上限"
    ws["D4"] = "='03_现金流'!C8"
    style_formula(ws["D4"])
    ws.merge_cells("E4:H4")
    ws["E4"] = "用于「一次性投入回本」。不扣 Bot，不混入 B/C/D，不随 02/04 开关抬高（因头条不抬高）。"
    ws["E4"].font = FONT_SM

    ws["A5"] = "固定成本口径B：Demo期月度持续下限"
    ws["B5"] = "='01_参数台'!I26"
    style_formula(ws["B5"])
    ws["C5"] = "上限"
    ws["D5"] = "='01_参数台'!J26"
    style_formula(ws["D5"])
    ws.merge_cells("E5:H5")
    ws["E5"] = "用于「月度平衡」：覆盖当月持续费用，不含一次性摊销，也不含年费。"
    ws["E5"].font = FONT_SM

    ws["A6"] = "年费（单独列，不并入月度平衡，以免口径含混）"
    ws["B6"] = "='01_参数台'!I27"
    style_formula(ws["B6"])
    ws["C6"] = "上限"
    ws["D6"] = "='01_参数台'!J27"
    style_formula(ws["D6"])

    ws.merge_cells("A7:M7")
    ws["A7"] = (
        "单位收入口径：①按毛单价=子线单价（不把空的 G-07 当 0 来扣减；G-07 已填时见「按单位贡献」列，本版所需量主列用毛单价，与已验收 Revenue 03 表一致）；"
        "②按净单价=毛单价×(1−G-06)，仅当 G-06 已填。"
        "所需量=固定成本÷单位收入；所需单价=固定成本÷已填数量（口径A）。"
        "单位收入、数量或固定成本为空，或分母≤0，则结果留空。当前收入参数均为空，故结果应为空白。"
    )
    ws["A7"].font = FONT_SM
    ws["A7"].alignment = LEFT
    ws.row_dimensions[7].height = 48

    headers = [
        "子线ID", "收入模式（待研究）", "毛单价（公式，空则空）", "数量（公式，空则空）",
        "按毛单价：回本所需量_下限（口径A）", "按毛单价：回本所需量_上限（口径A）",
        "回本所需单价_下限（口径A，须有数量）", "回本所需单价_上限（口径A，须有数量）",
        "月度平衡所需量_下限（口径B，按毛单价）", "月度平衡所需量_上限（口径B，按毛单价）",
        "按净单价：回本所需量_下限（口径A，须G-06）", "按净单价：回本所需量_上限（口径A，须G-06）",
        "状态",
    ]
    for i, h in enumerate(headers, 1):
        ws.cell(9, i, h)
    style_header_row(ws, 9, 1, 13)

    # Map each subunit: title, mode name, unit-price source, qty source
    # Price/qty are already empty-safe on 04 sheet factor columns, but we'll pull from 参数台 directly.
    lines = [
        (10, "A1", "A 小程序/AR互动 · 项目制", "'01_参数台'!C57", "'01_参数台'!C58"),
        (11, "A2", "A 小程序/AR互动 · 年框", "'01_参数台'!C59", "'01_参数台'!C60"),
        (12, "A3", "A 小程序/AR互动 · C端（人均单价）", "'01_参数台'!C62", None),  # qty = users*times, more complex
        (13, "B1", "B IP内容与数字产品 · 内容包", "'01_参数台'!C66", "'01_参数台'!C67"),
        (14, "B2", "B IP内容与数字产品 · 订阅（每期单价）", "'01_参数台'!C68", None),
        (15, "C1", "C 授权联名 · 授权金", "'01_参数台'!C73", "'01_参数台'!C74"),
        (16, "C2", "C 授权联名 · 分成（单位=分成基数的「1 元基数」不适用于量；本行数量用 C-04 须谨慎）",
         "'01_参数台'!C73", "'01_参数台'!C74"),  # C2 is rate*base, not a simple unit price — leave special
        (17, "C3", "C 授权联名 · 联名项目", "'01_参数台'!C77", "'01_参数台'!C78"),
        (18, "D1", "D 酒店文旅 · 单店年费/服务费", "'01_参数台'!C81", "'01_参数台'!C82"),
        (19, "D2", "D 酒店文旅 · 试点项目款", "'01_参数台'!C83", "'01_参数台'!C84"),
        (20, "E1", "E 衍生品与线下体验 · 衍生品", "'01_参数台'!C90", "'01_参数台'!C91"),
        (21, "E2", "E 衍生品与线下体验 · 线下体验", "'01_参数台'!C92", "'01_参数台'!C93"),
    ]
    # For A3, quantity for "所需单价" could be A-05*A-07 (users*times) when both filled; unit = A-06
    # For B2, qty = B-04*B-05, unit = B-03
    # For C2 (share): unit income = C-03 (rate) applied to base — this is messy. Better treat
    # unit income as empty unless both rate and we define 所需分成基数 = 固定成本/费率.
    # I'll handle C2 separately: 毛「单位收入」用费率，所需「分成基数」=固定成本/费率（当费率已填）。
    # To keep it consistent: C2 price cell = C-03 (rate), qty = C-04 (base). 所需量 would be 所需基数.
    # Let me fix C2 in the list: unit=C-03, qty=C-04. 所需量 = 固定成本/费率, meaning required sales base if rate is the "unit".
    # Actually 所需量 = 固定成本 / (费率) would be the required base, yes, when qty is the base.
    # Wait: if unit income = rate (0.01) that's not money. Break-even needed base = 固定成本 / rate.
    # "所需单价" doesn't make as much sense. I'll still use the same formula structure:
    # 所需量 = 固定成本 / C3(rate) only if we treat rate as unit income — that's dimensionally "元 ÷ 比率 = 元" = required base. OK if labeled.
    # Let me change C2 name already says 须谨慎. I'll set unit income for C2 to formula: if C-03 filled then C-03 else blank,
    # and 所需量 = 固定成本/C-03 (= required base). Don't use C-03 as if it were 元.

    # I'll special-case A3, B2, C2, D3 in writing.

    def be_row(r, sid, mode, price_src, qty_src, qty_formula=None, unit_formula=None, note_qty="数量"):
        ws.cell(r, 1, sid).font = FONT_B
        ws.cell(r, 1).border = THIN
        ws.cell(r, 2, mode)
        style_text(ws.cell(r, 2))
        if unit_formula:
            ws.cell(r, 3, unit_formula)
        else:
            ws.cell(r, 3, if_blank(price_src))
        style_formula(ws.cell(r, 3), num=False)
        ws.cell(r, 3).number_format = YUAN2
        if qty_formula:
            ws.cell(r, 4, qty_formula)
        elif qty_src:
            ws.cell(r, 4, if_blank(qty_src))
        else:
            ws.cell(r, 4, '=""')
        style_formula(ws.cell(r, 4), num=False)
        # 所需量 口径A 按毛单价
        ws.cell(r, 5, f'=IF(OR(C{r}="",C{r}<=0,$B$4=""),"",$B$4/C{r})')
        ws.cell(r, 6, f'=IF(OR(C{r}="",C{r}<=0,$D$4=""),"",$D$4/C{r})')
        # 所需单价 口径A 须有数量
        ws.cell(r, 7, f'=IF(OR(D{r}="",D{r}<=0,$B$4=""),"",$B$4/D{r})')
        ws.cell(r, 8, f'=IF(OR(D{r}="",D{r}<=0,$D$4=""),"",$D$4/D{r})')
        # 月度平衡 口径B
        ws.cell(r, 9, f'=IF(OR(C{r}="",C{r}<=0,$B$5=""),"",$B$5/C{r})')
        ws.cell(r, 10, f'=IF(OR(C{r}="",C{r}<=0,$D$5=""),"",$D$5/C{r})')
        # 按净单价 须 G-06（嵌套 IF，避免 OR 对空的 G-06 做算术而产生 #VALUE!）
        ws.cell(r, 11, f'=IF(C{r}="","",IF(OR(C{r}<=0,$B$4=""),"",IF(\'01_参数台\'!C53="","",IF((C{r}*(1-\'01_参数台\'!C53))<=0,"",$B$4/(C{r}*(1-\'01_参数台\'!C53))))))')
        ws.cell(r, 12, f'=IF(C{r}="","",IF(OR(C{r}<=0,$D$4=""),"",IF(\'01_参数台\'!C53="","",IF((C{r}*(1-\'01_参数台\'!C53))<=0,"",$D$4/(C{r}*(1-\'01_参数台\'!C53))))))')
        ws.cell(r, 13, f'=IF(AND(C{r}="",D{r}=""),"待确认：参数为空，未测算",IF(C{r}="","待确认：单价为空，未测算","已按输入试算（仍属待研究；相对当前档 "+$B$3+"）"))')
        for c in range(5, 13):
            style_formula(ws.cell(r, c))
        style_formula(ws.cell(r, 13), num=False)

    be_row(10, "A1", "A 小程序/AR互动 · 项目制", "'01_参数台'!C57", "'01_参数台'!C58")
    be_row(11, "A2", "A 小程序/AR互动 · 年框", "'01_参数台'!C59", "'01_参数台'!C60")
    be_row(12, "A3", "A 小程序/AR互动 · C端（单价=A-06；数量=A-05×A-07，须两因子皆填）",
           "'01_参数台'!C62", None,
           qty_formula='=IF(COUNT(\'01_参数台\'!C61,\'01_参数台\'!C63)<2,"",\'01_参数台\'!C61*\'01_参数台\'!C63)')
    be_row(13, "B1", "B IP内容与数字产品 · 内容包", "'01_参数台'!C66", "'01_参数台'!C67")
    be_row(14, "B2", "B IP内容与数字产品 · 订阅（单价=B-03；数量=B-04×B-05，须两因子皆填）",
           "'01_参数台'!C68", None,
           qty_formula='=IF(COUNT(\'01_参数台\'!C69,\'01_参数台\'!C70)<2,"",\'01_参数台\'!C69*\'01_参数台\'!C70)')
    be_row(15, "C1", "C 授权联名 · 授权金", "'01_参数台'!C73", "'01_参数台'!C74")
    be_row(16, "C2", "C 授权联名 · 分成（「单价」取分成费率 C-03；所需量=所需分成基数，仅当费率已填）",
           "'01_参数台'!C75", "'01_参数台'!C76")
    be_row(17, "C3", "C 授权联名 · 联名项目", "'01_参数台'!C77", "'01_参数台'!C78")
    be_row(18, "D1", "D 酒店文旅 · 单店年费/服务费", "'01_参数台'!C81", "'01_参数台'!C82")
    be_row(19, "D2", "D 酒店文旅 · 试点项目款", "'01_参数台'!C83", "'01_参数台'!C84")
    be_row(20, "D3", "D 酒店文旅 · 主题房溢价分成（单位收入=D-05×D-07，须两因子皆填；数量=D-06）",
           None, "'01_参数台'!C86",
           unit_formula='=IF(COUNT(\'01_参数台\'!C85,\'01_参数台\'!C87)<2,"",\'01_参数台\'!C85*\'01_参数台\'!C87)')
    be_row(21, "E1", "E 衍生品与线下体验 · 衍生品", "'01_参数台'!C90", "'01_参数台'!C91")
    be_row(22, "E2", "E 衍生品与线下体验 · 线下体验", "'01_参数台'!C92", "'01_参数台'!C93")

    # C2 rate format
    ws["C16"].number_format = PCT

    ws.merge_cells("A24:M25")
    ws["A24"] = (
        "v0.2：五种收入模式参数（A-01 至 E-04、G-06、G-07）均为空，故第10–22行所需量、所需单价应为空白，"
        "这是符合验收的结果，不是遗漏计算。填入参数台相应因子后，将按当前档一次性仍需（口径A，相对 B3 所示档位）"
        "与当月持续费用（口径B）自动计算。本表不把认证年费摊进月度平衡，也不把 B/C/D 成本并入固定成本，未使用人天费率倒推平衡点。"
        "覆盖一次性 Demo 对照成本，并不等于完整经营盈亏平衡。官方 19.9 元/月（P-003）不进入本表固定成本。"
    )
    ws["A24"].font = FONT_SM
    ws["A24"].alignment = LEFT
    ws.row_dimensions[24].height = 30
    ws.row_dimensions[25].height = 30
    ws.sheet_view.showGridLines = False
    return ws


def build_appendix(wb):
    ws = wb.create_sheet("06_附录BCD")
    ws.sheet_properties.tabColor = "8064A2"
    set_widths(ws, {"A": 28, "B": 42, "C": 18, "D": 18, "E": 16, "F": 16, "G": 48, "H": 24})

    ws.merge_cells("A1:H1")
    ws["A1"] = "附录：B/C/D 阶段区间与分项（Cost 已验收情景，待专项复核）— 严禁混入 A 阶段合计或 A 现金流主表"
    ws["A1"].font = FONT_WHITE
    ws["A1"].fill = FILL_TITLE
    for col in range(1, 9):
        ws.cell(1, col).fill = FILL_TITLE
        ws.cell(1, col).font = FONT_WHITE

    ws.merge_cells("A2:H2")
    ws["A2"] = (
        "本表数字全部链接参数台 D 区与 G 区。不进入 02/03/00/05 合计。不是本轮主算。"
        "空参数必须显示为空白：先判断参数台源格是否为空，不用直接引用，也不用 D 列=\"\" 去识别被引用成 0 的空值。"
    )
    ws["A2"].font = FONT_SM
    ws["A2"].alignment = LEFT

    for i, h in enumerate(["阶段/编码", "含义（口径原文）", "下限（元）", "上限（元）",
                           "下限（万元）", "上限（万元）", "状态", "空值规则"], 1):
        ws.cell(4, i, h)
    style_header_row(ws, 4, 1, 8)

    def wan_pair(r, lo_src_is_cell=True):
        # 万元：判断对应元列来源或本表 C/D，但 D 上限必须 look at source C47 not D7=""
        pass

    # B total
    ws["A5"] = "B 产品验证（B-TOTAL）"
    ws["B5"] = "真实用户走完/愿再开/想留"
    ws["C5"] = "='01_参数台'!C42"
    ws["D5"] = "='01_参数台'!C43"
    style_formula(ws["C5"])
    style_formula(ws["D5"])
    ws["E5"] = '=IF(\'01_参数台\'!C42="","",C5/10000)'
    ws["F5"] = '=IF(\'01_参数台\'!C43="","",D5/10000)'
    style_formula(ws["E5"], fmt=WAN)
    style_formula(ws["F5"], fmt=WAN)
    style_text(ws["G5"], FILL_PENDING)
    ws["G5"] = "待专项复核；不得混入 A"
    style_text(ws["H5"])
    ws["H5"] = "源格已填，直接引用安全"

    ws["A6"] = "C 商业试点（C-TOTAL）"
    ws["B6"] = "小规模试点 1–3 月感"
    ws["C6"] = "='01_参数台'!C44"
    ws["D6"] = "='01_参数台'!C45"
    style_formula(ws["C6"])
    style_formula(ws["D6"])
    ws["E6"] = '=IF(\'01_参数台\'!C44="","",C6/10000)'
    ws["F6"] = '=IF(\'01_参数台\'!C45="","",D6/10000)'
    style_formula(ws["E6"], fmt=WAN)
    style_formula(ws["F6"], fmt=WAN)
    style_text(ws["G6"], FILL_PENDING)
    ws["G6"] = "待专项复核；不得混入 A"
    style_text(ws["H6"])
    ws["H6"] = "源格已填，直接引用安全"

    # D total — MUST blank-safe on C47 for D7 and F7
    ws["A7"] = "D 规模化（D-TOTAL）"
    ws["B7"] = "多渠道；若上硬件则供应链单列"
    ws["C7"] = '=IF(\'01_参数台\'!C46="","",\'01_参数台\'!C46)'
    # v0.2 MUST fix: judge 01_参数台!C47 emptiness first; do not bare-reference; do not rely on D7="" to catch 0
    ws["D7"] = '=IF(\'01_参数台\'!C47="","",\'01_参数台\'!C47)'
    style_formula(ws["C7"])
    style_formula(ws["D7"], pending=True)
    ws["E7"] = '=IF(\'01_参数台\'!C46="","",C7/10000)'
    ws["F7"] = '=IF(\'01_参数台\'!C47="","",D7/10000)'
    style_formula(ws["E7"], fmt=WAN)
    style_formula(ws["F7"], pending=True, fmt=WAN)
    style_text(ws["G7"], FILL_PENDING)
    ws["G7"] = "上限旧稿为「数百万+」，参数台 C47 留空未倒推；待专项复核；不得混入 A。C47 为空时本行上限（D7/F7）必须为空白，不得显示 0。"
    style_text(ws["H7"], FILL_NOTE)
    ws["H7"] = "D7/F7 先判断 01_参数台!C47 是否为空；不得编造上限"

    # detail section
    ws.merge_cells("A9:H9")
    ws["A9"] = "B/C/D 分项（Cost 已验收编码；仅附录；不替代上表粗区间，不计入 A）"
    ws["A9"].font = FONT_WHITE
    ws["A9"].fill = FILL_SECTION
    for col in range(1, 9):
        ws.cell(9, col).fill = FILL_SECTION
        ws.cell(9, col).font = FONT_WHITE

    def app_row(r, title, meaning, lo_src, hi_src, status):
        ws.cell(r, 1, title).font = FONT_B
        ws.cell(r, 1).border = THIN
        ws.cell(r, 2, meaning)
        style_text(ws.cell(r, 2))
        ws.cell(r, 3, f'=IF({lo_src}="","",{lo_src})')
        ws.cell(r, 4, f'=IF({hi_src}="","",{hi_src})')
        style_formula(ws.cell(r, 3), pending=(hi_src.endswith("D133") or "C134" in lo_src))
        style_formula(ws.cell(r, 4), pending=True)
        ws.cell(r, 5, f'=IF({lo_src}="","",C{r}/10000)')
        ws.cell(r, 6, f'=IF({hi_src}="","",D{r}/10000)')
        style_formula(ws.cell(r, 5), fmt=WAN)
        style_formula(ws.cell(r, 6), fmt=WAN)
        style_text(ws.cell(r, 7, status), FILL_PENDING)
        style_text(ws.cell(r, 8, "先判断源格是否为空"))

    app_row(10, "B-DEV", "B · 迭代开发", "'01_参数台'!C124", "'01_参数台'!D124", "仅附录；不得混入 A")
    app_row(11, "B-REC", "B · 招募礼品访谈（非规模化 CAC）", "'01_参数台'!C125", "'01_参数台'!D125", "仅附录；不得混入 A")
    app_row(12, "B-RPT", "B · 分析报告", "'01_参数台'!C126", "'01_参数台'!D126", "仅附录；不得混入 A")
    app_row(13, "B-CHECK", "B 分项算术", "'01_参数台'!C127", "'01_参数台'!D127", "校验，不替代 B-TOTAL")
    app_row(14, "B-GAP", "B 分项算术 − B 粗区间（低列预期 3,000，不衬平）", "'01_参数台'!C128", "'01_参数台'!D128", "已披露差额，不编造调平项")
    app_row(15, "C-PROD", "C · 产品增量（不是 A 的 02/04）", "'01_参数台'!C129", "'01_参数台'!D129", "仅附录；不得混入 A")
    app_row(16, "C-MAT", "C · 台卡物料（A 阶段台卡后置）", "'01_参数台'!C130", "'01_参数台'!D130", "仅附录；不得混入 A")
    app_row(17, "C-OPS", "C · 驻场运营（元/月；月数未定，不自动相乘）", "'01_参数台'!C131", "'01_参数台'!D131", "月级，不与一次性分项加总")
    app_row(18, "D-SW", "D · 软件中台/客服（首年感；高列只取写出的 80 万，「+」未量化）", "'01_参数台'!C132", "'01_参数台'!D132", "仅附录；不得混入 A")
    app_row(19, "D-MKT", "D · 市场推广（上沿「数百万」高列留空，不编造）", "'01_参数台'!C133", "'01_参数台'!D133", "高列源格为空时应显示空白而非 0")
    app_row(20, "D-HW", "D · 硬件量产模具+首批（红线后置；低/高均留空）", "'01_参数台'!C134", "'01_参数台'!D134", "低/高源格均为空，应显示空白而非 0；不列为本轮已定投入")

    ws.merge_cells("A22:H22")
    ws["A22"] = (
        "硬件量产、完整商业化软件系统、酒店规模化部署不列为本轮必须完成或已确定投入。"
        "D 若上硬件须供应链单列，本附录未编造供应链数字或 D 上限。"
        "v0.2 已改正 v0.1 附录 D7 直接引用空参数导致重算显示 0 的展示问题。"
    )
    ws["A22"].font = FONT_SM
    ws["A22"].alignment = LEFT
    ws.sheet_view.showGridLines = False
    ws.row_dimensions[7].height = 36
    return ws


def build_pending(wb):
    ws = wb.create_sheet("07_待确认清单")
    ws.sheet_properties.tabColor = "C65911"
    set_widths(ws, {"A": 10, "B": 52, "C": 64, "D": 40, "E": 28, "F": 22})
    ws.merge_cells("A1:F1")
    ws["A1"] = "待确认清单（v0.2；并入 Cost / Revenue / Benchmark v1.1 已验收待确认项的模型相关条目）"
    ws["A1"].font = FONT_WHITE
    ws["A1"].fill = FILL_TITLE
    for col in range(1, 7):
        ws.cell(1, col).fill = FILL_TITLE
        ws.cell(1, col).font = FONT_WHITE

    ws.merge_cells("A2:F2")
    ws["A2"] = "本清单不是已经向用户提交的正式请示。确认前，对应数值保持空白或维持占位并标注。本件未自审。"
    ws["A2"].font = FONT_SM

    for i, h in enumerate(["序号", "事项", "当前状态（公式或说明）", "影响", "建议裁决人", "是否阻断 v0.2 交稿"], 1):
        ws.cell(3, i, h)
    style_header_row(ws, 3, 1, 6)

    items = [
        ("T01", "预算档位（精益/基准/完整）用户尚未锁定",
         '="当前展示档："&\'01_参数台\'!C3&"（默认基准仅为旧稿建议首选，不是已定案）"',
         "所有当前档结果随 C3 切换，不得写成已定案", "用户（经 CFO/CEO，不由本 Bot 越级）", "否：三档可切换已交付"),
        ("T02", "A 阶段全部分项与头条均为待询价，非合同价、非已批准预算",
         "待 2–3 家询价后回填参数台分项/头条",
         "绝对额可能变化，但结构与公式已就绪", "CFO 组织询价", "否"),
        ("T03", "已发生现金 ≈ 0（H8）待票据回填",
         '="参数台已发生现金="&TEXT(\'01_参数台\'!C32,"#,##0")&" 元"',
         "回填后仍需一次性=头条−已发生 自动变", "CFO / 票据持有人", "否"),
        ("T04", "分项求和与旧稿头条合计存在差额（已裁决，不再待裁决）",
         '="当前档差额下限="&TEXT(\'01_参数台\'!I21,"#,##0")&"；上限="&TEXT(\'01_参数台\'!J21,"#,##0")&"。已裁决：单独列示、禁止衬平；正差=未归类余量；完整档负差不得用分项加总抬高头条。"',
         "仍需主口径按头条对齐；差额单独列示，无虚拟补差行", "已由 CMQ-CFO 裁决（MODEL v0.1 / COST）", "否：已按裁决实现"),
        ("T05", "完整档 02/04 可选是否纳入分项合计（纳入不得自动抬高头条）",
         '="含02="&\'01_参数台\'!C4&"；含04="&\'01_参数台\'!C5',
         "开关为「是」时完整分项合计上升，差额更负；PACK 与仍需主口径不变", "CMQ-CFO / 用户（不越级）", "否：默认不含"),
        ("T06", "基准/完整认证年费是否与精益同为 300 元/年（维持待确认，不升格）",
         "旧稿仅对精益写明 300，本表按同额占位。P-001：官方为微信认证 300 元/次，不一定支付（企业可对公打款），官方未把「每年」写成小程序口径（Benchmark T-001/T-002）。",
         "影响现金流年费与示意月度串；不改 PACK", "CMQ-CFO", "否：已占位并标注"),
        ("T07", "五种收入模式参数（A-01 至 E-04 及 G-05/G-06/G-07）均为空",
         '="A1状态："&\'04_收入与收支结构\'!H13&"；五种模式合计："&IF(\'04_收入与收支结构\'!C36="","空白（符合缺参数不倒推）","非空")',
         "收入与盈亏平衡量/单价留空，符合「缺参数不倒推」", "见 Revenue Q-00 至 Q-19；不越级请用户拍板", "否：结构已并入"),
        ("T08", "已验收 Cost / Revenue / Benchmark v1.1 已并入本版（不再是「尚未引入」）",
         "v0.2 已引用 Cost 编码 A01–A08/PACK/GAP 与 B/C/D 分项；Revenue 参数 ID；Benchmark v1.1 的 P-001 至 P-020。禁止再用 Benchmark 第一版分项或已作废中值差。",
         "收入结果仍为空；官方价目只作对照，不改总包", "已并入，待后续回填确认项", "否"),
        ("T09", "B/C/D 区间待专项复核；D 上限旧稿为「数百万+」已留空（展示不得为 0）",
         '="D上限源格C47为空? "&IF(\'01_参数台\'!C47="","是（附录D7应空白）","否")',
         "不影响 A 主算；附录须保持空白而非 0", "CFO 专项复核", "否"),
        ("T10", "人天费率 550/830/1290 与外包 1200–2000 仅为折算锚点（P-RATE / P-OUT；T-009）",
         "未用来倒推已确认人天或替代分项报价",
         "禁止把折算写成合同成本", "询价后回填", "否"),
        ("T11", "示意月数换算（周×7÷30）及分数月 vs 整月示意串的取整口径",
         "参数台 DAYS_M 可改；03 表第16行为分数月，第17行与月度串为 ROUNDUP 整月，差额来源已加注。非合同安排。",
         "仅影响示意层，不影响头条与仍需主口径", "CMQ-CFO", "否"),
        ("T12", "含税与否、A05 与期间云/认证是否部分重叠（Cost P3/P6；Revenue Q-02）",
         "云+认证一次性已单列；认证年费另列；含税未拆；G-05 为空",
         "询价时应按口径第7节补全字段", "询价模板", "否"),
        ("T13", "02/04 可选的业务内容未在模型中展开（仅金额区间）；完整档打包是否已含 02/04（Cost P5）",
         "金额来自旧稿完整档可选包；纳入不得自动抬高头条",
         "不影响默认主预算（开关=否）", "产品/CFO", "否"),
        ("T14", "官方云价 19.9 元/月（P-003）与旧稿持续月费如何衔接（Benchmark T-010）",
         "本模型只并排对照，不把 19.9 写入 OPEX_M，不改 PACK 总包。免费环境有截止日期（P-005，至 2026-12-31）。",
         "不改变 A 阶段主口径", "成本线对照，不由模型改档", "否"),
        ("T15", "收入侧扣点/变动成本/模式优先级与防双计（Revenue Q-03/Q-04/Q-19）",
         "G-06/G-07 为空；P-011 至 P-018 只作对照，不自动写入 G-06；五种模式不简单加总对外引用",
         "有参数后再算净收入与单位贡献", "与 Revenue 对齐后回填，不得填经验 CAC", "否"),
        ("T16", "B 分项低与粗区间低差 3,000 元（Cost P11）；C 月数未定；D 多项上沿非闭区间",
         "附录已用公式展示 B-GAP，不衬平；C-OPS 不自动乘月；D-MKT/D-HW/D-TOTAL-H 留空",
         "不影响 A 主算", "CFO 专项复核", "否"),
        ("T17", "Revenue 资料缺口 Q-18（cmo-extend.md 本箱缺失）及 CAC/留存无过核验数字（T-005）",
         "未因此编造 SKU 价格、销量、获客成本或留存。获客与留存保持留空。",
         "不影响当前「收入结果留空」的结论", "CEO 提供原文件或确认以已读页面为准（不越级）", "否"),
    ]
    for i, (sid, matter, status, impact, who, block) in enumerate(items):
        r = 4 + i
        ws.cell(r, 1, sid).font = FONT_B
        ws.cell(r, 1).border = THIN
        ws.cell(r, 2, matter)
        style_text(ws.cell(r, 2))
        ws.cell(r, 3, status)
        if isinstance(status, str) and status.startswith("="):
            style_formula(ws.cell(r, 3), num=False)
            ws.cell(r, 3).alignment = LEFT
        else:
            style_text(ws.cell(r, 3))
        style_text(ws.cell(r, 4, impact))
        style_text(ws.cell(r, 5, who))
        style_text(ws.cell(r, 6, block), FILL_NOTE)
    ws.row_dimensions[7].height = 36  # T04
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"
    return ws


def build_hypotheses(wb):
    ws = wb.create_sheet("08_假设H1-H8")
    set_widths(ws, {"A": 10, "B": 70, "C": 22, "D": 70, "E": 22})
    ws.merge_cells("A1:E1")
    ws["A1"] = "关键假设 H1–H8（类型=假设，不是事实；沿用 2026-11-07 旧稿）"
    ws["A1"].font = FONT_WHITE
    ws["A1"].fill = FILL_TITLE
    for col in range(1, 6):
        ws.cell(1, col).fill = FILL_TITLE
        ws.cell(1, col).font = FONT_WHITE

    for i, h in enumerate(["编号", "假设内容", "类型", "来源", "日期"], 1):
        ws.cell(3, i, h)
    style_header_row(ws, 3, 1, 5)

    hyps = [
        ("H1", "VisionKit V1 + 预设躲猫猫足以验收"),
        ("H2", "霁霁先通，五皮不同开"),
        ("H3", "真遮挡 / 人体 / 暗房满血不做进 A 阶段主预算"),
        ("H4", "02/04 不进精益/基准（完整为可选，见参数台开关；纳入不得自动抬高头条）"),
        ("H5", "费率 550/830/1290 仅折算，非雇佣、非合同价"),
        ("H6", "WeTest 仍可采购"),
        ("H7", "Demo 期无大额云与登录中台"),
        ("H8", "已发生现金 ≈ 0（估算，待票据回填）"),
    ]
    src = "眠语 Demo 产品方案与开发成本测算——BP 前期财务底稿（Notion 定稿页）；00-统一参数口径-20261112.md；统一口径第5节；Cost 待确认假设表"
    for i, (hid, text) in enumerate(hyps):
        r = 4 + i
        ws.cell(r, 1, hid).font = FONT_B
        ws.cell(r, 1).border = THIN
        ws.cell(r, 2, text)
        style_text(ws.cell(r, 2))
        style_text(ws.cell(r, 3, "假设，不是事实"), FILL_PENDING)
        style_text(ws.cell(r, 4, src))
        style_text(ws.cell(r, 5, DATE_EST))

    ws.merge_cells("A13:E13")
    ws["A13"] = (
        "另：预算档位待用户确认；收入模式全部待研究。以上假设成立与否会影响范围和测试能否按旧稿采购，"
        "但不改变「未确认不得写成事实」的标注要求。"
    )
    ws["A13"].font = FONT_SM
    ws["A13"].alignment = LEFT
    ws.sheet_view.showGridLines = False
    return ws


def build_benchmark_sheet(wb):
    ws = wb.create_sheet("09_基准对照")
    ws.sheet_properties.tabColor = "1F4E79"
    set_widths(ws, {"A": 12, "B": 54, "C": 14, "D": 14, "E": 16, "F": 16, "G": 18, "H": 70, "I": 28})
    ws.merge_cells("A1:I1")
    ws["A1"] = "行业基准对照（全部公式链接参数台 F 区；引用须带参数 ID；来源为已复验通过的 Benchmark v1.1，禁止使用第一版分项或已作废中值差）"
    ws["A1"].font = FONT_WHITE
    ws["A1"].fill = FILL_TITLE
    for col in range(1, 10):
        ws.cell(1, col).fill = FILL_TITLE
        ws.cell(1, col).font = FONT_WHITE

    ws.merge_cells("A2:I2")
    ws["A2"] = (
        "本表不进入 02/03 的 A 阶段合计或仍需主口径，也不自动写入 G-06 或 CERT_Y。"
        "官方 19.9 元/月（P-003）只作对照，不改总包。P-013 中值不是官方档位。"
        "P-019/P-020 是案例事实，不是金额驱动；禁止把 P-020 的 2400 填入 D-02。"
        "访问日 2026-11-12。"
    )
    ws["A2"].font = FONT_SM
    ws["A2"].alignment = LEFT
    ws.row_dimensions[2].height = 36

    for i, h in enumerate(["参数ID", "参数名称", "低值", "高值", "中值（公式）", "万元（仅金额）",
                           "单位", "口径/限制（摘自参数台）", "性质"], 1):
        ws.cell(4, i, h)
    style_header_row(ws, 4, 1, 9)

    # param rows 99-118 map to sheet rows 5-24
    amount_ids = {
        "P-001", "P-002", "P-003", "P-004", "P-005", "P-006", "P-009", "P-010",
    }
    for i in range(20):
        pr = 99 + i
        r = 5 + i
        ws.cell(r, 1, f"='01_参数台'!A{pr}")
        ws.cell(r, 2, f"='01_参数台'!B{pr}")
        ws.cell(r, 3, f'=IF(\'01_参数台\'!C{pr}="","",\'01_参数台\'!C{pr})')
        ws.cell(r, 4, f'=IF(\'01_参数台\'!D{pr}="","",\'01_参数台\'!D{pr})')
        ws.cell(r, 5, f'=IF(\'01_参数台\'!E{pr}="","",\'01_参数台\'!E{pr})')
        # 万元 only for amount-like rows; still formula-safe. Use unit text from param sheet.
        ws.cell(r, 6, f'=IF(OR(\'01_参数台\'!E{pr}="",\'01_参数台\'!K{pr}="分钟/周·每小程序",\'01_参数台\'!K{pr}="分钟/项目·一次",\'01_参数台\'!K{pr}="家（稿称 more than，下界）",\'01_参数台\'!K{pr}="—（非金额）",LEFT(\'01_参数台\'!K{pr},2)="比率"),"",\'01_参数台\'!E{pr}/10000)')
        ws.cell(r, 7, f"='01_参数台'!K{pr}")
        ws.cell(r, 8, f"='01_参数台'!M{pr}")
        ws.cell(r, 9, f"='01_参数台'!O{pr}")
        for c in range(1, 10):
            style_formula(ws.cell(r, c), num=False)
        ws.cell(r, 3).number_format = "General"
        ws.cell(r, 4).number_format = "General"
        ws.cell(r, 5).number_format = "General"
        ws.cell(r, 6).number_format = WAN

    # official vs draft opex contrast (does not change package)
    ws.merge_cells("A26:I26")
    ws["A26"] = "对照：旧稿 Demo 期持续月费 vs 官方基础套餐现价（P-003）。本对照不改 OPEX_M，不改 PACK。"
    ws["A26"].font = FONT_WHITE
    ws["A26"].fill = FILL_SECTION
    for col in range(1, 10):
        ws.cell(26, col).fill = FILL_SECTION
        ws.cell(26, col).font = FONT_WHITE
    for i, h in enumerate(["档位", "旧稿持续月费下限（元/月）", "旧稿持续月费上限（元/月）",
                           "官方基础套餐现价 P-003（元/月）", "说明"], 1):
        ws.cell(27, i, h)
    style_header_row(ws, 27, 1, 5)
    ws["A28"] = "精益"
    ws["B28"] = "='01_参数台'!C26"
    ws["C28"] = "='01_参数台'!D26"
    ws["D28"] = '=IF(\'01_参数台\'!C101="","",\'01_参数台\'!C101)'
    ws["E28"] = "只作对照。不得把持续月费改写成 19.9 元/月。"
    ws["A29"] = "基准"
    ws["B29"] = "='01_参数台'!E26"
    ws["C29"] = "='01_参数台'!F26"
    ws["D29"] = '=IF(\'01_参数台\'!C101="","",\'01_参数台\'!C101)'
    ws["E29"] = "只作对照。不得把持续月费改写成 19.9 元/月。"
    ws["A30"] = "完整"
    ws["B30"] = "='01_参数台'!G26"
    ws["C30"] = "='01_参数台'!H26"
    ws["D30"] = '=IF(\'01_参数台\'!C101="","",\'01_参数台\'!C101)'
    ws["E30"] = "只作对照。不得把持续月费改写成 19.9 元/月。"
    for r in range(28, 31):
        for c in range(1, 5):
            style_formula(ws.cell(r, c), num=(c > 1), fmt=YUAN2 if c == 4 else YUAN)
        style_text(ws.cell(r, 5), FILL_NOTE)

    # structure check (uses model GAP, not obsolete mid-value diffs)
    ws.merge_cells("A32:I32")
    ws["A32"] = "结构校验（公式，与已裁决模型口径一致）：差额=头条−分项，上下限分列。中值差不在本表作为引用数字。禁止引用已作废的第一版中值差 −8,350 / −15,000 / −22,000。"
    ws["A32"].font = FONT_WHITE
    ws["A32"].fill = FILL_SECTION
    for col in range(1, 10):
        ws.cell(32, col).fill = FILL_SECTION
        ws.cell(32, col).font = FONT_WHITE
    for i, h in enumerate(["口径", "分项合计下限", "分项合计上限", "头条下限", "头条上限",
                           "差额下限（头条−分项）", "差额上限（头条−分项）", "归类（已裁决）"], 1):
        ws.cell(33, i, h)
    style_header_row(ws, 33, 1, 8)

    checks = [
        (34, "精益（不含 02/04）", "='01_参数台'!C19", "='01_参数台'!D19", "='01_参数台'!C20", "='01_参数台'!D20",
         "='01_参数台'!C21", "='01_参数台'!D21",
         "未归类余量，不是已确认可开支成本包"),
        (35, "基准（不含 02/04）", "='01_参数台'!E19", "='01_参数台'!F19", "='01_参数台'!E20", "='01_参数台'!F20",
         "='01_参数台'!E21", "='01_参数台'!F21",
         "未归类余量，不是已确认可开支成本包"),
        (36, "完整（不含 02/04）",
         "='01_参数台'!G19",  # this depends on switches — for "不含" we need SUM of A01-A06 only
         None, None, None, None, None, None),
    ]
    # For 完整不含 / 含, G19/H19 depend on C4/C5. Use SUM of items for a switch-independent display.
    # 精益/基准 SUM-SWITCH already excludes 02/04 (items are 0 and G19 formula only adds if switch yes on 完整 columns).
    # For 精益 C19 = SUM(C11:C16)+0, good.
    # For 完整不含: should be SUM(G11:G16) not G19.
    # I'll write explicit formulas.

    def chk(r, name, slo, shi, hlo, hhi, glo, ghi, klass):
        ws.cell(r, 1, name).font = FONT_B
        ws.cell(r, 1).border = THIN
        for c, f in enumerate([slo, shi, hlo, hhi, glo, ghi], 2):
            ws.cell(r, c, f)
            style_formula(ws.cell(r, c))
        style_text(ws.cell(r, 8, klass), FILL_GAP)

    chk(34, "精益（不含 02/04）",
        "='01_参数台'!C19", "='01_参数台'!D19", "='01_参数台'!C20", "='01_参数台'!D20",
        "='01_参数台'!C21", "='01_参数台'!D21",
        "未归类余量，不是已确认可开支成本包")
    chk(35, "基准（不含 02/04）",
        "='01_参数台'!E19", "='01_参数台'!F19", "='01_参数台'!E20", "='01_参数台'!F20",
        "='01_参数台'!E21", "='01_参数台'!F21",
        "未归类余量，不是已确认可开支成本包")
    chk(36, "完整（不含 02/04）",
        "=SUM('01_参数台'!G11:G16)", "=SUM('01_参数台'!H11:H16)",
        "='01_参数台'!G20", "='01_参数台'!H20",
        "='01_参数台'!G20-SUM('01_参数台'!G11:G16)", "='01_参数台'!H20-SUM('01_参数台'!H11:H16)",
        "分项之和已高于头条；对外仍以 11–22 万为锚，不得按分项加总抬高预算")
    chk(37, "完整（含 02+04）",
        "=SUM('01_参数台'!G11:G18)", "=SUM('01_参数台'!H11:H18)",
        "='01_参数台'!G20", "='01_参数台'!H20",
        "='01_参数台'!G20-SUM('01_参数台'!G11:G18)", "='01_参数台'!H20-SUM('01_参数台'!H11:H18)",
        "纳入 02/04 不得自动抬高头条；须另行决策")

    ws.merge_cells("A39:I39")
    ws["A39"] = (
        "读表注意：数字差距（例如持续月费中值远高于 P-003 的 19.9）不能得出「应把持续月费改成 19.9 元」的结论。"
        "旧稿持续项构成未拆开前，用 19.9 直接改三档总预算会变成重切档位。CAC/留存本轮无过核验数字，保持留空。"
    )
    ws["A39"].font = FONT_SM
    ws["A39"].alignment = LEFT
    ws.sheet_view.showGridLines = False
    return ws


def apply_print(ws):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "1:1"
    ws.oddFooter.left.text = "眠语财务模型 v0.2｜非正式 BP｜未自审"
    ws.oddFooter.right.text = "第 &P 页 / 共 &N 页"


def main():
    # Safety: never write to v0.1 paths
    v01_xlsx = Path("/workspace/mianyu-cfo/CFO-FinancialModel-眠语财务模型v0.1-20261112.xlsx")
    v01_md = Path("/workspace/mianyu-cfo/CFO-FinancialModel-测算说明-20261112.md")
    v01_py = Path("/workspace/mianyu-cfo/_build_CFO-FinancialModel-v0.1.py")
    assert OUT_XLSX.resolve() != v01_xlsx.resolve()
    assert OUT_XLSX.name != v01_xlsx.name
    assert v01_xlsx.exists() and v01_md.exists() and v01_py.exists()

    wb = Workbook()
    ws_p = build_params(wb)
    build_params_rest(ws_p)
    build_cover(wb)
    build_cost_split(wb)
    build_cashflow(wb)
    build_revenue(wb)
    build_breakeven(wb)
    build_appendix(wb)
    build_pending(wb)
    build_hypotheses(wb)
    build_benchmark_sheet(wb)

    # Desired sheet order
    order = [
        "00_封面", "01_参数台", "02_A阶段成本拆分", "03_现金流",
        "04_收入与收支结构", "05_盈亏平衡", "06_附录BCD",
        "07_待确认清单", "08_假设H1-H8", "09_基准对照",
    ]
    for i, name in enumerate(order):
        wb.move_sheet(name, offset=i - wb.sheetnames.index(name))

    # Remove leftover default sheet if any
    for name in list(wb.sheetnames):
        if name not in order:
            del wb[name]

    for ws in wb.worksheets:
        apply_print(ws)
        ws.sheet_view.zoomScale = 100

    # defined names for key inputs
    from openpyxl.workbook.defined_name import DefinedName
    names = {
        "当前档位": "'01_参数台'!$C$3",
        "含02": "'01_参数台'!$C$4",
        "含04": "'01_参数台'!$C$5",
        "已发生现金": "'01_参数台'!$C$32",
        "D规模化上限": "'01_参数台'!$C$47",
    }
    for nm, ref in names.items():
        defn = DefinedName(nm, attr_text=ref)
        # openpyxl 3: wb.defined_names.add
        try:
            wb.defined_names.add(defn)
        except Exception:
            wb.defined_names.append(defn)

    OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT_XLSX)
    print(f"Wrote {OUT_XLSX} ({OUT_XLSX.stat().st_size} bytes)")
    print("Sheets:", wb.sheetnames)


if __name__ == "__main__":
    main()

