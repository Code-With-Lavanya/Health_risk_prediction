

import streamlit as st
import numpy as np
import pandas as pd
import time

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="VitalScan AI · Health Risk Predictor",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  (dark clinical-futuristic theme)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* ---------- RESET & ROOT ---------- */
:root {
    --bg:        #080d12;
    --surface:   #0e1621;
    --border:    #1e2e42;
    --accent:    #00e5ff;
    --accent2:   #ff3864;
    --accent3:   #39ff14;
    --text:      #cdd9e5;
    --muted:     #5a7085;
    --card-bg:   #0b1520;
    --danger:    #ff3864;
    --safe:      #39ff14;
    --warn:      #ffba08;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Syne', sans-serif;
    color: var(--text);
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 50% -10%, rgba(0,229,255,.08) 0%, transparent 70%),
        radial-gradient(ellipse 50% 40% at 100% 80%, rgba(255,56,100,.06) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ---------- HEADER ---------- */
.vitalscan-header {
    text-align: center;
    padding: 2.5rem 0 1rem;
    position: relative;
}
.vitalscan-header h1 {
    font-size: clamp(2.2rem, 5vw, 4rem);
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #00e5ff 0%, #ffffff 50%, #ff3864 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.vitalscan-header .tagline {
    font-family: 'Space Mono', monospace;
    font-size: .78rem;
    color: var(--muted);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: .4rem;
}
.pulse-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--accent3);
    box-shadow: 0 0 10px var(--accent3);
    animation: pulse 1.4s ease-in-out infinite;
    margin-right: 8px;
    vertical-align: middle;
}
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(.7)} }

/* ---------- SECTION LABELS ---------- */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: .65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    border-left: 2px solid var(--accent);
    padding-left: .6rem;
    margin-bottom: 1rem;
    margin-top: 2rem;
}

/* ---------- CARDS ---------- */
.card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent);
}

/* ---------- STREAMLIT OVERRIDES ---------- */
[data-testid="stSlider"] > div > div > div > div {
    background: var(--accent) !important;
}
[data-testid="stSlider"] > div > div {
    background: var(--border) !important;
}
div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}
div[data-baseweb="radio"] label, div[data-baseweb="checkbox"] label {
    color: var(--text) !important;
}
.stSelectbox label, .stSlider label, .stRadio label, .stNumberInput label {
    color: var(--muted) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: .72rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}
input[type="number"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
}
button[kind="primary"], .stButton > button {
    background: linear-gradient(135deg, #00e5ff22, #ff386422) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    padding: .65rem 2rem !important;
    font-size: .8rem !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    background: var(--accent) !important;
    color: var(--bg) !important;
    box-shadow: 0 0 20px rgba(0,229,255,.4) !important;
}

/* ---------- RESULT CARD ---------- */
.result-safe   { border-color: var(--safe)   !important; }
.result-warn   { border-color: var(--warn)   !important; }
.result-danger { border-color: var(--danger) !important; }

.result-safe::before   { background: linear-gradient(90deg, var(--safe),   transparent) !important; }
.result-warn::before   { background: linear-gradient(90deg, var(--warn),   transparent) !important; }
.result-danger::before { background: linear-gradient(90deg, var(--danger), transparent) !important; }

.risk-score {
    font-size: 5rem;
    font-weight: 800;
    font-family: 'Space Mono', monospace;
    line-height: 1;
}
.risk-label {
    font-size: 1.2rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: .3rem;
}

/* ---------- DISEASE TAG ---------- */
.disease-tag {
    display: inline-block;
    padding: .3rem .75rem;
    border-radius: 100px;
    font-family: 'Space Mono', monospace;
    font-size: .68rem;
    margin: .25rem;
    border: 1px solid;
}
.tag-high   { border-color: var(--danger); color: var(--danger); background: rgba(255,56,100,.08); }
.tag-medium { border-color: var(--warn);   color: var(--warn);   background: rgba(255,186,8,.08);  }
.tag-low    { border-color: var(--muted);  color: var(--muted);  background: transparent;           }

/* ---------- PROGRESS BAR OVERRIDE ---------- */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
}

/* ---------- DIVIDER ---------- */
hr { border-color: var(--border) !important; }

