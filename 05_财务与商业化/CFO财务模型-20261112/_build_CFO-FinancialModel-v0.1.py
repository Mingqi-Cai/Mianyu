#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build 眠语财务模型 v0.1. Inputs live on 参数台; key results are Excel formulas."""

from openpyxl import Workbook
from openpyxl.styles import Font, Fill, PatternFill, Border, Side, Alignment, Protection, NamedStyle
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.chart.label import DataLabelList
from pathlib import Path
from datetime import datetime
from copy import copy

OUT_XLSX = Path("/workspace/mianyu-cfo/CFO-FinancialModel-眠语财务模型v0.1-20261112.xlsx")
OUT_MD = Path("/workspace/mianyu-cfo/CFO-FinancialModel-测算说明-20261112.md")

# styles
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
FONT_WHITE = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
FONT_WHITE_LG = Font(name="Calibri", bold=True, color="FFFFFF", size=16)
FONT_WHITE_MD = Font(name="Calibri", bold=True, color="FFFFFF", size=13)
FONT_TITLE = Font(name="Calibri", bold=True, size=14, color="1F4E79")
FONT_H = Font(name="Calibri", bold=True, size=11, color="1F4E79")
FONT_N = Font(name="Calibri", size=10)
FONT_B = Font(name="Calibri", size=10, bold=True)
FONT_SM = Font(name="Calibri", size=9, italic=True, color="666666")
FONT_WARN = Font(name="Calibri", size=10, bold=True, color="C65911")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
RIGHT = Alignment(horizontal="right", vertical="center")
YUAN = '#,##0'
YUAN2 = '#,##0.00'

SRC_COST = "眠语 Demo 产品方案与开发成本测算——BP 前期财务底稿（Notion 定稿页）；00-统一参数口径-20261112.md"
SRC_URL = "https://app.notion.com/p/411340bcc396814a9b16de9c7b11419c"
DATE_EST = "估算日 2026-11-07"
NATURE_EST = "已有底稿估算 / 待询价"
NATURE_ASSUME = "待确认假设"
CALIBER_ONEOFF = "CNY 元；一次性；含税口径未拆，旧稿未分含税/不含税；待询价，非合同价，非用户已锁定"
CALIBER_MONTH = "CNY 元/月；Demo 期持续；另加认证年费；待询价"
SCOPE_A = "A 当前 Demo"

def style_header_row(ws, row, start, end):
    for col in range(start, end + 1):
        c = ws.cell(row, col)
        c.fill = FILL_HEADER
        c.font = FONT_WHITE
        c.alignment = CENTER
        c.border = THIN

def style_input(c, num=False):
    c.fill = FILL_INPUT
    c.font = FONT_N
    c.alignment = CENTER if num else LEFT
    c.border = THIN
    if num:
        c.number_format = YUAN

def style_formula(c, num=True, pending=False):
    c.fill = FILL_GAP if pending else FILL_FORMULA
    c.font = FONT_N
    c.alignment = CENTER
    c.border = THIN
    if num:
        c.number_format = YUAN

def style_text(c, fill=None):
    c.fill = fill or FILL_GREY
    c.font = FONT_N
    c.alignment = LEFT
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

def current_low(src_lean, src_base, src_full):
    # C3 is 当前档位 on 参数台
    return f'=IF($C$3="精益",{src_lean},IF($C$3="基准",{src_base},IF($C$3="完整",{src_full},"")))'

def current_high(src_lean, src_base, src_full):
    return f'=IF($C$3="精益",{src_lean},IF($C$3="基准",{src_base},IF($C$3="完整",{src_full},"")))'


wb = Workbook()

# ============================================================
# 01 参数台  (build first so other sheets can reference)
# ============================================================
ws_p = wb.active
ws_p.title = "01_参数台"

ws_p.merge_cells("A1:Q1")
ws_p["A1"] = "眠语财务模型 v0.1 · 参数台（全部可调输入集中本表；请勿在其他表改数）"
ws_p["A1"].font = FONT_WHITE_LG
ws_p["A1"].fill = FILL_TITLE
ws_p["A1"].alignment = LEFT
for col in range(1, 18):
    ws_p.cell(1, col).fill = FILL_TITLE
    ws_p.cell(1, col).font = FONT_WHITE_LG

ws_p.merge_cells("A2:Q2")
ws_p["A2"] = "单号 CFO-20261112-MODEL｜状态：财务准备 / 非正式 BP｜默认展示档=基准（旧稿建议首选，用户尚未锁定）｜改 C3/C4/C5 或黄色输入格，成本、现金流、盈亏平衡随公式联动"
ws_p["A2"].font = Font(name="Calibri", size=9, color="FFFFFF", italic=True)
ws_p["A2"].fill = PatternFill("solid", fgColor="2E75B6")
ws_p["A2"].alignment = LEFT
for col in range(1, 18):
    ws_p.cell(2, col).fill = PatternFill("solid", fgColor="2E75B6")

# Controls
ws_p["A3"] = "当前档位"
ws_p["A3"].font = FONT_B
ws_p["A3"].alignment = LEFT
ws_p["C3"] = "基准"
style_input(ws_p["C3"])
ws_p["C3"].font = FONT_B
ws_p["D3"] = "待确认：用户尚未锁定档位。三档均可切换，不得视为已定案。"
ws_p["D3"].font = FONT_WARN
ws_p.merge_cells("D3:Q3")

ws_p["A4"] = "完整档是否含02可选"
ws_p["A4"].font = FONT_B
ws_p["C4"] = "否"
style_input(ws_p["C4"])
ws_p["D4"] = "默认不含。H4：02/04 不进精益/基准；完整为可选。纳入后分项求和可能高于旧稿头条合计。"
ws_p["D4"].font = FONT_SM
ws_p.merge_cells("D4:Q4")

ws_p["A5"] = "完整档是否含04可选"
ws_p["A5"].font = FONT_B
ws_p["C5"] = "否"
style_input(ws_p["C5"])
ws_p["D5"] = "默认不含。同上。"
ws_p["D5"].font = FONT_SM
ws_p.merge_cells("D5:Q5")

dv_tier = DataValidation(type="list", formula1='"精益,基准,完整"', allow_blank=False)
dv_tier.error = "请选择 精益 / 基准 / 完整"
dv_tier.errorTitle = "档位"
dv_tier.prompt = "选择当前测算档位"
dv_tier.showDropDown = False
ws_p.add_data_validation(dv_tier)
dv_tier.add(ws_p["C3"])

dv_yn = DataValidation(type="list", formula1='"是,否"', allow_blank=False)
ws_p.add_data_validation(dv_yn)
dv_yn.add(ws_p["C4"])
dv_yn.add(ws_p["C5"])

ws_p["A6"] = "货币"
ws_p["C6"] = "CNY 元（表内统一用元；摘要万元=元/10000，为公式）"
ws_p["C6"].font = FONT_N
ws_p.merge_cells("C6:Q6")
ws_p["A7"] = "控制区说明"
ws_p["C7"] = "黄色=输入；蓝色=公式；橙色=待确认/待裁决。每一笔数字含来源、口径、适用范围、性质、日期。"
ws_p["C7"].font = FONT_SM
ws_p.merge_cells("C7:Q7")

# ---- A-stage cost items ----
section_bar(ws_p, 9, "A. A阶段成本参数（一次性，元；沿用 2026-11-07 旧稿区间，待询价）", 1, 17)

headers = [
    "参数ID", "参数名称", "精益_下限", "精益_上限", "基准_下限", "基准_上限",
    "完整_下限", "完整_上限", "当前_下限", "当前_上限", "单位",
    "来源", "口径", "适用范围", "性质", "日期", "待确认"
]
for i, h in enumerate(headers, 1):
    ws_p.cell(10, i, h)
style_header_row(ws_p, 10, 1, 17)

# rows 11-18 cost items
# id, name, Llo, Lhi, Blo, Bhi, Flo, Fhi, special current formula?
items = [
    # row, id, name, values
    (11, "ENG", "工程包", 12000, 25000, 25000, 50000, 50000, 90000, False),
    (12, "IP", "IP美术（完整档为五皮）", 3000, 8000, 8000, 15000, 35000, 55000, False),
    (13, "UX", "UI/UX", 0, 7000, 10000, 20000, 20000, 40000, False),
    (14, "COPY", "互动文案", 0, 2000, 2000, 6000, 8000, 15000, False),
    (15, "CLOUD", "云+认证一次性", 400, 800, 2000, 5000, 5000, 10000, False),
    (16, "TEST", "测试", 0, 2000, 4000, 7000, 11000, 23000, False),
    (17, "OPT02", "02可选（仅完整）", 0, 0, 0, 0, 15000, 50000, "02"),
    (18, "OPT04", "04可选（仅完整）", 0, 0, 0, 0, 5000, 20000, "04"),
]

for row, pid, name, llo, lhi, blo, bhi, flo, fhi, special in items:
    ws_p.cell(row, 1, pid).font = FONT_B
    ws_p.cell(row, 1).alignment = CENTER
    ws_p.cell(row, 1).border = THIN
    ws_p.cell(row, 2, name).font = FONT_N
    ws_p.cell(row, 2).alignment = LEFT
    ws_p.cell(row, 2).border = THIN
    vals = [llo, lhi, blo, bhi, flo, fhi]
    for i, v in enumerate(vals):
        cell = ws_p.cell(row, 3 + i, v)
        style_input(cell, num=True)
    # current low/high
    if special == "02":
        # only count when 完整 AND 含02=是
        ws_p.cell(row, 9, f'=IF(AND($C$3="完整",$C$4="是"),G{row},0)')
        ws_p.cell(row, 10, f'=IF(AND($C$3="完整",$C$4="是"),H{row},0)')
    elif special == "04":
        ws_p.cell(row, 9, f'=IF(AND($C$3="完整",$C$5="是"),G{row},0)')
        ws_p.cell(row, 10, f'=IF(AND($C$3="完整",$C$5="是"),H{row},0)')
    else:
        ws_p.cell(row, 9, current_low(f"C{row}", f"E{row}", f"G{row}"))
        ws_p.cell(row, 10, current_high(f"D{row}", f"F{row}", f"H{row}"))
    style_formula(ws_p.cell(row, 9))
    style_formula(ws_p.cell(row, 10))
    meta = [
        "元",
        SRC_COST + "；" + SRC_URL,
        CALIBER_ONEOFF + ("；仅完整可选，精益/基准为 0（H4）" if special else ""),
        SCOPE_A + ("；仅完整可选" if special else ""),
        NATURE_EST,
        DATE_EST,
        "是：待询价，非合同价",
    ]
    for i, v in enumerate(meta):
        cell = ws_p.cell(row, 11 + i, v)
        style_text(cell, FILL_PENDING if i == 6 else FILL_GREY)

