import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Konfigurasi Halaman 
st.set_page_config(page_title="Mamikiaypuansunan Berceritera", page_icon="📜", layout="centered")

# 2. CSS TOBAT NASUHA
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    html, body, [class*="st-"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
    }
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
    st.info("💡 Sistem membutuhkan API Key untuk mulai menenun cerita.")

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
        st.warning("Mohon lengkapi Nama Mahakarya dan Jiwa Produk terlebih dahulu.")
    else:
        with st.spinner("📜 Mamiki sedang menenun simfoni visual dan audio..."):
            try:
                image_parts = []
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    image_parts = [image]

                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # --- PROMPT FINAL: STRUKTUR LENGKAP + ESTETIKA NUSANTARA ---
                master_prompt = f"""
                Anda adalah Creative Director kelas dunia dan Ahli AI Prompt Engineering yang memahami kekayaan visual budaya.
                Buatlah storyboard iklan sinematik {duration} rasio {format_video} untuk mahakarya '{prod_name}'.
                Kategori: {category}. Model: {model_type}. Deskripsi: {details}.

                INSTRUKSI PENTING: Berikan sentuhan kehangatan tropis, tekstur organik, atau elemen kearifan lokal yang dikemas secara super eksklusif dan mewah. Hindari gaya visual yang terlalu Skandinavia/Eropa dingin.

                UBAH TOTAL FORMAT OUTPUT ANDA. Langsung berikan output per Scene dengan struktur WAJIB berikut ini secara berurutan:

                ---
                🎬 SCENE [Nomor]: [Nama Scene] ([Durasi detik])

                👁️ DESKRIPSI VISUAL (Bahasa Indonesia):
                [Jelaskan detail apa yang terlihat di layar. Jelaskan komposisi, negative space, pencahayaan, objek utama, dan suasana visual secara menyeluruh menggunakan bahasa yang mudah dipahami klien].

                📸 PROMPT GAMBAR (English - Siap Copy ke Midjourney/DALL-E):
                [Tulis prompt visual statis yang SANGAT DETAIL. Tentukan: Subject placement, extreme detail texture, camera angle, lens type, lighting setup (e.g., warm cinematic lighting), color grading, dan negative space. DILARANG memasukkan perintah teks/tulisan di dalam prompt ini].

                🎥 PROMPT VIDEO ALL-IN-ONE (English - Siap Copy ke Kling/Runway/Sora):
                [Tulis SATU PARAGRAF PANJANG yang SANGAT DETAIL dan BERDIRI SENDIRI. Ulangi deskripsi wujud objek, tekstur, warna, latar belakang, dan pencahayaan agar AI Video tidak bingung. LALU gabungkan dengan: Pergerakan kamera (e.g., slow dolly in), pergerakan dinamis subjek, efek atmosfer, dan instruksi audio visual. Prompt ini harus sangat padat dan komprehensif].

                🎙️ ELEMEN AUDIO & TEKS (Bahasa Indonesia):
                - Voice Over (VO): "[Naskah puitis, elegan, dan menjual]"
                - SFX & Musik: "[Deskripsi detail suara taktil dan instrumen musik]"
                - On-Screen Text: "[Teks singkat dan estetik yang muncul di layar]"
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