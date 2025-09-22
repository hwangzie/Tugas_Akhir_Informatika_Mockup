import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Monitoring Titik Panas Pontianak",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk generate data mock khusus Pontianak
@st.cache_data
def generate_pontianak_data(days=30):
    """Generate data mock untuk monitoring Pontianak"""
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=days),
        end=datetime.now() + timedelta(days=7),
        freq='D'
    )
    
    # Wilayah/Kecamatan di Kota Pontianak
    pontianak_areas = [
        'Pontianak Kota',
        'Pontianak Selatan', 
        'Pontianak Utara',
        'Pontianak Timur',
        'Pontianak Barat',
        'Pontianak Tenggara'
    ]
    
    # Koordinat approximate untuk setiap area
    area_coords = {
        'Pontianak Kota': {'lat': -0.0263, 'lon': 109.3425},
        'Pontianak Selatan': {'lat': -0.0500, 'lon': 109.3200},
        'Pontianak Utara': {'lat': 0.0100, 'lon': 109.3300},
        'Pontianak Timur': {'lat': -0.0200, 'lon': 109.3600},
        'Pontianak Barat': {'lat': -0.0300, 'lon': 109.3000},
        'Pontianak Tenggara': {'lat': -0.0600, 'lon': 109.3500}
    }
    
    data = []
    for date in dates:
        for area in pontianak_areas:
            # Faktor musim (Pontianak di khatulistiwa - pola hujan)
            # Musim hujan: Nov-Mar, Musim kemarau: Apr-Okt
            month = date.month
            is_dry_season = month in [4, 5, 6, 7, 8, 9, 10]
            
            # Faktor El Nino/La Nina (simulasi)
            climate_oscillation = np.sin(2 * np.pi * date.dayofyear / 1095)  # 3-year cycle
            
            # Titik panas - lebih tinggi di musim kemarau
            if is_dry_season:
                hotspot_base = 25 + climate_oscillation * 15
                # Area urban lebih rendah, area pinggiran lebih tinggi
                if area in ['Pontianak Kota']:
                    hotspot_base *= 0.6
                elif area in ['Pontianak Utara', 'Pontianak Timur']:
                    hotspot_base *= 1.3
            else:
                hotspot_base = 8 + climate_oscillation * 5
                
            hotspot_count = max(0, int(hotspot_base + np.random.normal(0, 8)))
            
            # Curah hujan - karakteristik iklim tropis basah Pontianak
            if is_dry_season:
                rainfall_base = 120 - climate_oscillation * 60
            else:
                rainfall_base = 280 + climate_oscillation * 80
            
            rainfall = max(0, rainfall_base + np.random.normal(0, 40))
            
            # Sinaran matahari - relatif konstan di khatulistiwa
            solar_base = 450 if is_dry_season else 350
            solar_radiation = solar_base + np.random.normal(0, 50)
            
            # Angin - pola angin khatulistiwa
            # Angin timur-tenggara di musim kemarau, barat daya di musim hujan
            if is_dry_season:
                wind_direction_base = 120  # SE
                wind_speed_base = 3.5
            else:
                wind_direction_base = 240  # SW
                wind_speed_base = 2.8
                
            wind_speed = max(0, wind_speed_base + np.random.normal(0, 1.2))
            wind_direction = (wind_direction_base + np.random.normal(0, 30)) % 360
            
            # Suhu - relatif stabil sepanjang tahun (iklim khatulistiwa)
            temp_base = 27.5 if is_dry_season else 26.8
            temperature = temp_base + np.random.normal(0, 1.5)
            
            # Kelembaban - tinggi sepanjang tahun
            humidity_base = 75 if is_dry_season else 85
            humidity = max(40, min(95, humidity_base + np.random.normal(0, 8)))
            
            # FFMC (Fine Fuel Moisture Code) - indikator kelembaban bahan bakar
            ffmc = max(20, min(95, 60 + (hotspot_count * 0.8) - (rainfall * 0.1)))
            
            # Risk level berdasarkan kondisi spesifik Pontianak
            risk_score = (
                hotspot_count * 0.35 + 
                max(0, (100 - rainfall/3)) * 0.25 +
                max(0, (temperature - 26)) * 0.15 +
                max(0, (ffmc - 40)) * 0.15 +
                max(0, (wind_speed - 2)) * 0.10
            )
            
            if risk_score > 70:
                risk_level = "Sangat Tinggi"
            elif risk_score > 50:
                risk_level = "Tinggi"
            elif risk_score > 30:
                risk_level = "Sedang"
            else:
                risk_level = "Rendah"
            
            # ISPU (Indeks Standar Pencemaran Udara) - simulasi
            # Lebih tinggi saat banyak titik panas
            ispu_base = 45 + (hotspot_count * 1.2)
            ispu = max(0, int(ispu_base + np.random.normal(0, 10)))
            
            data.append({
                'tanggal': date,
                'area': area,
                'latitude': area_coords[area]['lat'],
                'longitude': area_coords[area]['lon'],
                'titik_panas': hotspot_count,
                'curah_hujan': rainfall,
                'sinaran_matahari': solar_radiation,
                'kecepatan_angin': wind_speed,
                'arah_angin': wind_direction,
                'suhu': temperature,
                'kelembaban': humidity,
                'ffmc': ffmc,
                'ispu': ispu,
                'tingkat_risiko': risk_level,
                'skor_risiko': risk_score,
                'musim': 'Kemarau' if is_dry_season else 'Hujan'
            })
    
    return pd.DataFrame(data)