# Row 19 分项求和_主预算
ws_p.cell(19, 1, "SUM_A")
ws_p.cell(19, 2, "分项求和（主预算：11–16行 + 按开关计入的02/04）")
ws_p["A19"].font = FONT_B
ws_p["B19"].font = FONT_B
for col, formula in [
    (3, "=SUM(C11:C16)+0"),  # 精益/基准 02/04 are 0; keep consistent: lean/base never include 02/04
    (4, "=SUM(D11:D16)+0"),
    (5, "=SUM(E11:E16)+0"),
    (6, "=SUM(F11:F16)+0"),
    (7, '=SUM(G11:G16)+IF($C$4="是",G17,0)+IF($C$5="是",G18,0)'),
    (8, '=SUM(H11:H16)+IF($C$4="是",H17,0)+IF($C$5="是",H18,0)'),
    (9, "=SUM(I11:I18)"),
    (10, "=SUM(J11:J18)"),
]:
    ws_p.cell(19, col, formula)
    style_formula(ws_p.cell(19, col))
for col in range(1, 3):
    ws_p.cell(19, col).border = THIN
    ws_p.cell(19, col).fill = FILL_FORMULA
for col, v in enumerate(["元", SRC_COST, "公式：分项下限/上限分别求和；02/04仅当完整且开关为「是」时计入", SCOPE_A, "公式结果（非新估算）", "跟随分项", "是：与头条合计可能存在差额，待 CFO 裁决"], 11):
    style_text(ws_p.cell(19, col, v), FILL_GAP if col == 17 else FILL_GREY)

# Row 20 旧稿头条合计
ws_p.cell(20, 1, "HEAD")
ws_p.cell(20, 2, "旧稿头条一次性合计（与 11-07 底稿硬对齐，验收锚点）")
ws_p["A20"].font = FONT_B
ws_p["B20"].font = FONT_B
head_vals = [25000, 55000, 55000, 110000, 110000, 220000]
for i, v in enumerate(head_vals):
    cell = ws_p.cell(20, 3 + i, v)
    style_input(cell, num=True)
ws_p.cell(20, 9, current_low("C20", "E20", "G20"))
ws_p.cell(20, 10, current_high("D20", "F20", "H20"))
style_formula(ws_p.cell(20, 9))
style_formula(ws_p.cell(20, 10))
for col, v in enumerate(["元", SRC_COST + "；" + SRC_URL, "CNY 元；一次性总预算区间；待询价，非合同价；用户尚未锁定档位", SCOPE_A, NATURE_EST, DATE_EST, "是：待询价；档位待用户确认"], 11):
    style_text(ws_p.cell(20, col, v), FILL_PENDING if col == 17 else FILL_GREY)
for col in range(1, 3):
    ws_p.cell(20, col).border = THIN
    ws_p.cell(20, col).fill = FILL_INPUT

# Row 21 差额
ws_p.cell(21, 1, "GAP")
ws_p.cell(21, 2, "差额（旧稿头条 − 分项求和）。正差=头条高于分项（未归类）；负差=分项高于头条。禁止用虚拟行衬平。")
ws_p["A21"].font = FONT_B
ws_p["B21"].font = FONT_WARN
ws_p["B21"].alignment = LEFT
for src_h, src_s, col in [("C20", "C19", 3), ("D20", "D19", 4), ("E20", "E19", 5), ("F20", "F19", 6), ("G20", "G19", 7), ("H20", "H19", 8), ("I20", "I19", 9), ("J20", "J19", 10)]:
    # wait I used wrong: col 9 should be I20-I19 meaning head-sum
    pass
for formula, col in [
    ("=C20-C19", 3), ("=D20-D19", 4), ("=E20-E19", 5), ("=F20-F19", 6),
    ("=G20-G19", 7), ("=H20-H19", 8), ("=I20-I19", 9), ("=J20-J19", 10),
]:
    ws_p.cell(21, col, formula)
    style_formula(ws_p.cell(21, col), pending=True)
for col in range(1, 3):
    ws_p.cell(21, col).border = THIN
    ws_p.cell(21, col).fill = FILL_GAP
for col, v in enumerate(["元", "由本表公式计算", "口径待 CFO 裁决：不得将差额写成已确认成本包或已批准预算", SCOPE_A, "公式结果 / 待裁决", "跟随公式", "是：待 CFO 裁决，未自行改数"], 11):
    style_text(ws_p.cell(21, col, v), FILL_GAP)

# Row 22 分项求和含全部可选（完整档对照，不受开关影响）
ws_p.cell(22, 1, "SUM_ALL")
ws_p.cell(22, 2, "分项求和（完整档对照：始终含 02+04；精益/基准仍为 0）")
for formula, col in [
    ("=SUM(C11:C18)", 3), ("=SUM(D11:D18)", 4), ("=SUM(E11:E18)", 5), ("=SUM(F11:F18)", 6),
    ("=SUM(G11:G18)", 7), ("=SUM(H11:H18)", 8),
    ('=IF($C$3="完整",SUM(G11:G18),SUM(I11:I16))', 9),
    ('=IF($C$3="完整",SUM(H11:H18),SUM(J11:J16))', 10),
]:
    ws_p.cell(22, col, formula)
    style_formula(ws_p.cell(22, col))
for col in range(1, 3):
    ws_p.cell(22, col).border = THIN
    ws_p.cell(22, col).fill = FILL_FORMULA
    ws_p.cell(22, col).font = FONT_N
for col, v in enumerate(["元", "公式对照", "仅展示完整档含全部可选时的分项合计，不替代头条验收锚点", SCOPE_A, "公式结果", "跟随分项", "是：对照用"], 11):
    style_text(ws_p.cell(22, col, v), FILL_GREY)

# ---- ongoing ----
section_bar(ws_p, 24, "B. Demo 期持续费用（元；不计入一次性头条合计）", 1, 17)
for i, h in enumerate(headers, 1):
    ws_p.cell(25, i, h)
style_header_row(ws_p, 25, 1, 17)

# row 26 monthly
ws_p.cell(26, 1, "OPEX_M")
ws_p.cell(26, 2, "Demo期月度持续")
for i, v in enumerate([100, 300, 200, 400, 400, 800]):
    style_input(ws_p.cell(26, 3 + i, v), num=True)
ws_p.cell(26, 9, current_low("C26", "E26", "G26"))
ws_p.cell(26, 10, current_high("D26", "F26", "H26"))
style_formula(ws_p.cell(26, 9))
style_formula(ws_p.cell(26, 10))
for col, v in enumerate(["元/月", SRC_COST, CALIBER_MONTH, SCOPE_A + "；Demo 期", NATURE_EST, DATE_EST, "是：待询价"], 11):
    style_text(ws_p.cell(26, col, v), FILL_PENDING if col == 17 else FILL_GREY)
ws_p["A26"].border = THIN
ws_p["B26"].border = THIN

# row 27 cert — 300 stated for 精益; 基准/完整 旧稿仅写「+认证」
ws_p.cell(27, 1, "CERT_Y")
ws_p.cell(27, 2, "认证年费（基准/完整按精益同额占位）")
for i, v in enumerate([300, 300, 300, 300, 300, 300]):
    style_input(ws_p.cell(27, 3 + i, v), num=True)
ws_p.cell(27, 9, current_low("C27", "E27", "G27"))
ws_p.cell(27, 10, current_high("D27", "F27", "H27"))
style_formula(ws_p.cell(27, 9))
style_formula(ws_p.cell(27, 10))
for col, v in enumerate(["元/年", SRC_COST, "CNY 元/年；旧稿仅对精益写明 300 元/年，基准与完整写「+认证」，本表按同额占位，不是已确认同价", SCOPE_A, "已有底稿估算 / 待确认占位（基准、完整）", DATE_EST, "是：基准/完整年费是否同为 300 待确认"], 11):
    style_text(ws_p.cell(27, col, v), FILL_PENDING)
ws_p["A27"].border = THIN
ws_p["B27"].border = THIN

# row 28-29 weeks
ws_p.cell(28, 1, "WEEKS")
ws_p.cell(28, 2, "开发周期（公历周）")
for i, v in enumerate([3, 4, 4, 6, 6, 10]):
    style_input(ws_p.cell(28, 3 + i, v), num=True)
    ws_p.cell(28, 3 + i).number_format = "0"
ws_p.cell(28, 9, current_low("C28", "E28", "G28"))
ws_p.cell(28, 10, current_high("D28", "F28", "H28"))
style_formula(ws_p.cell(28, 9))
style_formula(ws_p.cell(28, 10))
ws_p["I28"].number_format = "0"
ws_p["J28"].number_format = "0"
for col, v in enumerate(["周", SRC_COST, "公历周（7 天）。人天按 1 人×1 工作日，不得把日历周直接当 7 人天", SCOPE_A, NATURE_EST, DATE_EST, "是：待排期确认"], 11):
    style_text(ws_p.cell(28, col, v), FILL_PENDING if col == 17 else FILL_GREY)
ws_p["A28"].border = THIN
ws_p["B28"].border = THIN

# row 29 days-per-month conversion
ws_p.cell(29, 1, "DAYS_M")
ws_p.cell(29, 2, "月换算分母（示意：周×7÷本参数）")
ws_p.cell(29, 3, 30)
style_input(ws_p["C29"], num=True)
ws_p["C29"].number_format = "0"
ws_p.merge_cells("C29:H29")
ws_p.cell(29, 9, "=C29")
ws_p.cell(29, 10, "=C29")
style_formula(ws_p["I29"])
style_formula(ws_p["J29"])
ws_p["I29"].number_format = "0"
ws_p["J29"].number_format = "0"
for col, v in enumerate(["天/月", "本模型设定（非旧稿原文）", "仅用于把开发周数示意折成月数，付款节奏未约定，非合同安排", SCOPE_A + "；示意", "待确认假设", "2026-11-12", "是：换算口径待确认"], 11):
    style_text(ws_p.cell(29, col, v), FILL_PENDING)
ws_p["A29"].border = THIN
ws_p["B29"].border = THIN

# ---- spent cash, rates ----
section_bar(ws_p, 31, "C. 已发生现金、人天费率锚点、Bot 非现金（不得从仍需现金扣减）", 1, 17)
ws_p["A32"] = "CASH_SPENT"
ws_p["B32"] = "已发生现金"
ws_p["C32"] = 0
style_input(ws_p["C32"], num=True)
ws_p.merge_cells("C32:J32")
for col, v in enumerate(["元", SRC_COST, "估算；有票据后回填。仍需现金=头条合计−已发生（见现金流表）", SCOPE_A, "已有底稿估算（H8）", DATE_EST, "是：待票据回填"], 11):
    style_text(ws_p.cell(32, col, v), FILL_PENDING)
