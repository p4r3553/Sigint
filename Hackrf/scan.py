import numpy as np
import matplotlib.pyplot as plt

sample_rate = 2_000_000  # 2 MHz
filename_template = "capture_channel_{}.raw"
ble_channels = {
    37: 2_402_000_000,
    38: 2_426_000_000,
    39: 2_480_000_000
}
capture_duration = 300  # 5 minutes en secondes

def iq_to_complex(iq_bytes):
    iq = np.frombuffer(iq_bytes, dtype=np.uint8).astype(np.int16) - 128
    return iq[::2] + 1j * iq[1::2]

def detect_activity(samples, window_size=1024, threshold=20):
    power = np.abs(samples)**2
    power_db = 10 * np.log10(np.convolve(power, np.ones(window_size)/window_size, mode='valid'))
    active_indices = np.where(power_db > threshold)[0]
    return power_db, active_indices

def gfsk_demap(iq_samples):
    phase = np.angle(iq_samples)
    dphase = np.diff(phase)
    bits = (dphase > 0).astype(np.uint8)
    return bits

def bits_to_str(bits):
    return ''.join(str(b) for b in bits)

def find_access_address(bits, access_address='10001110100010011011111011010110'):
    aa_len = len(access_address)
    found_indices = []
    for i in range(len(bits) - aa_len):
        segment = bits[i:i+aa_len]
        segment_str = bits_to_str(segment)
        if segment_str == access_address:
            found_indices.append(i)
    return found_indices

def main():
    access_address = '10001110100010011011111011010110'

    samples_per_capture = sample_rate * capture_duration * 2  # 2 octets par échantillon IQ (I et Q)

    for ch in ble_channels:
        filename = filename_template.format(ch)
        print(f"Lecture du canal {ch} ({ble_channels[ch]/1e6} MHz) depuis {filename}...")
        with open(filename, "rb") as f:
            raw_data = f.read(samples_per_capture)
        print(f"Taille de la capture chargée : {len(raw_data)} octets")

        samples = iq_to_complex(raw_data)
        
        power_db, active_indices = detect_activity(samples)
        print(f"Canal {ch} - Périodes actives détectées : {len(active_indices)}")

        bits = gfsk_demap(samples)
        print(f"Nombre de bits extraits : {len(bits)}")

        found_positions = find_access_address(bits, access_address)
        print(f"Occurrences Access Address détectées : {len(found_positions)} aux positions : {found_positions[:10]}")

        plt.figure(figsize=(12,4))
        plt.plot(power_db, label='Puissance (dB)')
        plt.scatter(active_indices, power_db[active_indices], color='red', s=5, label='Activité détectée')
        plt.title(f"Détection d'activité sur canal {ch}")
        plt.xlabel("Index fenêtre")
        plt.ylabel("Puissance (dB)")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    main()

