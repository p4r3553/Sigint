import numpy as np

# Paramètres
filename_template = "capture_channel_{}.raw"
ble_channels = {
    37: 2_402_000_000,
    38: 2_426_000_000,
    39: 2_480_000_000
}
sample_rate = 2_000_000

# Access Address BLE (32 bits) = 0x8E89BED6 en binaire (LSB first)
ACCESS_ADDRESS_BIN = '01101011111101100010001110001110'  # 0x8E89BED6 en LSB first

def iq_to_complex(iq_bytes):
    iq = np.frombuffer(iq_bytes, dtype=np.uint8).astype(np.int16) - 128
    return iq[::2] + 1j * iq[1::2]

def samples_to_bits(samples, threshold=0):
    """
    Démodule les échantillons IQ en bits en utilisant la phase.
    Simplification : on regarde le signe de la partie réelle.
    """
    # On prend seulement la partie réelle
    real = samples.real
    bits = (real > threshold).astype(np.uint8)
    return bits

def find_access_address_sliding(bits, access_address=ACCESS_ADDRESS_BIN, max_shift=8):
    aa_len = len(access_address)
    found_positions = []
    for shift in range(max_shift):
        for i in range(len(bits) - aa_len - shift):
            segment = bits[i+shift:i+shift+aa_len]
            segment_str = ''.join(str(b) for b in segment)
            if segment_str == access_address:
                found_positions.append(i+shift)
    return found_positions

def decode_ble_advertising_packet(bits, start_idx):
    """
    Décodage simple du paquet BLE à partir du début de l'Access Address.
    On suppose que le paquet est au format BLE publicitaire.

    bits : tableau numpy ou liste de bits (0/1)
    start_idx : position de l'Access Address détectée

    Retourne la MAC si trouvée, sinon None.
    """

    # Vérifier qu'il y a assez de bits pour header + length + MAC (au moins 10 octets = 80 bits)
    if start_idx + 32 + 16 + 8 + 48 > len(bits):
        return None

    # Header (16 bits) après l'Access Address
    header_bits = bits[start_idx+32 : start_idx+48]
    # Le PDU type est sur 4 bits, bit order inversé (LSB first)
    pdu_type_bits = header_bits[:4]
    pdu_type_str = ''.join(str(b) for b in pdu_type_bits[::-1])
    pdu_type = int(pdu_type_str, 2)

    # Longueur (8 bits) après le header
    length_bits = bits[start_idx+48 : start_idx+56]
    length_str = ''.join(str(b) for b in length_bits[::-1])
    length = int(length_str, 2)

    # Payload commence après Access Address + header + length (32 + 16 + 8 bits)
    payload_start = start_idx + 56
    payload_end = payload_start + length * 8
    if payload_end > len(bits):
        return None  # Paquet incomplet

    # On extrait la payload bits
    payload_bits = bits[payload_start : payload_end]

    # Dans la publicité ADV_IND (pdu_type=0), les 6 premiers octets du payload sont l'adresse MAC (48 bits)
    if pdu_type == 0:  
        mac_bits = payload_bits[:48]
        # On convertit en octets (LSB first par octet)
        mac_bytes = []
        for i in range(6):
            byte_bits = mac_bits[i*8:(i+1)*8]
            byte_str = ''.join(str(b) for b in byte_bits[::-1])
            mac_bytes.append(int(byte_str, 2))
        # La MAC s'affiche en MSB first, donc on inverse l'ordre des octets
        mac_str = ':'.join(f"{b:02X}" for b in mac_bytes[::-1])
        return mac_str
    else:
        return None

def main():
    all_macs = set()

    for ch in ble_channels:
        filename = filename_template.format(ch)
        print(f"Lecture du canal {ch} ({ble_channels[ch]/1e6} MHz) depuis {filename}...")
        with open(filename, "rb") as f:
            raw_data = f.read()
        samples = iq_to_complex(raw_data)
        bits = samples_to_bits(samples)

        print(f"Recherche de l'Access Address sur le canal {ch}...")
        positions = find_access_address_sliding(bits)
        print(f"Positions Access Address trouvées : {len(positions)}")

        for pos in positions:
            mac = decode_ble_advertising_packet(bits, pos)
            if mac is not None:
                all_macs.add(mac)

    print("\n=== Liste des adresses MAC détectées ===")
    for mac in sorted(all_macs):
        print(mac)

if __name__ == "__main__":
    main()