ws_p["A32"].border = THIN
ws_p["B32"].border = THIN

ws_p["A33"] = "RATE_L"
ws_p["B33"] = "人天费率_低（折算非雇佣）"
ws_p["C33"] = 550
style_input(ws_p["C33"], num=True)
ws_p.merge_cells("C33:J33")
for col, v in enumerate(["元/人天", SRC_COST, "仅折算锚点（H5），不得用其倒推已确认人天或代替分项报价", SCOPE_A, NATURE_EST, DATE_EST, "是：待询价；禁止倒推人天充成本"], 11):
    style_text(ws_p.cell(33, col, v), FILL_PENDING)
ws_p["A33"].border = THIN
ws_p["B33"].border = THIN

ws_p["A34"] = "RATE_M"
ws_p["B34"] = "人天费率_中（折算非雇佣）"
ws_p["C34"] = 830
style_input(ws_p["C34"], num=True)
ws_p.merge_cells("C34:J34")
for col, v in enumerate(["元/人天", SRC_COST, "仅折算锚点（H5）", SCOPE_A, NATURE_EST, DATE_EST, "是：待询价"], 11):
    style_text(ws_p.cell(34, col, v), FILL_PENDING)
ws_p["A34"].border = THIN
ws_p["B34"].border = THIN

ws_p["A35"] = "RATE_H"
ws_p["B35"] = "人天费率_高（折算非雇佣）"
ws_p["C35"] = 1290
style_input(ws_p["C35"], num=True)
ws_p.merge_cells("C35:J35")
for col, v in enumerate(["元/人天", SRC_COST, "仅折算锚点（H5）", SCOPE_A, NATURE_EST, DATE_EST, "是：待询价"], 11):
    style_text(ws_p.cell(35, col, v), FILL_PENDING)
ws_p["A35"].border = THIN
ws_p["B35"].border = THIN

ws_p["A36"] = "OUT_LO"
ws_p["B36"] = "外包加成经验_下限"
ws_p["C36"] = 1200
style_input(ws_p["C36"], num=True)
ws_p.merge_cells("C36:J36")
for col, v in enumerate(["元/人天", SRC_COST, "外包加成经验区间，待询价，非雇佣工资", SCOPE_A, NATURE_EST, DATE_EST, "是：待询价"], 11):
    style_text(ws_p.cell(36, col, v), FILL_PENDING)
ws_p["A36"].border = THIN
ws_p["B36"].border = THIN

ws_p["A37"] = "OUT_HI"
ws_p["B37"] = "外包加成经验_上限"
ws_p["C37"] = 2000
style_input(ws_p["C37"], num=True)
ws_p.merge_cells("C37:J37")
for col, v in enumerate(["元/人天", SRC_COST, "外包加成经验区间，待询价，非雇佣工资", SCOPE_A, NATURE_EST, DATE_EST, "是：待询价"], 11):
    style_text(ws_p.cell(37, col, v), FILL_PENDING)
ws_p["A37"].border = THIN
ws_p["B37"].border = THIN

ws_p["A38"] = "BOT_LO"
ws_p["B38"] = "Bot替代价值_下限（非现金）"
ws_p["C38"] = 50000
style_input(ws_p["C38"], num=True)
ws_p.merge_cells("C38:J38")
for col, v in enumerate(["元", SRC_COST, "非现金；不可入账为已节省，不得从仍需现金直接扣减", "附注，不进入 A 现金主表合计", NATURE_EST, DATE_EST, "是：非现金，禁止扣减"], 11):
    style_text(ws_p.cell(38, col, v), FILL_PENDING)
ws_p["A38"].border = THIN
ws_p["B38"].border = THIN

ws_p["A39"] = "BOT_HI"
ws_p["B39"] = "Bot替代价值_上限（非现金）"
ws_p["C39"] = 120000
style_input(ws_p["C39"], num=True)
ws_p.merge_cells("C39:J39")
for col, v in enumerate(["元", SRC_COST, "非现金；不可入账为已节省，不得从仍需现金直接扣减", "附注，不进入 A 现金主表合计", NATURE_EST, DATE_EST, "是：非现金，禁止扣减"], 11):
    style_text(ws_p.cell(39, col, v), FILL_PENDING)
ws_p["A39"].border = THIN
ws_p["B39"].border = THIN

# ---- BCD ----
section_bar(ws_p, 41, "D. B/C/D 阶段区间（旧稿情景，待专项复核；严禁混入 A）", 1, 17)
ws_p["A42"] = "B_LO"
ws_p["B42"] = "B产品验证_下限"
ws_p["C42"] = 20000
style_input(ws_p["C42"], num=True)
ws_p.merge_cells("C42:J42")
for col, v in enumerate(["元", SRC_COST + "；统一口径第3节", "旧稿情景区间，待专项复核；不得混入 A 合计或 A 现金流", "B 产品验证", "已有底稿估算 / 待专项复核", DATE_EST, "是：待专项复核，不得混入 A"], 11):
    style_text(ws_p.cell(42, col, v), FILL_PENDING)
ws_p["A42"].border = THIN
ws_p["B42"].border = THIN

ws_p["A43"] = "B_HI"
ws_p["B43"] = "B产品验证_上限"
ws_p["C43"] = 80000
style_input(ws_p["C43"], num=True)
ws_p.merge_cells("C43:J43")
for col, v in enumerate(["元", SRC_COST + "；统一口径第3节", "旧稿情景区间，待专项复核；不得混入 A", "B 产品验证", "已有底稿估算 / 待专项复核", DATE_EST, "是：待专项复核，不得混入 A"], 11):
    style_text(ws_p.cell(43, col, v), FILL_PENDING)
ws_p["A43"].border = THIN
ws_p["B43"].border = THIN

ws_p["A44"] = "C_LO"
ws_p["B44"] = "C商业试点_下限"
ws_p["C44"] = 50000
style_input(ws_p["C44"], num=True)
ws_p.merge_cells("C44:J44")
for col, v in enumerate(["元", SRC_COST + "；统一口径第3节", "旧稿情景区间，待专项复核；不得混入 A", "C 商业试点", "已有底稿估算 / 待专项复核", DATE_EST, "是：待专项复核，不得混入 A"], 11):
    style_text(ws_p.cell(44, col, v), FILL_PENDING)
ws_p["A44"].border = THIN
ws_p["B44"].border = THIN

ws_p["A45"] = "C_HI"
ws_p["B45"] = "C商业试点_上限"
ws_p["C45"] = 300000
style_input(ws_p["C45"], num=True)
ws_p.merge_cells("C45:J45")
for col, v in enumerate(["元", SRC_COST + "；统一口径第3节", "旧稿情景区间，待专项复核；不得混入 A", "C 商业试点", "已有底稿估算 / 待专项复核", DATE_EST, "是：待专项复核，不得混入 A"], 11):
    style_text(ws_p.cell(45, col, v), FILL_PENDING)
ws_p["A45"].border = THIN
ws_p["B45"].border = THIN

ws_p["A46"] = "D_LO"
ws_p["B46"] = "D规模化_下限"
ws_p["C46"] = 500000
style_input(ws_p["C46"], num=True)
ws_p.merge_cells("C46:J46")
for col, v in enumerate(["元", SRC_COST + "；统一口径第3节", "旧稿为 ¥500,000–数百万+；上限未给出单一数字，见 D_HI_NOTE", "D 规模化；若上硬件则供应链单列", "已有底稿估算 / 待专项复核", DATE_EST, "是：待专项复核，不得混入 A"], 11):
    style_text(ws_p.cell(46, col, v), FILL_PENDING)
ws_p["A46"].border = THIN
ws_p["B46"].border = THIN

ws_p["A47"] = "D_HI_NOTE"
ws_p["B47"] = "D规模化_上限（旧稿未给单一数字）"
ws_p["C47"] = ""  # leave empty, do not invent
style_input(ws_p["C47"])
ws_p.merge_cells("C47:J47")
ws_p["C47"].fill = FILL_PENDING
for col, v in enumerate(["元", SRC_COST + "；统一口径第3节", "旧稿表述为「数百万+」，本格留空，不倒推上限", "D 规模化", "待确认（旧稿无单一上限）", DATE_EST, "是：上限留空，禁止倒推"], 11):
    style_text(ws_p.cell(47, col, v), FILL_PENDING)
ws_p["A47"].border = THIN
ws_p["B47"].border = THIN
ws_p["K47"] = "（旧稿：数百万+，本格留空）"
ws_p["K47"].font = FONT_SM

# ---- revenue placeholders ----
section_bar(ws_p, 49, "E. 收入模式占位参数（全部待研究；缺参数留空，禁止填入看起来合理的虚数）", 1, 17)
rev_headers = ["模式ID", "模式名称（待研究，非已定决策）", "单价", "数量", "单位变动成本", "数量单位", "周期", "含税", "来源", "口径", "适用范围", "性质", "日期", "待确认"]
# put on row 50, columns A-N
for i, h in enumerate(rev_headers, 1):
    ws_p.cell(50, i, h)
style_header_row(ws_p, 50, 1, 14)

modes = [
    ("R1", "小程序/AR互动"),
    ("R2", "IP内容与数字产品"),
    ("R3", "授权联名"),
    ("R4", "酒店文旅"),
    ("R5", "衍生品与线下体验"),
]
for i, (mid, mname) in enumerate(modes):
    row = 51 + i
    ws_p.cell(row, 1, mid).border = THIN
    ws_p.cell(row, 2, mname).border = THIN
    ws_p.cell(row, 2).font = FONT_N
    for col in (3, 4, 5):  # price, qty, unit vc — EMPTY inputs
        c = ws_p.cell(row, col, None)
        style_input(c, num=True)
        c.fill = FILL_PENDING
        c.number_format = YUAN2
    ws_p.cell(row, 6, "")
    style_input(ws_p.cell(row, 6))
    ws_p.cell(row, 6).fill = FILL_PENDING
    ws_p.cell(row, 7, "")
    style_input(ws_p.cell(row, 7))
    ws_p.cell(row, 7).fill = FILL_PENDING
    ws_p.cell(row, 8, "")
    style_input(ws_p.cell(row, 8))
    ws_p.cell(row, 8).fill = FILL_PENDING
    for col, v in enumerate([
        "同级 CFO-Revenue / CFO-Benchmark 文件在 v0.1 交稿时尚未就绪；未引用用户交档中的市场调研以免把待研究写成预测",
        "单价、数量、单位变动成本均为待确认；含税与周期未定。给区间时须写清月/年、含税否、是否含获客",
        "待研究情景，非已确定商业决策",
        "待确认假设 / 待研究",
        "2026-11-12（本轮占位，无采集值）",
        "是：参数为空，禁止倒推",
    ], 9):
        style_text(ws_p.cell(row, col, v), FILL_PENDING)

