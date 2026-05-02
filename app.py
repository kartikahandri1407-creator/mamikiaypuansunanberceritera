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
uploaded_file = st.file_uploader("Unggah foto produk asli (Referansi Label & Kemasan)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Identitas Visual Asli Terdeteksi", use_container_width=True)

st.divider()

st.markdown("### ✍️ Narasi Produk")
prod_name = st.text_input("Nama Mahakarya", placeholder="Misal: Keripik Pisang Sumber Rejeki")

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
        with st.spinner("📜 Mamiki sedang membaca label dan mengunci identitas produk..."):
            try:
                image_parts = []
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    image_parts = [image]

                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # --- PROMPT VERSION: IDENTITY LOCK & TEXT PRESERVATION ---
                master_prompt = f"""
                Anda adalah Creative Director & Ahli Fotografi Produk Komersial.
                Tugas: Buat storyboard iklan {duration} rasio {format_video} untuk '{prod_name}'.

                ATURAN KHUSUS ANALISIS GAMBAR (BRANDING LOCK):
                1. IDENTIFIKASI LABEL: Lihat gambar yang diunggah. Ada label kuning dengan teks dan logo (misal: Logo Halal, Nama Merek, No WA). 
                2. REPLIKASI TEKS: Pada Prompt Gambar dan Video di Scene terakhir, Anda WAJIB mendeskripsikan label tersebut secara mendetail: "Yellow label with original branding text, cartoon mascot, and Halal logo as seen in the reference image."
                3. ANTI-BLANK LABEL: Dilarang keras membiarkan label menjadi polos atau kosong. Kemasan harus tampil 1:1 dengan aslinya namun dengan pencahayaan sinematik.

                STRUKTUR SCENE (Potongan 5 detik):
                - Scene awal: Fokus ke tekstur isi produk (organik & sinematik).
                - Scene akhir: Fokus ke kemasan utuh (Product Reveal) sesuai foto referensi.

                FORMAT OUTPUT (WAJIB):
                ---
                🎬 SCENE [Nomor]: [Nama Scene] (5 detik)

                👁️ DESKRIPSI VISUAL (Bahasa Indonesia):
                [Jelaskan visual secara puitis. Scene akhir wajib menyebutkan kemasan dengan branding yang utuh sesuai gambar].

                📸 PROMPT GAMBAR (English - Midjourney Style):
                [Sertakan instruksi: "Exact replica of the yellow label from the reference image, including all text and logos, realistic lighting, macro texture"].

                🎥 PROMPT VIDEO ALL-IN-ONE (English - Kling Style):
                [Deskripsikan pergerakan kamera 5 detik yang menyorot label dan kemasan asli secara perlahan (slow zoom/pan). Tegaskan bahwa teks pada label harus terlihat jelas dan tidak boleh dihilangkan].

                🎙️ ELEMEN AUDIO & TEKS (Bahasa Indonesia):
                - Voice Over (VO): "[Naskah puitis]"
                - SFX & Musik: "[Suara taktil & instrumen lokal]"
                - On-Screen Text: "[Teks estetik]"
                ---
                """
                res = model.generate_content([master_prompt] + image_parts)
                st.balloons()
                
                st.markdown("### 🎞️ Hasil Racikan Mahakarya (Identity Locked)")
                st.info(res.text) 
                
                st.download_button("Simpan Storyboard (TXT)", res.text, file_name=f"Storyboard_{prod_name}.txt", use_container_width=True)
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {e}")

# 7. Footer
st.markdown('<div class="footer-manis">@mamikiaypuansunan</div>', unsafe_allow_html=True)