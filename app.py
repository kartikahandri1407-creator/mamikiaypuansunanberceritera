import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Mamikiaypuansunan Berceritera", page_icon="📜", layout="centered")

# 2. CSS - JURUS PAMUNGKAS UPLOADER V2 (TOTAL ANNIHILATION)
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
        margin-bottom: 30px;
        text-transform: uppercase;
    }

    /* --- JURUS PAMUNGKAS UPLOADER V2 - TOTAL ANNIHILATION --- */
    
    /* 1. Sembunyikan LABEL uploader */
    [data-testid="stFileUploader"] label {
        display: none !important;
    }
    
    /* 2. Sembunyikan SEMUA teks default di dropzone */
    [data-testid="stFileUploadDropzone"] > div > div > span,
    [data-testid="stFileUploadDropzone"] > div > div > small,
    [data-testid="stFileUploadDropzone"] div[style*="text-align: center"] {
        display: none !important;
    }
    
    /* 3. Custom tombol cantik */
    [data-testid="stFileUploadDropzone"] button {
        color: transparent !important;
        font-size: 0px !important; 
        background: linear-gradient(135deg, #ffffff 0%, #f8f5f2 100%) !important;
        border: 2px solid #d4af37 !important;
        border-radius: 12px !important;
        position: relative !important;
        height: 48px !important; 
        width: 220px !important; 
        margin: 0 auto !important;
        display: block !important;
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.15);
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploadDropzone"] button:hover {
        border-color: #b8942f !important;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.25);
        transform: translateY(-2px);
    }
    
    /* 4. Teks custom yang elegan */
    [data-testid="stFileUploadDropzone"] button::after {
        content: '📸 Pilih Mahakarya';
        font-size: 14px !important;
        color: #1c1917 !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
    }
    
    /* 5. Hilangkan input file asli */
    [data-testid="stFileUploadDropzone"] input[type="file"] {
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* --- Form Input styling --- */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        border-radius: 8px !important;
        border: 1px solid #e7e5e4 !important;
        padding: 12px !important;
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus, .stTextArea>div>div>textarea:focus {
        border-color: #d4af37 !important;
        box-shadow: 0 0 0 1px #d4af37 !important;
    }

    /* --- Tombol Generate --- */
    .stButton>button {
        background-color: #1c1917; 
        color: #ffffff; 
        border-radius: 8px; 
        font-weight: 600; 
        width: 100%; 
        border: 1px solid #1c1917;
        padding: 12px;
        margin-top: 15px;
    }
    .stButton>button:hover { 
        background-color: #ffffff; 
        color: #1c1917; 
        border: 1px solid #d4af37;
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
    
    .result-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e7e5e4;
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
st.subheader("📸 Visual Produk")
# Mengosongkan string label pertama agar tidak muncul judul bawaan Streamlit
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], help="Unggah foto mahakarya (Opsional)")

if uploaded_file:
    st.image(uploaded_file, caption="Visual Terdeteksi", use_container_width=True)

st.divider()

st.subheader("✍️ Narasi Produk")
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
        st.warning("Mohon lengkapi Nama Mahakarya dan Jiwa Produk terlebih dahulu.")
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
                
                st.subheader("🎞️ Hasil Racikan Mahakarya")
                st.markdown(f"<div class='result-box'>{res.text}</div>", unsafe_allow_html=True)
                
                st.download_button("Simpan Storyboard (TXT)", res.text, file_name=f"Storyboard_{prod_name}.txt", use_container_width=True)
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {e}")

# 7. Footer
st.markdown('<div class="footer-manis">@mamikiaypuansunan</div>', unsafe_allow_html=True)