ws_p.merge_cells("A56:N56")
ws_p["A56"] = "v0.1 说明：CFO-Revenue-收入测算准备-20261112.xlsx 与 CFO-Benchmark-行业基准-20261112.xlsx 若后续就绪，将在 v0.2 引用已标注条目，不在本版填入无来源数字。单位贡献边际、收入、盈亏平衡公式见 04/05 表，参数为空时结果留空（不以 0 冒充已测算）。"
ws_p["A56"].font = FONT_SM
ws_p["A56"].alignment = LEFT

# column widths for 参数台
widths = {
    "A": 14, "B": 42, "C": 12, "D": 12, "E": 12, "F": 12, "G": 12, "H": 12,
    "I": 12, "J": 12, "K": 12, "L": 40, "M": 36, "N": 22, "O": 28, "P": 22, "Q": 28,
}
for k, v in widths.items():
    ws_p.column_dimensions[k].width = v
ws_p.row_dimensions[1].height = 24
ws_p.freeze_panes = "C11"
ws_p.sheet_properties.pageSetUpPr.fitToPage = True
ws_p.page_setup.orientation = "landscape"
ws_p.page_setup.fitToWidth = 1
ws_p.page_setup.fitToHeight = 0
ws_p.sheet_view.showGridLines = False

# named ranges
def add_name(name, ref):
    wb.defined_names.add(DefinedName(name, attr_text=ref))

add_name("当前档位", "'01_参数台'!$C$3")
add_name("含02", "'01_参数台'!$C$4")
add_name("含04", "'01_参数台'!$C$5")
add_name("已发生现金", "'01_参数台'!$C$32")
add_name("头条当前下限", "'01_参数台'!$I$20")
add_name("头条当前上限", "'01_参数台'!$J$20")

# ============================================================
# 00 封面
# ============================================================
ws0 = wb.create_sheet("00_封面", 0)
ws0.merge_cells("A1:G1")
ws0["A1"] = "眠语财务模型 v0.1"
ws0["A1"].font = FONT_WHITE_LG
ws0["A1"].fill = FILL_TITLE
ws0["A1"].alignment = LEFT
for col in range(1, 8):
    ws0.cell(1, col).fill = FILL_TITLE

ws0.merge_cells("A2:G2")
ws0["A2"] = "财务准备测算｜非正式 BP 正文｜单号 CFO-20261112-MODEL｜交 CMQ-CFO 第一次验收后转 Audit｜本文件未自审通过"
ws0["A2"].font = Font(name="Calibri", size=10, color="FFFFFF")
ws0["A2"].fill = PatternFill("solid", fgColor="2E75B6")
for col in range(1, 8):
    ws0.cell(2, col).fill = PatternFill("solid", fgColor="2E75B6")
    ws0.cell(2, col).font = Font(name="Calibri", size=10, color="FFFFFF")

meta_rows = [
    (4, "版本", "v0.1（旧稿成本区间 + 收入/基准占位；同级 Cost/Revenue/Benchmark 文件交稿时尚未就绪）"),
    (5, "日期", "2026-11-12（Asia/Shanghai）；旧稿数字估算日 2026-11-07"),
    (6, "口径文件", "/workspace/mianyu-cfo/00-统一参数口径-20261112.md"),
    (7, "成本底稿（只读，未改）", "https://app.notion.com/p/411340bcc396814a9b16de9c7b11419c"),
    (8, "产品口径", "A 当前 Demo：微信小程序 AR（点按平面落位 → 预设偏移躲猫猫 → 一次轻互动），先通霁霁，屏内同玩法必达。真遮挡/人体跟随/暗房满血 6DoF/硬件不做进 A 阶段主预算。"),
    (9, "定位红线", "低唤醒夜间陪伴搭子；不是儿童哄睡、医疗助眠或依赖 AI 长对话的虚拟陪伴。不宣传未验证助眠疗效。"),
]
for r, k, v in meta_rows:
    ws0.cell(r, 1, k).font = FONT_B
    ws0.cell(r, 1).fill = FILL_HEADER
    ws0.cell(r, 1).font = FONT_WHITE
    ws0.cell(r, 1).alignment = LEFT
    ws0.cell(r, 1).border = THIN
    ws0.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
    ws0.cell(r, 2, v).font = FONT_N
    ws0.cell(r, 2).alignment = LEFT
    for c in range(2, 8):
        ws0.cell(r, c).border = THIN
        ws0.cell(r, c).fill = FILL_GREY

ws0["A11"] = "颜色约定"
ws0["A11"].font = FONT_WHITE
ws0["A11"].fill = FILL_HEADER
ws0.merge_cells("B11:C11")
ws0["B11"] = "黄色格子 = 可调输入（请只改这些）"
ws0["B11"].fill = FILL_INPUT
ws0["B11"].border = THIN
ws0.merge_cells("D11:E11")
ws0["D11"] = "蓝色格子 = 公式结果（不要覆盖）"
ws0["D11"].fill = FILL_FORMULA
ws0["D11"].border = THIN
ws0.merge_cells("F11:G11")
ws0["F11"] = "橙色格子 = 待确认 / 待裁决 / 占位"
ws0["F11"].fill = FILL_PENDING
ws0["F11"].border = THIN

ws0["A13"] = "使用方法"
ws0["A13"].font = FONT_WHITE
ws0["A13"].fill = FILL_HEADER
ws0.merge_cells("B13:G15")
ws0["B13"] = (
    "1. 在「01_参数台」C3 切换 精益 / 基准 / 完整（默认基准仅作展示，不是已锁定）。"
    "2. 完整档如需把 02/04 可选纳入主预算，将 C4/C5 改为「是」。"
    "3. 修改任一分项上下限或一个收入单价后，02 成本拆分、03 现金流、05 盈亏平衡会按公式重算。"
    "4. 收入参数现在为空：05 表盈亏平衡结果应显示为空白，不会倒推出量或单价。"
    "5. B/C/D 只在附录，不进入 A 的合计与现金流主表。"
)
ws0["B13"].alignment = Alignment(wrap_text=True, vertical="center")
ws0["B13"].fill = FILL_NOTE
for c in range(2, 8):
    ws0.cell(13, c).fill = FILL_NOTE
    ws0.cell(13, c).border = THIN
    ws0.cell(14, c).fill = FILL_NOTE
    ws0.cell(14, c).border = THIN
    ws0.cell(15, c).fill = FILL_NOTE
    ws0.cell(15, c).border = THIN
ws0.row_dimensions[13].height = 20
ws0.row_dimensions[15].height = 20
ws0.merge_cells("A13:A15")
ws0["A13"].alignment = CENTER

# live summary — all formulas
section_bar(ws0, 17, "当前档摘要（全部为公式，随参数台联动）", 1, 7)
sum_headers = ["指标", "下限（元）", "上限（元）", "下限（万元）", "上限（万元）", "口径", "待确认"]
for i, h in enumerate(sum_headers, 1):
    ws0.cell(18, i, h)
style_header_row(ws0, 18, 1, 7)

summary_items = [
    (19, "当前档位", "='01_参数台'!C3", None, "展示档，用户尚未锁定"),
    (20, "旧稿头条一次性合计（验收锚点）", "='01_参数台'!I20", "='01_参数台'!J20", "与 11-07 底稿硬对齐；待询价"),
    (21, "分项求和（主预算，含开关控制的02/04）", "='01_参数台'!I19", "='01_参数台'!J19", "公式求和"),
    (22, "差额（头条−分项）待 CFO 裁决", "='01_参数台'!I21", "='01_参数台'!J21", "禁止衬平，待裁决"),
    (23, "已发生现金", "='01_参数台'!C32", "='01_参数台'!C32", "H8 估算，待票据"),
    (24, "仍需一次性（按头条−已发生）", "='03_现金流'!B8", "='03_现金流'!C8", "主口径：与旧稿头条对齐"),
    (25, "仍需一次性（按分项求和−已发生）", "='03_现金流'!B10", "='03_现金流'!C10", "对照口径，非验收替代"),
    (26, "Demo期月度持续", "='01_参数台'!I26", "='01_参数台'!J26", "待询价；另加认证年费"),
    (27, "认证年费", "='01_参数台'!I27", "='01_参数台'!J27", "基准/完整是否同 300 待确认"),
]
# row 19 档位 is text
ws0["A19"] = "当前档位"
ws0["B19"] = "='01_参数台'!C3"
style_formula(ws0["B19"], num=False)
ws0.merge_cells("B19:E19")
ws0["F19"] = "默认展示=基准（旧稿建议首选）"
ws0["G19"] = "是：用户尚未锁定"
style_text(ws0["F19"], FILL_GREY)
style_text(ws0["G19"], FILL_PENDING)
ws0["A19"].border = THIN
ws0["A19"].font = FONT_B

for r, name, lo, hi, note in [
    (20, "旧稿头条一次性合计（验收锚点）", "='01_参数台'!I20", "='01_参数台'!J20", "与 11-07 底稿硬对齐；待询价"),
    (21, "分项求和（主预算，含开关控制的02/04）", "='01_参数台'!I19", "='01_参数台'!J19", "公式求和"),
    (22, "差额（头条−分项）待 CFO 裁决", "='01_参数台'!I21", "='01_参数台'!J21", "禁止衬平，待裁决"),
    (23, "已发生现金", "='01_参数台'!C32", "='01_参数台'!C32", "H8 估算，待票据"),
    (24, "仍需一次性（按头条−已发生）", "='03_现金流'!B8", "='03_现金流'!C8", "主口径：与旧稿头条对齐"),
    (25, "仍需一次性（按分项求和−已发生）", "='03_现金流'!B10", "='03_现金流'!C10", "对照口径，非验收替代"),
    (26, "Demo期月度持续", "='01_参数台'!I26", "='01_参数台'!J26", "待询价；另加认证年费"),
    (27, "认证年费", "='01_参数台'!I27", "='01_参数台'!J27", "基准/完整是否同 300 待确认"),
]:
    ws0.cell(r, 1, name).font = FONT_B
    ws0.cell(r, 1).border = THIN
    ws0.cell(r, 1).alignment = LEFT
    ws0.cell(r, 2, lo)
    style_formula(ws0.cell(r, 2), pending=(r == 22))
    ws0.cell(r, 3, hi)
    style_formula(ws0.cell(r, 3), pending=(r == 22))
    ws0.cell(r, 4, f"=IF(B{r}=\"\",\"\",B{r}/10000)")
    style_formula(ws0.cell(r, 4), pending=(r == 22))
    ws0.cell(r, 4).number_format = "0.000"
    ws0.cell(r, 5, f"=IF(C{r}=\"\",\"\",C{r}/10000)")
    style_formula(ws0.cell(r, 5), pending=(r == 22))
    ws0.cell(r, 5).number_format = "0.000"
    style_text(ws0.cell(r, 6, note), FILL_GREY)
    style_text(ws0.cell(r, 7, "是"), FILL_PENDING)

