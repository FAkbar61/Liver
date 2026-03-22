# 🩺 LiverAI — Sistem Pakar Identifikasi Penyakit Liver

Aplikasi web edukasi/skrining awal penyakit liver berbasis **Forward Chaining** (rule-based expert system).

> ⚠️ **Disclaimer:** Aplikasi ini adalah alat edukasi dan skrining awal, **bukan pengganti** diagnosis dokter atau tenaga medis berlisensi.

---

## Fitur Utama

- ✅ Forward Chaining inference engine (35+ aturan, iterasi hingga konvergen)
- ✅ 25 parameter gejala dalam Bahasa Indonesia
- ✅ 5 kategori penyakit: Hepatitis Akut, Hepatitis Kronis, Fatty Liver/NAFLD, Sirosis, Kolestasis
- ✅ **Red Flag** detection → peringatan "SEGERA KE IGD"
- ✅ Top-3 dugaan dengan skor & badge keyakinan (Tinggi/Sedang/Rendah)
- ✅ Trace penalaran (rule mana yang aktif + fakta yang memicu)
- ✅ Wizard form 4 langkah + progress bar
- ✅ Halaman admin Basis Pengetahuan (read-only, searchable)
- ✅ Dark glassmorphism UI

---

## Struktur Folder

```
Liver/
├── app.py              # Flask routes
├── engine.py           # Forward chaining inference engine
├── requirements.txt
├── README.md
├── data/
│   ├── symptoms.json   # 25 gejala
│   └── rules.json      # 36 aturan
├── templates/
│   ├── base.html
│   ├── index.html      # Form wizard
│   ├── result.html     # Halaman hasil
│   └── admin_rules.html
└── static/
    ├── css/style.css
    └── js/main.js
```

---

## Cara Menjalankan Lokal

### 1. Pastikan Python 3.8+ terinstal

```bash
python --version
```

### 2. Buat & aktifkan virtual environment

```bash
# Buat venv
python -m venv venv

# Aktifkan (Windows)
venv\Scripts\activate

# Aktifkan (Linux/macOS)
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan server Flask

```bash
python app.py
```

Atau dengan Flask CLI:
```bash
flask --app app run --debug
```

### 5. Buka di browser

```
http://127.0.0.1:5000/
```

---

## Halaman

| URL | Deskripsi |
|---|---|
| `/` | Form skrining gejala (wizard 4 langkah) |
| `/result` | Hasil inferensi + trace + red flag |
| `/admin/rules` | Basis pengetahuan — tabel rules (read-only) |
| `/api/infer` | API JSON untuk inferensi (POST) |

---

## API Usage

**POST `/api/infer`**

```json
// Request
{
  "facts": {
    "jaundice": true,
    "dark_urine": true,
    "fever": true,
    "hepatitis_risk": true
  }
}

// Response
{
  "top_3": [...],
  "fired_rules": [...],
  "red_flags": [...],
  "recommendations": [...],
  "has_significant": true
}
```

---

## Contoh Skenario Uji

### Skenario 1 — Hepatitis Akut
**Input:** `jaundice=true, dark_urine=true, fever=true, nausea_vomiting=true, hepatitis_risk=true`

**Hasil Diharapkan:**
- Top-1: **Hepatitis Akut** — keyakinan **Tinggi** (≥0.70)
- Rules aktif: R03, R11, R12, R14

---

### Skenario 2 — Sirosis Dekompensata + Red Flag
**Input:** `abdominal_swelling_ascites=true, confusion_drowsy=true, easy_bruising_bleeding=true, vomiting_blood_melena=true, weight_loss=true, fatigue=true`

**Hasil Diharapkan:**
- ⚠️ **SEGERA KE IGD** muncul
- Top-1: **Sirosis** — keyakinan Tinggi
- Rules aktif: R06, R05, R08, R30, R31, R32

---

### Skenario 3 — Fatty Liver / NAFLD
**Input:** `obesity_or_diabetes=true, fatigue=true, loss_of_appetite=true, weight_loss=true, right_upper_quadrant_pain=true`

**Hasil Diharapkan:**
- Top-1: **Fatty Liver / NAFLD** — keyakinan Sedang/Tinggi
- Rules aktif: R07, R08, R18, R19, R20

---

## Teknologi

- **Backend:** Python 3.8+ · Flask 3.x
- **Frontend:** Bootstrap 5.3 · Bootstrap Icons · Vanilla JS
- **Font:** Inter + Plus Jakarta Sans (Google Fonts)
- **Inference:** Forward Chaining rule-based (tidak ada ML/AI eksternal)
- **Data:** JSON (lokal, offline sepenuhnya)
