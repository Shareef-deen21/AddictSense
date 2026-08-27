
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from utils import (
    inject_css, PALETTE as P,
    LEVEL_COLORS, LEVEL_ICONS, LEVEL_ADVICE, LEVEL_ALTERNATIVES,
    FEATURE_DISPLAY_NAMES,
)

st.set_page_config(
    page_title="AddictSence Prediction",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()

st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
.block-container { max-width: 1080px !important; padding-top: 1.2rem !important; }
</style>
""", unsafe_allow_html=True)

#Auth guard
if not st.session_state.get("authenticated"):
    st.switch_page("pages/2_Login.py")

#All 8 platforms from dataset
ALL_PLATFORMS = [
    "Select…",
    "Facebook", "Instagram", "WhatsApp", "YouTube", "LinkedIn",
    "Snapchat", "TikTok", "Twitter",
]

#All countries
ALL_COUNTRIES = [
    "Select…",
    "Afghanistan","Albania","Andorra","Argentina","Armenia","Australia","Austria",
    "Azerbaijan","Bahamas","Bahrain","Bangladesh","Belarus","Belgium","Bhutan",
    "Bolivia","Bosnia","Brazil","Bulgaria","Canada","Chile","China","Colombia",
    "Costa Rica","Croatia","Cyprus","Czech Republic","Denmark","Ecuador","Egypt",
    "Estonia","Finland","France","Georgia","Germany","Ghana","Greece","Hong Kong",
    "Hungary","Iceland","India","Indonesia","Iraq","Ireland","Italy",
    "Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kosovo","Kuwait","Kyrgyzstan",
    "Latvia","Lebanon","Lithuania","Luxembourg","Malaysia","Maldives","Malta",
    "Mexico","Moldova","Morocco","Nepal","Netherlands","New Zealand","Nigeria",
    "Norway","Oman","Pakistan","Panama","Paraguay","Palestine","Peru","Philippines","Poland",
    "Portugal","Qatar","Romania","Russia","Serbia","Singapore","Slovakia",
    "Slovenia","South Africa","South Korea","Spain","Sri Lanka","Sweden",
    "Switzerland","Taiwan","Thailand","Turkey","UAE","UK","USA","Ukraine",
    "Uruguay","Uzbekistan","Venezuela","Vietnam","Other",
]

#Load artifacts, fully safe with per-model error handling
@st.cache_resource(show_spinner=False)
def load_artifacts():
    base       = os.path.dirname(os.path.dirname(__file__))
    models_dir = os.path.join(base, "models")


    meta_path = os.path.join(models_dir, "metadata.json")
    if not os.path.exists(meta_path):
        st.error("models/metadata.json not found. Run the notebook first.")
        st.stop()

    with open(meta_path) as f:
        meta = json.load(f)


    encoders = joblib.load(os.path.join(models_dir, "label_encoders.pkl"))
    scaler   = joblib.load(os.path.join(models_dir, "scaler.pkl"))

    #model loading map
    mdl_map = {
        "Random Forest":       ("random_forest_tuned.pkl",       "random_forest_model.pkl",       False),
        "XGBoost":             ("xgboost_tuned.json",            "xgboost_model.json",            True),
        "LightGBM":            ("lightgbm_tuned.pkl",            "lightgbm_model.pkl",            False),
        "CatBoost":            ("catboost_model.pkl",            "catboost_model.pkl",            False),
        "Logistic Regression": ("logistic_regression_model.pkl", "logistic_regression_model.pkl", False),
    }

    models     = {}
    model_tags = {}
    skipped    = []

    for display_name, (tuned_file, fallback_file, is_xgb) in mdl_map.items():
        tuned_path    = os.path.join(models_dir, tuned_file)
        fallback_path = os.path.join(models_dir, fallback_file)

        loaded    = False
        tag       = ""


        for path, label in [(tuned_path, "Tuned"), (fallback_path, "Non-Tuned")]:
            if not os.path.exists(path):
                continue
            try:
                if is_xgb:
                    from xgboost import XGBClassifier
                    mdl = XGBClassifier()
                    mdl.load_model(path)
                else:
                    mdl = joblib.load(path)

                models[display_name]     = mdl
                model_tags[display_name] = label
                loaded = True
                break

            except Exception as e:
                continue

        if not loaded:
            skipped.append(display_name)

    return meta, encoders, scaler, models, model_tags, skipped


#Run loader show clear error if it fails
try:
    meta, encoders, scaler, trained_models, model_tags, skipped_models = load_artifacts()
except Exception as e:
    st.error(f"Failed to load model artifacts: {e}")
    st.info("Make sure you have run the notebook and downloaded all files to the models/ folder.")
    st.stop()

# ── Guard: stop if no models loaded at all ────────────────────────────────────
if not trained_models:
    st.error("No models could be loaded from the models/ folder.")
    st.info("""
    **Common causes:**
    - models/ folder is empty or missing
    - All .pkl files are version-incompatible
    - XGBoost .json files are missing (save with `.save_model()` in notebook)

    **Run this in your notebook to resave XGBoost:**
```python
    model.save_model('models/xgboost_tuned.json')
```
    """)
    st.stop()

#Show warning for any skipped models
if skipped_models:
    st.warning(
        f"These models could not be loaded (version mismatch or corrupted file): "
        f"{', '.join(skipped_models)}. They have been excluded from the selector."
    )

FEATURE_COLS = meta["feature_cols"]
CAT_FEATURES = meta["cat_features"]
LABEL_MAP    = {int(k): v for k, v in meta["label_map"].items()}
MODEL_SCORES = meta.get("model_scores", {})


#SHAP helper
def compute_shap_values(model, input_arr, model_name, pred_class):
    import shap


    if model_name in ("XGBoost", "CatBoost", "LightGBM", "Random Forest"):
        try:
            explainer = shap.TreeExplainer(model)
            shap_vals = explainer.shap_values(input_arr)

            if isinstance(shap_vals, list):
                # Random Forest: list[n_classes] each (n_samples, n_features)
                class_shap = np.array(shap_vals[pred_class][0])
            elif shap_vals.ndim == 3:
                # XGBoost / LightGBM: (n_samples, n_features, n_classes)
                class_shap = shap_vals[0, :, pred_class]
            else:
                class_shap = shap_vals[0]

            return list(zip(FEATURE_COLS, class_shap.tolist())), "shap"

        except Exception:
            pass


    if model_name == "Logistic Regression":
        try:

            background = np.zeros((1, input_arr.shape[1]))

            explainer = shap.LinearExplainer(
                model,
                background,
                feature_perturbation="interventional",
            )
            shap_vals = explainer.shap_values(input_arr)


            if isinstance(shap_vals, list):

                class_shap = np.array(shap_vals[pred_class][0])
            elif shap_vals.ndim == 2:

                class_shap = shap_vals[0]
            else:
                class_shap = np.array(shap_vals).flatten()

            return list(zip(FEATURE_COLS, class_shap.tolist())), "shap"

        except Exception:
            pass

        try:
            coef        = model.coef_[pred_class]
            input_flat  = input_arr[0]
            contributions = [
                (feat, float(coef[i]) * float(input_flat[i]))
                for i, feat in enumerate(FEATURE_COLS)
            ]
            return contributions, "coef"

        except Exception:
            pass


    try:
        if hasattr(model, "feature_importances_"):
            importance = model.feature_importances_
            signed = [
                (feat, float(importance[i]) * (1 if float(input_arr[0, i]) > 0 else -1))
                for i, feat in enumerate(FEATURE_COLS)
            ]
            return signed, "importance"
    except Exception:
        pass

    return [(f, 0.0) for f in FEATURE_COLS], "none"


#SHAP chart renderer
def render_shap_chart(shap_pairs, pred_label, model_name, source):
    sorted_pairs = sorted(shap_pairs, key=lambda x: abs(x[1]), reverse=True)[:8]
    sorted_pairs = sorted(sorted_pairs, key=lambda x: x[1])

    features    = [FEATURE_DISPLAY_NAMES.get(f, f) for f, _ in sorted_pairs]
    values      = [v for _, v in sorted_pairs]
    level_color = LEVEL_COLORS[pred_label]
    max_abs     = max(abs(v) for v in values) if values else 1.0

    fig, ax = plt.subplots(figsize=(6, 3.8))
    fig.patch.set_facecolor(P["card"])
    ax.set_facecolor(P["card"])

    colors = [level_color if v >= 0 else P["primary"] for v in values]
    bars   = ax.barh(features, values, color=colors, height=0.58,
                     edgecolor="none", zorder=2)

    for bar, val in zip(bars, values):
        offset = max_abs * 0.03
        x_pos  = val + offset if val >= 0 else val - offset
        ha     = "left" if val >= 0 else "right"
        ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
                f"{val:+.3f}", va="center", ha=ha,
                fontsize=7.5, color=P["text"], fontweight="600")

    ax.axvline(0, color=P["border"], linewidth=1, zorder=1)
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color=P["border"], linewidth=0.4, alpha=0.6)
    ax.yaxis.grid(False)
    ax.tick_params(axis="y", labelsize=8, colors=P["text"],  length=0)
    ax.tick_params(axis="x", labelsize=7, colors=P["muted"], length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    title_suffix = "SHAP Values" if source == "shap" else "Feature Impact"
    ax.set_title(f" {title_suffix}  ({pred_label}) Risk",
                 color=P["text"], fontsize=9, fontweight="700",
                 loc="left", pad=10)

    pos_patch = mpatches.Patch(color=level_color,   label="↑ Increases risk")
    neg_patch = mpatches.Patch(color=P["primary"],   label="↓ Decreases risk")
    ax.legend(handles=[pos_patch, neg_patch], fontsize=7, loc="lower right",
              facecolor=P["surface"], edgecolor=P["border"],
              labelcolor=P["text"], framealpha=0.9)

    plt.tight_layout(pad=0.6)
    return fig


#Nav Bar
nav_l, nav_r = st.columns([6, 1])
with nav_l:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;padding:0.4rem 0 1.4rem 0;margin-bottom:0;">
        <span style="font-family:'Space Grotesk',sans-serif;font-size:1.8rem;
                     font-weight:700;color:{P['white']};letter-spacing:-0.02em;">
            Addict<span style="color:{P['primary_lt']};">Sence</span>
        </span>
        <span style="color:{P['border']};margin:0 0.4rem;">·</span>
        <span style="color:{P['muted']};font-size:0.88rem;">Prediction</span>
        <span style="margin-left:auto;color:{P['muted']};font-size:0.82rem;">
            Signed in as <strong style="color:{P['text']};">
            {st.session_state.get('username','user')}</strong>
        </span>
    </div>
    """, unsafe_allow_html=True)
