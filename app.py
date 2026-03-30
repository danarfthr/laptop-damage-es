import streamlit as st
from knowledge_base import RULES, ALL_SYMPTOMS, SYMPTOM_LABELS, WHY_NOTES
from inference import forward_chain
from explanation import how_explanation

st.set_page_config(
    page_title="Sistem Pakar Diagnosis Laptop",
    page_icon="💻",
    layout="centered",
)

# --- KATEGORI GEJALA ---
SYMPTOM_CATEGORIES = {
    "⚡ Daya & Power": [
        "laptop_tidak_menyala",
        "lampu_indikator_mati",
        "lampu_indikator_menyala",
        "tidak_ada_suara",
        "adaptor_terhubung",
        "baterai_tidak_mengisi",
    ],
    "🖥️ Layar & Display": [
        "laptop_menyala",
        "layar_hitam",
        "layar_bergaris",
        "warna_tidak_normal",
    ],
    "⚙️ Performa & Stabilitas": [
        "laptop_lambat",
        "sering_hang",
        "sering_mati_sendiri",
        "sering_restart_sendiri",
        "bsod",
    ],
    "💾 Penyimpanan": [
        "hard_disk_berbunyi",
        "hard_disk_tidak_berbunyi",
    ],
    "🌡️ Suhu & Pendinginan": [
        "ada_suara_kipas",
        "laptop_panas_berlebih",
    ],
    "⌨️ Input Devices": [
        "keyboard_tidak_berfungsi",
        "beberapa_tombol_tidak_merespons",
        "touchpad_tidak_merespons",
    ],
    "📶 Jaringan": [
        "wifi_tidak_terdeteksi",
        "bluetooth_tidak_berfungsi",
    ],
}

st.title("💻 Diagnosis Kerusakan Laptop")
st.caption("Sistem Pakar berbasis Forward Chaining & Certainty Factor")

st.divider()

# --- STEP 1: PILIH GEJALA ---
st.subheader("Langkah 1 — Pilih gejala yang dialami")
st.info("Klik kategori untuk melihat gejala, centang yang relevan.")

CF_LEVELS = {
    "Tidak dialami": 0.0,
    "Kurang yakin": 0.3,
    "Cukup yakin": 0.6,
    "Yakin sekali": 1.0,
}

selected_symptoms = []

# Render each category as an expander
for category, symptoms in SYMPTOM_CATEGORIES.items():
    with st.expander(f"{category} ({len(symptoms)} gejala)", expanded=False):
        for symptom in symptoms:
            if symptom in SYMPTOM_LABELS:
                label = SYMPTOM_LABELS.get(symptom, symptom)
                checked = st.checkbox(label, key=f"check_{symptom}")
                if checked:
                    selected_symptoms.append(symptom)

st.divider()

# --- STEP 2: ATUR TINGKAT KEYAKINAN ---
symptom_cf_map = {}

if selected_symptoms:
    st.subheader("Langkah 2 — Seberapa yakin Anda dengan gejala tersebut?")

    # Group selected symptoms by category
    selected_by_category = {}
    for symptom in selected_symptoms:
        for category, cats in SYMPTOM_CATEGORIES.items():
            if symptom in cats:
                if category not in selected_by_category:
                    selected_by_category[category] = []
                selected_by_category[category].append(symptom)
                break

    # Render each category with its symptoms
    for category, symptoms in selected_by_category.items():
        with st.expander(f"📋 {category}", expanded=True):
            for symptom in symptoms:
                label = SYMPTOM_LABELS.get(symptom, symptom)
                why = WHY_NOTES.get(symptom, "")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(f"✅ {label}")
                with col2:
                    level = st.select_slider(
                        "Keyakinan",
                        options=list(CF_LEVELS.keys()),
                        value="Cukup yakin",
                        key=f"cf_{symptom}",
                        help=why,
                        label_visibility="collapsed",
                    )
                cf_val = CF_LEVELS[level]
                if cf_val > 0.0:
                    symptom_cf_map[symptom] = cf_val

    st.divider()

# --- STEP 3: DIAGNOSA ---
st.subheader("Langkah 3 — Diagnosa")

col1, col2 = st.columns([2, 1])
with col1:
    diagnose_btn = st.button(
        "🔍 Mulai Diagnosa",
        type="primary",
        disabled=len(symptom_cf_map) == 0,
        use_container_width=True,
    )
with col2:
    st.metric("Gejala dipilih", len(symptom_cf_map))

if diagnose_btn:
    results = forward_chain(symptom_cf_map, RULES)

    if not results:
        st.warning(
            "Tidak ada aturan yang cocok dengan gejala ini. "
            "Coba tambahkan lebih banyak gejala, atau konsultasikan langsung ke teknisi."
        )
    else:
        st.success(f"Ditemukan **{len(results)}** kemungkinan diagnosis.")
        st.caption("Diurutkan dari Certainty Factor tertinggi ke terendah.")
        st.divider()

        for i, result in enumerate(results, 1):
            rule = result["rule"]
            cf = result["result_cf"]

            if cf >= 0.7:
                badge = "🟢 Keyakinan Tinggi"
            elif cf >= 0.4:
                badge = "🟡 Keyakinan Sedang"
            else:
                badge = "🔴 Keyakinan Rendah"

            st.markdown(f"#### Diagnosis {i} — {badge} (CF = {cf:.2f})")
            st.markdown(f"**Penyebab:** {rule['cause']}")
            st.markdown(f"**Solusi:** {rule['solution']}")

            with st.expander("Lihat penjelasan HOW (bagaimana sistem menyimpulkan ini)"):
                st.markdown(how_explanation(result, SYMPTOM_LABELS))

            if i < len(results):
                st.divider()
