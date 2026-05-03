import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Konfigurasi Halaman (Layout Boutique)
st.set_page_config(page_title="Mamikiaypuansunan Berceritera", page_icon="📜", layout="centered")

# 2. CSS TOBAT NASUHA
st.markdown("""
    <style>
    @import url('[https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&family=Playfair+Display:ital,wght@0,700;1,700&display=swap](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&family=Playfair+Display:ital,wght@0,700;1,700&display=swap)');
    
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
uploaded_file = st.file_uploader("Unggah foto produk (Referensi Wajib untuk Brand Lock)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Referensi Visual Terkunci", use_container_width=True)

st.divider()

st.markdown("### ✍️ Narasi & Gaya")
prod_name = st.text_input("Nama Mahakarya", placeholder="Misal: Keripik Pisang Sumber Rejeki")

# Baris 1: Klasifikasi & Durasi
c1, c2 = st.columns(2)
with c1:
    category = st.selectbox("Klasifikasi Produk", ["Kuliner Premium", "Kriya & Warisan", "Fashion & Lifestyle", "Beauty & Aura", "Hospitality"])
    duration = st.selectbox("Durasi Iklan", ["15 Detik", "30 Detik", "60 Detik"])
with c2:
    format_video = st.selectbox("Format/Rasio", ["9:16 (Vertical)", "1:1 (Square)", "16:9 (Widescreen)"])
    model_type = st.selectbox("Tokoh (Model)", ["Tanpa Model", "Wanita Dewasa", "Pria Dewasa", "Anak-anak", "Lansia"])

# Baris 2: Tone & Bahasa
c3, c4 = st.columns(2)
with c3:
    tone_style = st.selectbox("Tone / Suasana", ["Mewah (Luxury/Gold)", "Tradisional (Heritage/Warm)", "Modern (Minimalist/Clean)", "Premium (High-End/Elegant)"])
with c4:
    lang_style = st.selectbox("Gaya Bahasa", ["Bahasa Indonesia Puitis", "English Kekinian (Gen-Z Style)", "Mixed (Indoglish/Bilingual)"])

details = st.text_area("Jiwa Produk & Pesan Utama", placeholder="Ceritakan rahasia atau nilai seni di balik produk ini...")

generate = st.button("Mulai Tenun Cerita ✨", use_container_width=True)

# 6. Logika Eksekusi
if generate:
    if not prod_name or not details:
        st.warning("Mohon lengkapi Nama Mahakarya dan Jiwa Produk.")
    else:
        with st.spinner(f"📜 Meracik mahakarya dengan tone {tone_style}..."):
            try:
                # Menyiapkan parameter Aspect Ratio otomatis untuk Midjourney
                ar_param = "--ar 9:16"
                if "1:1" in format_video:
                    ar_param = "--ar 1:1"
                elif "16:9" in format_video:
                    ar_param = "--ar 16:9"

                image_parts = []
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    image_parts = [image]

                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # --- PROMPT VERSION: ULTIMATE COMPLETE (KAMERA, ANGLE, AUDIO, AUTO-COPY) ---
                master_prompt = f"""
                Anda adalah Creative Director & Brand Guardian Senior.
                Tugas: Buat storyboard iklan {duration} rasio {format_video} untuk '{prod_name}'.
                
                GAYA VISUAL: {tone_style}. 
                GAYA BAHASA VO/TEKS: {lang_style}.
                MODEL: {model_type}.

                ATURAN VISUAL LOCK (HARGA MATI):
                1. IDENTITAS: Jika ada gambar referensi, identifikasi Merek, Logo, Warna Label, dan Bentuk Produk. DILARANG KERAS halusinasi mengubah teks kemasan.
                2. KONSISTENSI FISIK: Bentuk fisik produk (isi) harus 100% konsisten di setiap scene.

                ATURAN TEKNIS LENGKAP:
                - KAMERA & ANGLE: Setiap Prompt Video WAJIB memiliki instruksi jenis lensa (macro, wide), sudut pandang (eye-level, low angle, extreme close-up), dan pergerakan kamera 5 detik (slow pan, dolly in).
                - AUDIO INTEGRATION: Prompt Video WAJIB mencantumkan instruksi *sound effects* (SFX) taktil (seperti suara "kriuk", desis angin) dan *cues* musik latar yang menyesuaikan *tone*.
                - TULIS PROMPT DALAM FORMAT MARKDOWN (```text ... ```) agar bisa langsung di-copy oleh user.

                FORMAT OUTPUT (WAJIB PER SCENE 5 DETIK):
                ---
                🎬 SCENE [Nomor]: [Nama Scene] (5 detik)

                👁️ DESKRIPSI VISUAL (Bahasa Indonesia):
                [Detail komposisi, angle kamera, interaksi model, dan suasana sesuai tone {tone_style}].

                📸 PROMPT GAMBAR (English - Midjourney Style):
                ```text
                [High-detail static prompt. Camera angle, lens type. Reference the uploaded branding precisely. NO HALUCINATIONS on labels] {ar_param} --style raw --v 6.0
                ```

                🎥 PROMPT VIDEO ALL-IN-ONE (English - Kling Style):
                ```text
                [Self-contained paragraph. Wujud kemasan/produk asli + Camera Angle + Pergerakan Kamera 5 detik + Pergerakan Subjek + Audio SFX & Music Cues sesuai tone {tone_style}]
                ```

                🎙️ ELEMEN AUDIO & TEKS ({lang_style}):
                - Voice Over (VO): "[Naskah sesuai gaya bahasa]"
                - SFX & Musik: "[Deskripsi spesifik efek suara dan instrumen musik]"
                - On-Screen Text & Posisi: "[Teks dan saran letak/font]"
                
                🎵 PROMPT MUSIK AI (English - Suno/Udio Ready):
                ```text
                [Genre, tempo, mood, and specific instrumentation matching the {tone_style} vibe]
                ```
                ---
                """
                res = model.generate_content([master_prompt] + image_parts)
                st.balloons()
                
                st.markdown(f"### 🎞️ Hasil Racikan: {tone_style} | {lang_style}")
                st.markdown(res.text) # Menggunakan st.markdown agar fitur code-block (kotak copy) berfungsi
                
                st.download_button("Simpan Storyboard (TXT)", res.text, file_name=f"Storyboard_{prod_name}.txt", use_container_width=True)
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {e}")

# 7. Footer
st.markdown('<div class="footer-manis">@mamikiaypuansunan</div>', unsafe_allow_html=True)