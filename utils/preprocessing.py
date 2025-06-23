import pandas as pd

def load_excel(filepath):
    df = pd.read_excel(filepath)
    # stripping and lowercaseasing everything
    df.columns = [col.strip().lower().replace(' ', '').replace('(', '').replace(')', '').replace('/', '').replace('^', '') for col in df.columns]
    # Required columns (in lowercase)
    required = ['date', 'timesec', 'accelerationmsec2']
    #checking if column is missing
    for col in required:
        if col not in df.columns:
            raise ValueError(f"❌ Missing required column: {col} ❌")

    return df