/* ---------- METRIC ---------- */
[data-testid="stMetric"] {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: .8rem 1rem;
}
[data-testid="stMetricValue"] { color: var(--accent) !important; font-family: 'Space Mono', monospace !important; }
[data-testid="stMetricLabel"] { color: var(--muted)  !important; font-size: .7rem !important; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="vitalscan-header">
    <h1>🫀 VitalScan AI</h1>
    <p class="tagline"><span class="pulse-dot"></span>Multi-Disease Risk Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin:0 0 2rem'>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HELPER: render section labels
# ─────────────────────────────────────────────
def section(text):
    st.markdown(f'<p class="section-label">{text}</p>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INPUT LAYOUT  (3-column grid)
# ─────────────────────────────────────────────
col_left, col_mid, col_right = st.columns([1, 1, 1], gap="large")

# ════════════════════════════════════════════
#  LEFT  — Demographics & Vitals
# ════════════════════════════════════════════
with col_left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("01 · Demographics & Vitals")

    age = st.slider("Age", min_value=1, max_value=100, value=35,
                    help="Patient age in years")

    gender = st.radio("Biological Sex", ["Male", "Female"],
                      horizontal=True)
    is_male = 1 if gender == "Male" else 0

    bmi = st.slider("BMI", min_value=10.0, max_value=55.0, value=24.5,
                    step=0.1, format="%.1f",
                    help="Body Mass Index (kg/m²)")

    # BMI indicator
    if bmi < 18.5:
        bmi_tag, bmi_color = "Underweight", "#00e5ff"
    elif bmi < 25:
        bmi_tag, bmi_color = "Normal", "#39ff14"
    elif bmi < 30:
        bmi_tag, bmi_color = "Overweight", "#ffba08"
    else:
        bmi_tag, bmi_color = "Obese", "#ff3864"

    st.markdown(f"""
    <div style="text-align:center; margin:-8px 0 8px;
         font-family:'Space Mono',monospace; font-size:.72rem;
         color:{bmi_color}; letter-spacing:2px;">
        ● {bmi_tag}
    </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Clinical Markers
    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("02 · Clinical Markers")

    bp = st.slider("Blood Pressure (mmHg)", 60, 200, 120,
                   help="Systolic blood pressure")
    cholesterol = st.slider("Cholesterol (mg/dL)", 100, 400, 190)
    glucose = st.slider("Glucose (mg/dL)", 50, 400, 100)

    # Quick status chips
    bp_status    = "⚠ High" if bp > 140 else ("✓ Normal" if bp >= 90 else "⚠ Low")
    chol_status  = "⚠ High" if cholesterol > 240 else "✓ Normal"
    gluc_status  = "⚠ High" if glucose > 125 else "✓ Normal"

    c1, c2, c3 = st.columns(3)
    c1.metric("BP", f"{bp}", bp_status)
    c2.metric("Chol", f"{cholesterol}", chol_status)
    c3.metric("Gluc", f"{glucose}", gluc_status)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
#  MIDDLE — Lifestyle
# ════════════════════════════════════════════
with col_mid:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("03 · Lifestyle Factors")

    smoking_map = {"Never": 0, "Ex-smoker": 1, "Current smoker": 2}
    smoking_sel = st.selectbox("Smoking Status",
                               list(smoking_map.keys()))
    smoking = smoking_map[smoking_sel]

    alcohol_map = {"None": 0, "Occasional": 1, "Regular": 2, "Heavy": 3}
    alcohol_sel = st.selectbox("Alcohol Consumption",
                               list(alcohol_map.keys()))
    alcohol = alcohol_map[alcohol_sel]

    exercise_map = {"Sedentary": 0, "Light (1-2×/wk)": 1,
                    "Moderate (3-4×/wk)": 2, "Active (5+×/wk)": 3}
    exercise_sel = st.selectbox("Exercise Frequency",
                                list(exercise_map.keys()))
    exercise = exercise_map[exercise_sel]

    # Visual lifestyle score
    lifestyle_score = max(0, (exercise * 25) - (smoking * 15) - (alcohol * 10))
    st.markdown(f"""
    <div style="margin-top:1rem">
        <p style="font-family:'Space Mono',monospace;font-size:.65rem;
           color:var(--muted);letter-spacing:2px;margin-bottom:.4rem">
           LIFESTYLE HEALTH INDEX</p>
    </div>""", unsafe_allow_html=True)
    st.progress(min(lifestyle_score / 75, 1.0))
    st.markdown(f"""
    <p style="font-family:'Space Mono',monospace;font-size:.8rem;
       color:{'#39ff14' if lifestyle_score>50 else '#ffba08' if lifestyle_score>25 else '#ff3864'};
       text-align:right; margin-top:-.5rem">{lifestyle_score}/75</p>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Family History
    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("04 · Family History")

    family_history = st.toggle("Known family medical history",
                               value=False,
                               help="Has a close blood relative been diagnosed with serious illness?")

    if family_history:
        st.markdown("""
        <div style="background:rgba(255,56,100,.07);border:1px solid rgba(255,56,100,.3);
             border-radius:8px;padding:.7rem .9rem;margin-top:.5rem;
             font-size:.78rem;color:#ff9ab0;">
            ⚡ Elevated genetic risk profile detected.
            Additional screening recommended.
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
#  RIGHT — Pre-existing Conditions
# ════════════════════════════════════════════
with col_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("05 · Pre-existing Conditions")

    conditions = {
        "Heart Disease":        "🫀",
        "Diabetes":             "🩸",
        "Stroke":               "🧠",
        "Kidney Disease":       "🫘",
        "Cancer":               "⚕",
        "Alzheimer's Disease":  "🔮",
        "COPD":                 "🫁",
        "Liver Disease":        "🟡",
        "Parkinson's Disease":  "⚡",
        "Tuberculosis":         "🦠",
    }

    condition_values = {}
    for cond, icon in conditions.items():
        val = st.toggle(f"{icon}  {cond}", value=False)
        condition_values[cond] = int(val)

    active_count = sum(condition_values.values())
    if active_count > 0:
        st.markdown(f"""
        <div style="margin-top:.5rem;
             font-family:'Space Mono',monospace;font-size:.72rem;
             color:#ffba08;letter-spacing:1px">
            {active_count} condition{'s' if active_count>1 else ''} flagged
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PREDICT BUTTON
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([2, 1, 2])

with btn_col:
    predict_btn = st.button("⟶  Run Analysis", use_container_width=True)

# ─────────────────────────────────────────────
#  PREDICTION LOGIC (mock — plug your model in)
# ─────────────────────────────────────────────
if predict_btn:

    with st.spinner(""):
        # ── Build feature vector
        feature_vector = np.array([[
            age, is_male, bp, cholesterol, glucose,
            smoking, alcohol, exercise, bmi,
            int(family_history),
            condition_values["Heart Disease"],
            condition_values["Diabetes"],
            condition_values["Stroke"],
            condition_values["Kidney Disease"],
            condition_values["Cancer"],
            condition_values["Alzheimer's Disease"],
            condition_values["COPD"],
            condition_values["Liver Disease"],
            condition_values["Parkinson's Disease"],
            condition_values["Tuberculosis"],
        ]])

        # ── MOCK RISK COMPUTATION
        # Replace everything below with:
        #   prediction = your_model.predict(feature_vector)[0]
        #   probability = your_model.predict_proba(feature_vector)[0][1]
        # ─────────────────────────────────────────────────────
        base = 0
        if age > 60: base += 20
        elif age > 40: base += 10
        if bp > 140: base += 15
        if cholesterol > 240: base += 12
        if glucose > 125: base += 10
        if smoking == 2: base += 15
        elif smoking == 1: base += 5
        if bmi > 30: base += 10
        elif bmi < 18.5: base += 5
        if family_history: base += 8
        base += active_count * 10
        base += alcohol * 5
        base = max(0, base - exercise * 5)
        probability = min(base / 100, 0.99)
        # ─────────────────────────────────────────────────────

        time.sleep(1.2)  # remove in production

    # ── RESULT DISPLAY
    st.markdown("<hr style='margin: 1.5rem 0'>", unsafe_allow_html=True)
    section("Diagnostic Report")

    risk_pct = int(probability * 100)
    if risk_pct < 30:
        level, color, card_cls = "LOW RISK", "#39ff14", "result-safe"
        emoji = "✅"
    elif risk_pct < 60:
        level, color, card_cls = "MODERATE RISK", "#ffba08", "result-warn"
        emoji = "⚠️"
    else:
        level, color, card_cls = "HIGH RISK", "#ff3864", "result-danger"
        emoji = "🚨"

    r1, r2 = st.columns([1, 2], gap="large")

    with r1:
        st.markdown(f"""
        <div class="card {card_cls}" style="text-align:center;padding:2rem">
            <p style="font-family:'Space Mono',monospace;font-size:.65rem;
               color:var(--muted);letter-spacing:3px;margin-bottom:.5rem">
               RISK PROBABILITY</p>
            <div class="risk-score" style="color:{color}">{risk_pct}<span style="font-size:2rem">%</span></div>
            <div class="risk-label" style="color:{color}">{emoji} {level}</div>
            <p style="font-family:'Space Mono',monospace;font-size:.62rem;
               color:var(--muted);margin-top:1rem;letter-spacing:1px">
               OVERALL HEALTH RISK SCORE</p>
        </div>""", unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
        <div class="card" style="height:100%">
            <p style="font-family:'Space Mono',monospace;font-size:.65rem;
               color:var(--muted);letter-spacing:3px;margin-bottom:.8rem">
               PATIENT SUMMARY VECTOR</p>
        """, unsafe_allow_html=True)

        # Summary metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Age", age)
        m2.metric("BMI", f"{bmi:.1f}")
        m3.metric("BP", bp)
        m4.metric("Glucose", glucose)

        # Conditions flagged
        flagged = [k for k, v in condition_values.items() if v == 1]
        if flagged:
            st.markdown("<p style='font-family:Space Mono,monospace;font-size:.65rem;"
                        "color:var(--muted);letter-spacing:2px;margin-top:.8rem'>FLAGGED CONDITIONS</p>",
                        unsafe_allow_html=True)
            tags_html = "".join(
                f'<span class="disease-tag tag-high">{c}</span>' for c in flagged
            )
            st.markdown(tags_html, unsafe_allow_html=True)

        # Lifestyle tags
        lifestyle_tags = []
        if smoking > 0: lifestyle_tags.append(("Smoker", "tag-medium" if smoking==1 else "tag-high"))
        if alcohol > 1: lifestyle_tags.append(("Alcohol", "tag-medium" if alcohol==2 else "tag-high"))
        if exercise >= 2: lifestyle_tags.append(("Active", "tag-low"))
        if family_history: lifestyle_tags.append(("Family Hx", "tag-medium"))

        if lifestyle_tags:
            st.markdown("<p style='font-family:Space Mono,monospace;font-size:.65rem;"
                        "color:var(--muted);letter-spacing:2px;margin-top:.5rem'>LIFESTYLE FLAGS</p>",
                        unsafe_allow_html=True)
            tags_html2 = "".join(
                f'<span class="disease-tag {cls}">{lbl}</span>' for lbl, cls in lifestyle_tags
            )
            st.markdown(tags_html2, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── RECOMMENDATIONS
    st.markdown("<br>", unsafe_allow_html=True)
    section("Clinical Insights")

    ins_cols = st.columns(3)
    insights = []

    if bp > 140:
        insights.append(("🩺", "Blood Pressure", "Hypertension detected. Lifestyle changes and medication review advised.", "tag-high"))
    if bmi > 30:
        insights.append(("⚖️", "Weight Management", "BMI indicates obesity. Dietary and exercise interventions recommended.", "tag-high"))
    if glucose > 125:
        insights.append(("🩸", "Glucose Control", "Elevated fasting glucose. Diabetes screening strongly recommended.", "tag-high"))
    if smoking == 2:
        insights.append(("🚬", "Smoking Cessation", "Active smoking significantly elevates cardiovascular and cancer risk.", "tag-high"))
    if cholesterol > 240:
        insights.append(("🫀", "Cholesterol", "High LDL risk marker. Consider lipid panel and dietary changes.", "tag-medium"))
    if exercise == 0:
        insights.append(("🏃", "Physical Activity", "Sedentary lifestyle detected. Even light daily activity has measurable benefits.", "tag-medium"))
    if not insights:
        insights.append(("✅", "Profile Looks Healthy", "No critical risk markers flagged. Continue current health habits.", "tag-low"))

    for i, (ico, title, desc, cls) in enumerate(insights[:3]):
        with ins_cols[i % 3]:
            clr = "#ff3864" if cls=="tag-high" else "#ffba08" if cls=="tag-medium" else "#39ff14"
            st.markdown(f"""
            <div class="card" style="border-color:{clr}33">
                <div style="font-size:1.6rem;margin-bottom:.5rem">{ico}</div>
                <div style="font-weight:700;font-size:.9rem;color:{clr};margin-bottom:.4rem">{title}</div>
                <div style="font-size:.8rem;color:var(--muted);line-height:1.5">{desc}</div>
            </div>""", unsafe_allow_html=True)

    # ── RAW VECTOR (expandable)
    with st.expander("🔬  View Raw Feature Vector"):
        feature_df = pd.DataFrame(feature_vector, columns=[
            'Age','Is_Male','Blood Pressure','Cholesterol','Glucose',
            'Smoking','Alcohol Consumption','Exercise','BMI','Family History',
            'Heart Disease','Diabetes','Stroke','Kidney Disease','Cancer',
            "Alzheimer's Disease",'COPD','Liver Disease',
            "Parkinson's Disease",'Tuberculosis'
        ])
        st.dataframe(feature_df, use_container_width=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;font-family:'Space Mono',monospace;
     font-size:.62rem;color:#2a3f55;letter-spacing:2px">
    VITALSCAN AI · FOR RESEARCH USE ONLY · NOT A MEDICAL DEVICE<br>
    Always consult a qualified healthcare professional for diagnosis and treatment.
</div>
""", unsafe_allow_html=True)

