import streamlit as st
from knowledge_base import RULES, ALL_SYMPTOMS, SYMPTOM_LABELS, WHY_NOTES
from inference import forward_chain
from explanation import how_explanation

st.set_page_config(
    page_title="Sistem Pakar Diagnosis Laptop",
    page_icon="💻",
    layout="centered",
)

st.title("💻 Diagnosis Kerusakan Laptop")
st.caption("Sistem Pakar berbasis Forward Chaining & Certainty Factor")

st.divider()

# --- STEP 1: PILIH GEJALA ---
st.subheader("Langkah 1 — Pilih gejala yang dialami")
st.info("Centang semua gejala yang relevan, lalu atur tingkat keyakinan Anda di bawahnya.")

CF_LEVELS = {
    "Tidak dialami": 0.0,
    "Kurang yakin": 0.3,
    "Cukup yakin": 0.6,
    "Yakin sekali": 1.0,
}

selected_symptoms = []
for symptom in ALL_SYMPTOMS:
    label = SYMPTOM_LABELS.get(symptom, symptom)
    checked = st.checkbox(label, key=f"check_{symptom}")
    if checked:
        selected_symptoms.append(symptom)

st.divider()

# --- STEP 2: ATUR TINGKAT KEYAKINAN ---
symptom_cf_map = {}

if selected_symptoms:
    st.subheader("Langkah 2 — Seberapa yakin Anda dengan gejala tersebut?")

    for symptom in selected_symptoms:
        label = SYMPTOM_LABELS.get(symptom, symptom)
        why = WHY_NOTES.get(symptom, "")
        level = st.select_slider(
            label,
            options=list(CF_LEVELS.keys()),
            value="Cukup yakin",
            key=f"cf_{symptom}",
            help=why,
        )
        cf_val = CF_LEVELS[level]
        if cf_val > 0.0:
            symptom_cf_map[symptom] = cf_val

    st.divider()

# --- STEP 3: DIAGNOSA ---
st.subheader("Langkah 3 — Diagnosa")

diagnose_btn = st.button(
    "Mulai Diagnosa",
    type="primary",
    disabled=len(symptom_cf_map) == 0,
    use_container_width=True,
)

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
