# Sistem Pakar Identifikasi Penyakit Liver — Implementation Plan

Aplikasi web edukasi/skrining awal penyakit liver berbasis **Forward Chaining** rule-based expert system. Backend: **Python Flask**. Frontend: **Bootstrap 5 + Vanilla JS**.

---

## Proposed Changes

### Project Structure
```
d:\OneDrive - uinjkt.ac.id\Liver\
├── app.py                   # Flask routes
├── engine.py                # Forward chaining inference engine
├── README.md
├── requirements.txt
├── data/
│   ├── symptoms.json        # 25 gejala + pertanyaan Bahasa Indonesia
│   └── rules.json           # 35 aturan forward chaining
├── templates/
│   ├── base.html            # Layout + navbar + footer disclaimer
│   ├── index.html           # Wizard form gejala (accordion / step)
│   ├── result.html          # Hasil diagnosis + trace + red flag
│   └── admin_rules.html     # Read-only rules viewer
└── static/
    ├── css/style.css        # Premium dark glassmorphism UI
    └── js/main.js           # Client wizard + form logic
```

---

### Component: Data Layer

#### [NEW] data/symptoms.json
25 gejala dengan field: `id`, `label` (Bahasa Indonesia), `description`, `red_flag` (bool).

#### [NEW] data/rules.json
35 aturan dengan schema:
```json
{
  "id": "R01",
  "if_all": [{"fact": "jaundice", "equals": true}, ...],
  "then": {
    "add_facts": [{"fact": "pattern_cholestatic", "value": true}],
    "add_score": [{"disease": "Kolestasis", "weight": 0.3}],
    "recommendations": ["Periksa bilirubin total"]
  },
  "explain": "Ikterus mengarah ke pola kolestasis",
  "red_flag": false
}
```

---

### Component: Backend (Flask)

#### [NEW] engine.py
Forward chaining inference engine:
- `run_inference(initial_facts: dict) -> dict` — iterasi rules, fire yang terpenuhi, akumulasi skor, tambah ke `facts` sampai tidak ada rule baru yang fire
- Kembalikan: `scores`, `fired_rules` (trace), `red_flags`, `recommendations`

#### [NEW] app.py
- `GET /` — render form gejala
- `POST /result` — terima JSON facts → jalankan inference → render hasil
- `GET /admin/rules` — tampilkan rules.json read-only

#### [NEW] requirements.txt
```
flask>=3.0
```

---

### Component: Frontend

#### [NEW] templates/base.html
Layout Bootstrap 5 + Google Fonts (Inter) + dark theme + footer disclaimer medis.

#### [NEW] templates/index.html
- Wizard accordion multi-step: Gejala Utama → Riwayat → Gejala Tambahan
- Tombol Proses + Reset
- Progress bar dinamis via JS

#### [NEW] templates/result.html
- Top-3 dugaan penyakit + skor bar + badge keyakinan (Tinggi/Sedang/Rendah)
- Alert merah "SEGERA KE IGD" jika red flag
- Accordion "Kenapa hasil ini?" dengan daftar rule yg fired + explain + facts yg memicu
- Tombol Mulai Ulang

#### [NEW] templates/admin_rules.html
- Tabel rules JSON dengan search/filter

#### [NEW] static/css/style.css
Dark glassmorphism, gradient cards, animasi smooth.

#### [NEW] static/js/main.js
- Accordion wizard step logic
- Submit form → kirim JSON ke `/result`

---

### Component: Documentation

#### [NEW] README.md
Instruksi setup lokal: buat venv, pip install, flask run. Contoh 3 skenario uji.

---

## Verification Plan

### Automated Test (via Browser Subagent)
1. Jalankan `flask run` di direktori proyek
2. Buka `http://127.0.0.1:5000` — verifikasi form gejala tampil
3. Isi skenario **Hepatitis Akut** (jaundice + dark_urine + fever + nausea + hepatitis_risk) → proses → cek hasil top-1 adalah Hepatitis Akut
4. Isi skenario **Red Flag / Sirosis Dekompensata** (ascites + confusion + easy_bruising + vomiting_blood) → proses → cek peringatan IGD muncul
5. Isi skenario **Fatty Liver** (obesity_or_diabetes + fatigue + loss_of_appetite, tanpa jaundice) → proses → cek Fatty Liver muncul

### 3 Skenario Validasi Manual
| Skenario | Fakta Input | Hasil Diharapkan |
|---|---|---|
| S1: Hepatitis Akut | jaundice, dark_urine, fever, nausea_vomiting, hepatitis_risk | Top-1: Hepatitis Akut, keyakinan Tinggi |
| S2: Sirosis + Red Flag | ascites, confusion_drowsy, easy_bruising, vomiting_blood_melena | "SEGERA KE IGD" + Top-1: Sirosis |
| S3: Fatty Liver | obesity_or_diabetes, fatigue, loss_of_appetite, weight_loss | Top-1: Fatty Liver/NAFLD, keyakinan Sedang |
