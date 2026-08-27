import streamlit as st
from utils import inject_css, PALETTE as P

st.set_page_config(
    page_title="AddiSence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()


st.markdown(f"""
<style>
/* Hide sidebar toggle on landing */
[data-testid="collapsedControl"] {{ display: none !important; }}

.hero-tag {{
    display: inline-block;
    background: {P['primary']}22;
    border: 1px solid {P['primary']}55;
    color: {P['primary_lt']};
    padding: 0.28rem 0.9rem;
    border-radius: 999px;
    font-size: 0.78rem;
    text-align: center;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}}
.hero-title {{
    font-family: 'Space Grotesk', sans-serif;
    width: 100%;
    margin: 0 auto 1rem auto;
    overflow-wrap: break-word;
    font-size: clamp(1rem, 4vw, 3rem);
    font-weight: 800;
    line-height: 1.15;
    color: {P['white']};
    letter-spacing: -0.03em;
    text-align: center;
}}
.hero-sub {{
    font-size: 1.05rem;
    color: {P['muted']};
    line-height: 1.7;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 2rem;
    text-align: center;
}}
.section-label {{
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {P['primary_lt']};
    margin-bottom: 0.5rem;
}}
.section-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.85rem;
    font-weight: 700;
    color: {P['white']};
    letter-spacing: -0.02em;
    margin-bottom: 0.6rem;
    transition: transform 0.5s, color 0.5s;
}}
.section-title:hover {{ color: {P['primary']}; transform: translateY(-3px) }}
.section-sub {{
    color: {P['muted']};
    font-size: 0.97rem;
    line-height: 1.65;
    max-width: 860px;
    margin-bottom: 2rem;
}}
.feat-card {{
    background: {P['card']};
    border: 1px solid {P['border']};
    border-radius: 14px;
    padding: 1.4rem;
    height: 100%;
    transition: border-color 0.2s;
    transition: transform 0.5s, color 0.5s;
}}
.feat-card:hover {{ border-color: {P['primary']}88; }}
.feat-card:hover .feat-title {{
    color: {P['primary']};
}}
.feat-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    text-align: center;
    color: {P['white']};
    margin-bottom: 0.4rem;
    transition: transform 0.5s, color 0.5s;
}}
.feat-desc {{
    font-size: 0.86rem;
    color: {P['muted']};
    line-height: 1.6;
    text-align: center;
}}
.stat-num {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, {P['primary_lt']}, {P['accent']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.stat-label {{
    font-size: 0.82rem;
    color: {P['muted']};
    margin-top: 0.2rem;
}}
.model-chip {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: {P['card']};
    border: 1px solid {P['border']};
    border-radius: 10px;
    padding: 0.55rem 0.9rem;
    font-size: 0.85rem;
    font-weight: 600;
    color: {P['text']};
    margin: 0.3rem;
}}
.model-dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
}}
.cta-band {{
    background: linear-gradient(135deg, {P['primary']}22, {P['accent']}15);
    border: 1px solid {P['primary']}33;
    border-radius: 18px;
    padding: 3rem 2.5rem;
    text-align: center;
    margin: 3rem 0 1rem 0;
}}
.nav-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 2rem;
    background: linear-gradient(
        135deg,
        {P['surface']},
        {P['card']}
    );
    border: 1px solid {P['border']};
    border-radius: 30px;
    margin-bottom: 3.5rem;
}}
.nav-logo {{
    display: flex;
    align-items: center;
    gap: 10px;
}}
.nav-links a {{
    color: {P['muted']};
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    margin-left: 1.8rem;
    transition: color 0.5s;
}}
.nav-links a:hover {{ color: {P['primary']}; }}
.learn-more-btn {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 0.6rem 1rem;
    background: linear-gradient(135deg, {P['primary']}, {P['accent']});
    color: {P['white']} !important;
    border-radius: 10px;
    text-decoration: none !important;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    box-sizing: border-box;
}}

.learn-more-btn:hover {{
    opacity: 0.88 !important;
    transform: translateY(-2px);
}}

.section-sep {{
    border: none;
    border-top: 1px solid {P['border']};
    margin: 3.5rem 0;
}}
.use-card {{
    background: {P['card']};
    border: 1px solid {P['border']};
    border-radius: 14px;
    padding: 1.5rem;
    height: 100%;
    transition: background 0.5s, transform 0.5s, color 0.5s;
}}
.use-card:hover {{ border-color: {P['primary']}88; transform: translateY(-7px) scale(1.03); }}
.use-num {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: {P['border']};
    margin-bottom: 0.6rem;
    line-height: 1;
}}
.use-title {{
    font-size: 0.98rem;
    font-weight: 700;
    color: {P['white']};
    margin-bottom: 0.4rem;
}}
.use-desc {{
    font-size: 0.84rem;
    color: {P['muted']};
    line-height: 1.6;
}}
.proc-card {{
    background: {P['card']};
    border: 1px solid {P['border']};
    border-radius: 14px;
    padding: 1.5rem;
    height: 100%;
    transition: background 0.5s, transform 0.5s, color 0.5s;
}}
.proc-card:hover {{ border-color: {P['primary_lt']}88; transform: translateY(7px) scale(1.03); }}
.proc-num {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: {P['primary_lt']};
    margin-bottom: 0.6rem;
    line-height: 1;
}}
.proc-title {{
    font-size: 0.98rem;
    font-weight: 700;
    color: {P['white']};
    margin-bottom: 0.4rem;
}}
.proc-desc {{
    font-size: 0.84rem;
    color: {P['muted']};
    line-height: 1.6;
}}
.footer {{
    border-top: 1px solid {P['border']};
    padding: 1.8rem 0 0.5rem 0;
    margin-top: 3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    flex-wrap: wrap;
    gap: 0.5rem;
}}
.footer-left {{
    font-size: 0.82rem;
    color: {P['muted']};
}}
.hero-gradient {{
    background: linear-gradient(135deg, #818CF8, #06B6D4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
</style>
""", unsafe_allow_html=True)

#Nav Bar
st.markdown(f"""
<div class="nav-bar">
    <div class="nav-logo">
        <span style="font-family:'Space Grotesk',sans-serif;font-size:1.8rem;
                     font-weight:700;color:{P['white']};letter-spacing:-0.02em;">
            Addict<span style="color:{P['primary_lt']};">Sence</span>
        </span>
    </div>
    <div class="nav-links">
        <a href="#about">About</a>
        <a href="#usecases">Use Cases</a>
        <a href="#process">Process</a>
        <a href="#techniques">Techniques</a>
    </div>
</div>
""", unsafe_allow_html=True)

#Hero Section

left, center, right = st.columns([0.5, 3, 0.5])

with center:
    st.markdown(
        '<div style="text-align:center;">'
        '<div class="hero-tag">ML-Powered · SHAP Explainable</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <h1 class="hero-title">
         <span>
        Detect Social Media <span class="hero-gradient">Addiction Patterns</span></span> with Machine Learning
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p class="hero-sub">
        AddictSence uses ensemble machine learning to assess social media
        dependency risk from behavioural and academic indicators,
        giving students and counsellors actionable, explainable insights.
    </p>
    """, unsafe_allow_html=True)

    _, btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 1.5, 1.5])
    with btn_col1:
        if st.button("Get Started", use_container_width=True):
            st.switch_page("pages/2_Login.py")
    with btn_col2:
        st.markdown(f"""
        <a href="#about" class="learn-more-btn">
            Learn More
        </a>
        """, unsafe_allow_html=True)


#Stats strip
st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)
s1, s2, s3, s4 = st.columns(4)
stats = [
    ("705", "Training Records"),
    ("11", "Behavioural Features"),
    ("5", "ML Algorithms"),
    ("98.6%", "Best Accuracy"),
]
for col, (num, label) in zip([s1, s2, s3, s4], stats):
    with col:
        st.markdown(f"""
        <div style="text-align:center;padding:0.5rem 0;">
            <div class="stat-num">{num}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)


#About Section
st.markdown("<hr class='section-sep'><a name='about'></a>", unsafe_allow_html=True)
st.markdown('<div class="section-label">About</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">What is AddictSence?</div>', unsafe_allow_html=True)
st.markdown(f"""
<p class="section-sub">
    AddictSense is an explainable machine learning platform designed to help users understand their 
    social media usage patterns. It predicts addiction severity across four levels, explains key 
    factors behind each prediction using SHAP, and provides personalized, actionable recommendations, which makes the 
    digital wellbeing insights more transparent, accessible, and meaningful.

</p>
""", unsafe_allow_html=True)

a1, a2, a3 = st.columns(3)
features = [
    ("Evidence-Based", "Built on peer-reviewed constructs: daily usage hours, mental health scores, academic impact, and conflict frequency."),
    ("SHAP Explainable", "Every prediction is backed by SHAP feature attribution, not a black box. See exactly why the model decided what it did."),
    ("Five-Model Ensemble", "XGBoost, CatBoost, LightGBM, Random Forest (best), and Logistic Regression, with per-model performance breakdown."),
    ("Imbalance-Corrected", "SMOTE oversampling balances the rare 'Low' class (originally only 2.4% of data) for fair, unbiased predictions."),
    ("Four Risk Levels", "Outputs Low, Moderate, High, Severe classification with probability confidence and personalised recommendations."),
    ("Young Adult-Focused", "Designed specifically for young adults and undergraduate students with relevant contextual features."),
]
for col, (title, desc) in zip([a1, a2, a3, a1, a2, a3], features):
    with col:
        st.markdown(f"""
        <div class="feat-card" style="margin-bottom:1rem;">
            <div class="feat-title">{title}</div>
            <div class="feat-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


#Use Cases Section
st.markdown("<hr class='section-sep'><a name='usecases'></a>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Use Cases</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Who benefits from AddiSence?</div>', unsafe_allow_html=True)

u1, u2, u3, u4 = st.columns(4, gap="medium")
usecases = [
    ("01", "Students", "Self-assess your own social media habits in minutes and receive a personalised risk level with targeted coping advice."),
    ("02", "Counsellors", "Screen student populations quickly and objectively; use SHAP scores to ground conversations in data rather than perception."),
    ("03", "Researchers", "Explore feature-importance rankings and cross-model comparisons to validate or extend addiction-detection hypotheses."),
    ("04", "Institutions", "Run anonymous cohort assessments to identify at-risk groups and evaluate intervention effectiveness over time."),
]
for col, (num, title, desc) in zip([u1, u2, u3, u4], usecases):
    with col:
        st.markdown(f"""
        <div class="use-card">
            <div class="use-num">{num}</div>
            <div class="use-title">{title}</div>
            <div class="use-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)



#Process Section
st.markdown("<hr class='section-sep'><a name='process'></a>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Process</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">How Does AddictSence Works?</div>', unsafe_allow_html=True)

p1, p2, p3 = st.columns(3, gap="medium")
process = [
    ("Step 1", "Sign Up", "Create your AddiSence account and sign in securely to begin your personalised addiction risk assessment."),
    ("Step 2", "Enter Your Details", "Provide the required information about your social media habits and daily usage in the input fields."),
    ("Step 3", "Get Your Prediction", "Click the Predict button to analyse your information and receive your estimated addiction risk level."),
]
for col, (num, title, desc) in zip([p1, p2, p3], process):
    with col:
        st.markdown(f"""
        <div class="proc-card">
            <div class="proc-num">{num}</div>
            <div class="proc-title">{title}</div>
            <div class="proc-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)



#Techniques Section
st.markdown("<hr class='section-sep'><a name='techniques'></a>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Techniques</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Machine Learning Stack</div>', unsafe_allow_html=True)

t_left, t_right = st.columns([1.1, 0.9], gap="large")

with t_left:
    models_info = [
        ("#6366F1", "Random Forest", "PRIMARY", "98.58%", "Bagged decision trees with feature subsampling. Captures non-linear relationships and provides robust performance across diverse feature sets."),
        ("#F59E0B", "XGBoost", "", "97.16%", "Regularised gradient-boosted trees. Captures complex non-linear patterns while controlling overfitting through regularisation and tree constraints."),
        ("#10B981", "LightGBM", "", "97.16%", "Leaf-wise tree growth for speed. Histogram binning allows fast training on the full SMOTE-balanced set."),
        ("#06B6D4", "CatBoost", "", "96.45%", "Categorical-native gradient boosting with ordered boosting. Symmetric trees prevent overfitting, ordered boosting avoids target leakage."),
        ("#EF4444", "Logistic Regression", "", "95.74%", "L2-regularised multinomial classifier. Linear baseline trained on standard-scaled features."),
    ]
    for color, name, badge, acc, desc in models_info:
        badge_html = f'<span style="background:{P["primary"]}33;color:{P["primary_lt"]};padding:0.15rem 0.5rem;border-radius:5px;font-size:0.68rem;font-weight:700;margin-left:0.5rem;">{badge}</span>' if badge else ""
        st.markdown(f"""
        <div style="background:{P['card']};border:1px solid {P['border']};border-left:3px solid {color};
                    border-radius:0 12px 12px 0;padding:1rem 1.2rem;margin-bottom:0.75rem;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.35rem;">
                <div style="font-weight:700;color:{P['white']};font-size:0.95rem;">
                    <span style="display:inline-block;width:10px;height:10px;border-radius:50%;
                                 background:{color};margin-right:8px;vertical-align:middle;"></span>
                    {name}{badge_html}
                </div>
                <span style="color:{color};font-weight:700;font-size:0.85rem;">{acc}</span>
            </div>
            <div style="font-size:0.82rem;color:{P['muted']};line-height:1.55;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

with t_right:
    pipeline_steps = [
        ("Data Loading", "705 records · 12 features · Kaggle dataset"),
        ("EDA", "Correlation analysis · class distribution · feature plots"),
        ("Preprocessing", "Label encoding · SMOTE balancing · StandardScaler"),
        ("Model Training", "5 algorithms · 5-fold stratified CV"),
        ("Evaluation", "Accuracy · F1 · ROC-AUC · Confusion matrix"),
        ("SHAP XAI", "TreeExplainer · feature attribution · summary plot"),
        ("Deployment", "joblib artifacts → Streamlit prediction UI"),
    ]
    st.markdown(f"""
    <div style="background:{P['card']};border:1px solid {P['border']};border-radius:14px;
                padding:1.4rem;">
        <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;
                    text-transform:uppercase;color:{P['primary_lt']};margin-bottom:1rem;">
            Pipeline Flow
        </div>
        {''.join([
            f'''<div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:{'0' if i==len(pipeline_steps)-1 else '0.8rem'};">
                <div>
                    <div style="font-size:0.88rem;font-weight:600;color:{P['white']};">{title}</div>
                    <div style="font-size:0.78rem;color:{P['muted']};margin-top:1px;">{detail}</div>
                </div>
            </div>
            {'<div style="margin-left:16px;border-left:1px dashed ' + P['border'] + ';height:12px;"></div>' if i<len(pipeline_steps)-1 else ""}'''
            for i,(title,detail) in enumerate(pipeline_steps)
        ])}
    </div>
    """, unsafe_allow_html=True)


# CTA Band
st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)
st.markdown(f"""
<div class="cta-band">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:1.7rem;font-weight:800;
                color:{P['white']};letter-spacing:-0.02em;margin-bottom:0.6rem;">
        Ready to check your risk level?
    </div>
    <p style="color:{P['muted']};font-size:0.97rem;margin-bottom:1.8rem;">
        Assess your social media addiction risk in under two minutes with secure assessment,<br> instant results, and no personal data stored.
    </p>
</div>
""", unsafe_allow_html=True)

_, cta_btn, _ = st.columns([2, 1, 2])
with cta_btn:
    if st.button("Login to Predict", use_container_width=True):
        st.switch_page("pages/2_Login.py")

#Footer
st.markdown(f"""
<div class="footer">
    <div class="footer-left">
        <strong style="color:{P['text']};">AddiSence</strong> &nbsp;|&nbsp;
        Social Media Addiction Prediction System &nbsp;|&nbsp; 2026 &nbsp;&nbsp;
    </div>
</div>
""", unsafe_allow_html=True)
