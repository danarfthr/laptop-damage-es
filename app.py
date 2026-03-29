# app.py
import streamlit as st
from knowledge_base import RULES, ALL_SYMPTOMS, SYMPTOM_LABELS, WHY_NOTES
from inference import forward_chain
from explanation import how_explanation, why_explanation

st.set_page_config(page_title="Sistem Pakar Diagnosis Laptop", layout="wide")

st.title("Sistem Pakar Diagnosis Kerusakan Laptop")
st.caption(
    "Pilih gejala yang dialami laptop Anda dan tingkat keyakinan Anda terhadap setiap gejala. "
    "Sistem akan mendiagnosa penyebab kerusakan menggunakan Forward Chaining dan Certainty Factor."
)

st.markdown("---")

# --- SYMPTOM INPUT WITH CF(E,e) ---
st.subheader("Masukkan Gejala")
st.markdown(
    "Untuk setiap gejala yang **terlihat pada laptop Anda**, pilih tingkat keyakinan Anda. "
    "Gejala yang tidak dialami tidak perlu diisi."
)

CF_OPTIONS = {
    "Yakin sekali (pasti terjadi)": 1.0,
    "Cukup yakin (kemungkinan besar terjadi)": 0.6,
    "Kurang yakin (mungkin terjadi)": 0.3,
    "Tidak dialami / tidak tahu": 0.0,
}

symptom_cf_map = {}

col1, col2 = st.columns(2)
for i, symptom in enumerate(ALL_SYMPTOMS):
    label = SYMPTOM_LABELS.get(symptom, symptom)
    why = why_explanation(symptom, WHY_NOTES)

    col = col1 if i % 2 == 0 else col2
    with col:
        with st.expander(f"{label}", expanded=False):
            st.caption(f"**Mengapa ditanyakan?** {why}")
            selection = st.selectbox(
                "Tingkat keyakinan:",
                options=list(CF_OPTIONS.keys()),
                index=3,  # default: "Tidak dialami"
                key=f"select_{symptom}"
            )
            cf_val = CF_OPTIONS[selection]
            if cf_val > 0.0:
                symptom_cf_map[symptom] = cf_val

st.markdown("---")

# --- DIAGNOSA ---
if st.button("Diagnosa Sekarang", type="primary", use_container_width=True):
    if not symptom_cf_map:
        st.warning("Pilih minimal satu gejala dengan tingkat keyakinan di atas 'Tidak dialami / tidak tahu'.")
    else:
        results = forward_chain(symptom_cf_map, RULES)

        if not results:
            st.error(
                "Tidak ada aturan yang cocok dengan kombinasi gejala ini (atau CF hasil terlalu rendah). "
                "Silakan konsultasikan langsung ke teknisi laptop."
            )
        else:
            st.success(f"Ditemukan **{len(results)}** kemungkinan diagnosis, diurutkan berdasarkan Certainty Factor tertinggi.")
            st.markdown("")

            for i, result in enumerate(results, 1):
                rule = result["rule"]
                cf = result["result_cf"]

                # CF color coding
                if cf >= 0.7:
                    cf_label = "Tinggi"
                    cf_color = "green"
                elif cf >= 0.4:
                    cf_label = "Sedang"
                    cf_color = "orange"
                else:
                    cf_label = "Rendah"
                    cf_color = "red"

                with st.expander(
                    f"Diagnosis {i}: {rule['cause']}  |  CF = {cf:.2f} ({cf_label})",
                    expanded=(i == 1)
                ):
                    st.markdown(f"**Solusi yang Direkomendasikan:**")
                    st.info(rule["solution"])

                    st.markdown("---")

                    # HOW Explanation
                    how = how_explanation(result, SYMPTOM_LABELS)
                    st.markdown(how)
