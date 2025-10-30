import pandas as pd
import sys
import os
def merge():
    if len(sys.argv) < 3:
        print("Usage: python merge.py <file1.csv> <file2.csv>")
        sys.exit(1)
    
    files = sys.argv[1:]
    #print(f"[LOADING] {file1} and {file2}")
    try:
        merged_df = None
        for idx,path in enumerate(files):
            df = pd.read_csv(path)
            if 'Count' in df.columns:
                df = df.drop(columns=['Count'])
            name = os.path.splitext(os.path.basename(path))[0]
            key = ['AA1','AA3']
            df = df.rename(columns={c: f"{name}" for c in df.columns if c not in key})
        
            if merged_df is None:
                merged_df = df
            else:
                merged_df = pd.merge(merged_df, df, on=key, how = 'inner')
        
        out_file = 'merged_output.csv'
        merged_df.to_csv(out_file, index=False)
        print(f"[SAVED] {out_file}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
if __name__ == "__main__":
    merge()