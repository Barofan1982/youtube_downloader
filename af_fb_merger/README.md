# AF × FB Merger

把 AppsFlyer 的激活/付费/留存数据和 Facebook 的消耗/展示/点击数据，按
**Campaign 名**（或地区名）精确合并，导出多 sheet 的 XLSX。

## 使用

双击 **`AFFBMerger.vbs`** 启动（首次运行会自动 pip 安装 `pandas` / `openpyxl`）。

- 顶部三个 Tab：`Campaign 合并` / `地区合并` / `国家×系列透视`，各自独立。
- 点「浏览...」分别选 AF 和 FB 的导出文件（支持 `.csv` / `.xlsx`，编码自动探测）。
- 点「导出 XLSX」，输出文件保存到 `~/Downloads/`，文件名带时间戳。

## 输出 XLSX 结构

### Campaign 维度
| Sheet | 内容 |
|---|---|
| `Campaign合并` | Campaign / 消耗(FB) / 展示(FB) / 点击(FB) / CTR / FB完成注册 / AF安装 / CPI / AF登录人数 / AF登录率 / AF付费人数 / CPA / AF付费率 / AF收入 / ROAS / D1/D7留存 / 匹配状态 |
| `原始AF_Campaign` | AF 原始数据（ad 级别，未聚合） |
| `原始FB_Campaign` | FB 原始数据（含合计行） |

**数据来源规则**（按你的要求）：
- 消耗 / 展示 / 点击 / 完成注册 → **FB**
- 安装 / 登录 / 付费 / 收入 → **AF**（更准确）
- FB 的「应用安装量」和「购物转化价值」被**忽略**，只保留在原始 sheet 里

**AF 自动聚合**：如果 AF CSV 是 ad 级别（有 `Ad` 列，每个 campaign 多行），程序会自动按 campaign 聚合（数值 sum，登录率/付费率按聚合后的 人数/安装 重算）。如果 AF 是 campaign 级别导出，直接使用不聚合。

**FB 合计行过滤**：FB 后台导出的第 2 行通常是全部合计（campaign 名为空），会被自动丢弃。

### 国家×系列透视
| Sheet | 内容 |
|---|---|
| `国家×系列透视` | 系统 / 地区 / 系列数 / 完整指标 / 匹配状态 |

按 **OS(Android/iOS) → 国家** 两级汇总，每个 (OS, 国家) 下所有 campaign 数据相加成一行；块内按消耗降序，末尾出 OS 合计，全表末尾出总计。

- Android 块 → `— Android 合计`
- iOS 块 → `— iOS 合计`
- `总计`

**系列数** 列显示该 (OS, 国家) 下的独立 campaign 数。

**匹配状态**（单行聚合多 campaign 的结果）：
- `全匹配`：该 (OS, 国家) 下所有 campaign 都在 AF 和 FB 双方都存在
- `部分 af_only` / `部分 fb_only`：有单侧存在的 campaign
- `混合`：两种单侧都有
- `小计` / `总计`：聚合行

**合并 key**：(country, campaign) 组合精确匹配；底层 merged 长表里的 AF / FB 一方缺失行被保留并在聚合时计入该 (OS, 国家) 的数据。OS 从 campaign 名中自动解析（`-iOS-` / `-Android-`，解析不出归 `Other`）。

### 地区维度
| Sheet | 内容 |
|---|---|
| `地区合并` | 地区 / 消耗 / 展示 / 点击 / 安装 / 付费用户 / 收入 / 匹配状态 |
| `原始AF_地区` | AF 原始数据 |
| `原始FB_地区` | FB 原始数据 |

**未匹配行**（AF 或 FB 单边存在的 campaign / 地区）会保留并填浅红底色
`#FFD7D7`，`_match_status` 列标记为 `af_only` / `fb_only`。

## 合并规则

- Campaign 合并：按 `campaign` 列做 outer join，**精确匹配**（去首尾空格，大小写敏感）。
- 地区合并：按 `country` 列做 outer join。
- 派生指标（缺一边则留空）：
  - CPI = 消耗 / 安装
  - CPA = 消耗 / 付费用户
  - CTR = 点击 / 展示

## 列名识别

AF 和 FB 的中英文导出列名都在 [`column_aliases.py`](column_aliases.py) 里维护。
如果导出时报 `Missing required columns`：

1. 打开原始 CSV/XLSX，看第一行的真实列名。
2. 打开 `column_aliases.py`，把真实列名加到对应 `canonical` 的候选列表里。
3. 重新导出即可。

## 文件结构

```
af_fb_merger/
├─ AFFBMerger.vbs       # 双击启动器（隐藏控制台）
├─ gui.py               # tkinter GUI
├─ merger.py            # 数据加载/合并/导出逻辑
├─ column_aliases.py    # AF/FB 列名别名字典（可编辑）
├─ requirements.txt
└─ README.md
```

## 不做什么

- FB 截图 OCR — FB 后台直接能导 CSV，走 CSV 零误差。
- 模糊匹配 — campaign 名不一致时保留并标红，人工处理。
- API 直连 — 需要授权，超出单机工具范围。
