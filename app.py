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
st.markdown("<div class='subtitle'>DIRECTOR'S CUT & CASTING AGENCY</div>", unsafe_allow_html=True)

# 5. Form Input
st.markdown("### 📸 Visual Referensi")

# DUA KOLOM UPLOAD
col_up1, col_up2 = st.columns(2)
with col_up1:
    uploaded_file = st.file_uploader("1. Foto Produk (WAJIB)", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Produk Terkunci", use_container_width=True)

with col_up2:
    uploaded_model = st.file_uploader("2. Foto Model (OPSIONAL)", type=["jpg", "jpeg", "png"])
    if uploaded_model:
        st.image(uploaded_model, caption="Aktor Terkunci", use_container_width=True)

st.divider()

st.markdown("### ✍️ Narasi & Gaya")
prod_name = st.text_input("Nama Mahakarya", placeholder="Misal: Keripik Pisang KWT Sumber Rejeki II")

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
    
    # Logika Cerdas: Jika user upload foto model, otomatis pilih "Pakai Model Sendiri"
    if uploaded_model:
        model_type = st.selectbox("Tokoh (Model)", ["Menggunakan Referensi Foto Model Terunggah"])
    else:
        model_type = st.selectbox("Tokoh (Model)", ["Tanpa Model", "Wanita Dewasa", "Pria Dewasa", "Anak-anak", "Lansia"])

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
    if not uploaded_file:
        st.error("🚨 Mohon unggah Foto Produk terlebih dahulu! Gambar ini wajib sebagai panduan mutlak AI.")
    elif not prod_name or not details:
        st.warning("🚨 Mohon lengkapi Nama Mahakarya dan Jiwa Produk.")
    elif category_select == "Lainnya (Ketik Manual)" and not category:
        st.warning("🚨 Mohon ketikkan Kategori Spesifik produk Anda.")
    else:
        with st.spinner(f"📜 Menyusun Mahakarya TVC & Social Media Kit untuk {category}..."):
            try:
                ar_param = "--ar 9:16"
                if "1:1" in format_video:
                    ar_param = "--ar 1:1"
                elif "16:9" in format_video:
                    ar_param = "--ar 16:9"

                # Siapkan Part Gambar untuk Gemini
                image_parts = [Image.open(uploaded_file)]
                
                # Instruksi dinamis jika ada foto model
                model_instruction = """
                - KONTINUITAS AKTOR/MODEL: Jika menggunakan model, tetapkan profil fisik yang SANGAT SPESIFIK (misal: "A 30-year-old Asian woman wearing an elegant minimalist white silk blouse"). Salin deskripsi ini di setiap prompt Gambar dan Video.
                """
                if uploaded_model:
                    image_parts.append(Image.open(uploaded_model))
                    model_instruction = """
                    - KONTINUITAS AKTOR/MODEL (WAJIB): Terdapat DUA gambar referensi yang diunggah. Gambar pertama adalah PRODUK. Gambar kedua adalah WAJAH DAN FISIK MODEL. Analisis dengan presisi fitur wajah, rambut, dan pakaian model dari gambar kedua. Gunakan deskripsi akurat model ini di SEMUA scene. Pada prompt Midjourney, WAJIB tambahkan instruksi `[INSERT MODEL IMAGE URL] --cref [INSERT MODEL IMAGE URL] --cw 100` di akhir prompt. Pada prompt Kling/Video, tulis "Character must perfectly match the uploaded facial reference image."
                    """

                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # --- PROMPT VERSION: ULTIMATE DIRECTOR + CASTING ---
                master_prompt = f"""
                Anda adalah Sutradara Iklan TV Komersial Kelas Dunia (sekelas sutradara iklan Apple, otomotif mewah) & Copywriter Elite.
                Tugas: Buat storyboard iklan TV {duration} rasio {format_video} untuk mahakarya '{prod_name}'.
                
                KATEGORI: {category}.
                GAYA VISUAL: {tone_style}. 
                GAYA BAHASA: {lang_style}.
                TIPE MODEL: {model_type}.

                ATURAN SINEMATOGRAFI KELAS DUNIA:
                - Visual "Iklan Mahal": Seluruh scene HARUS memancarkan aura iklan berbiaya miliaran rupiah.
                - Kamera & Lighting: Di prompt bahasa Inggris, WAJIB gunakan istilah ("Shot on Arri Alexa 65", "Phantom Flex 4k", "Laowa Probe Lens", "cinematic chiaroscuro").
                
                ATURAN KONTINUITAS VISUAL & AUDIO (SANGAT PENTING):
                {model_instruction}
                - KONTINUITAS VO: Tetapkan SATU karakter suara eksplisit (misal: "VO: Suara Pria Dewasa, berwibawa"). Jangan biarkan suaranya berubah-ubah.
                - KONTINUITAS MUSIK: Musik dari Scene 1 sampai akhir HARUS berupa SATU lagu yang utuh. Gunakan genre dan instrumen yang sama di setiap scene, hanya ubah dinamikanya (Intro, Build-up, Klimaks).

                ATURAN HARGA MATI (ANTI-HALU GAMBAR PRODUK):
                1. BENTUK FISIK: Deskripsikan bentuk asli produk (Gambar Pertama) dengan presisi. JANGAN MENGARANG bentuk.
                2. BRANDING: Replikasi 100% detail teks, warna, dan logo pada kemasan.
                3. KONSISTENSI PRODUK: Di setiap prompt Inggris, WAJIB sertakan: "Product exactly matching the provided reference image".

                FORMAT OUTPUT (WAJIB GUNAKAN MARKDOWN INI SEBAGAIMANA ADANYA):
                
                ## 🔍 ANALISIS VISUAL REFERENSI & KONTINUITAS
                - **Analisis Produk:** [Detail akurat fisik produk dan kemasan]
                - **Profil Model Kontinu:** [Detail analisis fisik dari gambar model kedua yang diunggah ATAU deskripsi fisik karangan jika tidak ada gambar model. Tulis "Fokus Produk" jika tanpa model]

                ---
                ## 🎬 SCENE 1: [Nama Scene] (5 detik)
                **👁️ DESKRIPSI VISUAL:** [Komposisi sinematik]

                **📸 PROMPT GAMBAR:**
                ```text
                [Cinematic photography. High-end lighting terms. EXACT physical shape & branding. INCLUDE Profil Model Kontinu jika ada. INCLUDE "Product exactly matching the provided reference image". Jika ada model referensi, tambahkan: --cref [URL_GAMBAR_MODEL] --cw 100] {ar_param} --style raw --v 6.0
                ```

                **🎥 PROMPT VIDEO:**
                ```text
                [EXACT product shape + Profil Model Kontinu jika ada + High-end Camera Angle. INCLUDE "Product and packaging must be identical to the uploaded reference image."]
                ```

                **🎙️ ELEMEN AUDIO:** [Karakter VO eksplisit] - "[Naskah kelas atas]" & [SFX/Musik taktil]
                
                **🎵 PROMPT MUSIK AI:**
                ```text
                [Genre, tempo, mood. Establish the core instrumentation here.]
                ```

                ---
                ## 🎬 SCENE 2: [Nama Scene] (5 detik)
                [Lanjutkan format scene. WAJIB ulangi deskripsi baju/fisik model. Teruskan instrumen musik yang sama.]

                ---
                ## 🎬 SCENE 3: [Nama Scene] (5 detik)
                [Lanjutkan format scene. WAJIB ulangi deskripsi baju/fisik model. Buat klimaks musik dari instrumen Scene 1.]

                ---
                ## 📱 CAMPAIGN KIT & SOCIAL MEDIA
                - **Caption Media Sosial:** "[Buat caption yang menjual dan elegan sesuai {lang_style}]"
                - **Hashtags Premium:** "[5 Hashtag]"
                """
                
                res = model.generate_content([master_prompt] + image_parts)
                st.balloons()
                
                st.markdown(f"### 🎞️ Mahakarya Selesai: {tone_style} | {lang_style}")
                
                # Tampilkan HasiL Full (Anti Terpotong)
                st.markdown(res.text)
                
                # Tombol Download di bawah
                st.divider()
                st.download_button("Simpan Proposal (.MD)", res.text, file_name=f"Director_Treatment_{prod_name}.md", use_container_width=True)
            
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {e}")

# 7. Footer
st.markdown('<div class="footer-manis">@mamikiaypuansunan</div>', unsafe_allow_html=True)