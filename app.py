import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Konfigurasi Halaman 
st.set_page_config(page_title="Mamikiaypuansunan Berceritera", page_icon="📜", layout="centered")

# 2. CSS Manis & Obat Ampuh Anti-Tumpuk
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    /* Font Global & Warna Latar */
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #fafaf9; }
    
    /* Judul Estetik ala Butik */
    .main-title {
        font-family: 'Playfair Display', serif;
        color: #1c1917;
        text-align: center; 
        font-size: 2.8rem !important;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    .subtitle {
        text-align: center; 
        color: #a8a29e; 
        letter-spacing: 2px;
        font-size: 0.85rem;
        margin-top: 5px;
        margin-bottom: 40px;
        text-transform: uppercase;
    }

    /* --- OBAT AMPUH UNTUK FILE UPLOADER --- */
    /* Menyembunyikan tulisan 'Drag and drop' dan 'Limit 200MB' yang bikin tumpuk */
    [data-testid="stFileUploadDropzone"] > div > div > span,
    [data-testid="stFileUploadDropzone"] > div > div > small {
        display: none !important;
    }
    /* Merapikan kotaknya agar tombol Upload pas di tengah */
    [data-testid="stFileUploadDropzone"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        border: 2px dashed #d6d3d1 !important;
        border-radius: 12px !important;
        background-color: #ffffff !important;
        padding: 30px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #1c1917 !important;
        background-color: #f5f5f5 !important;
    }

    /* Input Form yang Empuk */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        border-radius: 8px !important;
        border: 1px solid #e7e5e4 !important;
        padding: 12px !important;
        box-shadow: none !important;
        background-color: #ffffff !important;
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus, .stTextArea>div>div>textarea:focus {
        border-color: #d4af37 !important;
        box-shadow: 0 0 0 1px #d4af37 !important;
    }

    /* Tombol Utama yang Elegan */
    .stButton>button {
        background-color: #1c1917; 
        color: #ffffff; 
        border-radius: 8px; 
        padding: 14px; 
        font-weight: 600; 
        width: 100%; 
        border: 1px solid #1c1917;
        transition: all 0.3s;
        margin-top: 10px;
    }
    .stButton>button:hover { 
        background-color: #ffffff; 
        color: #1c1917; 
        border: 1px solid #d4af37;
        transform: translateY(-2px);
    }

    /* Menyembunyikan Header/Footer bawaan Streamlit */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Footer @mamikiaypuansunan yang Bersih */
    .footer-manis {
        text-align: center;
        padding: 20px;
        font-size: 13px;
        font-weight: 600;
        color: #a8a29e;
        margin-top: 60px;
        border-top: 1px solid #e7e5e4;
        letter-spacing: 1px;
    }
    
    /* Styling Card Hasil */
    .result-box {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #e7e5e4;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 3. API Setup
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Sistem membutuhkan API Key untuk mulai menenun cerita.")

# 4. Header
st.markdown("<h1 class='main-title'>Mamikiaypuansunan Berceritera</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>BEYOND ADS: WE WEAVE LEGENDS</div>", unsafe_allow_html=True)

# 5. Form Input 
st.markdown("### 📸 Visual Produk")
uploaded_file = st.file_uploader("Unggah foto mahakarya (Opsional)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Visual Terdeteksi", use_container_width=True)

st.markdown("---")
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

generate = st.button("Mulai Tenun Cerita ✨")

# 6. Logika Eksekusi
if generate:
    if not prod_name or not details:
        st.warning("Cerita tak bisa dirangkai tanpa nama dan jiwa produk.")
    else:
        with st.spinner("📜 Mamiki sedang menenun simfoni visual dan audio..."):
            try:
                image_parts = []
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    image_parts = [image]

                model = genai.GenerativeModel('gemini-2.5-flash')
                master_prompt = f"""
                Berperanlah sebagai Creative Director & Master Storyteller. Buatlah storyboard iklan {duration} rasio {format_video} untuk '{prod_name}'.
                Kategori: {category}. Model: {model_type}. Deskripsi: {details}.
                WAJIB SERTAKAN: Visual (Negative Space), Musik, SFX Taktil, dan Naskah VO puitis Bahasa Indonesia.
                Prompt teknis video harus dalam Bahasa Inggris yang sangat detail.
                """
                res = model.generate_content([master_prompt] + image_parts)
                st.balloons()
                
                st.markdown("### 🎞️ Hasil Racikan Mahakarya")
                st.markdown(f"<div class='result-box'>{res.text}</div>", unsafe_allow_html=True)
                
                _, col_btn, _ = st.columns([1, 2, 1])
                with col_btn:
                    st.download_button("Simpan Storyboard (TXT)", res.text, file_name=f"Storyboard_{prod_name}.txt", use_container_width=True)
            except Exception as e:
                st.error(f"Mesin pencerita butuh istirahat: {e}")

# 7. Footer Super Bersih
st.markdown('<div class="footer-manis">@mamikiaypuansunan</div>', unsafe_allow_html=True)