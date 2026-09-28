# StuntingAI

**StuntingAI** adalah aplikasi web berbasis Streamlit untuk membantu skrining dan pemantauan stunting pada balita. Aplikasi ini menggabungkan model *machine learning* untuk mendeteksi risiko stunting dengan rekomendasi gizi yang dihasilkan oleh LLM (Groq), serta dashboard untuk melihat gambaran kasus di kota-kota di Jawa Tengah.

> **Disclaimer:** Aplikasi ini adalah proyek edukasi/prototipe dan **bukan alat diagnosis medis**. Hasil prediksi hanya berdasarkan data statistik. Selalu konsultasikan kondisi anak dengan dokter, bidan, atau tenaga kesehatan.

---

## Fitur

| Menu | Deskripsi |
|------|-----------|
| **Dashboard** | Ringkasan kasus stunting di Jawa Tengah: total kasus, rata-rata angka stunting, kasus per kota, distribusi tingkat keparahan, dan tren 6 bulan. |
| **Predict Stunting** | Masukkan umur, jenis kelamin, tinggi badan, dan berat badan anak untuk mendapatkan prediksi risiko stunting dari model ML, disertai analisis dan saran gizi dari AI. |
| **City Analysis** | Analisis per kota (Semarang, Solo, Pekalongan): metrik utama, tren bulanan, kasus per kecamatan, dan distribusi kelompok usia. |
| **Monitoring** | Halaman manajemen pasien (daftar pasien dan status risiko). |
| **Settings** | Halaman pengaturan aplikasi. |

## Cara Kerja Prediksi

1. Model dilatih dari `data_balita.csv` menggunakan **Decision Tree Classifier** (scikit-learn).
2. Fitur yang digunakan: **Umur (bulan)** dan **Tinggi Badan (cm)**.
3. Label: status gizi `stunted` dan `severely stunted` dikelompokkan menjadi kelas *stunting* (1), sisanya *normal* (0). Data dibagi 80:20 dengan *stratified split*.
4. Model disimpan ke `model/model.pkl`. Jika file belum ada atau rusak, model akan dilatih ulang otomatis saat halaman **Predict Stunting** dibuka.
5. Setelah prediksi, aplikasi memanggil **Groq API** (model `openai/gpt-oss-120b`) untuk menghasilkan analisis berat-untuk-tinggi badan, 3 rekomendasi menu gizi lokal (konteks Indonesia), dan saran pengasuhan sesuai usia.

## Struktur Proyek

```
stunting-app/
├── app.py                 # Entry point, sidebar & navigasi
├── dashboard.py           # Halaman Dashboard
├── stunting_detection.py  # Halaman prediksi + saran AI
├── city_analysis.py       # Halaman analisis per kota
├── monitoring.py          # Halaman monitoring pasien
├── settings.py            # Halaman pengaturan
├── ai.py                  # Pelatihan model Decision Tree
├── data_balita.csv        # Dataset pelatihan
├── model/                 # Model terlatih (model.pkl)
├── assets/                # Ikon & gambar
├── .streamlit/            # Konfigurasi & secrets Streamlit
├── .devcontainer/         # Konfigurasi dev container
└── requirements.txt
```

## Menjalankan Secara Lokal

### 1. Clone repositori

```bash
git clone https://github.com/gracehdy/stunting-app.git
cd stunting-app
```

### 2. (Opsional) Buat virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependensi

```bash
pip install -r requirements.txt
```

### 4. Atur API key Groq (untuk saran gizi AI)

Buat file `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "isi_api_key_groq_kamu"
```

API key bisa didapatkan di [console.groq.com](https://console.groq.com). Tanpa API key, prediksi tetap berjalan, tetapi bagian analisis AI tidak akan muncul.

> Jangan pernah meng-commit `secrets.toml` ke GitHub.

### 5. (Opsional) Latih ulang model

```bash
python ai.py
```

### 6. Jalankan aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di `http://localhost:8501`.

## Teknologi

- [Streamlit](https://streamlit.io/) & [streamlit-option-menu](https://github.com/victoryhb/streamlit-option-menu) — antarmuka web
- [pandas](https://pandas.pydata.org/) — pengolahan data
- [scikit-learn](https://scikit-learn.org/) — model Decision Tree
- [Altair](https://altair-viz.github.io/) — visualisasi data
- [Groq](https://groq.com/) — LLM untuk rekomendasi gizi

## Catatan Pengembangan

- Data pada **Dashboard**, **City Analysis**, dan **Monitoring** saat ini masih berupa **data contoh (dummy)** dan belum terhubung ke sumber data nyata.
- Model prediksi saat ini hanya memakai umur dan tinggi badan; jenis kelamin dan berat badan dipakai sebagai konteks untuk saran AI.

## 👤 Author

**Grace** — [@gracehdy](https://github.com/gracehdy)
