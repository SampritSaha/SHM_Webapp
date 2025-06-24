import pandas as pd
import numpy as np

# Loading EXCEL Checking coloumn and saving with proper coloum name and file name
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




def label_iso2372(df):
    # Velocity in mm/s (your VPP is in inch/sec, so convert)
    df['velocity_mm_s'] = df['vpeaktopeak'] * 25.4  # 1 inch = 25.4 mm

    # Example thresholds (ISO 2372 machine class based):
    # Class I: small motors (<= 0.71 kW)
    # Safe: velocity <= 1.8 mm/s
    df["label"] = (df["velocity_mm_s"] > 1.8).astype(int)

    return df

def label_din4150(df):
    # Convert inch/sec to mm/s
    df['velocity_mm_s'] = df['vpeaktopeak'] * 25.4

    # DIN 4150 suggests damage occurs > 5 mm/s for residential-type buildings
    df["label"] = (df["velocity_mm_s"] > 5.0).astype(int)

    return df

def label_nchrp(df):
    # Already in inch/sec, use threshold directly
    df["label"] = (df["vpeaktopeak"] > 0.1).astype(int)
    return df

def label_fft_analysis(df):
    # Assuming time and acceleration are clean
    time = df["timesec"].values
    accel = df["accelerationmsec2"].values

    # Remove DC offset
    accel = accel - accel.mean()

    # Calculate dt and sampling rate
    if len(time) < 2:
        raise ValueError("❌ Not enough data for FFT")

    dt = time[1] - time[0]
    if dt == 0:
        raise ValueError("❌ Time interval is zero")

    fs = 1 / dt  # sampling rate
    n = len(accel)

    fft_vals = np.fft.fft(accel)
    freqs = np.fft.fftfreq(n, d=dt)
    amplitude = np.abs(fft_vals) / n

    # Only positive frequencies
    positive_freqs = freqs[:n // 2]
    positive_amp = amplitude[:n // 2]

    # Find the dominant frequency (max amplitude)
    dominant_freq = positive_freqs[np.argmax(positive_amp)]

    # Threshold check
    label = 1 if dominant_freq > 50 else 0

    df["label"] = label
    return df

def label_bs7385(df):
    # Convert velocity to mm/s
    df['velocity_mm_s'] = df['vpeaktopeak'] * 25.4

    # BS 7385 Threshold (e.g., 15 mm/s for cosmetic damage)
    df["label"] = (df["velocity_mm_s"] > 15.0).astype(int)

    return df

def label_is2974_rotary_med_high(df):
    # Convert Vpp from inch/sec to mm/s
    df['velocity_mm_s'] = df['vpeaktopeak'] * 25.4

    # Threshold based on ISO/IS recommendations for rotary machines
    df["label"] = (df["velocity_mm_s"] > 3.5).astype(int)

    return df

def label_is2974_rotary_low(df):
    # Convert from inch/sec to mm/s
    df['velocity_mm_s'] = df['vpeaktopeak'] * 25.4

    # Threshold for low frequency rotary machines
    df["label"] = (df["velocity_mm_s"] > 2.3).astype(int)

    return df

def label_is2974_impact(df):
    # Convert from inch/sec to mm/s
    df['velocity_mm_s'] = df['vpeaktopeak'] * 25.4

    # Higher tolerance for impact machines
    df["label"] = (df["velocity_mm_s"] > 5.0).astype(int)

    return df

def label_is1893_general(df):
    # Basic threshold on raw acceleration
    df["label"] = (df["accelerationmsec2"] > 0.05).astype(int)
    return df

def label_is1893_industrial(df):
    df["label"] = (df["accelerationmsec2"] > 0.03).astype(int)
    return df

def label_iso4866(df):
    df["velocity_mm_s"] = df["vpeaktopeak"] * 25.4  # in/s to mm/s
    df["label"] = (df["velocity_mm_s"] > 5).astype(int)
    return df

def label_is2974_reciprocating(df):
    # Convert VPP from inch/sec to mm/s
    df['velocity_mm_s'] = df['vpeaktopeak'] * 25.4

    # Label: 1 if unsafe (velocity > 2.5 mm/s), else 0
    df["label"] = (df["velocity_mm_s"] > 2.5).astype(int)

    return df

#code for different codes
def label_data_by_code(df, code):
    if code == "ISO2372":
        return label_iso2372(df)["label"]
    elif code == "DIN4150":
        return label_din4150(df)["label"]
    elif code == "NCHRP":
        return label_nchrp(df)["label"]
    elif code == "FFT_ANALYSIS":
        return label_fft_analysis(df)["label"]
    elif code == "BS7385":
        return label_bs7385(df)["label"]
    elif code == "IS2974_RECIPROCATING":
        return label_is2974_reciprocating(df)["label"]
    elif code == "IS2974_ROTARY_MED_HIGH":
        return label_is2974_rotary_med_high(df)["label"]
    elif code == "IS2974_ROTARY_LOW":
        return label_is2974_rotary_low(df)["label"]
    elif code == "IS2974_IMPACT":
        return label_is2974_impact(df)["label"]
    elif code == "IS1893_GENERAL":
        return label_is1893_general(df)["label"]
    elif code == "IS1893_INDUSTRIAL":
        return label_is1893_industrial(df)["label"]
    elif code == "ISO4866":
        return label_iso4866(df)["label"]
    else:
        raise ValueError(f"❌ No labeling rule defined for code: {code}")

    