import os
import matplotlib.pyplot as plt
import numpy as np

def plot_acceleration_time(df, filename):
    time = df['timesec'].values
    accel = df['accelerationmsec2'].values

    plt.figure(figsize=(10, 4))
    plt.plot(time, accel, label='Acceleration', color='green')
    plt.xlabel('Time (sec)')
    plt.ylabel('Acceleration (m/sec²)')
    plt.title('Acceleration vs Time')
    plt.grid(True)
    plt.tight_layout()

    plot_filename = f"{filename}_acc.png"
    save_path = os.path.join('static', plot_filename)
    plt.savefig(save_path)
    plt.close()

    return plot_filename



def plot_amplitude_frequency(df, filename):
    time = df['timesec'].values
    accel = df['accelerationmsec2'].values

    # Step 1: Remove DC component
    accel = accel - np.mean(accel)

    # Step 2: Get total duration from time (Excel-style logic)
    n = len(accel)
    total_duration = time[-1] if time[-1] != 0 else 1  # avoid divide by zero

    # Step 3: Compute FFT and amplitude
    fft_vals = np.fft.fft(accel)
    amplitude = np.abs(fft_vals) / n

    # Step 4: Frequency axis as per Excel method
    freq = np.arange(n) / total_duration

    # Step 5: Keep only first half (positive frequencies)
    half_n = n // 2
    freq = freq[:half_n]
    amplitude = amplitude[:half_n]

    # Step 6: Plot
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



def plot_velocity_peak_to_peak(df, filename):
    time = df['timesec'].values
    accel = df['accelerationmsec2'].values

    # Compute vpp using the formula from Excel
    vpp = accel * time * 0.0393701

    # Plot vpp vs time
    plt.figure(figsize=(10, 4))
    plt.plot(time, vpp, color='blue')
    plt.title("Velocity Peak to Peak vs Time")
    plt.xlabel("Time (sec)")
    plt.ylabel("Velocity Peak to Peak (inches/sec)")
    plt.grid(True)
    plt.tight_layout()

    plot_filename = f"{filename}_vpp.png"
    save_path = os.path.join('static', plot_filename)
    plt.savefig(save_path)
    plt.close()

    return plot_filename