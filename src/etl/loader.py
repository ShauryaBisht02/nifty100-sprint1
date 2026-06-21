import pandas as pd

def load_excel(file_path):
    try:
        df = pd.read_excel(file_path, header=1)

        print(f"Loaded {file_path}")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        return df

    except Exception as e:
        print("Error:", e)
        return None