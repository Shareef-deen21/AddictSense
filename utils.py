
PALETTE = {
    "bg":        "#0F1117",
    "surface":   "#1A1D27",
    "card":      "#22263A",
    "border":    "#2E3250",
    "primary":   "#6366F1",
    "primary_lt":"#818CF8",
    "accent":    "#06B6D4",
    "success":   "#22C55E",
    "warning":   "#F59E0B",
    "danger":    "#EF4444",
    "orange":    "#F97316",
    "text":      "#E8EAF6",
    "muted":     "#9094B0",
    "white":     "#FFFFFF",
}

LEVEL_COLORS = {
    "Low":      "#22C55E",
    "Moderate": "#F59E0B",
    "High":     "#F97316",
    "Severe":   "#EF4444",
}

LEVEL_ICONS = {
    "Low":      "🟢",
    "Moderate": "🟡",
    "High":     "🟠",
    "Severe":   "🔴",
}

#Clinical-style recommendations per level
LEVEL_ADVICE = {
    "Low": [
        "Your social media usage appears healthy and well-balanced.",
        "Continue maintaining mindful screen-time habits.",
        "Use social media intentionally rather than out of habit.",
        "Keep prioritising real-world social connections.",
        "Perform a monthly self-check to ensure habits don't creep up.",
    ],
    "Moderate": [
        "You show some signs of over-reliance on social media.",
        "Try scheduling specific 'offline hours' each day.",
        "Enable built-in screen-time limits on your devices.",
        "Replace one daily scroll session with a walk or hobby.",
        "Consider a 24-hour digital detox once a week.",
        "Turn off non-essential push notifications to break the reflex.",
    ],
    "High": [
        "Your usage patterns indicate a significant dependency.",
        "Set strict daily time limits, aim for ≤ 2 hours total.",
        "Remove social apps from your phone's home screen.",
        "Talk to a counsellor or trusted person about how you feel.",
        "Track your mood before and after each session, patterns emerge fast.",
        "Replace evening scrolling with reading, journaling, or a creative hobby.",
        "Use grayscale mode on your phone to make screens less stimulating.",
    ],
    "Severe": [
        "Your responses suggest a severe social media addiction.",
        "Seek professional support, a therapist can help you rebuild healthy habits.",
        "Perform a full digital detox for at least 72 hours this week.",
        "Inform a trusted friend or family member and ask them to hold you accountable.",
        "Temporarily deactivate your most-used accounts to break the loop.",
        "Sleep hygiene is critical, no screens at least 1 hour before bed.",
        "Replace every urge to scroll with a deliberate offline action (see alternatives below).",
    ],
}

#Lifestyle alternative activities per level
LEVEL_ALTERNATIVES = {
    "Low": [
        ("Stay Mindful", "Continue with mindful walks, journaling, or light stretching to keep balance."),
        ("Read Intentionally", "Swap 30 minutes of scrolling for a book, article, or podcast you've been meaning to try."),
        ("Invest in People", "Arrange a weekly in-person catch-up with a friend instead of a DM."),
    ],
    "Moderate": [
        ("Go for a Run", "A 20–30 min run releases dopamine naturally, which is same reward loop social media hijacks."),
        ("Spend Time in Nature", "A walk in a park or green space for 20 minutes measurably reduces cortisol and anxiety."),
        ("Pick Up a Creative Hobby", "Drawing, photography, cooking, or music give your brain a stimulating offline reward."),
        ("Try Mindfulness", "Apps like Headspace or simple 5-minute breathing exercises help rewire the scroll reflex."),
        ("Read Before Bed", "Replace evening scrolling with reading, even 15 minutes improves sleep quality significantly."),
    ],
    "High": [
        ("Hit the Gym", "Structured weight training 3× a week rebuilds discipline, reduces anxiety, and gives a daily goal that isn't a screen."),
        ("Spend Time in Nature Daily", "Research shows 20-40 minutes outdoors daily lowers stress hormones. Walk, sit in a park, or find a trail."),
        ("Join a Sports Team or Club", "Team sports, which are football, basketball and badminton, replace the social validation loop with real human connection."),
        ("Start Gardening", "Tending to plants gives you a daily offline ritual with visible progress. Even a small balcony pot counts."),
        ("Set a 30-Day Challenge", "Pick one offline skill, cooking, running 5km, learning an instrument, and track progress in a notebook, not an app."),
        ("Speak to a Counsellor", "A professional can give you structured CBT techniques designed specifically for digital addiction patterns."),
    ],
    "Severe": [
        ("Hit the Gym Daily if Possible", "Physical exercise is the single most evidence-backed intervention for addiction. Aim for 45–60 min of weights or cardio daily. It restores dopamine regulation broken by overconsumption."),
        ("Nature Immersion", "Spend at least 1 hour outdoors every day, something like walking, hiking, or simply sitting in a green space. Research links nature exposure to reduced compulsive behaviour and improved mood."),
        ("Gardening", "Growing plants creates a slow, rewarding offline loop. Watering, pruning, and watching growth happen gives your brain a patient, screen-free dopamine source."),
        ("Outdoor Sports or Events", "Join a local football league, cricket club, cycling group, or attend community sports events. Physical group activity replaces digital social validation with real presence."),
        ("Adventure Activities", "Hiking, swimming, rock climbing, or even beach volleyball, the activities that demand your full physical attention make scrolling feel unappealing by comparison."),
        ("Volunteer in Your Community", "Giving time to a cause, food banks, animal shelters, local events, fills the social connection need that social media falsely promises."),
        ("Creative Outlet", "Music, painting, woodworking, writing, pick one creative discipline and dedicate 1 hour daily. Creativity rebuilds patience and deep focus, both eroded by short-form content."),
        ("Structured Mindfulness + Therapy", "Combine daily 10-min meditation with professional CBT or addiction counselling. Severe dependency benefits most from a structured, guided programme."),
    ],
}

