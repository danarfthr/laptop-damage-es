# Sistem Pakar Diagnosis Kerusakan Laptop
Tugas Project Mata Kuliah Sistem Pakar — Universitas Gadjah Mada

---

## Penjelasan

Aplikasi berbasis web sederhana yang bisa mendiagnosa kerusakan laptop berdasarkan gejala yang dialami pengguna. Dibuat pakai Python dan Streamlit, pakai metode Forward Chaining dan Certainty Factor.

---

## Cara Menjalankan

Pastikan Python dan `uv` sudah terinstall, lalu jalankan perintah berikut di terminal:

```bash
uv sync
uv run streamlit run app.py
```

Setelah itu buka browser dan akses `http://localhost:8501`.

---

## Struktur File

```
laptop-damage-es/
├── app.py               # tampilan utama (UI)
├── knowledge_base.py    # kumpulan aturan IF-THEN
├── inference.py         # mesin inferensi forward chaining
├── certainty.py         # perhitungan certainty factor
├── explanation.py       # fasilitas penjelasan HOW & WHY
├── pyproject.toml
└── uv.lock
```

---

## Teknologi yang Digunakan

- Python 3.x
- Streamlit

## Anggota Kelompok
- Kenji Ratanaputra (24/534421/PA/22664)
- Danar Fathurahman (24/538200/PA/22828)
- Melinda Annastasia Budijono (24/542840/PA/23052)
- Ayasha Rahmadinni (24/545462/PA/23178)
- Widad Muhammad Rafi (24/545635/PA/23190)
