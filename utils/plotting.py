import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
import numpy as np

def plot_acceleration_time(df, filename_prefix):
    time = df["timesec"]
    accel = df["accelerationmsec2"]

    plt.figure(figsize=(10, 4))
    plt.plot(time, accel, color='green', linewidth=1)
    plt.xlabel("Time (sec)")
    plt.ylabel("Acceleration (m/sec²)")
    plt.title("Acceleration vs Time")
    plt.tight_layout()

    plot_name = f"{filename_prefix}_acc_time.png"
    plot_path = os.path.join("static", plot_name)
    plt.savefig(plot_path)
    plt.close()

    return plot_name

def plot_amplitude_frequency(df, filename):
    time = df['timesec'].values
    accel = df['accelerationmsec2'].values

    # ✅ Safety checks
    if len(time) < 2:
        raise ValueError("❌ Not enough data points for FFT.")
    
    dt = np.mean(np.diff(time))
    if dt == 0:
        raise ValueError("❌ Time interval is zero. Cannot compute FFT.")

    # ✅ Remove DC component
    accel = accel - np.mean(accel)

    n = len(accel)
    freq = np.fft.fftfreq(n, d=dt)
    fft_vals = np.fft.fft(accel)
    amplitude = np.abs(fft_vals) / n

    # Take only positive frequencies
    half_n = n // 2
    freq = freq[:half_n]
    amplitude = amplitude[:half_n]

    # Focus on low frequency range to match Excel plot
    mask = freq <= 1  # Or try 0.5 if needed
    freq = freq[mask]
    amplitude = amplitude[mask]

    # Debug print
    print("Checking FFT input data:")
    print("Time column sample:", time[:5])
    print("Acceleration column sample:", accel[:5])

    # Plot
    plt.figure(figsize=(10, 4))
    plt.plot(freq, amplitude, color='red')
    plt.title("Amplitude vs Frequency")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()

    plot_filename = f"{filename}_amp.png"
    save_path = os.path.join('static', plot_filename)
    plt.savefig(save_path)
    plt.close()

    return plot_filename