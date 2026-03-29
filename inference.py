from certainty import cf_and, cf_rule, cf_combine

def forward_chain(symptom_cf_map: dict[str, float], rules: list[dict]) -> list[dict]:
    """
    Forward Chaining:
    - Memori kerja = symptom_cf_map (fakta: pasangan CF(E,e))
    - Untuk setiap aturan, periksa apakah SEMUA kondisinya ada di memori kerja dengan CF > 0
    - Jika ya, hitung CF yang dihasilkan dan catat aturan yang dipicu
    - Terapkan resolusi konflik: urutkan berdasarkan jumlah kondisi yang cocok (pencocokan terpanjang)
    - Gabungkan CF untuk aturan yang mencapai kesimpulan yang sama
    Mengembalikan daftar dict diagnosis yang diurutkan berdasarkan CF menurun.
    """
    fired = []
    for rule in rules:
        conditions = rule["conditions"]
        # Periksa apakah semua kondisi ada dengan CF > 0 (telah dikonfirmasi pengguna)
        evidence_cfs = []
        all_matched = True
        for cond in conditions:
            cf_e = symptom_cf_map.get(cond, 0.0)
            if cf_e <= 0.0:
                all_matched = False
                break
            evidence_cfs.append(cf_e)
        if not all_matched:
            continue
        
        # CF(E, e) untuk kondisi AND = nilai minimum dari semua CF individu
        combined_evidence_cf = cf_and(evidence_cfs)
        
        # CF(H, e) = CF(E, e) × CF(H, E)
        result_cf = cf_rule(combined_evidence_cf, rule["cf_he"])
        
        fired.append({
            "rule": rule,
            "matched_conditions": conditions,
            "evidence_cfs": dict(zip(conditions, evidence_cfs)),
            "combined_evidence_cf": combined_evidence_cf,
            "result_cf": result_cf,
        })
        
    # Resolusi konflik: strategi pencocokan terpanjang (kondisi paling banyak cocok = lebih spesifik)
    fired.sort(key=lambda x: (len(x["matched_conditions"]), x["result_cf"]), reverse=True)
    
    # Gabungkan CF untuk aturan yang memiliki penyebab yang sama (hipotesis yang sama)
    combined_results = {}
    for item in fired:
        cause = item["rule"]["cause"]
        if cause not in combined_results:
            combined_results[cause] = item
        else:
            existing_cf = combined_results[cause]["result_cf"]
            new_cf = cf_combine(existing_cf, item["result_cf"])
            combined_results[cause]["result_cf"] = new_cf
            combined_results[cause]["combined_from"] = combined_results[cause].get("combined_from", []) + [item]
            
    results = list(combined_results.values())
    results.sort(key=lambda x: x["result_cf"], reverse=True)
    
    # Filter: hanya tampilkan diagnosis dengan CF di atas ambang batas minimum
    results = [r for r in results if r["result_cf"] > 0.2]
    
    return results