with nav_r:
    if st.button("Sign Out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username      = ""
        st.switch_page("pages/2_Login.py")

# Full-width line
st.markdown(f"""
<div style="
    width:100%;
    border-bottom:1px solid {P['border']};
    margin-bottom:1.3rem;
">
</div>
""", unsafe_allow_html=True)

#Page header
st.markdown(f"""
<div style="margin-bottom:1.8rem;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:1.65rem;
                font-weight:800;color:{P['white']};letter-spacing:-0.02em;">
        Social Media Addiction Assessment
    </div>
    <div style="color:{P['muted']};font-size:0.93rem;margin-top:0.35rem;">
        Complete all fields below. The model will predict your risk level with
        SHAP explainability, clinical recommendations, and lifestyle alternatives.
    </div>
</div>
""", unsafe_allow_html=True)


#Input Form  (left column)

form_col, result_col = st.columns([1.05, 0.95], gap="large")

with form_col:

    #Student profile
    st.markdown(f"""
    <div style="background:{P['card']};border:1px solid {P['border']};
                border-radius:16px;padding:1.6rem 1.6rem 0.5rem 1.6rem;
                margin-bottom:1rem;">
        <div style="font-size:0.8rem;font-weight:700;letter-spacing:0.1em;
                    ;color:{P['primary_lt']};
                    margin-bottom:1.2rem;">Profile</div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Age", min_value=10, max_value=60, value=20, step=1)
    with c2:
        # FIX 1: removed "Non-binary" — only Male / Female in training data
        gender = st.selectbox("Gender", ["Select…", "Male", "Female"])

    c3, c4 = st.columns(2)
    with c3:

        academic_level = st.selectbox("Academic Level",
            ["Select…", "High School", "Undergraduate", "Graduate"])
    with c4:

        country = st.selectbox("Country", ALL_COUNTRIES)

    relationship_status = st.selectbox("Relationship Status",
        ["Select…", "Single", "In Relationship", "Complicated"])

    st.markdown("</div>", unsafe_allow_html=True)

    #Usage habits
    st.markdown(f"""
    <div style="background:{P['card']};border:1px solid {P['border']};
                border-radius:16px;padding:1.6rem 1.6rem 0.5rem 1.6rem;
                margin-bottom:1rem;">
        <div style="font-size:0.8rem;font-weight:700;letter-spacing:0.1em;
                    color:{P['primary_lt']};
                    margin-bottom:1.2rem;">Usage Habits</div>
    """, unsafe_allow_html=True)

    avg_hours = st.slider(
        "Average Daily Social Media Usage (hours)",
        min_value=0.0, max_value=16.0, value=3.0, step=0.5,
        help="Include all platforms combined.",
    )


    most_used = st.selectbox("Most Used Platform", [
        "Select…",
        "Facebook", "Instagram", "WhatsApp", "YouTube", "LinkedIn",
        "Snapchat", "TikTok", "Twitter",
    ])

    c5, c6 = st.columns(2)
    with c5:
        sleep_hours = st.number_input("Sleep Hours Per Night",
            min_value=0.0, max_value=12.0, value=7.0, step=0.5)
    with c6:
        conflicts = st.number_input("Social Media Conflicts / Week",
            min_value=0, max_value=20, value=1, step=1,
            help="Arguments or tensions caused by your social media use.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Wellbeing & Academics
    st.markdown(f"""
    <div style="background:{P['card']};border:1px solid {P['border']};
                border-radius:16px;padding:1.6rem 1.6rem 0.5rem 1.6rem;
                margin-bottom:1rem;">
        <div style="font-size:0.8rem;font-weight:700;letter-spacing:0.1em;
                    color:{P['primary_lt']};
                    margin-bottom:1.2rem;">Wellbeing & Academics</div>
    """, unsafe_allow_html=True)

    mental_health = st.slider(
        "Mental health score  (1 = very poor · 10 = excellent)",
        min_value=1, max_value=10, value=7,
        help="Your self-assessed mental wellbeing on a scale of 1–10.",
    )
    affects_academic = st.radio(
        "Does social media negatively affect your academic or career performance?",
        options=["No", "Yes"], horizontal=True, index=0,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    #Model Selector
    st.markdown(f"""
    <div style="background:{P['card']};border:1px solid {P['border']};
                border-radius:16px;padding:1.4rem 1.6rem 1rem 1.6rem;
                margin-bottom:1.2rem;">
        <div style="font-size:0.8rem;font-weight:700;letter-spacing:0.1em;
                    color:{P['primary_lt']};
                    margin-bottom:0.9rem;">Model Selection</div>
    """, unsafe_allow_html=True)

    model_choice = st.selectbox(
        "Choose Algorithm",
        list(trained_models.keys()),
        index=0,
        help="Random Forest is the best-performing model.",
    )

    # Show metric cards from metadata
    score_key = model_choice
    if score_key not in MODEL_SCORES and f"{model_choice} (Tuned)" in MODEL_SCORES:
        score_key = f"{model_choice} (Tuned)"
    if MODEL_SCORES and score_key in MODEL_SCORES:
        sc = MODEL_SCORES[score_key]
        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("Accuracy", f"{sc['accuracy']*100:.1f}%")
        mc2.metric("F1 Score", f"{sc['f1']*100:.1f}%")
        mc3.metric("ROC-AUC",  f"{sc['roc_auc']*100:.1f}%")

    shap_enabled = st.toggle(
        "Enable SHAP Explainability", value=True,
        help="Shows which features drove this prediction. Adds ~1–2 seconds.",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    predict_btn = st.button("Run Prediction", use_container_width=True)


#Results (right column)

with result_col:

    if not predict_btn:
        #Idle placeholder
        st.markdown(f"""
        <div style="background:{P['card']};border:1px solid {P['border']};
                    border-radius:16px;padding:3rem 2rem;text-align:center;
                    color:{P['muted']};">
            <div style="font-size:2.5rem;margin-bottom:1rem;"></div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:1rem;
                        font-weight:600;color:{P['text']};margin-bottom:0.5rem;">
                Awaiting Input
            </div>
            <div style="font-size:0.85rem;line-height:1.6;">
                Fill in your details on the left and click<br>
                <strong style="color:{P['primary_lt']};">Run Prediction</strong>
                to see your results.
            </div>
        </div>
        <div style="background:{P['card']};border:1px solid {P['border']};
                    border-radius:16px;padding:1.4rem;margin-top:1rem;">
            <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;
                        text-transform:uppercase;color:{P['primary_lt']};
                        margin-bottom:1rem;">Risk Level Guide</div>
            {''.join([
                f"""<div style="display:flex;align-items:center;gap:10px;
                                margin-bottom:0.7rem;">
                    <div style="width:10px;height:10px;border-radius:50%;
                                background:{color};flex-shrink:0;"></div>
                    <div>
                        <span style="font-weight:600;color:{P['white']};
                                     font-size:0.88rem;">{level}</span>
                        <span style="color:{P['muted']};font-size:0.8rem;
                                     margin-left:6px;">{desc}</span>
                    </div>
                </div>"""
                for level, color, desc in [
                    ("Low",      "#22C55E", "Healthy balanced usage"),
                    ("Moderate", "#F59E0B", "Some over-reliance signs"),
                    ("High",     "#F97316", "Significant dependency"),
                    ("Severe",   "#EF4444", "Requires intervention"),
                ]
            ])}
        </div>
        """, unsafe_allow_html=True)

    else:
        #Validation
        errors, warns = [], []

        if gender            == "Select…": errors.append("Please select your gender.")
        if academic_level    == "Select…": errors.append("Please select your academic level.")
        if country           == "Select…": errors.append("Please select your country.")
        if relationship_status == "Select…": errors.append("Please select your relationship status.")
        if most_used         == "Select…": errors.append("Please select your most used platform.")
        if not (10 <= age <= 60):          errors.append("Age must be between 10 and 60.")
        if not (0  <= sleep_hours <= 12):  errors.append("Sleep hours must be between 0 and 12.")
        if not (0  <= conflicts <= 20):    errors.append("Conflicts must be between 0 and 20.")
        if avg_hours > 12:
            warns.append("Very high daily usage (>12 h), want to be more concern in your daily usage.")
        if sleep_hours < 4:
            warns.append("Sleep < 4 h/night may indicate other health concerns beyond social media.")

        if errors:
            st.markdown(f"""
            <div style="background:{P['danger']}15;border:1px solid {P['danger']}44;
                        border-radius:14px;padding:1.2rem 1.4rem;margin-bottom:1rem;">
                <div style="font-weight:700;color:#FCA5A5;margin-bottom:0.6rem;">
                    Please fix the following:
                </div>
                {''.join([
                    f'<div style="font-size:0.86rem;color:#FCA5A5;margin-bottom:0.3rem;">'
                    f'• {e}</div>'
                    for e in errors
                ])}
            </div>
            """, unsafe_allow_html=True)

        elif model_choice not in trained_models:
            st.markdown(
                f'<div class="as-error">Model "{model_choice}" not loaded. '
                f'Run the notebook first.</div>',
                unsafe_allow_html=True,
            )

        else:
            #Non-blocking warnings
            for w in warns:
                st.markdown(f"""
                <div style="background:{P['warning']}15;border:1px solid {P['warning']}44;
                            border-radius:10px;padding:0.7rem 1rem;margin-bottom:0.5rem;
                            font-size:0.83rem;color:#FDE68A;">⚡ {w}</div>
                """, unsafe_allow_html=True)

            #Build feature vector
            affects_int = 1 if affects_academic == "Yes" else 0
            raw_input   = {
                "Age":                          age,
                "Gender":                       gender,
                "Academic_Level":               academic_level,
                "Country":                      country,
                "Avg_Daily_Usage_Hours":        avg_hours,
                "Most_Used_Platform":           most_used,
                "Affects_Academic_Performance": affects_int,
                "Sleep_Hours_Per_Night":        sleep_hours,
                "Mental_Health_Score":          float(mental_health),
                "Relationship_Status":          relationship_status,
                "Conflicts_Over_Social_Media":  conflicts,
            }

            input_df = pd.DataFrame([raw_input])

            for col in CAT_FEATURES:
                le  = encoders[col]
                val = str(raw_input[col])
                if val not in le.classes_:
                    val = le.classes_[0]          # silent fallback
                input_df[col] = le.transform([val])

            input_arr = input_df[FEATURE_COLS].values.astype(float)


            model         = trained_models[model_choice]
            input_arr_use = (scaler.transform(input_arr)
                             if model_choice == "Logistic Regression"
                             else input_arr)

            #Inference
            raw_pred = model.predict(input_arr_use)
            pred_class = int(np.array(raw_pred).flatten()[0])
            pred_proba = model.predict_proba(input_arr_use)[0]
            pred_label = LABEL_MAP[pred_class]
            confidence = float(pred_proba[pred_class]) * 100
            level_color = LEVEL_COLORS[pred_label]
            level_icon = LEVEL_ICONS[pred_label]

            #Result card
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{level_color}18,{P['card']});
                        border:1.5px solid {level_color}55;border-radius:16px;
                        padding:1.8rem;margin-bottom:1rem;text-align:center;">
                <div style="font-size:2.8rem;margin-bottom:0.5rem;">{level_icon}</div>
                <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;
                            text-transform:uppercase;color:{P['muted']};
                            margin-bottom:0.3rem;">Addiction Risk Level</div>
                <div style="font-family:'Space Grotesk',sans-serif;font-size:2rem;
                            font-weight:800;color:{level_color};
                            letter-spacing:-0.02em;">{pred_label}</div>
                <div style="color:{P['muted']};font-size:0.85rem;margin-top:0.4rem;">
                    Confidence: <strong style="color:{P['text']};">{confidence:.1f}%</strong>
                    &nbsp;·&nbsp; Model:
                    <strong style="color:{P['text']};">{model_choice}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            #Tabs
            t1, t2, t3, t4 = st.tabs([
                "Probabilities", "Why This?",
                "Advice",        "Alternatives",
            ])

            # Tab 1 probabilities
            with t1:
                st.markdown(f"""
                <div style="padding:0.2rem 0 0.8rem 0;">
                    {''.join([
                        f"""<div style="margin-bottom:0.9rem;">
                            <div style="display:flex;justify-content:space-between;
                                        font-size:0.84rem;margin-bottom:0.3rem;">
                                <span style="color:{LEVEL_COLORS[LABEL_MAP[i]]};
                                             font-weight:600;">
                                    {LEVEL_ICONS[LABEL_MAP[i]]} {LABEL_MAP[i]}
                                </span>
                                <span style="color:{P['text']};font-weight:700;">
                                    {pred_proba[i]*100:.1f}%
                                </span>
                            </div>
                            <div style="background:{P['border']};border-radius:999px;
                                        height:8px;">
                                <div style="width:{pred_proba[i]*100:.1f}%;height:8px;
                                            border-radius:999px;
                                            background:{LEVEL_COLORS[LABEL_MAP[i]]};"></div>
                            </div>
                        </div>"""
                        for i in range(4)
                    ])}
                </div>
                <hr style="border:none;border-top:1px solid {P['border']};margin:0.8rem 0;">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;
                            padding-bottom:0.5rem;">
                    {''.join([
                        f"""<div style="font-size:0.82rem;">
                            <span style="color:{P['muted']};">{lbl}:</span>
                            <span style="color:{P['text']};font-weight:500;
                                         margin-left:4px;">{val}</span>
                        </div>"""
                        for lbl, val in [
                            ("Age",           age),
                            ("Daily Usage",   f"{avg_hours}h"),
                            ("Sleep",         f"{sleep_hours}h/night"),
                            ("Mental Health", f"{mental_health}/10"),
                            ("Conflicts",     f"{conflicts}/week"),
                            ("Acad. Impact",  affects_academic),
                        ]
                    ])}
                </div>
                """, unsafe_allow_html=True)

            # Tab 2 SHAP
            with t2:
                if not shap_enabled:
                    st.markdown(f"""
                    <div style="text-align:center;padding:2rem;color:{P['muted']};
                                font-size:0.88rem;">
                        Enable the SHAP toggle in the form to see feature explanations.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    with st.spinner("Computing SHAP values…"):
                        shap_pairs, shap_source = compute_shap_values(
                            model, input_arr_use, model_choice, pred_class
                        )

                    fig = render_shap_chart(
                        shap_pairs, pred_label, model_choice, shap_source
                    )
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)

                    top3 = sorted(shap_pairs, key=lambda x: abs(x[1]), reverse=True)[:3]
                    driver_lines = []
                    for feat, val in top3:
                        display   = FEATURE_DISPLAY_NAMES.get(feat, feat)
                        direction = "↑ increases" if val >= 0 else "↓ decreases"
                        color     = level_color if val >= 0 else P["primary_lt"]
                        driver_lines.append(
                            f'<div style="display:flex;gap:8px;margin-bottom:0.45rem;">'
                            f'<span style="color:{color};font-weight:700;font-size:0.88rem;">'
                            f'{direction}</span>'
                            f'<span style="font-size:0.85rem;color:{P["text"]};">'
                            f'{display}&nbsp;'
                            f'<span style="color:{P["muted"]};">({val:+.3f})</span>'
                            f'</span></div>'
                        )

                    label_note_map = {
                        "shap": "SHAP values",
                        "coef": "Logistic Regression coefficient contributions",
                        "importance": "Feature importances (SHAP unavailable)",
                        "none": "Explainability unavailable",
                    }
                    label_note = label_note_map.get(shap_source, shap_source)

                    st.markdown(f"""
                    <div style="background:{P['surface']};border:1px solid {P['border']};
                                border-radius:12px;padding:1rem 1.2rem;margin-top:0.8rem;">
                        <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.08em;
                                    text-transform:uppercase;color:{P['primary_lt']};
                                    margin-bottom:0.7rem;">Top 3 Drivers</div>
                        {''.join(driver_lines)}
                        <div style="margin-top:0.7rem;font-size:0.74rem;
                                    color:{P['border']};">Source: {label_note}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Tab 3 Advice
            with t3:
                advice_list = LEVEL_ADVICE.get(pred_label, [])
                st.markdown(f"""
                <div style="padding:0.2rem 0;">
                    {''.join([
                        f'<div style="display:flex;gap:10px;margin-bottom:0.75rem;'
                        f'align-items:flex-start;">'
                        f'<span style="color:{level_color};font-size:1rem;'
                        f'flex-shrink:0;margin-top:1px;">→</span>'
                        f'<span style="font-size:0.87rem;color:{P["text"]};'
                        f'line-height:1.6;">{tip}</span></div>'
                        for tip in advice_list
                    ])}
                </div>
                <div style="margin-top:0.8rem;padding:0.8rem 1rem;
                            background:{P['surface']};border-radius:10px;
                            font-size:0.76rem;color:{P['muted']};line-height:1.5;">
                    These recommendations are for educational purposes only
                    and do not constitute clinical advice. Please consult a
                    qualified mental health professional for personal guidance.
                </div>
                """, unsafe_allow_html=True)

            # Tab 4 Lifestyle alternatives
            with t4:
                alternatives = LEVEL_ALTERNATIVES.get(pred_label, [])
                st.markdown(f"""
                <div style="font-size:0.8rem;color:{P['muted']};
                            margin-bottom:1rem;line-height:1.5;">
                    Replace screen time with these offline activities. Each one
                    targets the same reward pathways social media exploits.
                </div>
                """, unsafe_allow_html=True)

                for title, desc in alternatives:
                    st.markdown(f"""
                    <div style="background:{P['surface']};border:1px solid {P['border']};
                                border-left:3px solid {level_color};
                                border-radius:0 12px 12px 0;
                                padding:1rem 1.2rem;margin-bottom:0.75rem;">
                        <div style="display:flex;align-items:center;gap:8px;
                                    margin-bottom:0.3rem;">
                            <span style="font-weight:700;color:{P['white']};
                                         font-size:0.92rem;padding-left:2rem;">{title}</span>
                        </div>
                        <div style="font-size:0.84rem;color:{P['muted']};
                                    line-height:1.6;padding-left:2rem;">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)

                motiv = {
                    "Low":      ("Keep it up!",
                                 "You're already doing great. Small habits maintained consistently lead to lifelong wellbeing."),
                    "Moderate": ("You've got this.",
                                 "Small, consistent swaps, one offline hour a day, add up fast. Start today."),
                    "High":     ("Time to reset.",
                                 "Every hour you spend offline is rebuilding the focus and patience social media eroded. It's worth it."),
                    "Severe":   ("Take this seriously.",
                                 "Severe dependency impacts every area of life. The activities above aren't optional extras and they're the path back. Start with just one today."),
                }
                m_title, m_body = motiv[pred_label]
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,{level_color}18,{P['card']});
                            border:1px solid {level_color}33;border-radius:12px;
                            padding:1rem 1.2rem;margin-top:0.5rem;text-align:center;">
                    <div style="font-weight:700;color:{level_color};
                                font-size:0.95rem;margin-bottom:0.3rem;">{m_title}</div>
                    <div style="font-size:0.83rem;color:{P['muted']};
                                line-height:1.55;">{m_body}</div>
                </div>
                """, unsafe_allow_html=True)