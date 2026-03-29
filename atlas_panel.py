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

        # --- ORTA PANEL: GRAFİKLER ---
        col_left, col_right = st.columns(2)
        
        with col_left:
           with col_right:
            st.markdown("### 🤖 ATLAS-1 Stratejik Analiz Raporu")
            
            pazar_ort = df['Price_ADR'].mean()
            
            # ATLAS-1 Muhakeme Katmanı
            st.info(f"📍 **Pazar Konumlandırması:** Şu an pazar ortalaması {pazar_ort:.2f} € seviyesinde.")
            
            for _, row in df.iterrows():
                fiyat_farki = ((row['Yeni_Fiyat'] / pazar_ort) - 1) * 100
                skor = row['Review_Score']
                otel = row['Hotel']
                
                # Dinamik Karar Algoritması
                if skor >= 9.0 and fiyat_farki > 20:
                    st.warning(f"⚠️ **{otel}**: Kaliteniz yüksek (Skor: {skor}) ancak pazarın %{fiyat_farki:.1f} üzerindesiniz. Lüks segment riskidir.")
                elif skor >= 9.0 and fiyat_farki <= 20:
                    st.success(f"💎 **{otel}**: İdeal Konum! Yüksek kalite ve makul fiyat farkı.")
                elif skor < 8.5 and fiyat_farki > 0:
                    st.error(f"🚨 **{otel}**: KRİTİK UYARI! Memnuniyet düşükken pahalı fiyatlama!")
                elif fiyat_farki < -15:
                    st.info(f"🏷️ **{otel}**: Agresif Fiyatlama! Rakiplerden talep çalacaktır.")
                else:
                    st.info(f"⚖️ **{otel}**: Denge Bölgesi. Strateji pazarla uyumlu.")

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
