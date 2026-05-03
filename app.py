import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Konfigurasi Halaman (Layout Boutique)
st.set_page_config(page_title="Mamikiaypuansunan Berceritera", page_icon="📜", layout="centered")

# 2. CSS TOBAT NASUHA
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
st.markdown("<div class='subtitle'>BEYOND ADS: WE WEAVE LEGENDS</div>", unsafe_allow_html=True)

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
    
    # Logika UX: Input manual jika pilih "Lainnya"
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
        with st.spinner(f"📜 Merajut mahakarya {category} dengan tone {tone_style}..."):
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
                
                # --- PROMPT VERSION: THE ULTIMATE MASTERPIECE ---
                master_prompt = f"""
                Anda adalah Creative Director, Ahli Analisis Visual, & Copywriter Kelas Dunia.
                Tugas: Buat storyboard iklan {duration} rasio {format_video} untuk mahakarya '{prod_name}'.
                
                KATEGORI: {category}.
                GAYA VISUAL: {tone_style}. 
                GAYA BAHASA: {lang_style}.
                MODEL: {model_type}.

                ATURAN HARGA MATI (GAMBAR REFERENSI ADALAH HUKUM TERTINGGI):
                1. ANALISIS WAJIB: Anda WAJIB menganalisis gambar referensi yang telah dilampirkan. Segala bentuk halusinasi visual yang bertentangan dengan gambar ini DILARANG KERAS.
                2. BENTUK FISIK: Deskripsikan bentuk asli produk dengan presisi (misal: jika keripik diiris memanjang, tulis "long lengthwise sliced"). JANGAN MENGARANG bentuk jika tidak sesuai gambar.
                3. BRANDING KEMASAN: Replikasi 100% detail teks, warna, dan logo pada kemasan persis seperti gambar di scene akhir.
                4. KONSISTENSI: Di setiap prompt bahasa Inggris, WAJIB sertakan instruksi: "Exactly matching the provided reference image".

                ATURAN TEKNIS LENGKAP:
                - Durasi: TEPAT 5 detik per Scene. (15s = 3 Scene, 30s = 6 Scene).
                - Kamera: Wajib ada instruksi Lensa, Angle, dan Pergerakan 5 detik.
                - Naskah (VO): Sesuaikan nada bicara dengan {lang_style}. Jangan puitis jika klien meminta kasual/fun.
                - Format Teks: PROMPT GAMBAR, VIDEO, DAN MUSIK WAJIB dibungkus dalam blok kode Markdown (```text ... ```) agar mudah di-copy klien.

                FORMAT OUTPUT (WAJIB PER SCENE):
                ---
                🔍 ANALISIS VISUAL REFERENSI (Sebutkan di awal saja):
                [Sebutkan dengan detail bentuk fisik produk dan detail kemasan dari gambar referensi agar Anda tidak berhalusinasi di langkah selanjutnya].

                🎬 SCENE [Nomor]: [Nama Scene] (5 detik)

                👁️ DESKRIPSI VISUAL (Bahasa Indonesia):
                [Detail komposisi, interaksi model, dan nuansa {tone_style} yang 100% konsisten dengan gambar referensi].

                📸 PROMPT GAMBAR (English - Midjourney Style):
                ```text
                [High-detail static prompt. MUST explicitly describe the accurate physical shape and EXACT branding. INCLUDE: "Exactly matching the provided reference image in shape, color, and branding."] {ar_param} --style raw --v 6.0
                ```

                🎥 PROMPT VIDEO ALL-IN-ONE (English - Kling Style):
                ```text
                [Self-contained paragraph. Describe EXACT product shape/packaging + Camera Angle + 5-second Camera Movement + Audio SFX & Music. INCLUDE: "Product and packaging must be identical to the uploaded reference image."]
                ```

                🎙️ ELEMEN AUDIO & TEKS ({lang_style}):
                - Voice Over (VO): "[Naskah sesuai {lang_style}]"
                - SFX & Musik: "[Efek suara taktil & instrumen sesuai {tone_style}]"
                - On-Screen Text & Posisi: "[Teks estetik dan saran letaknya]"
                
                🎵 PROMPT MUSIK AI (English - Suno/Udio Ready):
                ```text
                [Genre, tempo, mood, and instrumentation matching {tone_style} and {category}]
                ```
                ---
                """
                res = model.generate_content([master_prompt] + image_parts)
                st.balloons()
                
                st.markdown(f"### 🎞️ Hasil Racikan: {tone_style} | {lang_style}")
                st.markdown(res.text)
                
                st.download_button("Simpan Storyboard (TXT)", res.text, file_name=f"Storyboard_{prod_name}.txt", use_container_width=True)
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {e}")

# 7. Footer
st.markdown('<div class="footer-manis">@mamikiaypuansunan</div>', unsafe_allow_html=True)