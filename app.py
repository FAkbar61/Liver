"""
app.py — Flask Application
Sistem Pakar Identifikasi Penyakit Liver
"""

import json
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for

from engine import run_inference, load_rules

app = Flask(__name__)
app.secret_key = "liver_expert_system_2024"

# Path ke file data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RULES_PATH = os.path.join(DATA_DIR, "rules.json")
SYMPTOMS_PATH = os.path.join(DATA_DIR, "symptoms.json")


def load_symptoms():
    with open(SYMPTOMS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_rules():
    return load_rules(RULES_PATH)


@app.route("/", methods=["GET"])
def index():
    """Halaman utama — form pertanyaan gejala."""
    symptoms = load_symptoms()

    # Kelompokkan berdasarkan kategori
    categories = {}
    for s in symptoms:
        cat = s.get("category", "Lainnya")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(s)

    return render_template("index.html", symptoms=symptoms, categories=categories)


@app.route("/result", methods=["POST"])
def result():
    """Terima form, jalankan inferensi, tampilkan hasil."""
    symptoms = load_symptoms()
    symptom_ids = [s["id"] for s in symptoms]

    # Parse input: checkbox = true jika diceklis
    initial_facts = {}
    for sid in symptom_ids:
        value = request.form.get(sid)
        initial_facts[sid] = (value == "true" or value == "on" or value == "1")

    # Validasi: minimal 1 gejala dipilih (tidak hitung riwayat saja)
    main_symptom_ids = [s["id"] for s in symptoms if s.get("category") not in ["Riwayat Medis", "Hasil Pemeriksaan"]]
    has_any_main = any(initial_facts.get(sid, False) for sid in main_symptom_ids)

    # Jalankan forward chaining
    rules = get_rules()
    result_data = run_inference(initial_facts, rules)

    # Siapkan data gejala yang dipilih untuk tampilan
    selected_symptoms = []
    for s in symptoms:
        if initial_facts.get(s["id"], False):
            selected_symptoms.append(s)

    return render_template(
        "result.html",
        result=result_data,
        selected_symptoms=selected_symptoms,
        initial_facts=initial_facts,
        has_any_main=has_any_main
    )


@app.route("/admin/rules", methods=["GET"])
def admin_rules():
    """Halaman admin — tampilkan rules JSON (read-only)."""
    rules = get_rules()
    symptoms = load_symptoms()

    # Statistik
    red_flag_rules = [r for r in rules if r.get("red_flag", False)]
    groups = {}
    for r in rules:
        g = r.get("group", "Lainnya")
        groups[g] = groups.get(g, 0) + 1

    stats = {
        "total_rules": len(rules),
        "total_symptoms": len(symptoms),
        "red_flag_count": len(red_flag_rules),
        "groups": groups
    }

    return render_template("admin_rules.html", rules=rules, symptoms=symptoms, stats=stats)


@app.route("/api/infer", methods=["POST"])
def api_infer():
    """API endpoint untuk inferensi (JSON in, JSON out)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body harus berupa JSON"}), 400

    initial_facts = data.get("facts", {})
    rules = get_rules()
    result_data = run_inference(initial_facts, rules)

    return jsonify(result_data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
