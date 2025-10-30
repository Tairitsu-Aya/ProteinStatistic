import sys
import pandas as pd
#FILE = None
df = pd.DataFrame({
    'AA1': ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V'],
    'AA3': ['Ala', 'Arg', 'Asn', 'Asp', 'Cys', 'Gln', 'Glu', 'Gly', 'His', 'Ile', 'Leu', 'Lys', 'Met', 'Phe', 'Pro', 'Ser', 'Thr', 'Trp', 'Tyr', 'Val'],
    'Count': [0] * 20
}).set_index('AA1')
def protein():
    if len(sys.argv) != 2:
        print("Usage: python.exe script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        with open(input_file, 'r', encoding = 'utf-8') as f:
            seq = f.read().upper()
            for i in seq:
                if i in df.index:
                    df.at[i, 'Count'] += 1
            sum_aa = df['Count'].sum()
            #df = pd.DataFrame.from_dict(AA, orient='index', columns=['Count'])
            df['Frequency(100)'] = df['Count'] / sum_aa *100
            print(df)
            out = input_file.rsplit('.', 1)[0] + '.csv'
            df.to_csv(out, index_label='AA1')
            print(f"[SAVED] {out}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
if __name__ == "__main__":
    protein()