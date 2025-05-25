import numpy as np
import subprocess
import matplotlib.pyplot as plt

# Paramètres
sample_rate = 2_000_000    # 2 MS/s
gain = 40                  # gain d'entrée
capture_duration = 60     # durée en secondes par canal (5 minutes)
filename_template = "capture_channel_{}.raw"

ble_channels = {
    37: 2_402_000_000,
    38: 2_426_000_000,
    39: 2_480_000_000
}

def iq_to_complex(iq_bytes):
    iq = np.frombuffer(iq_bytes, dtype=np.uint8).astype(np.int16) - 128
    return iq[::2] + 1j * iq[1::2]

def capture_with_hackrf_transfer(freq, filename):
    cmd = [
        "hackrf_transfer",
        "-r", filename,
        "-f", str(freq),
        "-s", str(sample_rate),
        "-a", "1",
        "-x", str(gain),
        "-n", str(sample_rate * capture_duration)
    ]
    print(f"Capture sur canal {freq/1e6:.1f} MHz pendant {capture_duration} secondes...")
    proc = subprocess.Popen(cmd)
    proc.wait()
    print(f"Capture sur {filename} terminée.")

def analyze_capture(filename, freq):
    with open(filename, "rb") as f:
        raw_data = f.read()
    samples = iq_to_complex(raw_data)
    print(f"{filename} : {len(samples)} échantillons capturés")

    plt.figure(figsize=(10, 4))
    plt.specgram(samples, NFFT=1024, Fs=sample_rate, noverlap=512, cmap='inferno')
    plt.title(f"Spectrogramme - Canal {freq/1e6:.1f} MHz ({filename})")
    plt.xlabel("Temps [fenêtres]")
    plt.ylabel("Fréquence relative (Hz)")
    plt.ylim(-5e6, 5e6)  # Zoom ±5 MHz autour de la fréquence centrale
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()

    # Sauvegarde optionnelle
    png_filename = filename.replace('.raw', '.png')
    plt.savefig(png_filename)
    print(f"Spectrogramme sauvegardé sous {png_filename}")

def main():
    for ch, freq in ble_channels.items():
        filename = filename_template.format(ch)
        capture_with_hackrf_transfer(freq, filename)
        analyze_capture(filename, freq)

if __name__ == "__main__":
    main()

