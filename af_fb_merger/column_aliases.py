"""
AppsFlyer / Facebook column name aliases.

Canonical key → list of possible raw column names (CN + EN). Matching is
case-insensitive and whitespace-insensitive (see resolve_columns in merger.py).
Full-width punctuation like 「（全部）」 must be in the alias list — it is NOT
auto-normalized to half-width.

Policy on which source wins for each metric (per user rules):
  - spend, impressions, clicks                  → Facebook
  - CPM, CTR, click→install CVR                 → computed
  - installs, logins, paying_users, revenue     → AppsFlyer (more accurate)
  - FB "应用安装量", FB revenue, FB 完成注册 are IGNORED on purpose
    (kept only in raw sheet for inspection)
"""

AF_ALIASES = {
    "campaign":       ["Campaign", "Campaign Name", "Campaign (Grouped)",
                       "系列", "广告系列", "广告系列名称"],
    "ad":             ["Ad", "Ad Name", "广告", "广告名称"],
    "country":        ["Country", "Geo", "Country Code",
                       "国家", "地区", "国家/地区"],
    # installs: prefer "Installs appsflyer" (first-time installs), fall back to
    # "Total attributions appsflyer" when the user's AF export only includes the
    # attributions column. These two are not identical (attributions ≥ installs
    # because they include re-attributions), but they match to within a few %
    # in practice.
    "installs":       ["Installs appsflyer", "Installs",
                       "Total attributions appsflyer", "Total Attributions",
                       "Total Installs", "Conversions",
                       "安装", "激活", "安装数", "激活数"],
    "logins":         ["Unique users ltv days cumulative appsflyer enter_server",
                       "Unique users enter_server",
                       "登录用户数", "登录用户"],
    "login_rate":     ["Conversion rate ltv days cumulative appsflyer enter_server",
                       "登录转化率"],
    "paying_users":   ["Unique users ltv days cumulative appsflyer purchase_value",
                       "Unique users purchase_value",
                       "Paying Users", "Unique Paying Users",
                       "付费用户数", "付费人数", "付费用户"],
    "pay_rate":       ["Conversion rate ltv days cumulative appsflyer purchase_value",
                       "付费转化率"],
    "purchase_count": ["Count ltv days cumulative appsflyer purchase_value",
                       "付费次数", "购买次数"],
    "revenue":        ["Revenue ltv days cumulative appsflyer purchase_value",
                       "Revenue", "Total Revenue",
                       "收入", "营收", "总收入"],
    "arppu":          ["LT ARPPU", "ARPPU"],
    "revenue_per_purchase": ["单次付费收入", "Revenue per purchase"],
    "retention_d1":   ["Retention rate 1 days on-period appsflyer",
                       "Retention Day 1", "Day 1 Retention", "Retention D1",
                       "次留", "D1留存", "次日留存"],
    "retention_d2":   ["Retention rate 2 days on-period appsflyer",
                       "D2留存"],
    "retention_d6":   ["Retention rate 6 days on-period appsflyer",
                       "D6留存"],
    "retention_d7":   ["Retention rate 7 days on-period appsflyer",
                       "Retention Day 7", "Day 7 Retention", "Retention D7",
                       "7留", "D7留存", "7日留存"],
    "retention_d14":  ["Retention rate 14 days on-period appsflyer",
                       "D14留存"],
    "retention_d21":  ["Retention rate 21 days on-period appsflyer",
                       "D21留存"],
    "retention_d30":  ["Retention rate 30 days on-period appsflyer",
                       "D30留存"],
}

FB_ALIASES = {
    "campaign":       ["Campaign name", "Campaign Name", "Campaign",
                       "广告系列名称", "系列名称", "广告系列"],
    "country":        ["Country", "Country code",
                       "国家", "国家/地区"],
    "spend":          ["Amount spent (USD)", "Amount Spent (USD)", "Amount spent",
                       "已花费金额 (USD)", "已花费金额", "花费", "消耗", "消费"],
    "impressions":    ["Impressions",
                       "展示次数", "展示"],
    "clicks":         ["Link clicks", "Clicks (all)", "Clicks",
                       "点击量（全部）", "点击量(全部)", "点击量", "链接点击量", "所有点击", "点击"],
    "registrations":  ["Completed registrations", "完成注册次数", "注册次数", "注册"],
    # FB installs & revenue intentionally NOT mapped — per user rule,
    # we trust AF for these. They'll stay in the raw sheet only.
}

# Final output column order (canonical names). Only the ones we actually
# compute/merge end up in the sheet.
CAMPAIGN_OUTPUT_COLUMNS = [
    "campaign",
    # FB frontend funnel
    "spend", "impressions", "cpm", "clicks", "ctr",
    # AF backend funnel (authoritative)
    "installs", "click_to_install_cvr", "cpi",
    "logins", "login_rate",
    "paying_users", "cpa", "pay_rate",
    "purchase_count",
    "revenue", "roas", "arppu", "revenue_per_purchase",
    "retention_d1", "retention_d2", "retention_d6", "retention_d7",
    "retention_d14", "retention_d21", "retention_d30",
    "_match_status",
]

REGION_OUTPUT_COLUMNS = [
    "country",
    "spend", "impressions", "cpm", "clicks", "ctr",
    "installs", "click_to_install_cvr", "cpi",
    "logins", "paying_users", "revenue", "cpa", "roas",
    "_match_status",
]

# OS × Country pivot — campaigns aggregated per (OS, country); Android block
# first, then iOS, each sorted by spend desc.
COUNTRY_CAMPAIGN_OUTPUT_COLUMNS = [
    "os", "country", "campaign_count",
    "spend", "impressions", "cpm", "clicks", "ctr",
    "installs", "click_to_install_cvr", "cpi",
    "logins", "login_rate",
    "paying_users", "cpa", "pay_rate",
    "purchase_count",
    "revenue", "roas", "arppu", "revenue_per_purchase",
    "retention_d1", "retention_d2", "retention_d6", "retention_d7",
    "retention_d14", "retention_d21", "retention_d30",
    "_match_status",
]

DISPLAY_HEADERS = {
    "campaign":             "Campaign",
    "country":              "地区",
    "os":                   "系统",
    "goal":                 "优化目标",
    "campaign_count":       "系列数",
    "spend":                "消耗(USD)",
    "impressions":          "展示",
    "cpm":                  "千次展示费用",
    "clicks":               "点击",
    "ctr":                  "CTR",
    "registrations":        "FB完成注册",
    "installs":             "AF安装",
    "click_to_install_cvr": "点击→安装CVR",
    "cpi":                  "CPI",
    "logins":               "AF登录人数",
    "login_rate":           "AF登录率",
    "paying_users":         "AF付费人数",
    "cpa":                  "CPA(付费)",
    "pay_rate":             "AF付费率",
    "purchase_count":       "AF付费次数",
    "revenue":              "AF收入",
    "roas":                 "ROAS",
    "arppu":                "ARPPU",
    "revenue_per_purchase": "单次付费收入",
    "retention_d1":         "D1留存",
    "retention_d2":         "D2留存",
    "retention_d6":         "D6留存",
    "retention_d7":         "D7留存",
    "retention_d14":        "D14留存",
    "retention_d21":        "D21留存",
    "retention_d30":        "D30留存",
    "_match_status":        "匹配状态",
}
