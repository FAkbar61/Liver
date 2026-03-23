# Sistem Pakar Penyakit Liver

> Alat skrining awal penyakit hati berbasis **Forward Chaining** — bukan pengganti dokter.

---

## ⚡ Cara Cepat Menjalankan

**Double-click** file di bawah ini:

```
📄 jalankan.bat
```

Browser akan terbuka otomatis ke `http://localhost:5000`

> **Syarat:** Python sudah terinstal dan folder `venv/` sudah ada (lihat [Setup Pertama Kali](#setup-pertama-kali) jika belum)

---

## Halaman Tersedia

| Alamat | Fungsi |
|---|---|
| `http://localhost:5000/` | Form skrining gejala (4 langkah) |
| `http://localhost:5000/result` | Hasil & penjelasan inferensi |
| `http://localhost:5000/admin/rules` | Tabel basis pengetahuan (read-only) |

---

## Fitur

- 25 parameter gejala dalam Bahasa Indonesia
- 36 aturan medis berbasis Forward Chaining
- Deteksi **Red Flag** — peringatan segera ke IGD
- Hasil **Top-3 dugaan kondisi** dengan skor keyakinan
- Jejak penalaran: rule apa yang aktif dan kenapa
- Form wizard 4 langkah yang mudah diisi

---

## Setup Pertama Kali

Lakukan ini **sekali saja** saat pertama kali menggunakan:

```bash
# 1. Buat virtual environment
python -m venv venv

# 2. Install Flask
venv\Scripts\pip install -r requirements.txt
```

Setelah itu, cukup double-click `jalankan.bat` setiap kali ingin membuka aplikasi.

---

## Struktur Folder

```
Liver/
├── jalankan.bat          ← double-click untuk menjalankan
├── app.py                ← server Flask
├── engine.py             ← mesin inferensi Forward Chaining
├── requirements.txt
├── data/
│   ├── symptoms.json     ← 25 gejala
│   └── rules.json        ← 36 aturan
└── templates/
    ├── index.html        ← form skrining
    ├── result.html       ← halaman hasil
    └── admin_rules.html  ← basis pengetahuan
```

---

## Teknologi

- **Backend:** Python 3.8+ · Flask 3.x
- **Frontend:** Bootstrap 5.3 · Vanilla JS
- **Data:** JSON lokal (offline sepenuhnya, tanpa database)
- **Inferensi:** Forward Chaining murni (tidak ada ML/model eksternal)

---

## Contoh Uji

| Skenario | Gejala Dipilih | Hasil yang Diharapkan |
|---|---|---|
| Hepatitis Akut | Jaundice, urin gelap, demam, mual, risiko hepatitis | Top-1: Hepatitis Akut (Keyakinan Tinggi) |
| Sirosis + Red Flag | Perut kembung, bingung, mudah memar, muntah darah | ⚠️ Peringatan IGD + Top-1: Sirosis |
| Fatty Liver | Obesitas/diabetes, kelelahan, nyeri perut kanan atas | Top-1: Fatty Liver/NAFLD (Keyakinan Sedang) |

---

> ⚠️ **Disclaimer Medis:** Aplikasi ini adalah alat edukasi dan skrining awal yang **tidak menggantikan** diagnosis, saran, atau tindakan medis dari dokter atau tenaga kesehatan berlisensi. Selalu konsultasikan kondisi Anda ke profesional medis.
