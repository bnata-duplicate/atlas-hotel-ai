import streamlit as st
import pandas as pd
import plotly.express as px

# Sayfa Ayarları
st.set_page_config(page_title="AI Atlas Strategic Engine", layout="wide", page_icon="📈")

st.title("📈 AI ATLAS STRATEGIC OPTIMIZATION ENGINE")
st.markdown("---")

# --- 📂 EXCEL YÜKLEME PANELİ ---
st.sidebar.header("📂 Veri Kaynağı")
uploaded_file = st.sidebar.file_uploader("Otel Veri Setini Yükleyin (Excel)", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # --- 🎯 AKTİF/PASİF OTEL SEÇİCİ ---
    st.sidebar.markdown("---")
    oteller = df['Hotel'].unique().tolist()
    secilen_oteller = st.sidebar.multiselect("Analiz Edilecek Otelleri Seçin:", options=oteller, default=oteller)
    df = df[df['Hotel'].isin(secilen_oteller)].copy()

    if not df.empty:
        # --- 🛠️ SİMÜLASYON ARAÇLARI ---
        st.sidebar.header("🛠️ Strateji Simülatörü")
        fiyat_degisimi = st.sidebar.slider("Fiyat Değişim Oranı (%)", -30, 30, 0)
        df['Yeni_Fiyat'] = df['Price_ADR'] * (1 + fiyat_degisimi/100)
        
        # --- 📊 ÜST ÖZET KARTLARI ---
        c1, c2, c3 = st.columns(3)
        c1.metric("Toplam Otel", len(df))
        c2.metric("Pazar Ortalama ADR", f"{df['Price_ADR'].mean():.2f} €")
        c3.metric("Simülasyon Fiyatı (Ort)", f"{df['Yeni_Fiyat'].mean():.2f} €", f"{fiyat_degisimi}%")

        # --- 📈 ANA ANALİZ GRAFİĞİ (TAM GENİŞLİK) ---
        st.markdown("### 📊 Pazar Konumlandırma Haritası")
        fig = px.scatter(df, x="Price_ADR", y="Review_Score", size="Occupancy_Est.", 
                         color="Hotel", hover_name="Hotel", text="Hotel", height=500) 
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # --- 🤖 ATLAS-1 STRATEJİK ANALİZ RAPORU ---
        st.markdown("### 🤖 ATLAS-1 Stratejik Analiz Raporu")
        pazar_ort = df['Price_ADR'].mean()
        st.info(f"📍 **Pazar Konumlandırması:** Pazar ortalama fiyatı {pazar_ort:.2f} € seviyesinde.")

        col1, col2 = st.columns(2)
        for i, (index, row) in enumerate(df.iterrows()):
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                # Slider hareketine duyarlı analiz (Kendi eski fiyatına göre):
                degisim_orani = ((row['Yeni_Fiyat'] / row['Price_ADR']) - 1) * 100
                skor = row['Review_Score']
                
                if degisim_orani > 15 and skor >= 9.0:
                    st.warning(f"⚠️ **{row['Hotel']}**: %{degisim_orani:.1f} Artış! Kalite yüksek ama bu sıçrama riskli.")
                elif degisim_orani > 5 and skor < 8.5:
                    st.error(f"🚨 **{row['Hotel']}**: Tehlike! Düşük skora rağmen fiyat artırıyorsunuz.")
                elif degisim_orani < -15:
                    st.info(f"🏷️ **{row['Hotel']}**: %{abs(degisim_orani):.1f} İndirim! Agresif pazar payı hamlesi.")
                elif degisim_orani > 25:
                    st.error(f"🛑 **{row['Hotel']}**: Aşırı Fiyatlama! Strateji pazarın çok üstünde.")
                else:
                    st.success(f"✅ **{row['Hotel']}**: Dengeli Hamle. Pazar skoruyla uyumlu.")

        st.caption("🔍 *ATLAS-1: Fiyat değişimlerini ve pazar skorlarını anlık analiz eder.*")
        
        # --- 📑 DETAYLI VERİ TABLOSU ---
        st.markdown("---")
        st.markdown("### 📑 Detaylı Veri Seti")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Lütfen en az bir otel seçin.")
else:
    st.info("👋 Hoş Geldiniz! Lütfen sol taraftan Excel dosyanızı yükleyin.")