ws0.merge_cells("A29:G31")
ws0["A29"] = (
    "工作表：00 封面｜01 参数台｜02 A阶段成本拆分｜03 现金流｜04 收入与收支结构｜05 盈亏平衡｜06 附录BCD｜07 待确认清单｜08 假设H1-H8。"
    "关键结果栏均为公式。未确认假设未写成事实。本工作簿不覆盖 2026-11-07 Notion 定稿页。"
    "测算说明：/workspace/mianyu-cfo/CFO-FinancialModel-测算说明-20261112.md"
)
ws0["A29"].alignment = Alignment(wrap_text=True, vertical="center")
ws0["A29"].font = FONT_SM
ws0.row_dimensions[29].height = 20
ws0.row_dimensions[8].height = 36
ws0.row_dimensions[9].height = 32
ws0.column_dimensions["A"].width = 42
for col in "BCDEFG":
    ws0.column_dimensions[col].width = 22
ws0.sheet_view.showGridLines = False
ws0.row_dimensions[1].height = 24

# ============================================================
# 02 A阶段成本拆分
# ============================================================
ws_c = wb.create_sheet("02_A阶段成本拆分")
ws_c.merge_cells("A1:K1")
ws_c["A1"] = "A 阶段成本拆分（全部公式链接参数台；B/C/D 不在本表）"
ws_c["A1"].font = FONT_WHITE_LG
ws_c["A1"].fill = FILL_TITLE
for col in range(1, 12):
    ws_c.cell(1, col).fill = FILL_TITLE
    ws_c.cell(1, col).font = FONT_WHITE_LG

ws_c["A2"] = "当前档位"
ws_c["B2"] = "='01_参数台'!C3"
style_formula(ws_c["B2"], num=False)
ws_c["C2"] = "完整档含02"
ws_c["D2"] = "='01_参数台'!C4"
style_formula(ws_c["D2"], num=False)
ws_c["E2"] = "完整档含04"
ws_c["F2"] = "='01_参数台'!C5"
style_formula(ws_c["F2"], num=False)
ws_c.merge_cells("G2:K2")
ws_c["G2"] = "分项与头条均来自参数台；差额不衬平，交 CFO 裁决。单位：元。"
ws_c["G2"].font = FONT_SM

ch = ["分项", "精益_下限", "精益_上限", "基准_下限", "基准_上限", "完整_下限", "完整_上限", "当前_下限", "当前_上限", "公式说明", "待确认"]
for i, h in enumerate(ch, 1):
    ws_c.cell(4, i, h)
style_header_row(ws_c, 4, 1, 11)

# map rows in 参数台 11-21
cost_lines = [
    (5, "工程包", 11, "='01_参数台'!C11", "参数台 ENG 行"),
    (6, "IP美术", 12, "='01_参数台'!C12", "参数台 IP 行；完整档为五皮"),
    (7, "UI/UX", 13, "='01_参数台'!C13", "参数台 UX 行"),
    (8, "互动文案", 14, "='01_参数台'!C14", "参数台 COPY 行"),
    (9, "云+认证一次性", 15, "='01_参数台'!C15", "参数台 CLOUD 行"),
    (10, "测试", 16, "='01_参数台'!C16", "参数台 TEST 行"),
    (11, "02可选（按开关计入当前列）", 17, "='01_参数台'!C17", "当前列已按 C4 开关；精益/基准列显示 0"),
    (12, "04可选（按开关计入当前列）", 18, "='01_参数台'!C18", "当前列已按 C5 开关；精益/基准列显示 0"),
]
for r, name, pr, _, note in cost_lines:
    ws_c.cell(r, 1, name).font = FONT_N
    ws_c.cell(r, 1).border = THIN
    for i, col in enumerate("CDEFGHIJ"):
        # C=3 ... J=10 on 参数台, same item row
        # 参数台 cols: C D E F G H I J = 3..10
        src_col = get_column_letter(3 + i)
        ws_c.cell(r, 2 + i, f"='01_参数台'!{src_col}{pr}")
        style_formula(ws_c.cell(r, 2 + i))
    style_text(ws_c.cell(r, 10, note), FILL_GREY)
    style_text(ws_c.cell(r, 11, "是：待询价"), FILL_PENDING)

ws_c.cell(13, 1, "分项求和（主预算）").font = FONT_B
ws_c["A13"].border = THIN
ws_c["A13"].fill = FILL_FORMULA
for i, col in enumerate("CDEFGHIJ"):
    ws_c.cell(13, 2 + i, f"='01_参数台'!{col}19")
    style_formula(ws_c.cell(13, 2 + i))
style_text(ws_c.cell(13, 10, "参数台第19行：11–16 + 开关控制的 02/04"), FILL_GREY)
style_text(ws_c.cell(13, 11, "是：与头条可能有差额"), FILL_GAP)

ws_c.cell(14, 1, "旧稿头条一次性合计（验收锚点）").font = FONT_B
ws_c["A14"].border = THIN
ws_c["A14"].fill = FILL_FORMULA
for i, col in enumerate("CDEFGHIJ"):
    ws_c.cell(14, 2 + i, f"='01_参数台'!{col}20")
    style_formula(ws_c.cell(14, 2 + i))
style_text(ws_c.cell(14, 10, "必须与旧稿 2.5–5.5 / 5.5–11 / 11–22 万元区间一致"), FILL_GREY)
style_text(ws_c.cell(14, 11, "是：待询价，档位未锁定"), FILL_PENDING)

ws_c.cell(15, 1, "差额（头条−分项）待 CFO 裁决").font = FONT_WARN
ws_c["A15"].border = THIN
ws_c["A15"].fill = FILL_GAP
for i, col in enumerate("CDEFGHIJ"):
    ws_c.cell(15, 2 + i, f"='01_参数台'!{col}21")
    style_formula(ws_c.cell(15, 2 + i), pending=True)
style_text(ws_c.cell(15, 10, "正差=头条含未归类；负差=分项高于头条。禁止虚拟行衬平。"), FILL_GAP)
style_text(ws_c.cell(15, 11, "是：待 CFO 裁决"), FILL_GAP)

ws_c.cell(16, 1, "分项求和（完整对照：始终含02+04）").font = FONT_N
ws_c["A16"].border = THIN
for i, col in enumerate("CDEFGHIJ"):
    ws_c.cell(16, 2 + i, f"='01_参数台'!{col}22")
    style_formula(ws_c.cell(16, 2 + i))
style_text(ws_c.cell(16, 10, "仅对照，不替代头条验收锚点"), FILL_GREY)
style_text(ws_c.cell(16, 11, "是：对照用"), FILL_PENDING)

ws_c.merge_cells("A18:K20")
ws_c["A18"] = (
    "对齐说明（按默认开关：02/04=否 计算的分项区间，供对照，非另估一套数）："
    "精益分项求和 15,400–44,800 vs 头条 25,000–55,000，差额 9,600–10,200；"
    "基准分项求和 51,000–103,000 vs 头条 55,000–110,000，差额 4,000–7,000；"
    "完整（不含02/04）分项求和 129,000–233,000 vs 头条 110,000–220,000，差额 −19,000–−13,000；"
    "完整（含02+04）分项求和 149,000–303,000 vs 头条 110,000–220,000，差额 −39,000–−83,000。"
    "上列差额由公式重算，改参数台分项后以公式为准。未自行改旧稿头条。"
)
ws_c["A18"].alignment = Alignment(wrap_text=True, vertical="center")
ws_c["A18"].font = FONT_SM
ws_c["A18"].fill = FILL_GAP
for r in range(18, 21):
    for c in range(1, 12):
        ws_c.cell(r, c).fill = FILL_GAP
        ws_c.cell(r, c).border = THIN
ws_c.row_dimensions[18].height = 22
ws_c.row_dimensions[20].height = 22

ws_c.column_dimensions["A"].width = 36
for col in "BCDEFGHI":
    ws_c.column_dimensions[col].width = 13
ws_c.column_dimensions["J"].width = 42
ws_c.column_dimensions["K"].width = 22
ws_c.freeze_panes = "B5"
ws_c.sheet_view.showGridLines = False

# ============================================================
# 03 现金流
# ============================================================
ws_f = wb.create_sheet("03_现金流")
ws_f.merge_cells("A1:G1")
ws_f["A1"] = "现金流：已发生 vs 仍需；一次性 vs 月度持续（A 阶段；不混入 B/C/D；不扣 Bot 替代价值）"
ws_f["A1"].font = FONT_WHITE_LG
ws_f["A1"].fill = FILL_TITLE
for col in range(1, 8):
    ws_f.cell(1, col).fill = FILL_TITLE
    ws_f.cell(1, col).font = FONT_WHITE_LG

ws_f["A2"] = "当前档位"
ws_f["B2"] = "='01_参数台'!C3"
style_formula(ws_f["B2"], num=False)
ws_f.merge_cells("C2:G2")
ws_f["C2"] = "主口径「仍需一次性」= 旧稿头条合计 − 已发生现金，以与验收标准（3）硬对齐。分项口径并列表对照。"
ws_f["C2"].font = FONT_SM

fh = ["项目", "下限（元）", "上限（元）", "下限（万元）", "上限（万元）", "口径 / 公式", "待确认"]
for i, h in enumerate(fh, 1):
    ws_f.cell(4, i, h)
style_header_row(ws_f, 4, 1, 7)

