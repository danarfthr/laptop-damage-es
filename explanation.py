def how_explanation(result: dict, symptom_labels: dict) -> str:
    rule = result["rule"]
    lines = []

    lines.append(f"### HOW: Bagaimana sistem mencapai kesimpulan ini?")
    lines.append("")
    lines.append(f"**Aturan yang digunakan: {rule['id']}**")
    lines.append("")
    lines.append("**Kondisi IF yang diperlukan oleh aturan ini (premis):**")

    for cond in result["matched_conditions"]:
        label = symptom_labels.get(cond, cond)
        cf_val = result["evidence_cfs"][cond]
        lines.append(f"- `{label}` → CF(E,e) = **{cf_val:.2f}** ✓")

    lines.append("")
    lines.append("**Perhitungan Certainty Factor:**")
    lines.append(f"- CF(E,e) gabungan [AND = min] = `min{list(result['evidence_cfs'].values())}` = **{result['combined_evidence_cf']:.2f}**")
    lines.append(f"- CF(H,E) pakar untuk aturan ini = **{rule['cf_he']:.2f}**")
    lines.append(f"- CF(H,e) = CF(E,e) × CF(H,E) = {result['combined_evidence_cf']:.2f} × {rule['cf_he']:.2f} = **{result['result_cf']:.2f}**")
    lines.append("")
    lines.append(f"**Kesimpulan THEN:**")
    lines.append(f"- Penyebab: {rule['cause']}")
    lines.append(f"- Solusi: {rule['solution']}")

    return "\n".join(lines)


def why_explanation(symptom_key: str, why_notes: dict) -> str:
    return why_notes.get(symptom_key, "Gejala ini relevan untuk menentukan komponen yang bermasalah.")
