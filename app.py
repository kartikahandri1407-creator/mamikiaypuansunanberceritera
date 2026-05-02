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
uploaded_file = st.file_uploader("Unggah foto produk asli (Referensi Utama)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Identitas Visual Terkunci", use_container_width=True)

st.divider()

st.markdown("### ✍️ Narasi Produk")
prod_name = st.text_input("Nama Mahakarya", placeholder="Misal: Keripik Pisang KWT Sumber Rejeki II")

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
        with st.spinner("📜 Mamiki sedang menyusun narasi dan teks butik Anda..."):
            try:
                image_parts = []
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    image_parts = [image]

                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # --- PROMPT VERSION: LUXURY UX & INDONESIAN PURITY ---
                master_prompt = f"""
                Anda adalah Creative Director & UX Copywriter Senior. 
                Tugas: Buat storyboard iklan {duration} rasio {format_video} untuk mahakarya: '{prod_name}'.

                ATURAN HARGA MATI TEKS & BAHASA:
                1. 100% BAHASA INDONESIA: Gunakan padanan kata yang puitis, eksklusif, dan indah. Dilarang menggunakan istilah Inggris seperti "Crisp", "Natural", "Best Seller", dll. Gunakan kata seperti "Renyah Alami", "Sentuhan Murni", "Warisan Terpilih".
                2. FONT & STYLE: Untuk setiap scene, tentukan jenis font yang digunakan (e.g., 'Modern Serif untuk kemewahan' atau 'Elegant Sans-Serif untuk kesegaran').
                3. UX PLACEMENT: Tentukan posisi teks di layar (misal: 'Sudut bawah kanan' atau 'Tengah atas dengan margin luas'). Teks TIDAK BOLEH mengganggu atau menutupi detail produk utama.
                4. BRANDING: Pastikan teks di layar konsisten dengan merek pada gambar referensi.

                ATURAN KONTINUITAS:
                - Durasi per Scene tepat 5 detik.
                - Jika ada model (Model: {model_type}), detail mikro (kutek kuku, baju) harus KONSISTEN di setiap prompt video.
                - Suara VO harus memiliki satu persona yang sama dari awal sampai akhir.

                FORMAT OUTPUT (WAJIB):
                ---
                🎬 SCENE [Nomor]: [Nama Scene] (5 detik)

                👁️ DESKRIPSI VISUAL (Bahasa Indonesia):
                [Detail komposisi, pencahayaan, dan konfirmasi konsistensi detail mikro].

                📸 PROMPT GAMBAR (English - Midjourney Style):
                [Static detail. Deskripsikan merek & kemasan SESUAI gambar referensi. NO TEXT IN IMAGE].

                🎥 PROMPT VIDEO ALL-IN-ONE (English - Kling Style):
                [Self-contained paragraph. Deskripsikan wujud produk/kemasan + pergerakan kamera 5 detik + detail model].

                🎙️ ELEMEN AUDIO & TEKS (Bahasa Indonesia):
                - Voice Over (VO): "[Naskah mengalir dan puitis]"
                - SFX & Musik: "[Deskripsi instrumen lokal & suara taktil]"
                - On-Screen Text: "[TEKS DALAM BAHASA INDONESIA YANG INDAH]"
                - Font Style & Position: "[Tentukan jenis font dan posisi agar tidak menutupi produk]"
                ---
                """
                res = model.generate_content([master_prompt] + image_parts)
                st.balloons()
                
                st.markdown("### 🎞️ Hasil Racikan Mahakarya (UX & Branding Optimized)")
                st.info(res.text) 
                
                st.download_button("Simpan Storyboard (TXT)", res.text, file_name=f"Storyboard_{prod_name}.txt", use_container_width=True)
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {e}")

# 7. Footer
st.markdown('<div class="footer-manis">@mamikiaypuansunan</div>', unsafe_allow_html=True)