# Generate data
df = generate_pontianak_data()

# Sidebar
st.sidebar.title("🔥 Dashboard Pontianak")
st.sidebar.markdown("**Monitoring Titik Panas Kota Pontianak**")
st.sidebar.markdown("*Kalimantan Barat*")
st.sidebar.markdown("---")

# Filter area
selected_areas = st.sidebar.multiselect(
    "Pilih Area/Kecamatan:",
    options=df['area'].unique(),
    default=df['area'].unique()
)

# Filter tanggal
date_range = st.sidebar.date_input(
    "Rentang Tanggal:",
    value=[df['tanggal'].min().date(), df['tanggal'].max().date()],
    min_value=df['tanggal'].min().date(),
    max_value=df['tanggal'].max().date()
)

# Filter musim
season_filter = st.sidebar.selectbox(
    "Filter Musim:",
    options=['Semua', 'Kemarau', 'Hujan']
)

# Filter data berdasarkan sidebar
filtered_df = df[df['area'].isin(selected_areas)]

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['tanggal'].dt.date >= date_range[0]) &
        (filtered_df['tanggal'].dt.date <= date_range[1])
    ]

if season_filter != 'Semua':
    filtered_df = filtered_df[filtered_df['musim'] == season_filter]

# Header
st.title("🔥 Dashboard Monitoring Titik Panas Pontianak")
st.markdown("**Sistem Monitoring dan Prakiraan Titik Panas Kota Pontianak, Kalimantan Barat**")
st.markdown("📍 *Lokasi: 0°0'N 109°20'E - Khatulistiwa*")
st.markdown("---")

# Info geografis Pontianak
with st.expander("ℹ️ Informasi Geografis Pontianak"):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Karakteristik Iklim:**")
        st.write("• Iklim tropis basah (Af)")
        st.write("• Suhu: 24-34°C sepanjang tahun")
        st.write("• Kelembaban: 70-90%")
        st.write("• Curah hujan: 3000-4000mm/tahun")
    with col2:
        st.write("**Musim:**")
        st.write("• **Kemarau**: April - Oktober")
        st.write("• **Hujan**: November - Maret")
        st.write("• **Risiko tinggi**: Juli - September")
        st.write("• **Angin dominan**: Tenggara & Barat Daya")

# Metrics utama
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_hotspots = filtered_df['titik_panas'].sum()
    yesterday_hotspots = df[df['tanggal'] == df['tanggal'].max() - timedelta(days=1)]['titik_panas'].sum()
    delta_hotspots = total_hotspots - yesterday_hotspots
    st.metric(
        label="Total Titik Panas",
        value=f"{total_hotspots:,.0f}",
        delta=f"{delta_hotspots:+.0f}"
    )

with col2:
    avg_rainfall = filtered_df['curah_hujan'].mean()
    st.metric(
        label="Rata-rata Curah Hujan",
        value=f"{avg_rainfall:.1f} mm",
        delta=f"{np.random.uniform(-5, 5):.1f}"
    )

with col3:
    avg_temp = filtered_df['suhu'].mean()
    st.metric(
        label="Suhu Rata-rata",
        value=f"{avg_temp:.1f}°C",
        delta=f"{np.random.uniform(-1, 1):.1f}"
    )

