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
    
    # Dynamic Scene Config
    scene_config = {
        "15 Detik": {"count": 3, "per_scene": "5 detik"},
        "30 Detik": {"count": 5, "per_scene": "6 detik"},
        "60 Detik": {"count": 6, "per_scene": "10 detik"},
    }
    cfg = scene_config[duration]
    scene_count = cfg["count"]
    scene_dur = cfg["per_scene"]

    # Aspect ratio parameter
    ar_param = "--ar 9:16"
    if "1:1" in format_video:
        ar_param = "--ar 1:1"
    elif "16:9" in format_video:
        ar_param = "--ar 16:9"

    # -------------------------------------------------------
    # WARDROBE RESOLUTION
    # Wardrobe_desc diteruskan ke setiap prompt secara eksplisit.
    # Jika user pilih "Otomatis", AI tetap punya anchor deskripsi.
    # -------------------------------------------------------
    WARDROBE_AUTO_MAP = {
        "Mewah (Luxury/Gold)":         "elegant silk blouse or well-fitted blazer in cream/gold tones, minimal jewelry",
        "Tradisional (Heritage/Warm)": "neat modern kebaya or batik outfit in warm earth tones, traditional Lampung accent",
        "Modern (Minimalist/Clean)":   "linen short-sleeve shirt in broken-white rolled at elbows, khaki or light-gray chino pants",
        "Premium (High-End/Elegant)":  "slim-fit blazer in charcoal or navy over a clean white shirt, no tie, minimal accessories",
        "Ceria (Fun/Energetic)":       "bright casual t-shirt in solid color (mustard/coral/white), clean jogger or chino pants",
    }

    if wardrobe_desc == "Otomatis Sesuai Tone Iklan":
        wardrobe_for_prompt = WARDROBE_AUTO_MAP.get(tone_style, "clean casual outfit appropriate for the ad tone")
        wardrobe_label = f"Auto ({tone_style}): {wardrobe_for_prompt}"
    else:
        wardrobe_for_prompt = wardrobe_desc
        wardrobe_label = wardrobe_desc

    # -------------------------------------------------------
    # TALENT DESCRIPTION
    # -------------------------------------------------------
    if uploaded_model:
        talent_anchor = (
            "EXACT same talent face and physical appearance as Image 2 (character reference). "
            f"Wardrobe locked: {wardrobe_for_prompt}. "
            "This wardrobe MUST be IDENTICAL across every single scene — no variation, no substitution."
        )
        talent_label_line = "📷 **Image 1** (produk) + 📷 **Image 2** (model/wajah talent) — keduanya WAJIB disertakan"
        image_ref_instruction = (
            "PENTING UNTUK TOOLS AI GAMBAR: "
            "Gunakan Image 1 sebagai product reference. "
            "Gunakan Image 2 sebagai character reference (--cref di Midjourney, atau 'Character Reference' di Flux/Kling). "
            "Wajah, kulit, rambut talent HARUS IDENTIK dengan Image 2 di semua scene tanpa pengecualian."
        )
    else:
        talent_anchor = (
            f"Generate consistent talent: {talent_gender}, usia {talent_age}, etnis/look {talent_ethnicity}. "
            f"Wardrobe locked: {wardrobe_for_prompt}. "
            "This SAME face, SAME body type, SAME wardrobe MUST appear IDENTICALLY across every single scene. "
            "Do NOT change the character's appearance between scenes."
        )
        talent_label_line = "📷 **Image 1** (produk) — wajib disertakan | Model: AI-generated (konsisten lintas scene)"
        image_ref_instruction = (
            "PENTING UNTUK TOOLS AI GAMBAR: "
            "Gunakan Image 1 sebagai product reference. "
            "Untuk konsistensi wajah model tanpa Image 2: gunakan fitur 'Consistent Character' atau seed yang sama di setiap scene generation."
        )

    # -------------------------------------------------------
    # BUILD SCENE BLOCKS
    # -------------------------------------------------------
    scene_blocks = []
    for i in range(1, scene_count + 1):
        # Scene role
        if i == 1:
            scene_role = "OPENING HOOK — Tarik perhatian dalam 1 detik pertama"
        elif i == scene_count:
            scene_role = f"KLIMAKS & CTA — Tampilkan produk jelas + ajakan '{cta_goal}'"
        elif i == scene_count - 1:
            scene_role = "PUNCAK EMOSI — Tunjukkan keunggulan & manfaat utama produk"
        else:
            scene_role = "BUILD UP — Bangun cerita, desire, dan koneksi emosi"

        # Scene-specific camera notes
        camera_notes = {
            1: f"Slow dolly-forward or slider shot. Establish setting at {location_desc}.",
            2: "Push-in close-up. Focus on product detail and talent reaction.",
            3: "Static medium shot with subtle pull-back. Build emotional peak.",
            4: "Low angle close-up of product. Hero shot — product is the star.",
            5: "Medium shot, talent facing camera confidently. Resolution moment.",
            6: f"Wide pull-out to full scene at {location_desc}. Grand finale with CTA overlay.",
        }
        cam = camera_notes.get(i, "Dynamic shot appropriate to scene energy.")

        scene_blocks.append(f"""
---

## 🎬 SCENE {i} / {scene_count}: [BERI NAMA SCENE INI] ({scene_dur})

**🎯 PERAN SCENE:** {scene_role}

**📷 REFERENSI GAMBAR YANG DIBUTUHKAN UNTUK SCENE INI:**
{talent_label_line}
> {image_ref_instruction}

**👁️ DESKRIPSI VISUAL (untuk sutradara/storyboard artist):**
[Tulis deskripsi sinematik detail: action talent, posisi produk, pencahayaan, komposisi frame. Setting wajib di {location_desc}. Talent wajib mengenakan {wardrobe_for_prompt}. Sinematografi gaya Arri Alexa, {format_video}.]

**📸 PROMPT GAMBAR — copy langsung ke Midjourney / Flux / Leonardo:**
```
[SHOT TYPE: contoh Cinematic medium shot / extreme close-up / wide establishing shot], EXACT product appearance from Image 1 ({prod_name} — [AI: deskripsikan kemasan/warna/bentuk/label persis dari Image 1]), {talent_anchor}, setting: {location_desc}, [AKSI SPESIFIK SCENE INI], [MOOD PENCAHAYAAN sesuai tone {tone_style}], shallow depth of field, warm bokeh, Arri Alexa color science, professional cinematography {ar_param} --v 6.0
```

**🎥 PROMPT VIDEO — copy langsung ke Kling AI / Runway / Hailuo:**
```
{cam} {talent_anchor} Setting: {location_desc}. [AKSI SPESIFIK SCENE INI]. EXACT {prod_name} from Image 1 [posisi & cara pegang produk]. {tone_style} mood, warm natural lighting. Arri Alexa cinematic grade, shallow DOF, smooth {ar_param.replace('--ar ', '')} framing. Duration: {scene_dur}.
```

**🎙️ ELEMEN AUDIO:**
- **VO Scene {i} ({lang_style}):** "[Kalimat VO yang menyambung dari scene sebelumnya — 1 narasi utuh yang dipotong per scene, BUKAN kalimat berdiri sendiri]"
- **SFX:** [Sound effect spesifik & realistis untuk momen ini]
- **Musik:** [Perkembangan musik dari scene sebelumnya — genre/instrumen/tempo harus KONSISTEN, hanya dinamika yang berubah]
""")

    scene_template = "\n".join(scene_blocks)

    # -------------------------------------------------------
    # MASTER PROMPT KE GEMINI
    # -------------------------------------------------------
    with st.spinner(f"📜 Menyusun {scene_count} scene mahakarya di {location_desc}..."):
        try:
            image_parts = [Image.open(uploaded_file)]
            if uploaded_model:
                image_parts.append(Image.open(uploaded_model))

            model_gemini = genai.GenerativeModel('gemini-2.5-flash')

            master_prompt = f"""
Anda adalah Sutradara TVC & Creative Director kelas internasional yang spesialis dalam branding UMKM Indonesia.
Misi Anda: Menghasilkan storyboard iklan TVC sinematik {duration} ({scene_count} scene, rasio {format_video}) untuk produk '{prod_name}'.
Setiap kata yang Anda tulis adalah instruksi produksi nyata. Tidak ada ruang untuk kemalasan kreatif.

=== CREATIVE BRIEF ===
- PRODUK: {prod_name}
- KATEGORI: {category}
- TONE IKLAN: {tone_style}
- LOKASI SYUTING: {location_desc}
- WARDROBE MODEL: {wardrobe_label}
- BAHASA VO: {lang_style}
- MOOD MUSIK: {music_mood}
- CTA (Tujuan Iklan): {cta_goal}
- CERITA & KEUNGGULAN: {details}

=== REFERENSI VISUAL ===
- Image 1 = Foto produk '{prod_name}' (product reference — warna, kemasan, label, tekstur HARUS dipertahankan identik)
{"- Image 2 = Foto talent/model (character reference — wajah, kulit, rambut HARUS identik di semua scene)" if uploaded_model else f"- Tidak ada Image 2 — generate model: {talent_gender}, {talent_age}, {talent_ethnicity}"}

=== WARDROBE LOCK (NON-NEGOTIABLE) ===
Model WAJIB mengenakan **{wardrobe_for_prompt}** di SETIAP scene tanpa pengecualian.
Tulis deskripsi pakaian ini secara LENGKAP dan EKSPLISIT di setiap prompt gambar dan video.
Jangan pernah tulis hanya "same wardrobe" — selalu tulis deskripsi lengkapnya.

=== 8 ATURAN KONSISTENSI WAJIB (SEMUA HARUS DIPATUHI) ===
1. KONSISTENSI LOKASI: Semua {scene_count} scene di '{location_desc}'. Variasi sudut kamera boleh, GANTI lokasi TIDAK BOLEH.
2. KONSISTENSI WAJAH TALENT: Wajah model HARUS IDENTIK lintas semua scene. Tulis instruksi ini eksplisit di setiap prompt.
3. KONSISTENSI WARDROBE: Pakaian model HARUS IDENTIK lintas semua scene. Tulis deskripsi lengkap pakaian di setiap prompt gambar dan video.
4. KONSISTENSI PRODUK: Bentuk, warna, kemasan, label {prod_name} HARUS IDENTIK dengan Image 1. Jangan imajinasikan variasi.
5. KONSISTENSI VO (NARASI UTUH): VO dari scene 1 sampai {scene_count} adalah SATU narasi yang dipotong per scene. Kalimat harus mengalir dan bersambung, bukan kalimat-kalimat terpisah.
6. KONSISTENSI MUSIK: Genre, instrumen utama, dan tempo musik SAMA dari scene 1 sampai {scene_count}. Dinamika boleh build-up, tapi DNA musik tidak boleh berubah.
7. PROMPT GAMBAR HARUS SPESIFIK: Setiap prompt gambar WAJIB menyebutkan: (a) jenis shot, (b) deskripsi fisik produk dari Image 1, (c) deskripsi lengkap wardrobe, (d) aksi spesifik scene, (e) referensi ke Image 1 dan Image 2.
8. PROMPT VIDEO HARUS EXECUTABLE: Prompt video harus bisa langsung dipakai di Kling/Runway. Sertakan: gerakan kamera, aksi talent, posisi produk, durasi, dan color grade reference.

=== FORMAT OUTPUT WAJIB (IKUTI PERSIS — JANGAN TAMBAH/KURANGI SECTION) ===

## 🎯 BIG IDEA & TAGLINE
- **Big Idea:** [1 kalimat konsep utama yang jadi jiwa seluruh iklan]
- **Tagline:** [Maks 7 kata, memorable, relevan dengan {prod_name} dan {tone_style}]

## 🔍 PRODUCTION PLAN

### Analisis Produk dari Image 1
[Deskripsikan DETAIL fisik produk dari foto: warna, tekstur, kemasan, label, ukuran relatif, kondisi. Ini akan jadi anchor semua prompt.]

### Location & Cinematography Blueprint
[Bagaimana {location_desc} dieksekusi secara sinematik: sudut, pencahayaan, props yang digunakan, bagaimana variasi antar scene dicapai tanpa ganti lokasi]

### Master Character & Wardrobe Lock
[Deskripsi LENGKAP talent dan wardrobe yang akan KONSISTEN di semua {scene_count} scene. Ini adalah "bible" yang harus dipatuhi setiap prompt.]
- **Wajah & Fisik:** [dari Image 2 atau deskripsi AI-generated]
- **Pakaian Atas:** [detail spesifik]
- **Pakaian Bawah:** [detail spesifik]
- **Aksesori:** [jika ada]
- **Rambut & Grooming:** [spesifik]

### Color Palette
[5 warna dominan dengan hex code, contoh #FFC107, dan keterangan penggunaannya]

### 🎵 Audio & VO Master Plan
- **Musik:** [Nama genre spesifik, instrumen utama, BPM range, referensi artis/lagu jika ada, bagaimana berkembang dari scene 1 ke {scene_count}]
- **VO Flow:** [Tulis FULL narasi VO dari scene 1 sampai {scene_count} sebagai 1 paragraf utuh — ini adalah "script bible" VO sebelum dipotong per scene]

{scene_template}

---

## 📱 CAMPAIGN KIT

### Caption Instagram/TikTok
[Caption lengkap: baris 1-2 adalah HOOK yang memaksa orang berhenti scroll, lanjutkan dengan body cerita, tutup dengan CTA '{cta_goal}'. Maks 150 kata. Gunakan gaya bahasa {lang_style}.]

### Hashtag Strategy
**Tier 1 — High Volume (5 hashtag):** [hashtag umum dengan jutaan postingan]
**Tier 2 — Mid Volume (5 hashtag):** [hashtag kategori dengan ratusan ribu postingan]
**Tier 3 — Niche/Branded (5 hashtag):** [hashtag unik produk + lokal Lampung/Indonesia]

### 🎙️ Voice Over Script Final (Siap Rekam)
[Compile semua VO jadi 1 script bersih dengan timing per scene. Format untuk talent rekam langsung.]

(0:00 - Scene 1) "[VO scene 1]"
[dst sesuai jumlah scene]

### 💰 3 Tips Produksi Hemat UMKM
[Tips eksekusi murah tapi hasilnya setara agency — spesifik, actionable, relevan dengan {location_desc} dan {tone_style}]
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

    # ---- PARSING & DISPLAY DENGAN TOMBOL COPY ----
    result_text = st.session_state.last_result
    lines = result_text.split('\n')

    # Render hasil dengan tombol copy untuk setiap blok kode prompt
    current_block = []
    in_code_block = False
    code_lang = ""
    prompt_count = 0

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```") and not in_code_block:
            # Flush accumulated non-code text
            if current_block:
                st.markdown('\n'.join(current_block))
                current_block = []
            in_code_block = True
            code_lang = stripped[3:].strip()

        elif stripped == "```" and in_code_block:
            # End of code block — render with copy button
            in_code_block = False
            prompt_count += 1
            prompt_text = '\n'.join(current_block)
            current_block = []

            # Determine label
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

    # Flush any remaining text
    if current_block:
        st.markdown('\n'.join(current_block))

    st.divider()

    # ---- DOWNLOAD & RESET ----
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