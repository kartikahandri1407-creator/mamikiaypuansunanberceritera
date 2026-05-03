import streamlit as st
import google.generativeai as genai
from PIL import Image

# ============================================
# 1. KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="Mamikiaypuansunan Berceritera",
    page_icon="📜",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# 2. INIT SESSION STATE
# ============================================
if 'preset_loaded' not in st.session_state:
    st.session_state.preset_loaded = None
if 'last_result' not in st.session_state:
    st.session_state.last_result = None
if 'last_prod_name' not in st.session_state:
    st.session_state.last_prod_name = "project"

# ============================================
# 3. CSS PREMIUM UI
# ============================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #fafaf9; }
    
    /* Hero */
    .main-title {
        font-family: 'Playfair Display', serif;
        color: #1c1917;
        text-align: center; 
        font-size: 2.6rem !important;
        margin-bottom: 0px;
        padding-top: 8px;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    .subtitle {
        text-align: center; 
        color: #a8a29e; 
        letter-spacing: 3px;
        font-size: 0.7rem;
        margin-bottom: 6px;
        text-transform: uppercase;
        font-weight: 700;
    }
    .tagline {
        text-align: center;
        color: #78716c;
        font-size: 0.95rem;
        margin-bottom: 30px;
        font-style: italic;
    }
    
    .preset-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #57534e;
        margin-bottom: 10px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1c1917 !important; 
        color: #ffffff !important; 
        border-radius: 10px !important; 
        font-weight: 600 !important; 
        border: 1px solid #1c1917 !important;
        padding: 12px !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover { 
        background-color: #ffffff !important; 
        color: #1c1917 !important; 
        border: 1px solid #d4af37 !important;
        transform: translateY(-1px);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f5f5f4;
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 14px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .stTabs [aria-selected="true"] {
        background: #1c1917 !important;
        color: white !important;
    }
    
    /* Helper Tip Box */
    .helper-tip {
        background: #fef3c7;
        border-left: 3px solid #d4af37;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 0.85rem;
        color: #57534e;
        margin: 10px 0 18px 0;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: #ffffff;
        border-radius: 10px;
        padding: 6px;
        border: 1px dashed #e7e5e4;
    }
    
    /* Hide Streamlit branding */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .footer-manis {
        text-align: center;
        padding: 25px;
        font-size: 11px;
        font-weight: 700;
        color: #a8a29e;
        margin-top: 50px;
        border-top: 1px solid #e7e5e4;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# 4. HEADER
# ============================================
st.markdown("<div class='subtitle'>The Ultimate Creative Studio</div>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>Mamikiaypuansunan Berceritera</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>Iklan TVC sinematik untuk UMKM, dalam hitungan menit.</p>", unsafe_allow_html=True)

# ============================================
# 5. API SETUP - HARD STOP KALAU GA ADA
# ============================================
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ API Key Gemini belum di-set di Streamlit Secrets. Tambahkan GEMINI_API_KEY dulu ya.")
    st.stop()
genai.configure(api_key=api_key)

# ============================================
# 6. PRESETS - QUICK START UNTUK UMKM
# ============================================
PRESETS = {
    "🍿 Kuliner Snack": {
        "category": "Kuliner Premium",
        "tone": "Ceria (Fun/Energetic)",
        "lang": "Bahasa Indonesia Kasual",
        "location": "Dapur Modern (Clean)",
        "wardrobe": "Kasual Minimalis (Clean & Simple)",
    },
    "☕ Kopi & Minuman": {
        "category": "Kuliner Premium",
        "tone": "Premium (High-End/Elegant)",
        "lang": "Bahasa Indonesia Puitis",
        "location": "Cafe Estetik & Cozy",
        "wardrobe": "Kasual Minimalis (Clean & Simple)",
    },
    "🧺 Kriya & Tapis": {
        "category": "Kriya & Warisan",
        "tone": "Tradisional (Heritage/Warm)",
        "lang": "Bahasa Indonesia Puitis",
        "location": "Studio Minimalis (Eksklusif)",
        "wardrobe": "Tradisional Modern (Kebaya/Batik Rapi)",
    },
    "👗 Fashion Lokal": {
        "category": "Fashion & Lifestyle",
        "tone": "Modern (Minimalist/Clean)",
        "lang": "Mixed (Indoglish)",
        "location": "Studio Minimalis (Eksklusif)",
        "wardrobe": "Otomatis Sesuai Tone Iklan",
    },
    "💄 Beauty & Skincare": {
        "category": "Beauty & Aura",
        "tone": "Mewah (Luxury/Gold)",
        "lang": "English Kekinian",
        "location": "Studio Minimalis (Eksklusif)",
        "wardrobe": "Formal Elegant (Jas/Blazer/Silk)",
    },
}

st.markdown("<p class='preset-label'>⚡ Mulai Cepat — Pilih Tipe Bisnismu</p>", unsafe_allow_html=True)
preset_cols = st.columns(5)
for idx, preset_name in enumerate(PRESETS.keys()):
    with preset_cols[idx]:
        if st.button(preset_name, key=f"preset_{idx}", use_container_width=True):
            st.session_state.preset_loaded = preset_name
            st.rerun()

def get_preset_value(field, default):
    if st.session_state.preset_loaded:
        return PRESETS[st.session_state.preset_loaded].get(field, default)
    return default

if st.session_state.preset_loaded:
    pcol1, pcol2 = st.columns([4, 1])
    with pcol1:
        st.success(f"✓ Template aktif: **{st.session_state.preset_loaded}** — semua field di tab di bawah sudah disesuaikan, masih bisa diubah.")
    with pcol2:
        if st.button("✕ Reset", use_container_width=True):
            st.session_state.preset_loaded = None
            st.rerun()

st.divider()

# ============================================
# 7. TABS UNTUK ORGANIZE INPUT
# ============================================
tab1, tab2, tab3, tab4 = st.tabs(["📸 Visual", "🏷️ Produk", "🎬 Setting", "✍️ Pesan"])

# --- TAB 1: VISUAL ---
with tab1:
    st.markdown("<div class='helper-tip'>💡 Foto produk WAJIB. Foto model boleh skip — AI akan generate model lokal sesuai profil yang kamu pilih.</div>", unsafe_allow_html=True)
    
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        uploaded_file = st.file_uploader(
            "Foto Produk *", 
            type=["jpg", "jpeg", "png"],
            help="Pakai foto produk yang jernih & cahaya cukup."
        )
        if uploaded_file:
            try:
                st.image(uploaded_file, caption="✓ Produk terkunci", use_container_width=True)
            except Exception:
                st.error("File foto produk korup. Coba upload ulang.")
                uploaded_file = None
    
    with col_up2:
        uploaded_model = st.file_uploader(
            "Foto Model (opsional)", 
            type=["jpg", "jpeg", "png"],
            help="Punya talent sendiri? Upload di sini biar AI lock wajahnya."
        )
        if uploaded_model:
            try:
                st.image(uploaded_model, caption="✓ Aktor terkunci", use_container_width=True)
            except Exception:
                st.error("File foto model korup. Coba upload ulang.")
                uploaded_model = None
    
    # Talent profile (kalau ga upload model)
    if not uploaded_model:
        st.markdown("**Profil Model (kalau tidak upload foto):**")
        td1, td2, td3 = st.columns(3)
        with td1:
            talent_age = st.selectbox(
                "Rentang Usia",
                ["20-30 tahun", "30-40 tahun", "40-50 tahun", "Remaja (15-20)", "Senior (50+)"]
            )
        with td2:
            talent_gender = st.selectbox("Gender", ["Wanita", "Pria", "Tidak Spesifik"])
        with td3:
            talent_ethnicity = st.selectbox(
                "Etnis / Look",
                ["Indonesia (Lampung/Sumatera)", "Indonesia (Jawa)", "Asia Tenggara", "Pan-Asian Modern"]
            )
    else:
        talent_age = talent_gender = talent_ethnicity = None

# --- TAB 2: PRODUK ---
with tab2:
    prod_name = st.text_input(
        "Nama Produk *",
        placeholder="Misal: Keripik Pisang Sumber Rejeki"
    )
    
    c1, c2 = st.columns(2)
    with c1:
        kategori_pilihan = ["Kuliner Premium", "Kriya & Warisan", "Fashion & Lifestyle",
                            "Beauty & Aura", "Agrobisnis & Herbal", "Hospitality", "Lainnya (Ketik Manual)"]
        default_cat = get_preset_value("category", "Kuliner Premium")
        cat_idx = kategori_pilihan.index(default_cat) if default_cat in kategori_pilihan else 0
        category_select = st.selectbox("Kategori Produk", kategori_pilihan, index=cat_idx)
        category = (st.text_input("Ketik Kategori", placeholder="Contoh: Otomotif")
                    if category_select == "Lainnya (Ketik Manual)" else category_select)
        
        duration = st.selectbox(
            "Durasi Iklan",
            ["15 Detik", "30 Detik", "60 Detik"],
            help="15 dtk: IG/TikTok Story. 30 dtk: Reels. 60 dtk: YouTube/TV."
        )
    
    with c2:
        format_video = st.selectbox(
            "Format / Rasio",
            ["9:16 (Vertical)", "1:1 (Square)", "16:9 (Widescreen)"],
            help="9:16 untuk Reels/TikTok. 1:1 untuk feed IG. 16:9 untuk YouTube."
        )
        
        cta_options = ["Order via WhatsApp", "Follow Instagram", "Kunjungi Toko Fisik",
                       "Lihat Website", "Datang ke Event/Bazar"]
        cta_goal = st.selectbox(
            "Tujuan Iklan (CTA)",
            cta_options,
            help="Apa yang harus penonton lakukan setelah lihat iklan?"
        )

# --- TAB 3: SETTING ---
with tab3:
    st.markdown("**🏛️ Lokasi Syuting**")
    location_options = [
        "Studio Minimalis (Eksklusif)",
        "Dapur Modern (Clean)",
        "Cafe Estetik & Cozy",
        "Menara Siger, Lampung (Ikonik)",
        "Pantai Gigi Hiu, Lampung (Dramatis)",
        "Pantai Mutun/Sari Ringgo (Tropis)",
        "Hutan Way Kambas (Alami)",
        "Pasar Tradisional (Authentic)",
        "Rumah Adat Lampung (Heritage)",
        "Ketik Custom Lokasi (Manual)"
    ]
    default_loc = get_preset_value("location", "Studio Minimalis (Eksklusif)")
    loc_idx = location_options.index(default_loc) if default_loc in location_options else 0
    location_select = st.selectbox("Pilih Lokasi", location_options, index=loc_idx)
    location_desc = (st.text_input("Deskripsi Lokasi Spesifik",
                                    placeholder="Misal: Di depan gedung putih megah dengan tiang marmer...")
                     if location_select == "Ketik Custom Lokasi (Manual)" else location_select)
    
    st.markdown("**👔 Tata Busana (Wardrobe)**")
    wardrobe_options = ["Otomatis Sesuai Tone Iklan", "Formal Elegant (Jas/Blazer/Silk)",
                        "Tradisional Modern (Kebaya/Batik Rapi)", "Kasual Minimalis (Clean & Simple)",
                        "Streetwear Modern", "Ketik Custom Baju (Manual)"]
    default_wd = get_preset_value("wardrobe", "Otomatis Sesuai Tone Iklan")
    wd_idx = wardrobe_options.index(default_wd) if default_wd in wardrobe_options else 0
    wardrobe_select = st.selectbox("Gaya Pakaian Model", wardrobe_options, index=wd_idx)
    wardrobe_desc = (st.text_input("Deskripsi Baju Spesifik",
                                    placeholder="Misal: Seragam batik rapi warna gold, motif Lampung...")
                     if wardrobe_select == "Ketik Custom Baju (Manual)" else wardrobe_select)
    
    st.markdown("**🎨 Mood & Bahasa**")
    c3, c4 = st.columns(2)
    with c3:
        tone_options = ["Mewah (Luxury/Gold)", "Tradisional (Heritage/Warm)",
                        "Modern (Minimalist/Clean)", "Premium (High-End/Elegant)", "Ceria (Fun/Energetic)"]
        default_tone = get_preset_value("tone", "Premium (High-End/Elegant)")
        tone_idx = tone_options.index(default_tone) if default_tone in tone_options else 3
        tone_style = st.selectbox("Tone / Suasana", tone_options, index=tone_idx)
    with c4:
        lang_options = ["Bahasa Indonesia Puitis", "Bahasa Indonesia Kasual",
                        "Bahasa Indonesia Profesional", "English Kekinian", "Mixed (Indoglish)"]
        default_lang = get_preset_value("lang", "Bahasa Indonesia Puitis")
        lang_idx = lang_options.index(default_lang) if default_lang in lang_options else 0
        lang_style = st.selectbox("Gaya Bahasa VO", lang_options, index=lang_idx)

# --- TAB 4: PESAN ---
with tab4:
    st.markdown("<div class='helper-tip'>💡 Ceritakan apa yang bikin produkmu spesial. Semakin detail, semakin tajam hasilnya.</div>", unsafe_allow_html=True)
    
    details = st.text_area(
        "Cerita & Keunggulan Produk *",
        placeholder="Misal: Keripik pisang ini dibuat dari pisang kepok pilihan dari petani lokal Lampung Selatan. Digoreng dengan minyak kelapa premium, renyah tahan 3 bulan tanpa pengawet. Bumbu rahasia turun-temurun dari nenek pendiri usaha...",
        height=160,
        max_chars=500
    )
    char_count = len(details) if details else 0
    st.caption(f"📝 {char_count}/500 karakter")
    
    music_mood = st.selectbox(
        "Mood Musik",
        ["Otomatis (sesuai tone)", "Akustik Hangat", "Cinematic Orchestral",
         "Upbeat Modern Pop", "Tradisional Lampung", "Minimalis Piano", "Lo-fi Chill"],
        help="Pilih kalau punya preferensi spesifik. Default: AI yang pilih sesuai tone."
    )

st.divider()

# ============================================
# 8. GENERATE BUTTON
# ============================================
generate = st.button("✨ Mulai Tenun Cerita", use_container_width=True, type="primary")

# ============================================
# 9. LOGIKA EKSEKUSI
# ============================================
if generate:
    # Validasi
    if not uploaded_file:
        st.error("🚨 Foto Produk wajib diunggah! Cek tab **Visual**.")
        st.stop()
    if not prod_name or not details:
        st.warning("🚨 Lengkapi **Nama Produk** (tab Produk) & **Cerita Produk** (tab Pesan) dulu ya!")
        st.stop()
    
    # Dynamic Scene Config (FIX BUG: scene count mengikuti durasi)
    scene_config = {
        "15 Detik": {"count": 3, "per_scene": "5 detik"},
        "30 Detik": {"count": 5, "per_scene": "6 detik"},
        "60 Detik": {"count": 6, "per_scene": "10 detik"},
    }
    cfg = scene_config[duration]
    scene_count = cfg["count"]
    scene_dur = cfg["per_scene"]
    
    # Talent Description
    if uploaded_model:
        talent_desc = "Gunakan profil wajah dari Gambar 2 (foto model). Pertahankan identitas wajah konsisten di semua scene."
    else:
        talent_desc = (f"Buat profil model: {talent_gender}, usia {talent_age}, look {talent_ethnicity}. "
                       "Pertahankan identitas wajah yang sama PERSIS di semua scene.")
    
    with st.spinner(f"📜 Menyusun {scene_count} scene mahakarya di {location_desc}..."):
        try:
            # Aspect ratio
            ar_param = "--ar 9:16"
            if "1:1" in format_video:
                ar_param = "--ar 1:1"
            elif "16:9" in format_video:
                ar_param = "--ar 16:9"
            
            image_parts = [Image.open(uploaded_file)]
            if uploaded_model:
                image_parts.append(Image.open(uploaded_model))
            
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Build dynamic scene template berdasarkan jumlah scene
            scene_blocks = []
            for i in range(1, scene_count + 1):
                if i == 1:
                    scene_role = "OPENING HOOK — Tarik perhatian dalam 1 detik pertama"
                elif i == scene_count:
                    scene_role = f"KLIMAKS & CTA — Tampilkan produk + ajak audiens '{cta_goal}'"
                elif i == scene_count - 1:
                    scene_role = "PUNCAK EMOSI — Tunjukkan keunggulan/manfaat utama produk"
                else:
                    scene_role = "BUILD UP — Bangun cerita & desire"
                
                scene_blocks.append(f"""
## 🎬 SCENE {i}: [Nama Scene] ({scene_dur})
**🎯 Peran Scene:** {scene_role}
**👁️ DESKRIPSI VISUAL:** [Setting di {location_desc}, kostum {wardrobe_desc}, sinematografi gaya Arri Alexa]
**📸 PROMPT GAMBAR:** ```text
[Cinematic shot, EXACT product from reference, Setting: {location_desc}, Wardrobe: {wardrobe_desc}, lighting & mood] {ar_param} --v 6.0
```
**🎥 PROMPT VIDEO:** ```text
[Camera movement, action, Setting: {location_desc}, Wardrobe details, Product placement, duration {scene_dur}]
```
**🎙️ ELEMEN AUDIO:**
- VO ({lang_style}): "[Kalimat voice over yang nyambung dengan scene sebelum & sesudah]"
- SFX: [Sound effect spesifik]
- Musik: [Mood musik — HARUS konsisten dengan scene lain]
""")
            
            scene_template = "\n---\n".join(scene_blocks)
            
            # MASTER PROMPT
            master_prompt = f"""
Anda adalah Sutradara TVC & Creative Director High-End yang spesialis branding UMKM Indonesia.
Tugas: Buat storyboard iklan TVC sinematik {duration} ({scene_count} scene) rasio {format_video} untuk produk '{prod_name}'.

=== BRIEF ===
- KATEGORI: {category}
- TONE: {tone_style}
- LOKASI: {location_desc}
- WARDROBE: {wardrobe_desc}
- BAHASA VO: {lang_style}
- MOOD MUSIK: {music_mood}
- CTA: {cta_goal}
- CERITA & KEUNGGULAN PRODUK: {details}

=== TALENT ===
{talent_desc}

=== ATURAN WAJIB (NON-NEGOTIABLE) ===
1. **KONSISTENSI LOKASI:** Semua {scene_count} scene WAJIB di '{location_desc}'. Variasi sudut kamera & komposisi, BUKAN ganti lokasi.
2. **KONSISTENSI TALENT:** Wajah & pakaian model HARUS sama di semua scene.
3. **KONSISTENSI VO (PENTING):** Voice over di setiap scene harus mengalir jadi 1 narasi utuh — kalimat scene 1 menyambung ke scene 2, dst. Bukan VO terpisah-pisah, tapi 1 cerita yang dipotong per scene. Tone & gaya bahasa harus konsisten dari awal sampai akhir.
4. **KONSISTENSI MUSIK (PENTING):** Mood musik bertahan SAMA dari scene 1 sampai scene {scene_count}. Boleh build-up dinamika (intro → klimaks), tapi DNA musik tetap satu (genre, instrumen utama, tempo).
5. **CTA EKSPLISIT:** Scene terakhir WAJIB ada visual + VO yang mengajak '{cta_goal}'. Tampilkan elemen visual jelas (logo WhatsApp, handle IG, alamat, dll).
6. **ANTI-HALU PRODUK:** Bentuk, warna, tekstur, kemasan produk WAJIB IDENTIK dengan Gambar 1 referensi. Jangan bikin variasi/imajinasi produk.
7. **BAHASA UMKM-FRIENDLY:** Pesan iklan harus relate ke audiens lokal/Indonesia, jangan terlalu corporate/jargon. Tetap elegan, tapi grounded.

=== FORMAT OUTPUT (IKUTI PERSIS) ===

## 🎯 BIG IDEA & TAGLINE
- **Big Idea:** [Konsep utama dalam 1 kalimat]
- **Tagline:** [Tagline catchy max 7 kata]

## 🔍 PRODUCTION PLAN
- **Analisis Produk:** [Detail fisik dari foto referensi]
- **Location & Mood:** [Bagaimana {location_desc} dipakai sinematik]
- **Master Wardrobe & Talent:** [Deskripsi yang konsisten lintas scene]
- **Color Palette:** [3-5 warna dominan + hex code, contoh #1c1917]
- **🎵 Music & VO Continuity:** [Penjelasan benang merah audio dari scene 1 sampai {scene_count}: bagaimana musik berkembang & bagaimana VO mengalir jadi 1 narasi]

---
{scene_template}

---
## 📱 CAMPAIGN KIT

### Caption Instagram/TikTok
[Caption lengkap dengan hook (1-2 baris pertama harus menjebak), body, CTA, max 150 kata]

### Hashtag Strategy
[10-15 hashtag mix: branded (nama produk) + kategori + lokal Lampung/Indonesia. Pisah jadi tier: high-volume, mid-volume, niche]

### 🎙️ Voice Over Script (Final — Untuk Talent)
[Compile semua VO dari scene 1 sampai {scene_count} jadi 1 script bersih tanpa direction visual. Format: per baris dengan timing. Siap rekam.]

### 💰 Tips Produksi Hemat untuk UMKM
[3 tips eksekusi murah meriah — kreatif, tapi ga butuh budget agency]
"""
            
            res = model.generate_content([master_prompt] + image_parts)
            st.session_state.last_result = res.text
            st.session_state.last_prod_name = prod_name
            st.balloons()
            
        except Exception as e:
            st.error(f"⚠️ Kendala teknis: {e}")
            st.stop()

# ============================================
# 10. DISPLAY HASIL (PERSIST VIA SESSION STATE)
# ============================================
if st.session_state.last_result:
    st.divider()
    st.markdown(st.session_state.last_result)
    st.divider()
    
    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button(
            "💾 Simpan Proposal (.MD)",
            st.session_state.last_result,
            file_name=f"TVC_Proposal_{st.session_state.last_prod_name}.md",
            use_container_width=True
        )
    with dl2:
        if st.button("🔄 Mulai Project Baru", use_container_width=True):
            st.session_state.last_result = None
            st.session_state.preset_loaded = None
            st.rerun()

# ============================================
# 11. FOOTER
# ============================================
st.markdown('<div class="footer-manis">@mamikiaypuansunan · Crafted with ❤️ for UMKM</div>', unsafe_allow_html=True)