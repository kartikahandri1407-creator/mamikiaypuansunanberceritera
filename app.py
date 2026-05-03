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
    .helper-tip {
        background: #fef3c7;
        border-left: 3px solid #d4af37;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 0.85rem;
        color: #57534e;
        margin: 10px 0 18px 0;
    }
    [data-testid="stFileUploader"] {
        background: #ffffff;
        border-radius: 10px;
        padding: 6px;
        border: 1px dashed #e7e5e4;
    }
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
# 5. API SETUP
# ============================================
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ API Key Gemini belum di-set di Streamlit Secrets. Tambahkan GEMINI_API_KEY dulu ya.")
    st.stop()
genai.configure(api_key=api_key)

# ============================================
# 6. PRESETS
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
        st.success(f"✓ Template aktif: **{st.session_state.preset_loaded}** — semua field sudah disesuaikan, masih bisa diubah.")
    with pcol2:
        if st.button("✕ Reset", use_container_width=True):
            st.session_state.preset_loaded = None
            st.rerun()

st.divider()

# ============================================
# 7. TABS INPUT
# ============================================
tab1, tab2, tab3, tab4 = st.tabs(["📸 Visual", "🏷️ Produk", "🎬 Setting", "✍️ Pesan"])

# --- TAB 1: VISUAL ---
with tab1:
    st.markdown("<div class='helper-tip'>💡 Foto produk WAJIB. Foto model boleh skip — AI akan generate model lokal sesuai profil yang kamu pilih.</div>", unsafe_allow_html=True)
    
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        uploaded_file = st.file_uploader(
            "Foto Produk * (Image 1)", 
            type=["jpg", "jpeg", "png"],
            help="Pakai foto produk yang jernih & cahaya cukup."
        )
        if uploaded_file:
            try:
                st.image(uploaded_file, caption="✓ Image 1 — Produk terkunci", use_container_width=True)
            except Exception:
                st.error("File foto produk korup. Coba upload ulang.")
                uploaded_file = None
    
    with col_up2:
        uploaded_model = st.file_uploader(
            "Foto Model (opsional) (Image 2)", 
            type=["jpg", "jpeg", "png"],
            help="Punya talent sendiri? Upload di sini biar AI lock wajahnya."
        )
        if uploaded_model:
            try:
                st.image(uploaded_model, caption="✓ Image 2 — Aktor terkunci", use_container_width=True)
            except Exception:
                st.error("File foto model korup. Coba upload ulang.")
                uploaded_model = None
    
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

    # Quality meter
    if char_count == 0:
        st.caption("📝 0/500 karakter")
    elif char_count < 50:
        st.error(f"📝 {char_count}/500 — Terlalu singkat. AI butuh minimal 50 karakter untuk output berkualitas.")
    elif char_count < 150:
        st.warning(f"📝 {char_count}/500 — Lumayan. Semakin detail, semakin sinematik hasilnya.")
    else:
        st.success(f"📝 {char_count}/500 — Bagus! Detail ini cukup untuk output kelas atas.")
    
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
    if char_count < 50:
        st.error("🚨 Cerita produk terlalu singkat. Tambahkan detail dulu (min. 50 karakter).")
        st.stop()

    # Dynamic Scene Config
    scene_config = {
        "15 Detik": {"count": 3, "per_scene": "5 detik"},
        "30 Detik": {"count": 5, "per_scene": "6 detik"},
        "60 Detik": {"count": 6, "per_scene": "10 detik"},
    }
    cfg = scene_config[duration]
    scene_count = cfg["count"]
    scene_dur = cfg["per_scene"]

    # Aspect ratio
    ar_param = "--ar 9:16"
    if "1:1" in format_video:
        ar_param = "--ar 1:1"
    elif "16:9" in format_video:
        ar_param = "--ar 16:9"

    ar_ratio = ar_param.replace("--ar ", "")

    # -------------------------------------------------------
    # WARDROBE SYSTEM — Deskripsi fisik super eksplisit
    # + CLOTHING OVERRIDE BLOCK wajib disuntik ke tiap prompt
    # -------------------------------------------------------

    WARDROBE_EXPLICIT_MAP = {
        "Kasual Minimalis (Clean & Simple)": (
            "plain white V-neck short-sleeve cotton t-shirt — COMPLETELY BLANK, "
            "NO text, NO logo, NO brand name, NO print, NO graphic of any kind on the shirt "
            "— paired with plain dark navy blue straight-fit jeans, no belt, no accessories"
        ),
        "Formal Elegant (Jas/Blazer/Silk)": (
            "slim-fit charcoal blazer over a crisp white dress shirt with top button open, no tie, "
            "dark tailored trousers, simple silver watch on left wrist — no other accessories"
        ),
        "Tradisional Modern (Kebaya/Batik Rapi)": (
            "neat modern batik shirt in warm earth-tone colors (brown/ochre/forest green), "
            "well-fitted and pressed, paired with dark formal trousers — clean and dignified"
        ),
        "Streetwear Modern": (
            "oversized solid-color crew neck sweatshirt in muted tone (sage/stone/slate), "
            "NO logo NO text NO graphic print anywhere on the fabric, "
            "paired with slim dark jogger pants and clean white sneakers"
        ),
    }

    WARDROBE_AUTO_MAP = {
        "Mewah (Luxury/Gold)": (
            "elegant silk blouse or well-fitted blazer in cream or soft gold tones, "
            "minimal jewelry — one simple necklace or earring only, no heavy accessories, "
            "NO text NO logo NO brand name on any garment"
        ),
        "Tradisional (Heritage/Warm)": (
            "neat modern kebaya or batik outfit in warm earth tones with traditional Lampung accent details, "
            "well-pressed and dignified, minimal modern accessories, "
            "NO text NO logo NO brand name on any garment"
        ),
        "Modern (Minimalist/Clean)": (
            "plain linen short-sleeve shirt in off-white or light beige, sleeves rolled neatly to elbow, "
            "NO text NO logo NO print of any kind, paired with khaki or light gray chino pants"
        ),
        "Premium (High-End/Elegant)": (
            "slim-fit blazer in charcoal or navy over a clean white shirt with top button open, "
            "no tie, minimal silver accessories, dark tailored trousers, "
            "NO text NO logo NO brand name on any garment"
        ),
        "Ceria (Fun/Energetic)": (
            "solid-color casual t-shirt in mustard yellow or coral or white — "
            "NO text NO logo NO print of any kind anywhere on the fabric, "
            "paired with clean chino pants or jogger in neutral tone"
        ),
    }

    if wardrobe_desc == "Otomatis Sesuai Tone Iklan":
        wardrobe_for_prompt = WARDROBE_AUTO_MAP.get(
            tone_style,
            "clean plain casual outfit — NO text NO logo NO brand name anywhere on clothing"
        )
        wardrobe_label = f"Auto ({tone_style}): {wardrobe_for_prompt}"
    elif wardrobe_desc in WARDROBE_EXPLICIT_MAP:
        wardrobe_for_prompt = WARDROBE_EXPLICIT_MAP[wardrobe_desc]
        wardrobe_label = wardrobe_desc
    else:
        wardrobe_for_prompt = (
            wardrobe_desc
            + " — CRITICAL: NO visible brand text, logo, or print on clothing unless explicitly described above"
        )
        wardrobe_label = wardrobe_desc

    # CLOTHING OVERRIDE BLOCK — disuntik ke SETIAP prompt gambar & video
    # Ini yang menyelesaikan masalah logo "AIRY" dari foto referensi
    CLOTHING_OVERRIDE = (
        "CLOTHING OVERRIDE — HIGHEST PRIORITY, OVERRIDES ALL REFERENCE IMAGES: "
        "The clothing in the OUTPUT must exactly match this description: {wardrobe}. "
        "The character reference photo (Image 2) may show a shirt with text, logo, or brand name (e.g. 'AIRY') — "
        "COMPLETELY IGNORE and ERASE any text, logo, brand name, or print visible on the clothing in the reference photo. "
        "Image 2 is used for FACE, SKIN TONE, HAIR, and BODY PROPORTIONS ONLY — NOT for clothing. "
        "Generate the exact wardrobe described above. The shirt must be 100% blank solid color with zero text or logo."
    ).format(wardrobe=wardrobe_for_prompt)

    # -------------------------------------------------------
    # TALENT ANCHOR — termasuk clothing override
    # -------------------------------------------------------
    if uploaded_model:
        talent_anchor = (
            "FACE & BODY: Use Image 2 as character reference (--cref in Midjourney / Character Reference in Flux/Kling). "
            "EXACT same face features, skin tone, hair color/style, facial hair, and body build as Image 2 in every scene. "
            f"{CLOTHING_OVERRIDE}"
        )
        talent_label_line = "📷 **Image 1** (produk) + 📷 **Image 2** (model/wajah talent) — keduanya WAJIB disertakan"
        image_ref_instruction = (
            "UNTUK AI IMAGE/VIDEO TOOLS: "
            "Image 1 = product reference (kemasan, warna, label). "
            "Image 2 = character reference untuk WAJAH & FISIK SAJA — bukan baju. "
            "Gunakan --cref (Midjourney) atau Character Reference (Flux/Kling). "
            "WAJAH talent HARUS IDENTIK Image 2 di semua scene. "
            "ABAIKAN dan HAPUS tulisan/logo pada baju di Image 2 — ikuti deskripsi wardrobe di atas."
        )
    else:
        talent_anchor = (
            f"GENERATE CONSISTENT TALENT: {talent_gender}, usia {talent_age}, etnis {talent_ethnicity}, "
            "natural Indonesian features, warm authentic expression, same face across ALL scenes. "
            f"{CLOTHING_OVERRIDE}"
        )
        talent_label_line = "📷 **Image 1** (produk) — wajib disertakan | Model: AI-generated (wajah konsisten lintas scene)"
        image_ref_instruction = (
            "UNTUK AI IMAGE/VIDEO TOOLS: "
            "Image 1 = product reference. "
            "Untuk konsistensi wajah: gunakan seed yang sama, 'Consistent Character', atau --sref di Midjourney. "
            "Wajah model HARUS IDENTIK di semua scene."
        )

    # -------------------------------------------------------
    # COLOR GRADE per tone
    # -------------------------------------------------------
    COLOR_GRADE_MAP = {
        "Mewah (Luxury/Gold)":         "warm gold-teal split tone, rich shadows, luminous highlights — Johnnie Walker luxury commercial grade",
        "Tradisional (Heritage/Warm)": "warm amber-brown grade, slightly desaturated, subtle film grain — heritage documentary warmth",
        "Modern (Minimalist/Clean)":   "clean neutral grade, soft contrast, slightly cool highlights — high-end lifestyle magazine editorial",
        "Premium (High-End/Elegant)":  "warm teal-orange complementary grade, deep blacks, glowing skin tones — Nescafé Asia series grade",
        "Ceria (Fun/Energetic)":       "bright punchy grade, warm saturation boost, clean whites — modern Southeast Asian food commercial energy",
    }
    color_grade = COLOR_GRADE_MAP.get(tone_style, "warm cinematic grade, Arri Alexa color science")

    # -------------------------------------------------------
    # CINEMATIC REFERENCE per tone — anchor kualitas sutradara
    # -------------------------------------------------------
    CINEMATIC_REF_MAP = {
        "Mewah (Luxury/Gold)":         "Cinematography reference: Roger Deakins. Ad reference: Johnnie Walker 'The Man Who Walked Around The World'. Every frame must feel like it costs a million dollars.",
        "Tradisional (Heritage/Warm)": "Cinematography reference: Wong Kar-wai warmth, Uberto Pasolini stillness. Ad reference: AQUA Indonesia 'Perjalanan'. Frames that make you miss a place you've never been.",
        "Modern (Minimalist/Clean)":   "Cinematography reference: Emmanuel Lubezki. Ad reference: Apple 'Shot on iPhone' series. Clean, elegant, the silence between sentences.",
        "Premium (High-End/Elegant)":  "Cinematography reference: Wally Pfister. Ad reference: Nescafé Asia regional series. The feeling of premium without saying premium.",
        "Ceria (Fun/Energetic)":       "Cinematography reference: Thai commercial school — warm, kinetic, human. Ad reference: Indomie 'Sahabat', Walls Thailand. Joy that feels real, not performed.",
    }
    cinematic_ref = CINEMATIC_REF_MAP.get(tone_style, "Cinematography reference: Arri Alexa, professional commercial grade.")

    # -------------------------------------------------------
    # SCENE NAMES — dikunci per tone & posisi, bukan diserahkan ke AI
    # -------------------------------------------------------
    SCENE_NAMES = {
        "Mewah (Luxury/Gold)":         {1: "DIAM SEBELUM EMAS", 2: "SENTUHAN PERTAMA", 3: "TIDAK ADA KATA LAIN", 4: "DUNIA YANG BERHENTI", 5: "INI MILIKMU", 6: "WARISAN RASA"},
        "Tradisional (Heritage/Warm)": {1: "SEBELUM SEGALANYA", 2: "TANGAN YANG TAHU", 3: "PULANG", 4: "AKAR YANG BERBICARA", 5: "DITURUNKAN", 6: "ABADI"},
        "Modern (Minimalist/Clean)":   {1: "RUANG UNTUK BERNAPAS", 2: "MOMEN ITU", 3: "CUKUP", 4: "DETAIL YANG JUJUR", 5: "PILIHAN YANG TEPAT", 6: "HIDUP YANG DIPILIH"},
        "Premium (High-End/Elegant)":  {1: "SEBELUM SEGALANYA", 2: "SAAT ITU TERJADI", 3: "TIDAK ADA KATA LAIN", 4: "YANG TERSISA", 5: "MILIK MEREKA YANG TAHU", 6: "SELALU"},
        "Ceria (Fun/Energetic)":       {1: "DETIK YANG DITUNGGU", 2: "LEDAKAN KECIL", 3: "MOMEN ITU", 4: "LAGI", 5: "BERBAGI", 6: "HARI INI MILIKMU"},
    }
    scene_name_map = SCENE_NAMES.get(tone_style, {i: f"SCENE {i}" for i in range(1, 7)})

    # -------------------------------------------------------
    # FOCAL LENGTH per scene
    # -------------------------------------------------------
    FOCAL_MAP = {
        1: ("35mm", "wide enough to breathe — talent belongs to the world, not posed in it"),
        2: ("85mm", "compression pulls viewer in — background melts, face fills emotional space"),
        3: ("50mm", "natural human perspective — honest, warm, real"),
        4: ("100mm macro", "extreme intimacy — texture of product, micro-expression of soul"),
        5: ("85mm", "quiet confidence — talent looks inward, viewer looks with them"),
        6: ("35mm", "pull back to show the world — product in context, story complete"),
    }

    # -------------------------------------------------------
    # CINEMATIC CAMERA NOTES per scene — momen, bukan deskripsi posisi
    # -------------------------------------------------------
    def build_camera_note(scene_num, location, tone):
        notes = {
            1: (
                f"OPENING FRAME: Start extreme tight — a detail only (steam from cup, edge of table, shadow on wall). "
                f"MOVEMENT: Imperceptibly slow pull-back on 35mm, so slow the viewer feels they're discovering the scene, not watching it. "
                f"BEAT (2s in): Talent already present, mid-action — never posed, never waiting for camera. "
                f"CLOSING FRAME: Talent + {location} established. Product visible but not featured. "
                f"EMOTIONAL TARGET: The viewer recognizes this moment from their own life before they understand what they're watching."
            ),
            2: (
                f"OPENING FRAME: Tight on the product — packaging detail, texture, light catching an edge. 85mm. "
                f"MOVEMENT: Slow drift upward or sideways from product to talent's hands, then to face. "
                f"THE BEAT (hold 2 full seconds): The micro-expression — NOT a big smile. Eyes soften. "
                f"Shoulders drop 2mm. The exhale that means 'I needed this.' "
                f"CLOSING FRAME: Face in focus, product softly visible in foreground. "
                f"EMOTIONAL TARGET: The release. This is the Signature Moment. Every other scene builds to this."
            ),
            3: (
                f"OPENING FRAME: 50mm static — talent slightly off-center, rule of thirds. "
                f"MOVEMENT: Almost none. A slight settle. The stillness IS the emotion. "
                f"CLOSING FRAME: Same as opening, but something has shifted — lighter. "
                f"EMOTIONAL TARGET: The afterglow. The viewer wants to be this person right now."
            ),
            4: (
                f"OPENING FRAME: 100mm macro — product texture fills frame. Light at 45°. "
                f"MOVEMENT: Rack focus from product surface to talent's eyes in one fluid breath. "
                f"BEAT: Hold on eyes for 1.5 seconds — the look of someone who has found something worth keeping. "
                f"CLOSING FRAME: Eyes and product both in soft focus together. "
                f"EMOTIONAL TARGET: Intimacy between person and product that feels earned, not staged."
            ),
            5: (
                f"OPENING FRAME: 85mm medium — talent faces camera with quiet presence. "
                f"MOVEMENT: Very slow pull-back reveals {location} around them — world expanding. "
                f"Product appears naturally in the frame — in hand, on table, never held for camera. "
                f"CLOSING FRAME: Talent + full world. Complete. "
                f"EMOTIONAL TARGET: Desire. The viewer wants this life."
            ),
            6: (
                f"OPENING FRAME: Close on product label — sharp, proud, specific. "
                f"MOVEMENT: 35mm pull-out to full scene at {location}. "
                f"CTA fades in at bottom — minimal, confident, one line only. "
                f"CLOSING FRAME: The world this product belongs to. "
                f"EMOTIONAL TARGET: The last frame must feel like the final page of a beautiful story, not an advertisement."
            ),
        }
        return notes.get(scene_num, f"Cinematic shot appropriate to scene {scene_num} energy and tone.")

    # -------------------------------------------------------
    # VO FORBIDDEN WORDS + ANCHOR EXAMPLES
    # -------------------------------------------------------
    VO_FORBIDDEN = (
        "ABSOLUTELY FORBIDDEN IN VO — do not use any of these words or concepts: "
        "harga, murah, mahal, terjangkau, hemat, diskon, promo, renyah, gurih, enak, lezat, crispy, crunchy, "
        "tekstur, rasa (sebagai deskripsi fisik), beli, order, dapatkan, stok, tersedia. "
        "VO is POETRY ABOUT HUMAN MOMENTS, not product description. "
        "If a word describes the physical property of the product, REMOVE IT. "
        "A good VO test: read it aloud without any image — it must still feel meaningful and beautiful."
    )

    # Contoh VO iklan TV mahal Asia nyata — anchor jiwa untuk Gemini
    # Ini yang membedakan output 'konten' vs output 'iklan ratusan juta'
    VO_ANCHOR_EXAMPLES = f"""
=== CONTOH VO IKLAN TV MAHAL ASIA — INI STANDAR YANG HARUS DICAPAI ===

CONTOH 1 — AQUA Indonesia (heritage/emotional):
"Ada perjalanan yang tidak tercatat di peta.
Yang hanya bisa dirasakan oleh mereka yang pernah sampai di sana.
Bukan tentang ke mana kamu pergi.
Tapi tentang siapa yang kamu temukan di perjalanan."
→ ZERO penyebutan air, mineral, kemurnian. Murni perasaan manusia tentang perjalanan.

CONTOH 2 — Indomie (belonging/warmth):
"Di mana pun kamu berada, ada satu hal yang selalu membawamu pulang.
Bukan jaraknya. Bukan waktunya.
Tapi rasa yang tidak pernah berubah."
→ ZERO penyebutan mie, kuah, bumbu. Murni tentang kerinduan dan rumah.

CONTOH 3 — Johnnie Walker Asia (aspiration/quiet luxury):
"Some roads you walk alone.
Not because no one's there.
But because some things — you can only discover yourself."
→ ZERO penyebutan whisky, rasa, aroma. Murni tentang perjalanan personal.

CONTOH 4 — Thai Life Insurance (human truth):
"Hari ini kamu mungkin tidak ingat apa yang kamu makan.
Tapi kamu akan selalu ingat siapa yang ada di sebelahmu."
→ ZERO penyebutan produk asuransi. Murni kebenaran manusia yang universal.

STANDAR: VO yang kamu tulis HARUS SETARA atau MELAMPAUI contoh-contoh di atas.
Bukan terinspirasi — tapi SETARA. Gunakan contoh ini sebagai ukuran minimum kualitas.
Gaya bahasa wajib mengikuti input user: {lang_style}
"""

    # -------------------------------------------------------
    # BUILD SCENE BLOCKS
    # -------------------------------------------------------
    scene_blocks = []
    for i in range(1, scene_count + 1):

        scene_name = scene_name_map.get(i, f"SCENE {i}")

        if i == 1:
            scene_role = "OPENING HOOK — Ciptakan TENSION emosional dalam 1 detik pertama. Jangan jelaskan — rasakan."
        elif i == scene_count:
            scene_role = f"KLIMAKS & CTA — DESIRE tercapai. Produk sebagai ikon momen. Ajakan '{cta_goal}' masuk natural, tidak memaksa."
        elif i == scene_count - 1:
            scene_role = "PUNCAK EMOSI — RELEASE: Signature Moment. Produk hadir sebagai kelegaan yang tak terhindarkan."
        else:
            scene_role = "BUILD UP — Perdalam TENSION. Bangun keintiman antara penonton dan momen yang sedang terjadi."

        focal_len, focal_note = FOCAL_MAP.get(i, ("50mm", "natural human perspective"))
        cam_note = build_camera_note(i, location_desc, tone_style)

        # ---- NEGATIVE PROMPTS per tool — dikunci per tone ----
        # Ini yang memisahkan hasil AI dari foto katalog / stock photo
        NEGATIVE_BASE = (
            "--no text on clothing, --no logo on clothing, --no brand name on shirt, "
            "--no AIRY text, --no watermark, --no posed smile, --no looking at camera, "
            "--no product held toward camera, --no studio lighting, --no white backdrop, "
            "--no stock photo composition, --no catalog pose, --no advertising smile"
        )
        NEGATIVE_TONE_EXTRA = {
            "Mewah (Luxury/Gold)":         "--no busy background, --no clutter, --no casual clothes",
            "Tradisional (Heritage/Warm)": "--no modern office, --no cold blue tones, --no fluorescent light",
            "Modern (Minimalist/Clean)":   "--no warm tones, --no rustic elements, --no heavy shadows",
            "Premium (High-End/Elegant)":  "--no casual setting, --no flat lighting, --no overexposed",
            "Ceria (Fun/Energetic)":       "--no sad expression, --no dark moody tones, --no static pose",
        }
        negative_extra = NEGATIVE_TONE_EXTRA.get(tone_style, "")
        negative_prompt = f"{NEGATIVE_BASE}, {negative_extra}"

        # ---- FRAME-BY-FRAME VIDEO TIMING per scene ----
        # Per 0.5s timing — ini yang membedakan brief iklan mahal vs brief biasa
        scene_duration_seconds = int(scene_dur.replace(" detik", ""))
        VIDEO_TIMING = {
            1: [
                f"0:00–{scene_duration_seconds*0.25:.1f}s → EXTREME TIGHT: single environmental detail only (steam, shadow, texture). No talent visible yet.",
                f"{scene_duration_seconds*0.25:.1f}s–{scene_duration_seconds*0.6:.1f}s → IMPERCEPTIBLY SLOW PULL-BACK begins. Talent enters frame mid-action, never posed.",
                f"{scene_duration_seconds*0.6:.1f}s–{scene_duration_seconds*0.85:.1f}s → HOLD: talent + location fully established. Product visible but passive.",
                f"{scene_duration_seconds*0.85:.1f}s–{scene_duration_seconds:.1f}s → FREEZE on tension. Viewer leans in. Cut.",
            ],
            2: [
                f"0:00–{scene_duration_seconds*0.3:.1f}s → TIGHT on product — packaging, texture, light at 45°. Face not yet visible.",
                f"{scene_duration_seconds*0.3:.1f}s–{scene_duration_seconds*0.5:.1f}s → RACK FOCUS begins: product to hand to face. Slow. Never rushed.",
                f"{scene_duration_seconds*0.5:.1f}s–{scene_duration_seconds*0.85:.1f}s → HOLD ON FACE: THE MICRO-EXPRESSION. Eyes soften. Exhale. 2mm shoulder drop. This is the Signature Moment.",
                f"{scene_duration_seconds*0.85:.1f}s–{scene_duration_seconds:.1f}s → Hold the silence. Do not cut early. Let the emotion breathe.",
            ],
            3: [
                f"0:00–{scene_duration_seconds*0.15:.1f}s → STATIC 50mm: talent slightly off-center, rule of thirds. World at rest.",
                f"{scene_duration_seconds*0.15:.1f}s–{scene_duration_seconds*0.7:.1f}s → ALMOST NO MOVEMENT. A slight settle. The stillness is the emotion.",
                f"{scene_duration_seconds*0.7:.1f}s–{scene_duration_seconds:.1f}s → Hold. Something invisible has shifted. Lighter. Cut on this feeling.",
            ],
            4: [
                f"0:00–{scene_duration_seconds*0.35:.1f}s → 100mm MACRO: product surface fills frame. Light refracting through texture.",
                f"{scene_duration_seconds*0.35:.1f}s–{scene_duration_seconds*0.6:.1f}s → RACK FOCUS: product → eyes. One breath. No cut.",
                f"{scene_duration_seconds*0.6:.1f}s–{scene_duration_seconds*0.9:.1f}s → HOLD on eyes: the look of someone who has found something worth keeping. 1.5 seconds minimum.",
                f"{scene_duration_seconds*0.9:.1f}s–{scene_duration_seconds:.1f}s → Eyes + product both in soft focus. Cut.",
            ],
            5: [
                f"0:00–{scene_duration_seconds*0.2:.1f}s → 85mm MEDIUM: talent faces camera, quiet presence. World not yet visible.",
                f"{scene_duration_seconds*0.2:.1f}s–{scene_duration_seconds*0.75:.1f}s → VERY SLOW PULL-BACK: location reveals itself around talent. World expands.",
                f"{scene_duration_seconds*0.75:.1f}s–{scene_duration_seconds:.1f}s → Product enters frame naturally — in hand or on table. Never held for camera. Cut.",
            ],
            6: [
                f"0:00–{scene_duration_seconds*0.25:.1f}s → CLOSE on product label: sharp, proud, specific. Maximum 3 seconds.",
                f"{scene_duration_seconds*0.25:.1f}s–{scene_duration_seconds*0.7:.1f}s → 35mm PULL-OUT: full scene at {location_desc} reveals.",
                f"{scene_duration_seconds*0.7:.1f}s–{scene_duration_seconds*0.85:.1f}s → CTA overlay fades in: minimal, confident, single line.",
                f"{scene_duration_seconds*0.85:.1f}s–{scene_duration_seconds:.1f}s → HOLD on final frame. The last page of a beautiful story.",
            ],
        }
        timing_lines = VIDEO_TIMING.get(i, [f"0:00–{scene_duration_seconds:.1f}s → Cinematic shot appropriate to scene {i}."])
        timing_block = "\n".join(timing_lines)

        # ---- PROMPT GAMBAR — LEVEL IKLAN RATUSAN JUTA ----
        cam_note_parts = cam_note.split('EMOTIONAL TARGET:')
        emotional_target = cam_note_parts[1].strip() if len(cam_note_parts) > 1 else 'A human moment worth remembering.'
        scene_action = cam_note_parts[0].strip()

        prompt_gambar = (
            f"CINEMATIC ADVERTISEMENT PHOTOGRAPHY — {tone_style.upper()} GRADE\n\n"
            f"THE EMOTIONAL MOMENT TO CAPTURE:\n"
            f"{emotional_target}\n\n"
            f"SHOT SETUP:\n"
            f"- Lens: {focal_len} — {focal_note}\n"
            f"- Format: {ar_ratio}\n"
            f"- Color grade: {color_grade}\n"
            f"- Depth of field: shallow, Arri Alexa color science\n\n"
            f"SCENE ACTION (frame by frame):\n"
            f"{scene_action}\n\n"
            f"LOCATION: {location_desc}\n\n"
            f"PRODUCT IN FRAME (Image 1 reference):\n"
            f"Use Image 1 as EXACT product reference. Match all packaging details — color, label text, shape, size, texture — identically. "
            f"Product placement: [describe exact position and prominence in this scene's frame].\n\n"
            f"CHARACTER (Image 2 reference — FACE & BODY ONLY):\n"
            f"{talent_anchor}\n\n"
            f"CINEMATIC REFERENCE: {cinematic_ref}\n\n"
            f"NEGATIVE PROMPT: {negative_prompt}\n\n"
            f"{ar_param} --v 6.0 --style raw --q 2"
        )

        # ---- PROMPT VIDEO — SHOT GRAMMAR + FRAME-BY-FRAME TIMING ----
        prompt_video = (
            f"CINEMATIC TVC — {tone_style.upper()} — {scene_dur} — {ar_ratio}\n\n"
            f"FRAME-BY-FRAME TIMING:\n"
            f"{timing_block}\n\n"
            f"SHOT GRAMMAR (overarching direction):\n"
            f"{cam_note}\n\n"
            f"TALENT:\n"
            f"{talent_anchor}\n\n"
            f"PRODUCT:\n"
            f"EXACT {prod_name} from Image 1 — identical packaging, color, label in every frame it appears. "
            f"Product is [describe exact position, how talent interacts with it, duration visible in frame].\n\n"
            f"LOCATION: {location_desc}\n\n"
            f"TECHNICAL:\n"
            f"- Lens simulation: {focal_len}\n"
            f"- Color grade: {color_grade}\n"
            f"- Camera movement speed: very slow, deliberate — never handheld shake\n"
            f"- Focus: shallow DOF, smooth rack focus if applicable\n"
            f"- Lighting: warm natural practical light, no hard artificial\n\n"
            f"AUDIO CUE: [describe sound that opens this scene — ambient environment, product sound, breath]\n\n"
            f"WHAT MUST NOT APPEAR: {negative_prompt}\n\n"
            f"CINEMATIC REFERENCE: {cinematic_ref}\n\n"
            f"Duration: {scene_dur}. Aspect ratio: {ar_ratio}."
        )

        scene_blocks.append(f"""
---

## 🎬 SCENE {i} / {scene_count}: {scene_name} ({scene_dur})

**🎯 PERAN SCENE:** {scene_role}

**📷 REFERENSI GAMBAR YANG DIBUTUHKAN UNTUK SCENE INI:**
{talent_label_line}
> {image_ref_instruction}

**🎥 LENS & CAMERA DIRECTION:**
- **Lensa:** {focal_len} — {focal_note}
- **Shot Grammar:** {cam_note}
- **Color Grade:** {color_grade}
- **Cinematic Ref:** {cinematic_ref}

**👁️ DESKRIPSI VISUAL (untuk sutradara/storyboard artist):**
[Deskripsikan momen sinematik secara frame-by-frame menggunakan lens {focal_len}: 
bukan "talent duduk pegang produk" — tapi DETIK SPESIFIK yang ditangkap kamera: 
micro-expression apa, gerakan tangan seberapa lambat, cahaya jatuh di sudut mana, 
produk di titik mana dalam komposisi. 
Setting wajib di {location_desc}. 
Talent wajib mengenakan: {wardrobe_for_prompt}.]

**📸 PROMPT GAMBAR — copy langsung ke Midjourney / Flux / Leonardo:**
```
{prompt_gambar}
```

**🎥 PROMPT VIDEO — copy langsung ke Kling AI / Runway / Hailuo:**
```
{prompt_video}
```

**🎙️ ELEMEN AUDIO:**
- **VO Scene {i} ({lang_style}):** "[Satu baris narasi puitis — BUKAN deskripsi produk, tapi PERASAAN MANUSIA. {VO_FORBIDDEN[:80]}...]"
- **SFX:** [Suara spesifik & imersif — ambient environment + signature product sound scene ini]
- **Musik:** [Dinamika dari scene sebelumnya — genre/instrumen/BPM KONSISTEN, intensitas emosi build-up]
""")

    scene_template = "\n".join(scene_blocks)

    # -------------------------------------------------------
    # MASTER PROMPT KE GEMINI — UPGRADED
    # -------------------------------------------------------
    with st.spinner(f"🎬 Meracik {scene_count} scene level iklan ratusan juta..."):
        try:
            image_parts = [Image.open(uploaded_file)]
            if uploaded_model:
                image_parts.append(Image.open(uploaded_model))

            model_gemini = genai.GenerativeModel('gemini-2.5-flash')

            master_prompt = f"""
Anda adalah Sutradara TVC kelas dunia — Cannes Lions Grand Prix winner — yang telah membuat iklan untuk brand-brand besar Asia Tenggara dengan budget ratusan juta rupiah per produksi.

Misi Anda hari ini bukan sekadar membuat iklan UMKM. Misi Anda adalah membuktikan bahwa UMKM '{prod_name}' layak tampil di layar TV nasional dengan kualitas yang sama persis seperti iklan Aqua, Indomie, Walls, atau Nescafé Asia — yang anggarannya jauh lebih besar.

Anda bekerja dengan standar yang sama seperti ketika Anda membuat iklan untuk brand multinasional. Tidak ada kompromi pada kualitas cerita, kualitas visual, atau kualitas emosi.

=== CREATIVE BRIEF ===
- PRODUK: {prod_name}
- KATEGORI: {category}
- TONE IKLAN: {tone_style}
- LOKASI SYUTING: {location_desc}
- WARDROBE MODEL: {wardrobe_label}
- BAHASA VO: {lang_style}
- MOOD MUSIK: {music_mood}
- CTA (Tujuan Iklan): {cta_goal}
- CERITA & KEUNGGULAN PRODUK: {details}

=== REFERENSI VISUAL ===
- Image 1 = Foto produk '{prod_name}' → product reference — warna, kemasan, label, tekstur HARUS identik di semua scene
{"- Image 2 = Foto talent → character reference untuk WAJAH & FISIK SAJA. Abaikan baju di foto — ikuti deskripsi wardrobe." if uploaded_model else f"- Tidak ada Image 2 → generate talent: {talent_gender}, {talent_age}, {talent_ethnicity}, konsisten lintas scene"}

=== WARDROBE LOCK — NON-NEGOTIABLE ===
Talent WAJIB mengenakan **{wardrobe_for_prompt}** di SETIAP scene.
CRITICAL: {CLOTHING_OVERRIDE}
Tulis deskripsi wardrobe ini LENGKAP dan EKSPLISIT di setiap prompt gambar dan video — JANGAN disingkat "same wardrobe".

=== STANDAR IKLAN TV RATUSAN JUTA — WAJIB DIPAHAMI ===

**PRINSIP 1: JUAL MOMEN MANUSIA, BUKAN PRODUK**
Iklan Aqua tidak menjual air. Ia menjual rasa rindu perjalanan.
Iklan Indomie tidak menjual mie. Ia menjual rasa pulang.
Iklan Walls tidak menjual es krim. Ia menjual kebahagiaan sederhana yang tulus.
Mereka tidak pernah MENDESKRIPSIKAN produk di VO. Mereka MENCIPTAKAN MOMEN.
{prod_name} harus jadi kendaraan menuju perasaan universal — bukan objek yang dijual.

**PRINSIP 2: VO ADALAH PUISI, BUKAN INFORMASI**
VO iklan mahal tidak menjelaskan produk. VO berbicara tentang kondisi manusia.
{VO_FORBIDDEN}
VO harus bisa dibacakan tanpa gambar dan masih terasa bermakna dan indah.
VO yang bagus: "Ada yang bilang hal-hal kecil tidak penting. Mereka belum menemukan yang ini."
VO yang buruk: "Keripik pisang ini renyah dan gurih, dibuat dari bahan pilihan."

{VO_ANCHOR_EXAMPLES}

**PRINSIP 3: SATU SIGNATURE MOMENT — SATU FRAME IKONIK**
Setiap iklan TV mahal punya 1 frame yang penonton ingat seumur hidup.
Tentukan 1 MOMEN SPESIFIK yang hanya bisa ada di {prod_name}.
Bukan pose. Bukan komposisi. Tapi DETIK — micro-expression, gerakan tangan, cahaya yang jatuh tepat.
Ini harus menjadi visual puncak iklan, dieksekusi dengan lensa makro atau 85mm.

**PRINSIP 4: STRUKTUR EMOSI — TENSION → RELEASE → DESIRE**
- TENSION: Penonton MENGENALI situasi dari hidup mereka. Bukan konflik dramatis — tapi momen "butuh sesuatu" yang universal.
- RELEASE: Produk hadir bukan sebagai solusi iklan. Ia hadir seperti teman lama yang muncul di saat yang tepat.
- DESIRE: Penonton tidak ingin membeli produk. Mereka ingin BERADA di momen itu. Pembelian adalah efek samping.

**PRINSIP 5: SINEMATOGRAFI MENCERITAKAN EMOSI**
Lensa bukan hanya alat teknis — ia adalah sudut pandang emosi.
- 35mm: penonton melihat dunia — establishing, connection to environment
- 85mm: penonton merasakan — compression, intimacy, the face as landscape
- 100mm macro: penonton menyentuh — texture, the decisive micro-detail
Shot grammar: setiap scene punya OPENING FRAME → MOVEMENT → BEAT (held) → CLOSING FRAME.
Tidak ada shot yang "talent memegang produk menghadap kamera". Semua terjadi secara natural.

**PRINSIP 6: PROMPT GAMBAR = TANGKAP MOMEN, BUKAN DESKRIPSI POSISI**
Prompt yang buruk: "Man sitting at cafe table holding product, warm light, smiling."
Prompt yang benar: "The exact second his eyes close halfway — not a blink, an exhale — 
as the taste registers. His shoulders have dropped 3mm from where they were.
The product is a blur in his hand. His face is the story."

=== ATURAN KONSISTENSI TEKNIS (NON-NEGOTIABLE) ===
1. LOKASI: Semua {scene_count} scene di '{location_desc}'. Variasi angle boleh, ganti lokasi tidak.
2. WAJAH TALENT: Identik di semua scene. Tulis instruksi ini eksplisit di setiap prompt.
3. WARDROBE: Identik di semua scene. Tulis deskripsi LENGKAP di setiap prompt — tidak boleh disingkat.
4. PRODUK: Bentuk, warna, kemasan, label {prod_name} IDENTIK dengan Image 1. Zero variasi.
5. VO SATU NARASI UTUH: Dipotong per scene tapi mengalir sebagai satu puisi. Zero kata deskripsi fisik produk.
6. MUSIK: DNA genre/instrumen sama dari scene 1 ke {scene_count}. Intensitas boleh naik, karakter tidak boleh berubah.
7. PROMPT GAMBAR WAJIB BERISI: (a) emotional moment description, (b) shot grammar, (c) product detail dari Image 1, (d) full wardrobe dengan clothing override, (e) cinematic reference.
8. PROMPT VIDEO WAJIB BERISI: (a) opening frame, (b) movement speed & direction, (c) beat timing, (d) closing frame, (e) talent + wardrobe + product description lengkap.

=== FORMAT OUTPUT (IKUTI PERSIS) ===

## 🎯 BIG IDEA & TAGLINE
- **Big Idea:** [1 kalimat — MOMEN MANUSIA, bukan deskripsi produk. "Momen kecil yang diam-diam jadi bagian terbaik hari ini" BUKAN "Keripik pisang yang enak dan berkualitas"]
- **Tagline:** [Maks 7 kata. Puitis. Bisa hidup tanpa konteks produk. Zero kata harga/fisik produk.]
- **Signature Moment:** [Deskripsikan 1 DETIK SPESIFIK — bukan pose, tapi micro-moment yang hanya bisa ada di {prod_name}. Sebutkan lensa, cahaya, ekspresi, gerakan. Ini puncak visual iklan.]

## 🔍 PRODUCTION PLAN

### Analisis Produk dari Image 1
[Detail fisik produk: warna, tekstur, kemasan, label, ukuran — anchor untuk semua prompt]

### Emotional Story Arc — {scene_count} Scene
[Blueprint emosi: apa TENSION-nya, bagaimana RELEASE-nya, bagaimana DESIRE terbentuk. Bukan sinopsis scene, tapi peta perasaan.]

### Location & Cinematography Blueprint
[Bagaimana {location_desc} dieksekusi: sudut, pencahayaan, props, bagaimana Signature Moment dieksekusi di sini]

### Master Character & Wardrobe Lock
- **Wajah & Fisik:** [dari Image 2 atau deskripsi AI-generated — detail sangat spesifik]
- **Pakaian Atas:** [detail lengkap — warna, bahan, potongan, zero logo/text]
- **Pakaian Bawah:** [detail lengkap]
- **Aksesori:** [jika ada, atau "tidak ada"]
- **Rambut & Grooming:** [spesifik]
- **Ekspresi Khas:** [bukan "senyum lebar" — ekspresi jujur yang spesifik]

### Color Palette
[5 warna dominan dengan hex code dan fungsinya — mendukung {tone_style}]

### 🎵 Audio & VO Master Plan
- **Musik:** [genre, instrumen utama, BPM, arc dinamika per scene, referensi artis/komposer]
- **Sound Design:** [signature sound produk ini — suara yang akan diingat penonton]
- **VO Philosophy:** [narasi internal, puisi manusia, zero deskripsi fisik produk]
- **VO Full Script (1 narasi utuh):** [Full VO dari awal sampai akhir sebagai 1 teks mengalir — ZERO kata deskripsi fisik produk. Murni puisi tentang momen manusia. Gaya bahasa: {lang_style}.]

{scene_template}

---

## 📱 CAMPAIGN KIT

### Caption Instagram/TikTok
[2 baris pertama = HOOK yang memaksa scroll stop. Body = cerita emosional. Tutup dengan CTA '{cta_goal}'. Maks 150 kata. Gaya: {lang_style}. Hashtag tanpa spasi.]

### Hashtag Strategy
**Tier 1 — High Volume (5 hashtag):** [tanpa spasi]
**Tier 2 — Mid Volume (5 hashtag):** [tanpa spasi]
**Tier 3 — Niche/Branded (5 hashtag):** [tanpa spasi]

### 🎙️ Voice Over Script Final (Siap Rekam)
[VO bersih per scene dengan timing. Siap baca tanpa arah visual.]
(0:00 - Scene 1) "..."
[dst]

### 📋 Shot List Manual (Untuk Shooting Smartphone)
[Tabel shot list yang bisa langsung dicetak untuk shooting sendiri:]
| Shot | Durasi | Zoom/Lensa | Aksi Talent | Props | Catatan Sutradara |
|------|--------|------------|-------------|-------|-------------------|
[Isi untuk semua {scene_count} scene]

### 💰 3 Tips Produksi Level Mahal dengan Budget UMKM
[Tips spesifik & actionable — bagaimana menangkap Signature Moment dengan smartphone, audio trick, lighting hack]
"""

            res = model_gemini.generate_content([master_prompt] + image_parts)
            st.session_state.last_result = res.text
            st.session_state.last_prod_name = prod_name
            st.balloons()

        except Exception as e:
            st.error(f"⚠️ Kendala teknis: {e}")
            st.stop()

# ============================================
# 10. DISPLAY HASIL
# ============================================
if st.session_state.last_result:
    st.divider()

    result_text = st.session_state.last_result
    lines = result_text.split('\n')

    current_block = []
    in_code_block = False
    prompt_count = 0

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```") and not in_code_block:
            if current_block:
                st.markdown('\n'.join(current_block))
                current_block = []
            in_code_block = True

        elif stripped == "```" and in_code_block:
            in_code_block = False
            prompt_count += 1
            prompt_text = '\n'.join(current_block)
            current_block = []

            # Label prompt gambar vs video
            if prompt_count % 2 == 1:
                label = "📸 Prompt Gambar"
                label_color = "#d97706"
            else:
                label = "🎥 Prompt Video"
                label_color = "#2563eb"

            st.markdown(
                f"<div style='font-size:11px; font-weight:700; letter-spacing:1px; "
                f"text-transform:uppercase; color:{label_color}; margin-bottom:4px;'>"
                f"{label}</div>",
                unsafe_allow_html=True
            )
            st.code(prompt_text, language=None)

        elif in_code_block:
            current_block.append(line)
        else:
            current_block.append(line)

    if current_block:
        st.markdown('\n'.join(current_block))

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