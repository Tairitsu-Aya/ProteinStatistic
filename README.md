# ProteinStatistic

基于三个脚本实现的**蛋白/氨基酸统计 → csv文件合并 → 可视化**：

- `protein.py`：读取**一份氨基酸序列文本**（逐字符统计 20 种标准氨基酸的一字母码），写出 `<input>.csv`（含 `AA1, AA3, Count, Frequency(100)`）。
- `merge.py`：将两份及以上的 `*.csv`（形如上一步输出）按照 `AA1, AA3` **内连接**合并，并把每个文件中除键列外的列名改成**文件名（不含扩展名）**，保存为 `merged_output.csv`。
- `draw.py`：从合并后的 CSV 中选定若干 `AA`，对多个列进行**分组柱状图**绘制；每个柱体顶部自动标注**两位小数**；可调画布大小与 DPI。



---

## 环境

- Python 3.8+（建议 3.10/3.11）
- 依赖：`pandas`、`numpy`、`matplotlib`（见 `requirements.txt` 或手动安装：`pip install pandas numpy matplotlib`）

可选的虚拟环境（Windows PowerShell 示例）：
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt    # 或：pip install pandas numpy matplotlib
```

---

## 一条龙示例（Quickstart）

假设你有若干个氨基酸序列文本（每行/整文件中均为**一字母码**，其它字符会被忽略）（你可以从dna文件翻译生成的蛋白质文件中直接拷贝氨基酸序列到txt中，暂不支持直接读取protein文件）：
```powershell
# 1) 逐个统计并生成 CSV（示例：FUS.txt、EGFP.txt、G3BP1.txt）
python protein.py FUS.txt
python protein.py EGFP.txt
python protein.py G3BP1.txt
# ↑ 会分别得到 FUS.csv、EGFP.csv、G3BP1.csv

# 2) 合并为一个宽表（键：AA1, AA3；列名改为各自文件名）
python merge.py FUS.csv EGFP.csv G3BP1.csv
# ↑ 生成 merged_output.csv

# 3) 选择若干氨基酸并绘图（示例：Tyr Arg Ser ...；列即各样本名）
python draw.py --file merged_output.csv --AA Tyr Arg Ser Asp Gly --out aa_frequency.png --width 11 --height 6 --dpi 200 --constrained
```

---

## `protein.py` — 统计单个序列文件

**用法**：
```powershell
python protein.py <input_file>
# 例如：python protein.py FUS.txt
```

**行为**：
- 读取 `<input_file>` 为文本，统一转为**大写**，逐字符累计 20 种氨基酸一字母码（`A R N D C Q E G H I L K M F P S T W Y V`）。
- 输出一个与输入同名的 CSV（如 `FUS.csv`）包含：
  - 索引列：`AA1`（一字母码）；数据列：`AA3`（三字母码）、`Count`（计数）、`Frequency(100)`（百分比）。
- 控制台同时打印统计表。

**注意**：输入文件若包含非氨基酸字符（如换行、空格、`>` 等）会被忽略；若路径错误会报错并退出。

---

## `merge.py` — 多 CSV 内连接合并

**用法**：
```powershell
python merge.py <file1.csv> <file2.csv> [file3.csv ...]
# 至少两个 CSV
```

**要求与规则**：
- 每个输入 CSV 必须包含键列 `AA1, AA3`（与 `protein.py` 输出兼容）。
- 若存在 `Count` 列，会被**丢弃**（避免与其它文件冲突）。
- 其余列会被重命名为该文件的**文件名（不含扩展名）**；随后按 `AA1, AA3` 做 **inner join**（只保留交集）。
- 结果写出为 `merged_output.csv`，位于当前工作目录。

---

## `draw.py` — 分组柱状图绘制

**用法**：
```powershell
python draw.py --file merged_output.csv --AA <AA 列表> [--out 输出图] [--dpi 160] [--width 10] [--height 6] [--constrained]
```

**参数说明**：
- `--file`：输入 CSV，推荐为 `merged_output.csv`；需包含 `AA3`（优先）或 `AA1` 两列以及**至少一个数值列**。
- `--AA`：要展示的氨基酸列表：
  - 若 CSV 有 `AA3` 列：传三字母码（如 `Tyr Arg Ser`）。
  - 若只有 `AA1` 列：传一字母码（如 `Y R S`）。
  - 程序会按输入顺序筛选，不存在的值会给出警告并忽略。
- `--out`：输出图片文件名（默认 `aa_frequency_bars.png`）。
- `--dpi`：图片 DPI，默认 160。
- `--width/--height`：画布大小（英寸）。
- `--constrained`：开启 `constrained_layout` 自动排版。

**绘图特性**：
- 对每个数值列绘制一组柱；每个柱子顶部**标注两位小数**（默认字号 `6`）。
- 自动适配组内柱宽，避免重叠，并保留间距。
- `AA3` 优先作为横轴标签，不存在时退回 `AA1`。

---

## 典型数据形态

`protein.py` 输出的单表：
```
AA1,AA3,Count,Frequency(100)
A,Ala,123,6.15
R,Arg,98,4.90
...
```

`merge.py` 合并后的宽表（示例三文件合并）：
```
AA1,AA3,FUS,EGFP,G3BP1
A,Ala,6.86,3.36,2.47
R,Arg,6.00,2.52,7.03
...
```

---

## 故障排查

- **`draw.py` 提示无数值列**：请确认 CSV 除 `AA1/AA3` 外还有至少一列数值（如来自合并后的样本列）。
- **`These AAs not found` 警告**：你传入的 `--AA` 与 CSV 的键列不匹配（三字母 vs 一字母），或拼写错误。
- **编码/中文显示**：若图表需显示中文，可在脚本里设置字体，例如：
  ```python
  import matplotlib as mpl
  mpl.rcParams["font.sans-serif"] = ["SimHei","Microsoft YaHei","Arial Unicode MS"]
  mpl.rcParams["axes.unicode_minus"] = False
  ```

---

## 许可证

MIT（如无特别说明）。
