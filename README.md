Bien sûr ! Voici une version du README plus sympa avec des emojis pour rendre tout ça plus vivant :

---

# 🚀 HackRF BLE & Wi-Fi Capture & Analysis 📡

Bienvenue dans ce dépôt dédié à la capture et à l’analyse des signaux **Bluetooth Low Energy (BLE)** et **Wi-Fi 2.4 GHz** avec un **HackRF One** !

---

## 🎯 Fonctionnalités

* 📥 Capture IQ brute des canaux BLE advertising (37, 38, 39) à 2 MS/s
* 📊 Analyse spectrogramme pour visualiser l’activité radio
* 🔍 Extraction des adresses MAC des appareils BLE
* 📡 Détection d’activité Wi-Fi 2.4 GHz et démodulation GFSK
* 📈 Visualisation de la puissance et des périodes actives

---

## 🛠️ Prérequis

* HackRF One avec `hackrf_transfer` installé
* Python 3.x
* Bibliothèques Python : `numpy`, `matplotlib`, `scipy`

Installe les dépendances avec :

```bash
pip install numpy matplotlib scipy
```

---

## 📂 Scripts principaux

| Script    | Description                                            |
| --------- | ------------------------------------------------------ |
| `uwu.py`  | Capture BLE + création spectrogrammes                  |
| `mac.py`  | Extraction des adresses MAC BLE depuis fichiers raw    |
| `scan.py` | Analyse puissance & démodulation des signaux BLE/Wi-Fi |

---

## 🚀 Usage rapide

1. Branche ton HackRF One
2. Lance la capture :

   ```bash
   python3 uwu.py
   ```
3. Analyse les fichiers `.raw` générés avec :

   ```bash
   python3 mac.py
   ```

   ou

   ```bash
   python3 scan.py
   ```
4. Visualise les spectrogrammes `.png` dans le dossier

---

## 💡 Conseils

* ⚠️ Pour éviter une charge CPU trop élevée, limite la durée des captures à **10-30 secondes**
* 📶 Canaux BLE 37, 38 et 39 = fréquences 2402, 2426 et 2480 MHz
* 🔎 Utilise `scan.py` pour détecter facilement les périodes d’activité

---

## ⚖️ Avertissement

Ce projet est destiné à un usage **éducatif** et **expérimental**. Respecte toujours les lois locales sur l’écoute et l’interception des signaux radio.

---