with col4:
    avg_ispu = filtered_df['ispu'].mean()
    ispu_status = "Baik" if avg_ispu < 50 else "Sedang" if avg_ispu < 100 else "Tidak Sehat"
    st.metric(
        label="ISPU Rata-rata",
        value=f"{avg_ispu:.0f}",
        delta=ispu_status
    )

with col5:
    high_risk_count = len(filtered_df[filtered_df['tingkat_risiko'].isin(['Tinggi', 'Sangat Tinggi'])])
    st.metric(
        label="Area Berisiko Tinggi",
        value=high_risk_count,
        delta=f"{np.random.randint(-2, 3):+d}"
    )

st.markdown("---")

# Tab untuk berbagai visualisasi
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Trend & Prakiraan", 
    "🗺️ Peta Pontianak", 
    "🌤️ Cuaca & Iklim", 
    "📊 Analisis Risiko",
    "🔬 FFMC & ISPU"
])

with tab1:
    st.subheader("Trend Titik Panas dan Cuaca Pontianak")
    
    # Aggregate data harian
    daily_data = filtered_df.groupby('tanggal').agg({
        'titik_panas': 'sum',
        'curah_hujan': 'mean',
        'suhu': 'mean',
        'kelembaban': 'mean',
        'skor_risiko': 'mean'
    }).reset_index()
    
    # Grafik trend utama
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_data['tanggal'],
        y=daily_data['titik_panas'],
        mode='lines+markers',
        name='Titik Panas',
        line=dict(color='red', width=3),
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_data['tanggal'],
        y=daily_data['curah_hujan'],
        mode='lines+markers',
        name='Curah Hujan (mm)',
        line=dict(color='blue', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Trend Titik Panas vs Curah Hujan di Pontianak",
        xaxis_title="Tanggal",
        yaxis=dict(title="Jumlah Titik Panas", side="left", color="red"),
        yaxis2=dict(title="Curah Hujan (mm)", side="right", overlaying="y", color="blue"),
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Analisis musiman
    col1, col2 = st.columns(2)
    
    with col1:
        seasonal_data = filtered_df.groupby('musim').agg({
            'titik_panas': 'mean',
            'curah_hujan': 'mean',
            'suhu': 'mean'
        }).reset_index()
        
        fig_season = px.bar(
            seasonal_data,
            x='musim',
            y='titik_panas',
            title="Rata-rata Titik Panas per Musim",
            color='musim',
            color_discrete_map={'Kemarau': 'orange', 'Hujan': 'lightblue'}
        )
        st.plotly_chart(fig_season, use_container_width=True)
    
    with col2:
        # Prediksi sederhana 7 hari
        st.subheader("Prakiraan 7 Hari")
        
        # Simulasi prediksi berdasarkan pola musiman
        recent_trend = daily_data.tail(14)
        current_month = datetime.now().month
        is_dry_prediction = current_month in [4, 5, 6, 7, 8, 9, 10]
        
        if is_dry_prediction:
            pred_hotspot_trend = "📈 Meningkat (Musim Kemarau)"
            pred_rainfall_trend = "📉 Menurun"
        else:
            pred_hotspot_trend = "📉 Menurun (Musim Hujan)"
            pred_rainfall_trend = "📈 Meningkat"
        
        st.info(f"**Prediksi Titik Panas:** {pred_hotspot_trend}")
        st.info(f"**Prediksi Curah Hujan:** {pred_rainfall_trend}")
        
        avg_recent_hotspot = recent_trend['titik_panas'].mean()
        avg_recent_rain = recent_trend['curah_hujan'].mean()
        
        st.metric("Titik Panas 7 Hari Terakhir", f"{avg_recent_hotspot:.1f}")
        st.metric("Curah Hujan 7 Hari Terakhir", f"{avg_recent_rain:.1f} mm")

with tab2:
    st.subheader("Peta Distribusi Risiko Area Pontianak")
    
    # Heatmap per area
    area_summary = filtered_df.groupby(['area', 'tingkat_risiko']).size().unstack(fill_value=0)
    
    if not area_summary.empty:
        fig_heatmap = px.imshow(
            area_summary.T,
            title="Distribusi Tingkat Risiko per Area di Pontianak",
            color_continuous_scale="Reds",
            aspect="auto"
        )
        fig_heatmap.update_layout(
            xaxis_title="Area/Kecamatan",
            yaxis_title="Tingkat Risiko"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Scatter map dengan koordinat
    latest_data = filtered_df[filtered_df['tanggal'] == filtered_df['tanggal'].max()]
    
    fig_map = px.scatter_mapbox(
        latest_data,
        lat='latitude',
        lon='longitude',
        size='titik_panas',
        color='tingkat_risiko',
        hover_name='area',
        hover_data=['titik_panas', 'curah_hujan', 'suhu'],
        color_discrete_map={
            'Rendah': 'green',
            'Sedang': 'yellow', 
            'Tinggi': 'orange',
            'Sangat Tinggi': 'red'
        },
        title="Peta Sebaran Titik Panas Pontianak (Data Terkini)",
        mapbox_style="open-street-map",
        zoom=11,
        center={"lat": -0.026, "lon": 109.34}
    )
    
    fig_map.update_layout(height=600)
    st.plotly_chart(fig_map, use_container_width=True)

with tab3:
    st.subheader("Analisis Cuaca dan Iklim Pontianak")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Wind rose Pontianak
        fig_wind = px.histogram(
            filtered_df,
            x='arah_angin',
            nbins=16,
            title="Mawar Angin Pontianak",
            labels={'arah_angin': 'Arah Angin (°)', 'count': 'Frekuensi'}
        )
        fig_wind.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
                ticktext=['U', 'TL', 'T', 'TG', 'S', 'BD', 'B', 'BL']
            )
        )
        st.plotly_chart(fig_wind, use_container_width=True)
        
        # Temperature vs Humidity
        fig_temp_hum = px.scatter(
            filtered_df,
            x='suhu',
            y='kelembaban',
            color='musim',
            size='titik_panas',
            title="Hubungan Suhu vs Kelembaban",
            color_discrete_map={'Kemarau': 'orange', 'Hujan': 'lightblue'}
        )
        st.plotly_chart(fig_temp_hum, use_container_width=True)
    
    with col2:
        # Variabel cuaca time series
        variables = ['curah_hujan', 'sinaran_matahari', 'kecepatan_angin', 'kelembaban']
        selected_var = st.selectbox("Pilih Variabel Cuaca:", variables)
        
        daily_var = filtered_df.groupby('tanggal')[selected_var].mean().reset_index()
        fig_var = px.line(
            daily_var,
            x='tanggal',
            y=selected_var,
            title=f"Trend {selected_var.replace('_', ' ').title()} di Pontianak"
        )
        st.plotly_chart(fig_var, use_container_width=True)
        
        # Box plot per musim
        fig_box = px.box(
            filtered_df,
            x='musim',
            y=selected_var,
            title=f"Distribusi {selected_var.replace('_', ' ').title()} per Musim",
            color='musim',
            color_discrete_map={'Kemarau': 'orange', 'Hujan': 'lightblue'}
        )
        st.plotly_chart(fig_box, use_container_width=True)

