# Implementasi fungsi certainty

def cf_and(cf_values: list[float]) -> float:
    if not cf_values:
        return 0.0
    return min(cf_values)

def cf_rule(cf_evidence: float, cf_he: float) -> float:
    return cf_evidence * cf_he

def cf_combine(cf1: float, cf2: float) -> float:
    if cf1 >= 0 and cf2 >= 0:
        return cf1 + cf2 * (1 - cf1)
    elif cf1 < 0 and cf2 < 0:
        return cf1 + cf2 * (1 + cf1)
    else:
        return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))