# helper to add a formula row
def cash_row(ws, r, name, lo, hi, note, pending=False, wan=True):
    ws.cell(r, 1, name).font = FONT_B
    ws.cell(r, 1).border = THIN
    ws.cell(r, 1).alignment = LEFT
    ws.cell(r, 2, lo)
    style_formula(ws.cell(r, 2), pending=pending)
    ws.cell(r, 3, hi)
    style_formula(ws.cell(r, 3), pending=pending)
    if wan:
        ws.cell(r, 4, f'=IF(OR(B{r}="",B{r}="-"),"",B{r}/10000)')
        ws.cell(r, 5, f'=IF(OR(C{r}="",C{r}="-"),"",C{r}/10000)')
        style_formula(ws.cell(r, 4), pending=pending)
        style_formula(ws.cell(r, 5), pending=pending)
        ws.cell(r, 4).number_format = "0.000"
        ws.cell(r, 5).number_format = "0.000"
    style_text(ws.cell(r, 6, note), FILL_GAP if pending else FILL_GREY)
    style_text(ws.cell(r, 7, "是"), FILL_PENDING)

cash_row(ws_f, 5, "已发生现金", "='01_参数台'!C32", "='01_参数台'!C32",
         "H8：≈0，估算；有票据后回填参数台 C32")
cash_row(ws_f, 6, "旧稿头条一次性合计", "='01_参数台'!I20", "='01_参数台'!J20",
         "验收锚点，随当前档联动")
cash_row(ws_f, 7, "分项求和（主预算）", "='01_参数台'!I19", "='01_参数台'!J19",
         "公式求和，随档位与 02/04 开关联动")
cash_row(ws_f, 8, "仍需一次性（主口径=头条−已发生）", "=B6-B5", "=C6-C5",
         "仍需现金=上列三档（口径原文）。改档位或已发生现金后联动。")
cash_row(ws_f, 9, "差额（头条−分项）", "='01_参数台'!I21", "='01_参数台'!J21",
         "未归类/超支对照，待 CFO 裁决", pending=True)
cash_row(ws_f, 10, "仍需一次性（对照=分项−已发生）", "=B7-B5", "=C7-C5",
         "对照口径，不替代主口径与旧稿硬对齐")
cash_row(ws_f, 11, "Bot替代价值（非现金，不扣减）", "='01_参数台'!C38", "='01_参数台'!C39",
         "非现金；不可入账为已节省，未从第8/10行扣减")
cash_row(ws_f, 12, "Demo期月度持续", "='01_参数台'!I26", "='01_参数台'!J26",
         "元/月；不计入一次性头条")
cash_row(ws_f, 13, "认证年费", "='01_参数台'!I27", "='01_参数台'!J27",
         "元/年；基准/完整是否同 300 待确认")
cash_row(ws_f, 14, "开发周期（公历周）", "='01_参数台'!I28", "='01_参数台'!J28",
         "公历周；非 7 人天")
ws_f["B14"].number_format = "0"
ws_f["C14"].number_format = "0"

# 示意月数
cash_row(ws_f, 15, "示意月数（周×7÷换算分母）", "=IF(OR('01_参数台'!I28=\"\",'01_参数台'!I29=0),\"\",'01_参数台'!I28*7/'01_参数台'!I29)",
         "=IF(OR('01_参数台'!J28=\"\",'01_参数台'!J29=0),\"\",'01_参数台'!J28*7/'01_参数台'!J29)",
         "示意折月，付款节奏未约定，待确认")
ws_f["B15"].number_format = "0.00"
ws_f["C15"].number_format = "0.00"
ws_f["D15"].number_format = "0.000"
ws_f["E15"].number_format = "0.000"

# 示意：Demo 期持续费用合计（月度×示意月数）+ 年费，不含一次性
cash_row(ws_f, 16, "示意：持续费用合计（月度×示意月数＋年费）",
         '=IF(OR(B12="",B15=""),"",B12*B15+B13)',
         '=IF(OR(C12="",C15=""),"",C12*C15+C13)',
         "示意，非合同付款安排；未计入营收（收入参数为空，不以 0 充当流入）")

ws_f.merge_cells("A18:G18")
ws_f["A18"] = "示意月度流出（非合同节奏，待确认）。一次性按期初一次流出；月度按月；年费放在第 1 月。无收入流入（参数为空，不编造营收）。列示 1–12 月，超出示意月数的月份仅当月度数仍发生则按月计（此处 Demo 期后月度是否延续未约定，故仅在示意月数范围内计月度；超出部分留空）。"
ws_f["A18"].font = FONT_SM
ws_f["A18"].alignment = LEFT

mh = ["月", "一次性流出_下限", "一次性流出_上限", "月度流出_下限", "月度流出_上限", "年费（仅第1月）", "当月合计_下限", "当月合计_上限", "累计仍需流出_下限", "累计仍需流出_上限"]
# I'll put this starting col A row 20, but 年费 and totals need more columns - use A-J
for i, h in enumerate(["月序", "一次性_下限", "一次性_上限", "月度_下限", "月度_上限", "年费_下限", "年费_上限", "当月合计_下限", "当月合计_上限", "累计_下限", "累计_上限"], 1):
    ws_f.cell(20, i, h)
style_header_row(ws_f, 20, 1, 11)

# For months 1-12:
# 一次性 only month 1 = 仍需主口径 B8/C8
# 月度: if month <= CEILING(示意月数上限? or show both?) — use: if month <= ROUNDUP(上限月数,0) still uncertain.
# Cleaner: 月度计入条件 = 月序 <= CEILING(示意月数_上限,0) would mix bounds.
# Better: 月度_下限: if 月序 <= ROUNDUP(示意月数_下限,0) then 月度下限, else 0? That's inconsistent.
# Simplest honest approach: provide 12 months; 月度流出 = IF(月序<=MAX(1,ROUNDUP(示意月数,0)), 月度, "")
# Use lower bound months for lower cash, upper bound months for upper cash.
# Month m:
# 一次性: m==1 then B8/C8 else 0
# 月度_下限: IF(m<=ROUNDUP(B15,0), B12, 0) but if B15 empty, empty
# 年费: m==1 then B13/C13 else 0
# 当月合计 = sum
# 累计 = running

for m in range(1, 13):
    r = 20 + m
    ws_f.cell(r, 1, m).alignment = CENTER
    ws_f.cell(r, 1).border = THIN
    # 一次性
    if m == 1:
        ws_f.cell(r, 2, "=$B$8")
        ws_f.cell(r, 3, "=$C$8")
        ws_f.cell(r, 6, "=$B$13")
        ws_f.cell(r, 7, "=$C$13")
    else:
        ws_f.cell(r, 2, 0)
        ws_f.cell(r, 3, 0)
        ws_f.cell(r, 6, 0)
        ws_f.cell(r, 7, 0)
        # wait - I should use formulas even for 0 to keep "key results are formulas"
        ws_f.cell(r, 2, "=0")
        ws_f.cell(r, 3, "=0")
        ws_f.cell(r, 6, "=0")
        ws_f.cell(r, 7, "=0")
    # 月度: lower uses lower months, upper uses upper months; if 示意月数 empty, blank
    ws_f.cell(r, 4, f'=IF($B$15="","",IF({m}<=ROUNDUP($B$15,0),$B$12,0))')
    ws_f.cell(r, 5, f'=IF($C$15="","",IF({m}<=ROUNDUP($C$15,0),$C$12,0))')
    for col in range(2, 12):
        style_formula(ws_f.cell(r, col))
    # 当月合计
    ws_f.cell(r, 8, f'=IF(OR(B{r}="",D{r}="",F{r}=""),"",B{r}+D{r}+F{r})')
    ws_f.cell(r, 9, f'=IF(OR(C{r}="",E{r}="",G{r}=""),"",C{r}+E{r}+G{r})')
    style_formula(ws_f.cell(r, 8))
    style_formula(ws_f.cell(r, 9))
    # 累计
    if m == 1:
        ws_f.cell(r, 10, f"=H{r}")
        ws_f.cell(r, 11, f"=I{r}")
    else:
        ws_f.cell(r, 10, f'=IF(OR(J{r-1}="",H{r}=""),"",J{r-1}+H{r})')
        ws_f.cell(r, 11, f'=IF(OR(K{r-1}="",I{r}=""),"",K{r-1}+I{r})')
    style_formula(ws_f.cell(r, 10))
    style_formula(ws_f.cell(r, 11))

ws_f.merge_cells("A34:K35")
ws_f["A34"] = "本表不含 B/C/D 支出，不含编造的收入流入。改参数台档位、头条、已发生现金、月度或年费后，本表公式全部联动。示意月度串不是付款计划。"
ws_f["A34"].font = FONT_SM
ws_f["A34"].alignment = LEFT

ws_f.column_dimensions["A"].width = 42
for col in "BCDEFGHIJK":
    ws_f.column_dimensions[col].width = 16
ws_f.freeze_panes = "B5"
ws_f.sheet_view.showGridLines = False

# ============================================================
# 04 收入与收支结构
# ============================================================
ws_r = wb.create_sheet("04_收入与收支结构")
ws_r.merge_cells("A1:L1")
ws_r["A1"] = "收入与不同模式收支结构（待研究情景，非已确定商业决策；参数未到则结果留空，不以 0 冒充已测算）"
ws_r["A1"].font = FONT_WHITE_LG
ws_r["A1"].fill = FILL_TITLE
for col in range(1, 13):
    ws_r.cell(1, col).fill = FILL_TITLE
    ws_r.cell(1, col).font = FONT_WHITE_LG

ws_r.merge_cells("A2:L2")
ws_r["A2"] = "输入全部在参数台第51–55行。公式：收入=单价×数量；单位贡献边际=单价−单位变动成本；贡献总额=单位贡献边际×数量。缺任一输入则对应结果为空白。"
ws_r["A2"].font = FONT_SM

rh = ["模式ID", "模式名称", "单价", "数量", "单位变动成本", "数量单位", "周期", "含税",
      "收入（公式）", "单位贡献边际（公式）", "贡献总额（公式）", "状态"]
for i, h in enumerate(rh, 1):
    ws_r.cell(4, i, h)
style_header_row(ws_r, 4, 1, 12)