with tab4:
    st.subheader("Analisis Tingkat Risiko Kebakaran")
    
    # Distribusi risiko
    risk_counts = filtered_df['tingkat_risiko'].value_counts()
    colors = {
        'Rendah': 'green',
        'Sedang': 'yellow',
        'Tinggi': 'orange', 
        'Sangat Tinggi': 'red'
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_risk_pie = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Distribusi Tingkat Risiko (%)",
            color=risk_counts.index,
            color_discrete_map=colors
        )
        st.plotly_chart(fig_risk_pie, use_container_width=True)
    
    with col2:
        # Risk score time series
        daily_risk = filtered_df.groupby('tanggal')['skor_risiko'].mean().reset_index()
        fig_risk_trend = px.line(
            daily_risk,
            x='tanggal',
            y='skor_risiko',
            title="Trend Skor Risiko Harian",
            color_discrete_sequence=['red']
        )
        fig_risk_trend.add_hline(y=70, line_dash="dash", line_color="red", 
                                annotation_text="Batas Sangat Tinggi")
        fig_risk_trend.add_hline(y=50, line_dash="dash", line_color="orange",
                                annotation_text="Batas Tinggi")
        st.plotly_chart(fig_risk_trend, use_container_width=True)
    
    # Correlation dengan faktor cuaca
    st.subheader("Korelasi Faktor Risiko")
    risk_factors = ['titik_panas', 'curah_hujan', 'suhu', 'kelembaban', 'kecepatan_angin', 'skor_risiko']
    corr_matrix = filtered_df[risk_factors].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        title="Matriks Korelasi Faktor Risiko",
        color_continuous_scale="RdBu",
        zmin=-1, zmax=1
    )
    st.plotly_chart(fig_corr, use_container_width=True)

