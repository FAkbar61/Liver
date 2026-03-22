"""
engine.py — Forward Chaining Inference Engine
Sistem Pakar Identifikasi Penyakit Liver
"""

import json
import os
from copy import deepcopy


def load_rules(rules_path: str) -> list:
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_condition(fact_value, condition_value) -> bool:
    """Evaluasi apakah nilai fakta memenuhi kondisi."""
    return fact_value == condition_value


def check_rule(rule: dict, facts: dict) -> bool:
    """Cek apakah semua kondisi IF dari sebuah rule terpenuhi oleh facts."""
    for cond in rule.get("if_all", []):
        fact_key = cond["fact"]
        expected = cond["equals"]
        actual = facts.get(fact_key)
        if actual is None or not evaluate_condition(actual, expected):
            return False
    return True


def run_inference(initial_facts: dict, rules: list) -> dict:
    """
    Jalankan forward chaining inference.
    
    Args:
        initial_facts: dict fakta awal dari input pengguna
        rules: list aturan dari rules.json
    
    Returns:
        dict berisi:
          - facts: semua fakta setelah inferensi
          - scores: skor per penyakit
          - fired_rules: list rule yang berhasil 'fire' (trace)
          - red_flags: list peringatan merah
          - recommendations: list rekomendasi unik
    """
    facts = deepcopy(initial_facts)
    fired_rule_ids = set()
    fired_rules = []
    scores = {}
    red_flags = []
    recommendations = []

    # Forward chaining: ulangi hingga tidak ada rule baru yang fire
    changed = True
    iteration = 0
    max_iterations = 50  # Batas maksimum untuk menghindari infinite loop

    while changed and iteration < max_iterations:
        changed = False
        iteration += 1

        for rule in rules:
            rule_id = rule["id"]
            if rule_id in fired_rule_ids:
                continue  # Rule sudah pernah fire, lewati

            if check_rule(rule, facts):
                # Rule FIRE!
                fired_rule_ids.add(rule_id)
                changed = True

                # Kumpulkan kondisi yang terpenuhi untuk trace
                triggered_facts = []
                for cond in rule.get("if_all", []):
                    fact_key = cond["fact"]
                    triggered_facts.append({
                        "fact": fact_key,
                        "value": facts.get(fact_key)
                    })

                # Tambahkan ke trace
                trace_entry = {
                    "rule_id": rule_id,
                    "group": rule.get("group", ""),
                    "explain": rule.get("explain", ""),
                    "triggered_facts": triggered_facts,
                    "added_facts": [],
                    "added_scores": [],
                    "is_red_flag": rule.get("red_flag", False)
                }

                then = rule.get("then", {})

                # Tambahkan fakta baru
                for add_fact in then.get("add_facts", []):
                    fact_key = add_fact["fact"]
                    fact_val = add_fact["value"]
                    facts[fact_key] = fact_val
                    trace_entry["added_facts"].append({"fact": fact_key, "value": fact_val})
                    changed = True  # Fakta baru ditambahkan, perlu iterasi lagi

                # Akumulasi skor penyakit
                for score_item in then.get("add_score", []):
                    disease = score_item["disease"]
                    weight = score_item["weight"]
                    scores[disease] = scores.get(disease, 0.0) + weight
                    trace_entry["added_scores"].append({"disease": disease, "weight": weight})

                # Kumpulkan rekomendasi
                for rec in then.get("recommendations", []):
                    if rec not in recommendations:
                        recommendations.append(rec)

                # Red flag
                if rule.get("red_flag", False):
                    red_flags.append({
                        "rule_id": rule_id,
                        "message": rule.get("explain", "Kondisi darurat terdeteksi")
                    })

                fired_rules.append(trace_entry)

    # Normalisasi skor: cap maksimum di 1.0
    for disease in scores:
        scores[disease] = min(scores[disease], 1.0)

    # Kategorisasi keyakinan
    categorized_scores = []
    for disease, score in scores.items():
        if score >= 0.70:
            confidence = "Tinggi"
            confidence_class = "high"
        elif score >= 0.40:
            confidence = "Sedang"
            confidence_class = "medium"
        else:
            confidence = "Rendah"
            confidence_class = "low"

        categorized_scores.append({
            "disease": disease,
            "score": round(score, 3),
            "score_percent": round(score * 100, 1),
            "confidence": confidence,
            "confidence_class": confidence_class
        })

    # Sort berdasarkan skor tertinggi
    categorized_scores.sort(key=lambda x: x["score"], reverse=True)
    top_3 = categorized_scores[:3]

    # Tentukan apakah ada temuan yang cukup signifikan
    has_significant = any(s["score"] >= 0.40 for s in top_3)

    return {
        "facts": facts,
        "all_scores": categorized_scores,
        "top_3": top_3,
        "fired_rules": fired_rules,
        "red_flags": red_flags,
        "recommendations": recommendations,
        "has_significant": has_significant,
        "iterations": iteration,
        "total_rules_fired": len(fired_rules)
    }
