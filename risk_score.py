import numpy as np

def risk_score(prob_fake: float, registry_fail: int, anomaly_flag: int, weights=(0.5,0.3,0.2)):
    w1,w2,w3 = weights
    return float(np.clip(w1*prob_fake + w2*registry_fail + w3*anomaly_flag, 0, 1))