with tab5:
    st.subheader("Fine Fuel Moisture Code (FFMC) & Indeks Kualitas Udara")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # FFMC analysis
        st.write("**FFMC (Fine Fuel Moisture Code)**")
        st.write("Indikator kelembaban bahan bakar halus (daun, rumput kering)")
        
        avg_ffmc = filtered_df['ffmc'].mean()
        if avg_ffmc > 85:
            ffmc_status = "🔴 Sangat Kering"
        elif avg_ffmc > 70:
            ffmc_status = "🟠 Kering"
        elif avg_ffmc > 50:
            ffmc_status = "🟡 Sedang"
        else:
            ffmc_status = "🟢 Lembab"
            
        st.metric("FFMC Rata-rata", f"{avg_ffmc:.1f}", ffmc_status)
        
        # FFMC trend
        daily_ffmc = filtered_df.groupby('tanggal')['ffmc'].mean().reset_index()
        fig_ffmc = px.line(
            daily_ffmc,
            x='tanggal',
            y='ffmc',
            title="Trend FFMC Pontianak",
            color_discrete_sequence=['brown']
        )
        fig_ffmc.add_hline(y=85, line_dash="dash", line_color="red")
        fig_ffmc.add_hline(y=70, line_dash="dash", line_color="orange")
        st.plotly_chart(fig_ffmc, use_container_width=True)
    
    with col2:
        # ISPU analysis
        st.write("**ISPU (Indeks Standar Pencemaran Udara)**")
        st.write("Indikator kualitas udara akibat asap kebakaran")
        
        avg_ispu = filtered_df['ispu'].mean()
        if avg_ispu > 300:
            ispu_status = "🔴 Berbahaya"
        elif avg_ispu > 200:
            ispu_status = "🟠 Sangat Tidak Sehat"
        elif avg_ispu > 100:
            ispu_status = "🟡 Tidak Sehat"
        elif avg_ispu > 50:
            ispu_status = "🟢 Sedang"
        else:
            ispu_status = "🟢 Baik"
            
        st.metric("ISPU Rata-rata", f"{avg_ispu:.0f}", ispu_status)
        
        # ISPU trend
        daily_ispu = filtered_df.groupby('tanggal')['ispu'].mean().reset_index()
        fig_ispu = px.line(
            daily_ispu,
            x='tanggal',
            y='ispu',
            title="Trend ISPU Pontianak",
            color_discrete_sequence=['purple']
        )
        fig_ispu.add_hline(y=100, line_dash="dash", line_color="orange")
        fig_ispu.add_hline(y=200, line_dash="dash", line_color="red")
        st.plotly_chart(fig_ispu, use_container_width=True)
    
    # Hubungan FFMC, ISPU dengan titik panas
    fig_relationship = px.scatter(
        filtered_df,
        x='ffmc',
        y='ispu',
        size='titik_panas',
        color='tingkat_risiko',
        title="Hubungan FFMC vs ISPU (ukuran = jumlah titik panas)",
        color_discrete_map=colors
    )
    st.plotly_chart(fig_relationship, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**🌍 Dashboard Monitoring Titik Panas Kota Pontianak**")
st.markdown("*Tugas Akhir Informatika - Sistem Prediksi dan Monitoring Kebakaran Hutan dan Lahan*")
st.markdown("📍 *Kota Pontianak, Kalimantan Barat - Indonesia*")

# Sidebar info detail
st.sidebar.markdown("---")
st.sidebar.info(
    "**📊 Tentang Dashboard**\n\n"
    "Dashboard khusus untuk monitoring:\n"
    "• 6 area/kecamatan di Pontianak\n"
    "• Pola iklim khatulistiwa\n"
    "• Analisis musiman\n"
    "• FFMC & ISPU monitoring\n"
    "• Prediksi risiko kebakaran\n\n"
    "*Data simulasi untuk demo*"
)

# Real-time status
current_season = "Kemarau" if datetime.now().month in [4,5,6,7,8,9,10] else "Hujan"
st.sidebar.success(f"**Musim Saat Ini:** {current_season}")

if current_season == "Kemarau":
    st.sidebar.warning("⚠️ **Peningkatan Kewaspadaan**\nRisiko kebakaran lebih tinggi")
else:
    st.sidebar.info("🌧️ **Musim Hujan**\nRisiko kebakaran relatif rendah")