for i in range(5):
    r = 5 + i
    pr = 51 + i
    ws_r.cell(r, 1, f"='01_参数台'!A{pr}")
    style_formula(ws_r.cell(r, 1), num=False)
    ws_r.cell(r, 2, f"='01_参数台'!B{pr}")
    style_formula(ws_r.cell(r, 2), num=False)
    for col, src in [(3, "C"), (4, "D"), (5, "E")]:
        ws_r.cell(r, col, f'=IF(\'01_参数台\'!{src}{pr}="","",\'01_参数台\'!{src}{pr})')
        style_formula(ws_r.cell(r, col))
        ws_r.cell(r, col).number_format = YUAN2
    for col, src in [(6, "F"), (7, "G"), (8, "H")]:
        ws_r.cell(r, col, f'=IF(\'01_参数台\'!{src}{pr}="","",\'01_参数台\'!{src}{pr})')
        style_formula(ws_r.cell(r, col), num=False)
    # 收入
    ws_r.cell(r, 9, f'=IF(OR(C{r}="",D{r}=""),"",C{r}*D{r})')
    style_formula(ws_r.cell(r, 9))
    ws_r.cell(r, 9).number_format = YUAN2
    # 单位贡献
    ws_r.cell(r, 10, f'=IF(OR(C{r}="",E{r}=""),"",C{r}-E{r})')
    style_formula(ws_r.cell(r, 10))
    ws_r.cell(r, 10).number_format = YUAN2
    # 贡献总额
    ws_r.cell(r, 11, f'=IF(OR(J{r}="",D{r}=""),"",J{r}*D{r})')
    style_formula(ws_r.cell(r, 11))
    ws_r.cell(r, 11).number_format = YUAN2
    ws_r.cell(r, 12, f'=IF(AND(C{r}="",D{r}="",E{r}=""),"待确认：参数为空，未测算",IF(OR(C{r}="",D{r}="",E{r}=""),"待确认：参数不完整","已按输入试算（仍属待研究情景）"))')
    style_formula(ws_r.cell(r, 12), num=False)
    ws_r.cell(r, 12).fill = FILL_PENDING

ws_r.merge_cells("A11:L12")
ws_r["A11"] = (
    "获客成本、税费、渠道分成等未列入：无经确认参数。同级收入/基准表 v0.1 交稿时不存在，故未引用任何公开可比数字，以免把未核对来源写成模型输入。"
    "不要把本表空白解读为收入为 0。"
)
ws_r["A11"].alignment = Alignment(wrap_text=True, vertical="center")
ws_r["A11"].font = FONT_SM

ws_r.column_dimensions["A"].width = 10
ws_r.column_dimensions["B"].width = 24
for col in "CDEFGHIJK":
    ws_r.column_dimensions[col].width = 16
ws_r.column_dimensions["L"].width = 36
ws_r.sheet_view.showGridLines = False

# ============================================================
# 05 盈亏平衡
# ============================================================
ws_b = wb.create_sheet("05_盈亏平衡")
ws_b.merge_cells("A1:L1")
ws_b["A1"] = "盈亏平衡（必须写明：相对哪一档成本、哪一收入模式、哪些固定/变动成本；缺参数留空，禁止倒推看起来合理的数）"
ws_b["A1"].font = FONT_WHITE_LG
ws_b["A1"].fill = FILL_TITLE
for col in range(1, 13):
    ws_b.cell(1, col).fill = FILL_TITLE
    ws_b.cell(1, col).font = FONT_WHITE_LG

ws_b["A3"] = "相对成本档位"
ws_b["B3"] = "='01_参数台'!C3"
style_formula(ws_b["B3"], num=False)
ws_b["C3"] = "随参数台 C3 联动，不是已锁定档位"
ws_b["C3"].font = FONT_SM

ws_b["A4"] = "固定成本口径A：仍需一次性_主口径（头条−已发生）下限"
ws_b["B4"] = "='03_现金流'!B8"
style_formula(ws_b["B4"])
ws_b["C4"] = "上限"
ws_b["D4"] = "='03_现金流'!C8"
style_formula(ws_b["D4"])
ws_b["E4"] = "用于「一次性投入回本」所需量/单价"
ws_b["E4"].font = FONT_SM

ws_b["A5"] = "固定成本口径B：Demo期月度持续下限"
ws_b["B5"] = "='01_参数台'!I26"
style_formula(ws_b["B5"])
ws_b["C5"] = "上限"
ws_b["D5"] = "='01_参数台'!J26"
style_formula(ws_b["D5"])
ws_b["E5"] = "用于「月度平衡」所需量（覆盖当月持续费用，不含一次性摊销，也不含年费）"
ws_b["E5"].font = FONT_SM

ws_b["A6"] = "年费（单独列，不并入月度平衡，以免口径含混）"
ws_b["B6"] = "='01_参数台'!I27"
style_formula(ws_b["B6"])
ws_b["C6"] = "上限"
ws_b["D6"] = "='01_参数台'!J27"
style_formula(ws_b["D6"])

ws_b.merge_cells("A7:L7")
ws_b["A7"] = "变动成本：各模式「单位变动成本」（参数台）。单位贡献边际≤0 或参数缺失时，结果留空。回本量=固定成本÷单位贡献边际；回本单价=单位变动成本+固定成本÷数量（须已有数量）。"
ws_b["A7"].font = FONT_SM

bh = [
    "模式ID", "收入模式（待研究）", "单价", "数量", "单位变动成本", "单位贡献边际",
    "回本所需量_下限（对口径A）", "回本所需量_上限（对口径A）",
    "回本所需单价_下限（对口径A，须有数量）", "回本所需单价_上限（对口径A，须有数量）",
    "月度平衡所需量_下限（对口径B）", "月度平衡所需量_上限（对口径B）",
]
for i, h in enumerate(bh, 1):
    ws_b.cell(9, i, h)
style_header_row(ws_b, 9, 1, 12)

for i in range(5):
    r = 10 + i
    rr = 5 + i  # row on sheet 04
    ws_b.cell(r, 1, f"='04_收入与收支结构'!A{rr}")
    style_formula(ws_b.cell(r, 1), num=False)
    ws_b.cell(r, 2, f"='04_收入与收支结构'!B{rr}")
    style_formula(ws_b.cell(r, 2), num=False)
    ws_b.cell(r, 3, f"='04_收入与收支结构'!C{rr}")
    ws_b.cell(r, 4, f"='04_收入与收支结构'!D{rr}")
    ws_b.cell(r, 5, f"='04_收入与收支结构'!E{rr}")
    for col in range(3, 6):
        style_formula(ws_b.cell(r, col))
        ws_b.cell(r, col).number_format = YUAN2
    ws_b.cell(r, 6, f"='04_收入与收支结构'!J{rr}")
    style_formula(ws_b.cell(r, 6))
    ws_b.cell(r, 6).number_format = YUAN2
    # 回本量 下限/上限： need unit contribution > 0
    ws_b.cell(r, 7, f'=IF(OR(F{r}="",F{r}<=0,$B$4=""),"",$B$4/F{r})')
    ws_b.cell(r, 8, f'=IF(OR(F{r}="",F{r}<=0,$D$4=""),"",$D$4/F{r})')
    # 回本单价： need qty > 0
    ws_b.cell(r, 9, f'=IF(OR(E{r}="",D{r}="",D{r}<=0,$B$4=""),"",E{r}+$B$4/D{r})')
    ws_b.cell(r, 10, f'=IF(OR(E{r}="",D{r}="",D{r}<=0,$D$4=""),"",E{r}+$D$4/D{r})')
    # 月度平衡量
    ws_b.cell(r, 11, f'=IF(OR(F{r}="",F{r}<=0,$B$5=""),"",$B$5/F{r})')
    ws_b.cell(r, 12, f'=IF(OR(F{r}="",F{r}<=0,$D$5=""),"",$D$5/F{r})')
    for col in range(7, 13):
        style_formula(ws_b.cell(r, col))
        ws_b.cell(r, col).number_format = YUAN2
        # if empty now, they'll stay pending visually? results are formulas - keep blue
        # when blank due to missing params, still formula cells

ws_b.merge_cells("A16:L18")
ws_b["A16"] = (
    "v0.1：五种收入模式参数均为空，故第10–14行回本量、回本单价、月度平衡量应为空白，这是符合验收的结果，不是遗漏计算。"
    "填入参数台单价与单位变动成本后，回本量会按当前档一次性仍需（口径A）自动计算；再填数量后，回本所需单价也会算出。"
    "本表不把认证年费摊进月度平衡，也不把 B/C/D 成本并入固定成本。未使用人天费率倒推平衡点。"
)
ws_b["A16"].alignment = Alignment(wrap_text=True, vertical="center")
ws_b["A16"].font = FONT_SM
ws_b["A16"].fill = FILL_NOTE
for r in range(16, 19):
    for c in range(1, 13):
        ws_b.cell(r, c).fill = FILL_NOTE
        ws_b.cell(r, c).border = THIN

ws_b.column_dimensions["A"].width = 12
ws_b.column_dimensions["B"].width = 22
for col in "CDEFGHIJKL":
    ws_b.column_dimensions[col].width = 16
ws_b.row_dimensions[9].height = 36
ws_b.sheet_view.showGridLines = False
ws_b.freeze_panes = "C10"

# ============================================================
# 06 附录 BCD
# ============================================================
ws_a = wb.create_sheet("06_附录BCD")
ws_a.merge_cells("A1:G1")
ws_a["A1"] = "附录：B/C/D 阶段区间（旧稿情景，待专项复核）— 严禁混入 A 阶段合计或 A 现金流主表"
ws_a["A1"].font = FONT_WHITE_LG
ws_a["A1"].fill = FILL_TITLE
for col in range(1, 8):
    ws_a.cell(1, col).fill = FILL_TITLE
    ws_a.cell(1, col).font = FONT_WHITE_LG

ws_a.merge_cells("A2:G2")
ws_a["A2"] = "本表数字全部链接参数台第42–47行。不进入 02/03 表合计。不是本轮主算。"
ws_a["A2"].font = FONT_SM

for i, h in enumerate(["阶段", "含义（口径原文）", "下限（元）", "上限（元）", "下限（万元）", "上限（万元）", "状态"], 1):
    ws_a.cell(4, i, h)
style_header_row(ws_a, 4, 1, 7)

ws_a["A5"] = "B 产品验证"
ws_a["B5"] = "真实用户走完/愿再开/想留"
ws_a["C5"] = "='01_参数台'!C42"
ws_a["D5"] = "='01_参数台'!C43"
ws_a["E5"] = "=IF(C5=\"\",\"\",C5/10000)"
ws_a["F5"] = "=IF(D5=\"\",\"\",D5/10000)"
ws_a["G5"] = "待专项复核；不得混入 A"

ws_a["A6"] = "C 商业试点"
ws_a["B6"] = "小规模试点 1–3 月感"
ws_a["C6"] = "='01_参数台'!C44"
ws_a["D6"] = "='01_参数台'!C45"
ws_a["E6"] = "=IF(C6=\"\",\"\",C6/10000)"
ws_a["F6"] = "=IF(D6=\"\",\"\",D6/10000)"
ws_a["G6"] = "待专项复核；不得混入 A"

