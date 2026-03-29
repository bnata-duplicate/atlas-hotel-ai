import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Sayfa Ayarları
st.set_page_config(page_title="AI Atlas Strategic Engine", layout="wide", page_icon="📈")

st.title("📈 AI ATLAS STRATEGIC OPTIMIZATION ENGINE")
st.markdown("---")

# --- 📂 EXCEL YÜKLEME PANELİ (BULUT UYUMLU) ---
st.sidebar.header("📂 Veri Kaynağı")
uploaded_file = st.sidebar.file_uploader("Otel Veri Setini Yükleyin (Excel)", type=["xlsx"])

if uploaded_file is not None:
    # Veriyi Oku
    df = pd.read_excel(uploaded_file)
    
    # --- 🎯 AKTİF/PASİF OTEL SEÇİCİ ---
    st.sidebar.markdown("---")
    oteller = df['Hotel'].unique().tolist()
    secilen_oteller = st.sidebar.multiselect(
        "Analiz Edilecek Otelleri Seçin:", 
        options=oteller, 
        default=oteller
    )
    
    # Seçilen otellere göre filtrele
    df = df[df['Hotel'].isin(secilen_oteller)].copy()

    if not df.empty:
        # --- SOL PANEL: SİMÜLASYON ARAÇLARI ---
        st.sidebar.header("🛠️ Strateji Simülatörü")
        fiyat_degisimi = st.sidebar.slider("Fiyat Değişim Oranı (%)", -30, 30, 0)
        
        # Simülasyon Hesaplama
        df['Yeni_Fiyat'] = df['Price_ADR'] * (1 + fiyat_degisimi/100)
        
        # --- ÜST ÖZET KARTLARI ---
        c1, c2, c3 = st.columns(3)
        c1.metric("Toplam Otel", len(df))
        c2.metric("Pazar Ortalama ADR", f"{df['Price_ADR'].mean():.2f} €")
        c3.metric("Simülasyon Fiyatı (Ort)", f"{df['Yeni_Fiyat'].mean():.2f} €", f"{fiyat_degisimi}%")
# --- 📈 ANA ANALİZ ALANI (TAM GENİŞLİK) ---
        st.markdown("---")
        st.markdown("### 📊 Pazar Konumlandırma Haritası")
        
        # Grafiği tam genişlikte oluşturuyoruz
        fig = px.scatter(df, x="Price_ADR", y="Review_Score", size="Occupancy_Est.", 
                         color="Hotel", hover_name="Hotel", text="Hotel",
                         height=500) 
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # --- 🤖 ATLAS-1 STRATEJİK ANALİZ RAPORU ---
        st.markdown("### 🤖 ATLAS-1 Stratejik Analiz Raporu")
        
        pazar_ort = df['Price_ADR'].mean()
        st.info(f"📍 **Pazar Konumlandırması:** Şu an pazar ortalama fiyatı {pazar_ort:.2f} € seviyesinde.")

        # Otel raporlarını yan yana iki sütunda gösterelim (Denge sağlar)
        c1, c2 = st.columns(2)
        
        for i, (index, row) in enumerate(df.iterrows()):
            # Otelleri sırayla sütunlara paylaştır (0, 2, 4 sola | 1, 3, 5 sağa)
            hedef_sutun = c1 if i % 2 == 0 else c2
            
            with hedef_sutun:
                fiyat_farki = ((row['Yeni_Fiyat'] / pazar_ort) - 1) * 100
                skor = row['Review_Score']
                otel = row['Hotel']
                
                if skor >= 9.0 and fiyat_farki > 20:
                    st.warning(f"⚠️ **{otel}**: Kalite yüksek (Skor: {skor}) ancak fiyat riskli! Pazarın %{fiyat_farki:.1f} üzerindesiniz.")
                elif skor >= 9.0 and fiyat_farki <= 20:
                    st.success(f"💎 **{otel}**: İdeal Konumlandırma! Kalite-Fiyat dengesi mükemmel.")
                elif skor < 8.5 and fiyat_farki > 0:
                    st.error(f"🚨 **{otel}**: KRİTİK! Memnuniyet düşükken pazar üstü fiyatlama!")
                elif fiyat_farki < -15:
                    st.info(f"🏷️ **{otel}**: Agresif Fiyatlama! Rakiplerden ciddi talep çalabilir.")
                else:
                    st.info(f"⚖️ **{otel}**: Denge Bölgesi. Pazar dinamikleriyle uyumlu.")

        st.caption("🔍 *ATLAS-1: Pazar verilerini ve kullanıcı senaryosunu gerçek zamanlı analiz eder.*")

            st.caption("🔍 *ATLAS-1: Pazar verilerini ve kullanıcı senaryosunu gerçek zamanlı analiz eder.*")
            st.markdown("### 📊 Fiyat vs Müşteri Memnuniyeti")
            fig = px.scatter(df, x="Price_ADR", y="Review_Score", size="Occupancy_Est.", 
                             color="Hotel", hover_name="Hotel", text="Hotel")
            st.plotly_chart(fig, use_container_width=True)

        
        # --- ALT PANEL: DETAYLI TABLO ---
        st.markdown("### 📑 Detaylı Veri Seti")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Lütfen analiz için en az bir otel seçin.")

else:
    st.info("👋 Hoş Geldiniz! Lütfen sol taraftaki panelden masaüstündeki 'otel_verileri.xlsx' dosyasını yükleyerek analizi başlatın.")
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100)
