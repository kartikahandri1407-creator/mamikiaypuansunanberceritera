import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Konfigurasi Halaman (Layout Boutique)
st.set_page_config(page_title="Mamikiaypuansunan Berceritera", page_icon="📜", layout="centered")

# 2. CSS TOBAT NASUHA (Premium UI)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #fafaf9; }
    
    .main-title {
        font-family: 'Playfair Display', serif;
        color: #1c1917;
        text-align: center; 
        font-size: 2.5rem !important;
        margin-bottom: 0px;
        padding-top: 10px;
    }
    .subtitle {
        text-align: center; 
        color: #a8a29e; 
        letter-spacing: 2px;
        font-size: 0.85rem;
        margin-bottom: 40px;
        text-transform: uppercase;
    }

    .stButton > button {
        background-color: #1c1917 !important; 
        color: #ffffff !important; 
        border-radius: 8px !important; 
        font-weight: 600 !important; 
        border: 1px solid #1c1917 !important;
        padding: 12px !important;
        margin-top: 20px !important;
    }
    .stButton > button:hover { 
        background-color: #ffffff !important; 
        color: #1c1917 !important; 
        border: 1px solid #d4af37 !important;
    }

    /* Style untuk Tabs Streamlit agar terlihat lebih premium */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        background-color: #f5f5f4;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1c1917 !important;
        color: white !important;
    }

    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .footer-manis {
        text-align: center;
        padding: 20px;
        font-size: 13px;
        font-weight: 600;
        color: #a8a29e;
        margin-top: 50px;
        border-top: 1px solid #e7e5e4;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. API Setup
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.info("💡 Masukkan API Key di Secrets Streamlit Cloud.")

# 4. Header
st.markdown("<h1 class='main-title'>Mamikiaypuansunan Berceritera</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>DIRECTOR'S CUT & CAMPAIGN KIT</div>", unsafe_allow_html=True)

# 5. Form Input
st.markdown("### 📸 Visual Produk")
# UPLOAD WAJIB
uploaded_file = st.file_uploader("Unggah foto produk asli (WAJIB untuk Kunci Bentuk & Kemasan)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Referensi Visual Terkunci", use_container_width=True)

st.divider()

st.markdown("### ✍️ Narasi & Gaya")
prod_name = st.text_input("Nama Mahakarya", placeholder="Misal: Keripik Pisang KWT Sumber Rejeki II")

# Baris 1: Klasifikasi & Durasi
c1, c2 = st.columns(2)
with c1:
    kategori_pilihan = [
        "Kuliner Premium", 
        "Kriya & Warisan", 
        "Fashion & Lifestyle", 
        "Beauty & Aura", 
        "Agrobisnis & Herbal", 
        "Hospitality", 
        "Lainnya (Ketik Manual)"
    ]
    category_select = st.selectbox("Klasifikasi Produk", kategori_pilihan)
    
    if category_select == "Lainnya (Ketik Manual)":
        category = st.text_input("Ketik Kategori Spesifik", placeholder="Misal: Elektronik, Jasa, dll.")
    else:
        category = category_select

    duration = st.selectbox("Durasi Iklan", ["15 Detik", "30 Detik", "60 Detik"])

with c2:
    format_video = st.selectbox("Format/Rasio", ["9:16 (Vertical)", "1:1 (Square)", "16:9 (Widescreen)"])
    model_type = st.selectbox("Tokoh (Model)", ["Tanpa Model", "Wanita Dewasa", "Pria Dewasa", "Anak-anak", "Lansia"])

# Baris 2: Tone & Bahasa
c3, c4 = st.columns(2)
with c3:
    tone_style = st.selectbox("Tone / Suasana", [
        "Mewah (Luxury/Gold)", 
        "Tradisional (Heritage/Warm)", 
        "Modern (Minimalist/Clean)", 
        "Premium (High-End/Elegant)",
        "Ceria (Fun/Energetic)"
    ])
with c4:
    lang_style = st.selectbox("Gaya Bahasa VO & Teks", [
        "Bahasa Indonesia Puitis (Elegan/Sastra)", 
        "Bahasa Indonesia Kasual (Hangat/Akrab)",
        "Bahasa Indonesia Profesional (Modern/Tegas)",
        "English Kekinian (Gen-Z Style)", 
        "Mixed (Indoglish/Bilingual)"
    ])

details = st.text_area("Jiwa Produk & Pesan Utama", placeholder="Ceritakan rahasia atau nilai seni di balik produk ini...")

generate = st.button("Mulai Tenun Cerita ✨", use_container_width=True)

# 6. Logika Eksekusi
if generate:
    # Validasi Berjenjang (Anti Error)
    if not uploaded_file:
        st.error("🚨 Mohon unggah Foto Produk terlebih dahulu! Gambar ini wajib sebagai panduan mutlak AI.")
    elif not prod_name or not details:
        st.warning("🚨 Mohon lengkapi Nama Mahakarya dan Jiwa Produk.")
    elif category_select == "Lainnya (Ketik Manual)" and not category:
        st.warning("🚨 Mohon ketikkan Kategori Spesifik produk Anda.")
    else:
        with st.spinner(f"📜 Menyusun Mahakarya TVC & Social Media Kit untuk {category}..."):
            try:
                # Setup Auto Parameter Midjourney
                ar_param = "--ar 9:16"
                if "1:1" in format_video:
                    ar_param = "--ar 1:1"
                elif "16:9" in format_video:
                    ar_param = "--ar 16:9"

                image = Image.open(uploaded_file)
                image_parts = [image]

                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # --- PROMPT VERSION: THE DIRECTOR + UI PARSER ---
                master_prompt = f"""
                Anda adalah Sutradara Iklan TV Komersial Kelas Dunia (sekelas sutradara iklan Apple, otomotif mewah) & Copywriter Elite.
                Tugas: Buat storyboard iklan TV {duration} rasio {format_video} untuk mahakarya '{prod_name}'.
                
                KATEGORI: {category}.
                GAYA VISUAL: {tone_style}. 
                GAYA BAHASA: {lang_style}.
                MODEL: {model_type}.

                ATURAN SINEMATOGRAFI KELAS DUNIA (WAJIB DITERAPKAN DI SEMUA TONE):
                - Visual "Iklan Mahal": Seluruh scene APAPUN tone-nya HARUS memancarkan aura iklan berbiaya miliaran rupiah.
                - Kamera & Lighting: Di prompt bahasa Inggris, WAJIB gunakan istilah alat berat Hollywood ("Shot on Arri Alexa 65", "Phantom Flex 4k", "Laowa Probe Lens", "cinematic chiaroscuro").
                - Naskah (VO): Walaupun memilih gaya bahasa kasual, eksekusinya harus tetap tajam, eksklusif, dan elegan layaknya iklan TV nasional.

                ATURAN HARGA MATI (ANTI-HALU GAMBAR):
                1. ANALISIS WAJIB: Anda WAJIB menganalisis gambar referensi. BENTUK FISIK: Deskripsikan bentuk asli produk dengan presisi (misal: jika keripik diiris memanjang, tulis "long lengthwise sliced"). JANGAN MENGARANG bentuk.
                2. BRANDING: Replikasi 100% detail teks, warna, dan logo pada kemasan persis seperti gambar.
                3. KONSISTENSI: Di setiap prompt bahasa Inggris, WAJIB sertakan instruksi: "Exactly matching the provided reference image".

                ATURAN UI (SANGAT PENTING):
                Anda WAJIB menggunakan pemisah teks yaitu `[BATAS_TAB]` sebelum setiap bagian utama agar sistem kami bisa memotongnya menjadi Tab UI.

                FORMAT OUTPUT (WAJIB IKUTI PEMISAH INI):

                [BATAS_TAB]
                🔍 ANALISIS VISUAL REFERENSI:
                [Detail analisis akurat bentuk fisik dan kemasan dari gambar referensi]

                [BATAS_TAB]
                🎬 SCENE 1: [Nama Scene] (5 detik)
                👁️ DESKRIPSI VISUAL: [Komposisi sinematik]
                📸 PROMPT GAMBAR: 
                ```text
                [Cinematic photography. High-end lighting/camera. EXACT physical shape & branding. INCLUDE: "Exactly matching the provided reference image."] {ar_param} --style raw --v 6.0
                ```
                🎥 PROMPT VIDEO: 
                ```text
                [EXACT product shape + High-end Camera Angle + 5-sec Camera Movement. INCLUDE: "Product and packaging must be identical to the uploaded reference image."]
                ```
                🎙️ ELEMEN AUDIO: [Naskah VO kelas atas sesuai {lang_style}] & [SFX/Musik taktil sesuai {tone_style}]
                🎵 PROMPT MUSIK AI: 
                ```text
                [Genre, tempo, mood for a high-budget commercial]
                ```

                [BATAS_TAB]
                🎬 SCENE 2: [Nama Scene] (5 detik)
                (Lanjutkan format scene di sini...)

                [BATAS_TAB]
                🎬 SCENE 3: [Nama Scene] (5 detik)
                (Lanjutkan format scene di sini...)

                [BATAS_TAB]
                📱 CAMPAIGN KIT & SOCIAL MEDIA
                - Caption Media Sosial: "[Buat caption yang menjual dan elegan sesuai {lang_style}]"
                - Hashtags Premium: "[5 Hashtag]"
                """
                res = model.generate_content([master_prompt] + image_parts)
                
                # --- LOGIKA PARSING TABS ---
                raw_text = res.text
                # Memotong teks berdasarkan pemisah ajaib
                sections = [s.strip() for s in raw_text.split("[BATAS_TAB]") if s.strip()]
                
                st.balloons()
                st.markdown(f"### 🎞️ Mahakarya Selesai: {tone_style} | {lang_style}")
                
                if len(sections) > 1:
                    # Membuat nama tab dinamis berdasarkan isi section
                    tab_titles = []
                    for s in sections:
                        if "ANALISIS" in s.upper()[:100]:
                            tab_titles.append("🔍 Analisis")
                        elif "SCENE 1" in s.upper()[:100]:
                            tab_titles.append("🎬 Scene 1")
                        elif "SCENE 2" in s.upper()[:100]:
                            tab_titles.append("🎬 Scene 2")
                        elif "SCENE 3" in s.upper()[:100]:
                            tab_titles.append("🎬 Scene 3")
                        elif "SCENE 4" in s.upper()[:100]:
                            tab_titles.append("🎬 Scene 4")
                        elif "SCENE 5" in s.upper()[:100]:
                            tab_titles.append("🎬 Scene 5")
                        elif "SCENE 6" in s.upper()[:100]:
                            tab_titles.append("🎬 Scene 6")
                        elif "CAMPAIGN" in s.upper()[:100]:
                            tab_titles.append("📱 Campaign Kit")
                        else:
                            tab_titles.append("✨ Bagian")
                            
                    # Render UI Tabs
                    tabs = st.tabs(tab_titles)
                    for i, tab in enumerate(tabs):
                        with tab:
                            st.markdown(sections[i])
                else:
                    # Fallback jika AI lupa kasih pemisah
                    st.markdown(raw_text)
                
                # Menggunakan format .md (Markdown) untuk file download agar format bold/code block aman
                st.download_button("Simpan Proposal (.MD)", raw_text.replace("[BATAS_TAB]", "\n\n---\n\n"), file_name=f"Director_Treatment_{prod_name}.md", use_container_width=True)
            
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {e}")

# 7. Footer
st.markdown('<div class="footer-manis">@mamikiaypuansunan</div>', unsafe_allow_html=True)