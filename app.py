import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Konfigurasi Halaman 
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
uploaded_file = st.file_uploader("Unggah foto mahakarya (Opsional)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Visual Terdeteksi", use_container_width=True)

st.divider()

st.markdown("### ✍️ Narasi Produk")
prod_name = st.text_input("Nama Mahakarya", placeholder="Misal: Tapis Pinang Mas")

col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("Klasifikasi", ["Kriya & Warisan", "Kuliner Premium", "Fashion & Lifestyle", "Beauty & Aura", "Hospitality", "Agrowisata"])
    duration = st.selectbox("Durasi", ["15 Detik", "30 Detik", "60 Detik"])
with col2:
    format_video = st.selectbox("Format/Rasio", ["9:16 (Vertical)", "1:1 (Square)", "16:9 (Widescreen)"])
    model_type = st.selectbox("Tokoh (Model)", ["Tanpa Model", "Wanita Dewasa", "Pria Dewasa", "Anak-anak", "Lansia", "Remaja"])

details = st.text_area("Jiwa Produk & Pesan Utama", placeholder="Ceritakan rahasia atau nilai seni di balik produk ini...")

generate = st.button("Mulai Tenun Cerita ✨", use_container_width=True)

# 6. Logika Eksekusi
if generate:
    if not prod_name or not details:
        st.warning("Mohon lengkapi Nama Mahakarya dan Jiwa Produk.")
    else:
        with st.spinner("📜 Mamiki sedang menenun simfoni visual dan audio..."):
            try:
                image_parts = []
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    image_parts = [image]

                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # --- PROMPT MASTER: TOTAL SYNCHRONIZATION ---
                master_prompt = f"""
                Anda adalah Creative Director & Expert Prompt Engineer.
                Tugas: Buat storyboard iklan {duration} rasio {format_video} untuk mahakarya: '{prod_name}'.
                Kategori: {category}. Model: {model_type}. Deskripsi: {details}.

                ATURAN SCENE (DURASI RENDER AI):
                AI Video (Kling/Runway) bekerja dalam potongan 5 detik.
                - 15 Detik = Tepat 3 Scene.
                - 30 Detik = Tepat 6 Scene.
                - 60 Detik = Tepat 12 Scene.
                Setiap scene WAJIB berdurasi 5 detik.

                ATURAN KONSISTENSI VISUAL (GAMBAR vs TEKS):
                1. Jika ada gambar: Identifikasi merek, warna, dan bentuk kemasan dari gambar. Gunakan detail tersebut di seluruh scene.
                2. Jika tidak ada gambar: Bangun visual 100% berdasarkan Nama Mahakarya: '{prod_name}'.
                3. Pastikan Prompt Gambar (Midjourney) dan Prompt Video (Kling) mendeskripsikan subjek yang SAMA PERSIS agar konsisten.

                ATURAN MODEL ({model_type}):
                - Jika 'Tanpa Model': Fokus 100% pada sinematografi produk (macro, slow motion, lighting).
                - Jika ada Model: Sertakan interaksi model dengan produk (memegang, menatap, menggunakan) sesuai kategori {category}.

                FORMAT OUTPUT (WAJIB):
                ---
                🎬 SCENE [Nomor]: [Nama Scene] (5 detik)

                👁️ DESKRIPSI VISUAL (Bahasa Indonesia):
                [Detail komposisi, pencahayaan, dan peran model jika ada].

                📸 PROMPT GAMBAR (English - Midjourney Style):
                [High-detail static prompt, focus on texture & lighting. NO TEXT IN IMAGE].

                🎥 PROMPT VIDEO ALL-IN-ONE (English - Kling/Runway Style):
                [Self-contained paragraph. Deskripsikan wujud produk secara utuh (warna, tekstur, merek) + pergerakan kamera 5 detik + pergerakan subjek. AI Video harus tahu apa yang digerakkan tanpa melihat prompt gambar].

                🎙️ ELEMEN AUDIO & TEKS (Bahasa Indonesia):
                - Voice Over (VO): "[Naskah puitis]"
                - SFX & Musik: "[Suara taktil & instrumen]"
                - On-Screen Text: "[Teks estetik]"
                ---
                """
                res = model.generate_content([master_prompt] + image_parts)
                st.balloons()
                
                st.markdown("### 🎞️ Hasil Racikan Mahakarya")
                st.info(res.text) 
                
                st.download_button("Simpan Storyboard (TXT)", res.text, file_name=f"Storyboard_{prod_name}.txt", use_container_width=True)
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {e}")

# 7. Footer
st.markdown('<div class="footer-manis">@mamikiaypuansunan</div>', unsafe_allow_html=True)