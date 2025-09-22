# 🔥 Dashboard Monitoring Titik Panas

Dashboard Streamlit untuk monitoring prakiraan titik panas dan analisis variabel cuaca terkait.

## 📋 Fitur Dashboard

### 1. **Metrics Utama**
- Total titik panas terdeteksi
- Rata-rata curah hujan
- Rata-rata sinaran matahari  
- Jumlah area berisiko tinggi

### 2. **Tab Analisis**

#### 📈 Trend Analisis
- Grafik trend titik panas vs curah hujan
- Prakiraan 7 hari ke depan
- Analisis time series

#### 🗺️ Peta Risiko
- Heatmap tingkat risiko per lokasi
- Distribusi tingkat risiko
- Visualisasi geografis

#### 🌤️ Variabel Cuaca
- Hubungan suhu vs kelembaban
- Distribusi arah angin (wind rose)
- Box plot variabel per tingkat risiko
- Time series variabel cuaca

#### 📊 Korelasi
- Matriks korelasi antar variabel
- Scatter plot matrix
- Analisis hubungan statistik

### 3. **Filter Interaktif**
- Filter berdasarkan lokasi
- Filter rentang tanggal
- Real-time update visualisasi

## 🚀 Cara Menjalankan

### Persiapan Environment
```bash
# Install dependencies
pip install -r requirements.txt
```

### Menjalankan Dashboard

#### Opsi 1: Langsung dengan Streamlit
```bash
streamlit run dashboard_titik_panas.py
```

#### Opsi 2: Menggunakan Script Runner
```bash
python run_dashboard.py
```

Dashboard akan terbuka di browser pada `http://localhost:8501`

## 📊 Data Mock-up

Dashboard menggunakan data simulasi yang mencakup:

### Variabel Utama:
- **Titik Panas**: Jumlah hotspot terdeteksi
- **Curah Hujan**: Data hujan dalam mm
- **Sinaran Matahari**: Radiasi solar dalam W/m²
- **Angin**: Kecepatan (m/s) dan arah (derajat)
- **Suhu**: Temperatur udara (°C)
- **Kelembaban**: Persentase kelembaban relatif

### Lokasi Monitor:
- Kalimantan Tengah
- Riau
- Sumatra Selatan
- Papua
- Jambi

### Tingkat Risiko:
- 🟢 **Rendah**: Skor risiko < 40
- 🟡 **Sedang**: Skor risiko 40-60
- 🟠 **Tinggi**: Skor risiko 60-80
- 🔴 **Sangat Tinggi**: Skor risiko > 80

## 🔧 Kustomisasi

### Menambah Lokasi Baru
Edit fungsi `generate_mock_data()` pada bagian:
```python
locations = ['Lokasi_Baru', 'Kalimantan Tengah', ...]
```

### Mengubah Parameter Simulasi
Sesuaikan formula di dalam fungsi `generate_mock_data()`:
- Seasonal factor untuk variasi musiman
- Random noise untuk variabilitas data
- Scoring formula untuk tingkat risiko

### Menambah Visualisasi
Tambahkan tab baru atau chart tambahan dengan:
```python
with st.tabs([...]):
    # Visualisasi baru
    fig = px.chart_type(...)
    st.plotly_chart(fig)
```

## 📱 Responsivitas

Dashboard didesain responsive dengan:
- Layout kolom yang adaptif
- Grafik yang menyesuaikan ukuran container
- Sidebar yang dapat di-collapse
- Mobile-friendly interface

## ⚠️ Catatan Penting

- **Data Mock-up**: Dashboard ini menggunakan data simulasi
- **Demo Purpose**: Hanya untuk keperluan demonstrasi
- **Performance**: Optimal untuk data dengan rentang 1-3 bulan
- **Browser**: Disarankan menggunakan Chrome/Firefox terbaru

## 🔮 Pengembangan Selanjutnya

Untuk implementasi dengan data real:
1. Ganti fungsi `generate_mock_data()` dengan koneksi database
2. Tambahkan autentikasi user
3. Implementasikan real-time data streaming
4. Tambahkan alert system
5. Integrasi dengan API cuaca eksternal

## 📞 Support

Untuk pertanyaan teknis atau bug report, silakan buat issue di repository ini.

---
**📊 Dashboard Monitoring Titik Panas - Tugas Akhir Informatika**  
*Developed with ❤️ using Streamlit*