#SHAP feature display names
FEATURE_DISPLAY_NAMES = {
    "Avg_Daily_Usage_Hours":        "Daily Usage (hours)",
    "Mental_Health_Score":          "Mental Health Score",
    "Conflicts_Over_Social_Media":  "Social Media Conflicts",
    "Sleep_Hours_Per_Night":        "Sleep Hours / Night",
    "Affects_Academic_Performance": "Academic Impact",
    "Age":                          "Age",
    "Gender":                       "Gender",
    "Academic_Level":               "Academic Level",
    "Country":                      "Country",
    "Most_Used_Platform":           "Most Used Platform",
    "Relationship_Status":          "Relationship Status",
}

BASE_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {{
    background-color: {PALETTE['bg']} !important;
    color: {PALETTE['text']} !important;
    font-family: 'Inter', sans-serif !important;
}}
[data-testid="stSidebar"] {{
    background-color: {PALETTE['surface']} !important;
    border-right: 1px solid {PALETTE['border']} !important;
}}
[data-testid="stSidebar"] * {{ color: {PALETTE['text']} !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stToolbar"] {{ display: none; }}
.block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1100px !important;
}}
.stButton > button {{
    background: linear-gradient(135deg, {PALETTE['primary']}, {PALETTE['accent']}) !important;
    color: {PALETTE['white']} !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.8rem !important;
    transition: opacity 0.2s ease, transform 0.15s ease !important;
    cursor: pointer !important;
}}
.stButton > button:hover {{
    opacity: 0.88 !important;
    transform: translateY(-2px) !important;
}}
.stButton > button:active {{ transform: translateY(0px) !important; }}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stSlider > div {{
    background-color: {PALETTE['card']} !important;
    padding: 1rem 0.8rem 1rem 0.8rem !important;
    border: 1px solid {PALETTE['border']} !important;
    border-radius: 8px !important;
    color: {PALETTE['text']} !important;
}}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {{
    border-color: {PALETTE['primary']} !important;
    box-shadow: 0 0 0 2px {PALETTE['primary']}33 !important;
}}
label, .stLabel {{
    color: {PALETTE['muted']} !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
}}
.as-card {{
    background: {PALETTE['card']};
    border: 1px solid {PALETTE['border']};
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}}
.as-error {{
    background: {PALETTE['danger']}18;
    border: 1px solid {PALETTE['danger']}55;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    color: #FCA5A5;
    font-size: 0.88rem;
}}
.as-success {{
    background: {PALETTE['success']}18;
    border: 1px solid {PALETTE['success']}55;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    color: #86EFAC;
    font-size: 0.88rem;
}}
.stProgress > div > div > div > div {{
    background: linear-gradient(90deg, {PALETTE['primary']}, {PALETTE['accent']}) !important;
    border-radius: 999px !important;
}}
.stProgress > div > div > div {{
    background: {PALETTE['border']} !important;
    border-radius: 999px !important;
}}
[data-testid="stMetric"] {{
    background: {PALETTE['card']} !important;
    border: 1px solid {PALETTE['border']} !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}}
[data-testid="stMetricValue"] {{
    color: {PALETTE['primary_lt']} !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.6rem !important;
}}
[data-testid="stMetricLabel"] {{ color: {PALETTE['muted']} !important; }}
.stTabs [data-baseweb="tab-list"] {{
    background: {PALETTE['surface']} !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 30px !important;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    color: {PALETTE['muted']} !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    
}}
.stTabs [aria-selected="true"] {{
    background: {PALETTE['primary']} !important;
    color: {PALETTE['white']} !important;
    padding: 10px !important;
    border-radius: 8px !important;
    margin-bottom: 8px !important;
}}
[data-testid="stSelectbox"] svg {{ fill: {PALETTE['muted']} !important; }}
.stRadio > div {{ gap: 0.5rem !important; }}
.stRadio label {{ text-transform: none !important; font-size: 0.9rem !important; }}
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: {PALETTE['surface']}; }}
::-webkit-scrollbar-thumb {{ background: {PALETTE['border']}; border-radius: 5px; }}
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(BASE_CSS, unsafe_allow_html=True)


def session_guard():
    import streamlit as st
    if not st.session_state.get("authenticated", False):
        st.switch_page("pages/2_Login.py")
        return False
    return True
