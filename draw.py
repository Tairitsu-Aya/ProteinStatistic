import argparse
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def parse_args():
    p = argparse.ArgumentParser(description="Draw grouped bar chart from merged_output.csv")
    p.add_argument("--file", required=True, help="CSV file path (e.g., merged_output.csv)")
    p.add_argument("--AA", nargs="+", required=True, help="AA3 names to include, e.g. Tyr Arg Ser ...")
    p.add_argument("--out", default="aa_frequency_bars.png", help="Output image filename")
    p.add_argument("--dpi", type=int, default=160, help="Output image DPI")
    p.add_argument("--width",  type=float, default=10, help="Figure width in inches")
    p.add_argument("--height", type=float, default=6, help="Figure height in inches")
    p.add_argument("--constrained", action="store_true", help="Use constrained_layout")


    return p.parse_args()

def draw():
    args = parse_args()
    csv_path = args.file
    if not os.path.isfile(csv_path):
        print(f"[ERROR] File not found: {csv_path}")
        sys.exit(1)

    df = pd.read_csv(csv_path)

    key_col = "AA3" if "AA3" in df.columns else ("AA1" if "AA1" in df.columns else None)
    if key_col is None:
        print("[ERROR] CSV must contain column 'AA3' or 'AA1'.")
        sys.exit(1)
    value_cols = [c for c in df.columns if c not in ("AA1", "AA3")]
    if not value_cols:
        print("[ERROR] No value columns found (columns other than AA1/AA3).")
        sys.exit(1)

    wanted = [aa[:1].upper() + aa[1:].lower() for aa in args.AA]
    avail = set(df[key_col].astype(str))
    missing = [aa for aa in wanted if aa not in avail]
    if missing:
        print(f"[WARN] These AAs not found in '{key_col}': {missing}")
    wanted = [aa for aa in wanted if aa in avail]
    if not wanted:
        print("[ERROR] None of the requested AAs are present in the file.")
        sys.exit(1)

    sub = df[df[key_col].astype(str).isin(wanted)].copy()
    sub[key_col] = pd.Categorical(sub[key_col].astype(str), categories=wanted, ordered=True)
    sub = sub.sort_values(key_col)

    x_labels = sub[key_col].tolist()
    N = len(x_labels)
    M = len(value_cols)
    x = np.arange(N)
    width = min(0.8 / M, 0.25)
    offsets = (np.arange(M) - (M - 1) / 2.0) * width

    
    w = args.width  if args.width  is not None else max(8, 1.2 * N)
    h = args.height if args.height is not None else 5
    fig, ax = plt.subplots(figsize=(w, h), constrained_layout=args.constrained)
    ax.margins(y=0.1)


    for j, col in enumerate(value_cols):
        y = sub[col].astype(float).to_numpy()
        bars = ax.bar(x + offsets[j], y, width=width, label=col)
        for rect, val in zip(bars, y):
            ax.annotate(f"{val:.2f}",
                        xy=(rect.get_x() + rect.get_width() / 2.0, rect.get_height()),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom", fontsize=6)

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel(key_col)
    ax.set_ylabel("Frequency")
    ax.set_title("AA Frequency (Grouped by AA)")
    ax.legend(loc="upper right")
    fig.tight_layout()

    fig.savefig(args.out, dpi=args.dpi, bbox_inches="tight")
    print(f"[SAVED] {args.out}")
    try:
        plt.show()
    except Exception:
        pass

if __name__ == "__main__":
    draw()
