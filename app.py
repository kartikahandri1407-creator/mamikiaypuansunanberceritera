import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Konfigurasi Halaman - Royal & Boutique Experience
st.set_page_config(page_title="Mamikiaypuansunan Berceritera", page_icon="📜", layout="wide")

# 2. Custom CSS: Estetika Maksimal & Perbaikan UI Streamlit
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    /* --- Font & Background Global --- */
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #fafaf9 0%, #e7e5e4 100%); }

    /* --- Card Utama --- */
    .result-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 40px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.08);
        margin-bottom: 80px; /* Jarak ekstra agar tidak tertutup footer */
    }

    /* --- Tipografi Judul --- */
    .main-title {
        font-family: 'Playfair Display', serif;
        background: linear-gradient(90deg, #1c1917, #d4af37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700; text-align: center; font-size: 3.5rem !important;
        padding-top: 20px;
    }

    /* --- FIX: UI UPLOAD (Anti Bertumpuk) --- */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #d4af37 !important; /* Aksen emas */
        border-radius: 16px !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        padding: 30px !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #1c1917 !important;
        background-color: rgba(212, 175, 55, 0.1) !important;
    }
    /* Mematikan teks limit file yang sering menyebabkan glitch UI */
    [data-testid="stFileUploadDropzone"] small {
        display: none !important; 
    }

    /* --- FIX: UI FORM INPUT --- */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        border-radius: 12px !important;
        border: 1px solid #d6d3d1 !important;
        background-color: #ffffff !important;
        padding: 12px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus, .stTextArea>div>div>textarea:focus {
        border-color: #d4af37 !important;
        box-shadow: 0 0 0 1px #d4af37 !important;
    }

    /* --- Tombol Utama --- */
    .stButton>button {
        background: #1c1917; 
        color: #f5f5f4; 
        border-radius: 12px; 
        padding: 18px; 
        font-weight: 600; 
        width: 100%; 
        border: none;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover { 
        transform: scale(1.02); 
        background: #d4af37; 
        color: #1c1917; 
    }

    /* --- Menyembunyikan Elemen Bawaan Streamlit --- */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* --- FIX: FOOTER BARU YANG SLEEK --- */
    .mamiki-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(250, 250, 249, 0.85); /* Semi transparan */
        backdrop-filter: blur(8px);
        text-align: center;
        padding: 12px;
        font-size: 13px;
        font-weight: 600;
        color: #a8a29e;
        letter-spacing: 2px;
        border-top: 1px solid rgba(214, 211, 209, 0.5);
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# 3. API Setup
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Sistem membutuhkan API Key untuk mulai menenun cerita.")

# 4. Header Section
st.markdown("<h1 class='main-title'>Mamikiaypuansunan Berceritera</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#78716c; letter-spacing: 2px;'>BEYOND ADS: WE WEAVE LEGENDS</p><br>", unsafe_allow_html=True)

# 5. Main Content Area
with st.container():
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    
    # Membalik porsi kolom agar area isian lebih lega
    col_input, col_img = st.columns([2, 1])
    
    with col_img:
        st.markdown("##### 📸 Visual Produk")
        uploaded_file = st.file_uploader("Unggah foto produk (Opsional)", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.image(uploaded_file, caption="Produk Terdeteksi", use_container_width=True)

    with col_input:
        st.markdown("##### ✍️ Narasi Produk")
        prod_name = st.text_input("Nama Mahakarya", placeholder="Misal: Tapis Pinang Mas")
        
        c1, c2 = st.columns(2)
        with c1:
            category = st.selectbox("Klasifikasi", ["Kriya & Warisan", "Kuliner Premium", "Fashion & Lifestyle", "Beauty & Aura", "Hospitality", "Agrowisata"])
            duration = st.selectbox("Durasi", ["15 Detik", "30 Detik", "60 Detik"])
        with c2:
            format_video = st.selectbox("Format/Rasio", ["9:16 (Vertical)", "1:1 (Square)", "16:9 (Widescreen)"])
            model_type = st.selectbox("Tokoh (Model)", ["Tanpa Model", "Wanita Dewasa", "Pria Dewasa", "Anak-anak", "Lansia", "Remaja"])
            
        details = st.text_area("Jiwa Produk & Pesan Utama", placeholder="Ceritakan rahasia atau nilai seni di balik produk ini...")

    st.markdown("<br>", unsafe_allow_html=True) # Spacer sebelum tombol
    generate = st.button("Mulai Tenun Cerita ✨")
    st.markdown("</div>", unsafe_allow_html=True)

# 6. Logika Generator
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
                st.markdown(f"<div class='result-card'>{res.text}</div>", unsafe_allow_html=True)
                st.download_button("Simpan Storyboard (TXT)", res.text, file_name=f"Storyboard_{prod_name}.txt")
            except Exception as e:
                st.error(f"Mesin pencerita butuh istirahat: {e}")

# 7. Sticky Footer Baru
st.markdown('<div class="mamiki-footer">@mamikiaypuansunan</div>', unsafe_allow_html=True)