ws_a["A7"] = "D 规模化"
ws_a["B7"] = "多渠道；若上硬件则供应链单列"
ws_a["C7"] = "='01_参数台'!C46"
ws_a["D7"] = "='01_参数台'!C47"  # may be empty
ws_a["E7"] = "=IF(C7=\"\",\"\",C7/10000)"
ws_a["F7"] = "=IF(D7=\"\",\"\",D7/10000)"
ws_a["G7"] = "上限旧稿为「数百万+」，参数台留空未倒推；待专项复核；不得混入 A"

for r in range(5, 8):
    ws_a.cell(r, 1).font = FONT_B
    ws_a.cell(r, 1).border = THIN
    style_text(ws_a.cell(r, 2), FILL_GREY)
    style_formula(ws_a.cell(r, 3))
    style_formula(ws_a.cell(r, 4))
    style_formula(ws_a.cell(r, 5))
    style_formula(ws_a.cell(r, 6))
    ws_a.cell(r, 5).number_format = "0.000"
    ws_a.cell(r, 6).number_format = "0.000"
    style_text(ws_a.cell(r, 7), FILL_PENDING)

ws_a.merge_cells("A9:G10")
ws_a["A9"] = "硬件量产、完整商业化软件系统、酒店规模化部署不列为本轮必须完成或已确定投入。D 若上硬件须供应链单列，本附录未编造供应链数字。"
ws_a["A9"].alignment = Alignment(wrap_text=True, vertical="center")
ws_a["A9"].font = FONT_SM

ws_a.column_dimensions["A"].width = 16
ws_a.column_dimensions["B"].width = 36
for col in "CDEF":
    ws_a.column_dimensions[col].width = 14
ws_a.column_dimensions["G"].width = 50
ws_a.sheet_view.showGridLines = False

# ============================================================
# 07 待确认清单
# ============================================================
ws_t = wb.create_sheet("07_待确认清单")
ws_t.merge_cells("A1:F1")
ws_t["A1"] = "待确认清单（v0.1）"
ws_t["A1"].font = FONT_WHITE_LG
ws_t["A1"].fill = FILL_TITLE
for col in range(1, 7):
    ws_t.cell(1, col).fill = FILL_TITLE
    ws_t.cell(1, col).font = FONT_WHITE_LG

for i, h in enumerate(["序号", "事项", "当前状态（公式或说明）", "影响", "建议裁决人", "是否阻断 v0.1 交稿"], 1):
    ws_t.cell(3, i, h)
style_header_row(ws_t, 3, 1, 6)

# some rows use formulas for live status
todos = [
    (4, "T01", "预算档位（精益/基准/完整）用户尚未锁定",
     "=\"当前展示档：\"&'01_参数台'!C3&\"（默认基准仅为旧稿建议首选，不是已定案）\"",
     "所有当前档结果随 C3 切换，不得写成已定案", "用户（经 CFO/CEO，不由本 Bot 越级）", "否：三档可切换已交付"),
    (5, "T02", "A 阶段全部分项与头条均为待询价，非合同价、非已批准预算",
     "待 2–3 家询价后回填参数台分项/头条",
     "绝对额可能变化，但结构与公式已就绪", "CFO 组织询价", "否"),
    (6, "T03", "已发生现金 ≈ 0（H8）待票据回填",
     "=\"参数台已发生现金=\"&TEXT('01_参数台'!C32,\"#,##0\")&\" 元\"",
     "回填后仍需一次性=头条−已发生 自动变", "CFO / 票据持有人", "否"),
    (7, "T04", "分项求和与旧稿头条合计存在差额，未衬平",
     "=\"当前档差额下限=\"&TEXT('01_参数台'!I21,\"#,##0\")&\"；上限=\"&TEXT('01_参数台'!J21,\"#,##0\")",
     "仍需主口径按头条对齐；差额单独列示待裁决", "CMQ-CFO 裁决", "否：已标注，未改旧稿头条"),
    (8, "T05", "完整档 02/04 可选是否纳入主预算",
     "=\"含02=\"&'01_参数台'!C4&\"；含04=\"&'01_参数台'!C5",
     "开关为「是」时完整分项合计上升，差额更负", "CMQ-CFO / 用户（不越级）", "否：默认不含"),
    (9, "T06", "基准/完整认证年费是否与精益同为 300 元/年",
     "旧稿仅对精益写明 300，本表按同额占位",
     "影响现金流年费与示意月度串", "CMQ-CFO", "否：已占位并标注"),
    (10, "T07", "五种收入模式参数（单价/数量/变动成本/周期/含税/获客）均为空",
     "=\"R1状态：\"&'04_收入与收支结构'!L5",
     "盈亏平衡量与单价留空，符合「缺参数不倒推」", "CMQ-CFO-Revenue / Benchmark 就绪后迭代 v0.2", "否：结构已建"),
    (11, "T08", "同级 Cost / Revenue / Benchmark xlsx 在本版交稿时尚未引入",
     "v0.1 交稿时目录中仅有口径与派单记录；若后续出现将在 v0.2 引用",
     "收入与可比基准暂无外部参数", "CMQ-CFO 协调同级交付", "否：按派单允许占位出 v0.1"),
    (12, "T09", "B/C/D 区间待专项复核；D 上限旧稿为「数百万+」已留空",
     "仅附录，未混入 A",
     "不影响 A 主算", "CFO 专项复核", "否"),
    (13, "T10", "人天费率 550/830/1290 与外包 1200–2000 仅为折算锚点",
     "未用来倒推已确认人天或替代分项报价",
     "禁止把折算写成合同成本", "询价后回填", "否"),
    (14, "T11", "示意月数换算（周×7÷30）及期初一次流出的付款节奏",
     "参数台 DAYS_M 可改；非合同安排",
     "仅影响示意月度串，不影响头条仍需", "CMQ-CFO", "否"),
    (15, "T12", "含税与否、是否含外包/云和认证的交叉口径，旧稿未逐项拆开",
     "云+认证一次性已单列；认证年费另列；含税未拆",
     "询价时应按口径第7节补全字段", "询价模板", "否"),
    (16, "T13", "02/04 可选的业务内容未在模型中展开（仅金额区间）",
     "金额来自旧稿完整档可选包",
     "不影响默认主预算（开关=否）", "产品/CFO", "否"),
]

for r, tid, item, status, impact, owner, block in todos:
    ws_t.cell(r, 1, tid).border = THIN
    ws_t.cell(r, 1).alignment = CENTER
    style_text(ws_t.cell(r, 2, item), FILL_GREY)
    if status.startswith("="):
        ws_t.cell(r, 3, status)
        style_formula(ws_t.cell(r, 3), num=False)
        ws_t.cell(r, 3).fill = FILL_PENDING
        ws_t.cell(r, 3).alignment = LEFT
    else:
        style_text(ws_t.cell(r, 3, status), FILL_PENDING)
    style_text(ws_t.cell(r, 4, impact), FILL_GREY)
    style_text(ws_t.cell(r, 5, owner), FILL_GREY)
    style_text(ws_t.cell(r, 6, block), FILL_NOTE)

ws_t.column_dimensions["A"].width = 8
ws_t.column_dimensions["B"].width = 52
ws_t.column_dimensions["C"].width = 56
ws_t.column_dimensions["D"].width = 40
ws_t.column_dimensions["E"].width = 36
ws_t.column_dimensions["F"].width = 28
ws_t.row_dimensions[3].height = 22
for r in range(4, 17):
    ws_t.row_dimensions[r].height = 32
ws_t.freeze_panes = "A4"
ws_t.sheet_view.showGridLines = False

# ============================================================
# 08 假设
# ============================================================
ws_h = wb.create_sheet("08_假设H1-H8")
ws_h.merge_cells("A1:E1")
ws_h["A1"] = "关键假设 H1–H8（类型=假设，不是事实；沿用 2026-11-07 旧稿）"
ws_h["A1"].font = FONT_WHITE_LG
ws_h["A1"].fill = FILL_TITLE
for col in range(1, 6):
    ws_h.cell(1, col).fill = FILL_TITLE
    ws_h.cell(1, col).font = FONT_WHITE_LG

for i, h in enumerate(["编号", "假设内容", "类型", "来源", "日期"], 1):
    ws_h.cell(3, i, h)
style_header_row(ws_h, 3, 1, 5)

hyps = [
    ("H1", "VisionKit V1 + 预设躲猫猫足以验收"),
    ("H2", "霁霁先通，五皮不同开"),
    ("H3", "真遮挡 / 人体 / 暗房满血不做进 A 阶段主预算"),
    ("H4", "02/04 不进精益/基准（完整为可选，见参数台开关）"),
    ("H5", "费率 550/830/1290 仅折算，非雇佣、非合同价"),
    ("H6", "WeTest 仍可采购"),
    ("H7", "Demo 期无大额云与登录中台"),
    ("H8", "已发生现金 ≈ 0（估算，待票据回填）"),
]
for i, (hid, text) in enumerate(hyps):
    r = 4 + i
    ws_h.cell(r, 1, hid).border = THIN
    ws_h.cell(r, 1).font = FONT_B
    style_text(ws_h.cell(r, 2, text), FILL_PENDING)
    style_text(ws_h.cell(r, 3, "假设，不是事实"), FILL_PENDING)
    style_text(ws_h.cell(r, 4, SRC_COST + "；统一口径第5节"), FILL_GREY)
    style_text(ws_h.cell(r, 5, DATE_EST), FILL_GREY)

ws_h.merge_cells("A13:E14")
ws_h["A13"] = "另：预算档位待用户确认；收入模式全部待研究。以上假设成立与否会影响范围和测试能否按旧稿采购，但不改变「未确认不得写成事实」的标注要求。"
ws_h["A13"].alignment = Alignment(wrap_text=True, vertical="center")
ws_h["A13"].font = FONT_SM

ws_h.column_dimensions["A"].width = 10
ws_h.column_dimensions["B"].width = 56
ws_h.column_dimensions["C"].width = 18
ws_h.column_dimensions["D"].width = 70
ws_h.column_dimensions["E"].width = 20
ws_h.sheet_view.showGridLines = False

# print / freeze
for ws in wb.worksheets:
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "1:1"
    ws.oddHeader.left.text = "眠语财务模型 v0.1｜非正式 BP"
    ws.oddFooter.left.text = "CFO-20261112-MODEL"
    ws.oddFooter.right.text = "第 &P 页"

wb.properties.title = "眠语财务模型 v0.1"
wb.properties.creator = "CMQ-CFO-FinancialModel"
wb.properties.description = "CFO-20261112-MODEL v0.1 财务准备，非正式 BP。未自审。"

OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT_XLSX)
print("WROTE", OUT_XLSX, "size", OUT_XLSX.stat().st_size)
