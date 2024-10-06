
# Dashboard Analisis Data dengan Streamlit

Repositori ini berisi sebuah proyek tugas akhir dari materi Belajar Analisis Data dengan Python - Dicoding. Proyek ini merupakan dashboard yang di-deploy dalam streamlit yang dapat dijalankan secara local.

## Daftar Isi
- [Deskripsi](#deskripsi)
- [Fitur](#fitur)
- [Instalasi](#instalasi)
  - [1. Membuat Virtual Environment](#1-membuat-virtual-environment)
  - [2. Menginstal Library yang Dibutuhkan](#2-menginstal-library-yang-dibutuhkan)
  - [3. Menjalankan Aplikasi](#3-menjalankan-aplikasi)

## Deskripsi
Proyek ini menyediakan dashboard interaktif untuk analisis data menggunakan `Streamlit` yang mana analisis data dilakukan terhadap Bike Sharing Dataset yang bersumber dari website Kaggle.

## Fitur
- Visualisasikan data dengan berbagai jenis grafik (garis, batang, sebar, dll.).
- Analisis korelasi antara variabel.
- Sesuaikan analisis menggunakan kontrol interaktif.
- Di-deploy di Streamlit Cloud untuk akses yang mudah serta dapat diakses melalui tautan dalam file url.txt.

## Instalasi

Untuk menjalankan proyek ini secara lokal, ikuti langkah-langkah di bawah ini:

### 1. Membuat Virtual Environment

Pastikan Anda sudah memiliki Python 3.7+ terinstal. Buatlah virtual environment untuk proyek ini agar dependensi terisolasi:

```bash
# Di macOS/Linux
python3 -m venv env

# Di Windows
python -m venv env
```

Aktifkan virtual environment:

```bash
# Di macOS/Linux
source env/bin/activate

# Di Windows
env\Scripts\activate
```

### 2. Menginstal Library yang Dibutuhkan

Setelah virtual environment aktif, instal library yang dibutuhkan dengan menggunakan file `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Menjalankan Aplikasi

Untuk menjalankan dashboard, navigasikan ke folder tempat `dashboard.py` berada dan gunakan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

Perintah ini akan menjalankan server lokal Streamlit. Buka URL yang diberikan di browser Anda untuk mengakses dashboard.