import streamlit as st
from focuslab_core.config import load_evidence
from focuslab_core.storage import load_history, export_history, clear_history

st.set_page_config(page_title="FocusLab", page_icon="◉", layout="wide", initial_sidebar_state="expanded")

DARK = """<style>
:root{--fl-bg:#080D18;--fl-surface:#111A2B;--fl-raised:#18243A;--fl-accent:#5EEAD4;--fl-purple:#A78BFA;--fl-text:#F1F5F9;--fl-muted:#A8B6CD}
.stApp{background:radial-gradient(ellipse at 15% 0%,rgba(94,234,212,.09),transparent 38%),radial-gradient(ellipse at 90% 10%,rgba(167,139,250,.10),transparent 34%),#080D18;color:var(--fl-text)}
[data-testid="stSidebar"]{background:#0d1525;border-right:1px solid #233149}
.fl-hero{padding:2rem 0 1.4rem}.fl-kicker{color:#5EEAD4;font-size:.8rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase}.fl-title{font-size:clamp(2.3rem,6vw,4.4rem);line-height:1.02;font-weight:800;letter-spacing:-.04em;margin:.65rem 0}.fl-gradient{background:linear-gradient(95deg,#5EEAD4,#A78BFA);-webkit-background-clip:text;background-clip:text;color:transparent}.fl-sub{font-size:1.12rem;color:#A8B6CD;max-width:760px;line-height:1.65}.fl-card{background:linear-gradient(145deg,rgba(24,36,58,.95),rgba(17,26,43,.95));border:1px solid #263650;border-radius:18px;padding:1.15rem 1.25rem;margin:.35rem 0 1rem}.fl-small{font-size:.88rem;color:#A8B6CD}.stButton>button{border-radius:12px;min-height:2.65rem;font-weight:650;border:1px solid #36516a;transition:transform .15s ease}.stButton>button:focus-visible{outline:3px solid #5EEAD4;outline-offset:2px}.stButton>button:hover{transform:translateY(-1px);border-color:#5EEAD4}div[data-testid="stMetric"]{background:#111A2B;border:1px solid #263650;border-radius:14px;padding:1rem}h1,h2,h3{letter-spacing:-.02em} [data-testid="stAlert"]{border-radius:12px}@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>"""
LIGHT = """<style>
.stApp{background:radial-gradient(ellipse at 15% 0%,rgba(13,148,136,.09),transparent 38%),radial-gradient(ellipse at 90% 10%,rgba(124,58,237,.08),transparent 34%),#F5F7FB;color:#172033}
[data-testid="stSidebar"]{background:#EDF2F8;border-right:1px solid #D6DFEB}.fl-kicker{color:#0F766E;font-size:.8rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase}.fl-title{font-size:clamp(2.3rem,6vw,4.4rem);line-height:1.02;font-weight:800;letter-spacing:-.04em;margin:.65rem 0}.fl-gradient{background:linear-gradient(95deg,#0F766E,#7C3AED);-webkit-background-clip:text;background-clip:text;color:transparent}.fl-sub,.fl-small{color:#53627A}.fl-card{background:linear-gradient(145deg,#fff,#F2F6FC);border:1px solid #D6DFEB;border-radius:18px;padding:1.15rem 1.25rem;margin:.35rem 0 1rem}div[data-testid="stMetric"]{background:#fff;border:1px solid #D6DFEB;border-radius:14px;padding:1rem}.stButton>button{border-radius:12px;min-height:2.65rem;font-weight:650}h1,h2,h3{letter-spacing:-.02em}
</style>"""

if "theme" not in st.session_state: st.session_state.theme="Dark"
with st.sidebar:
    st.markdown("## ◉ FocusLab")
    st.caption("Understand your focus. Take back your attention.")
    st.session_state.theme=st.selectbox("Appearance",["Dark","Light"],index=0 if st.session_state.theme=="Dark" else 1)
    st.divider()
    st.markdown("**Your lab**")
    st.page_link("app.py",label="Overview",icon="🏠")
    st.page_link("pages/1_Focus_Intake.py",label="01 · Focus intake",icon="🧭")
    st.page_link("pages/2_Experiment.py",label="02 · Experiment",icon="🧪")
    st.page_link("pages/3_Results.py",label="03 · Results",icon="📊")
    st.page_link("pages/4_AI_Coach.py",label="04 · Focus coach",icon="✨")
    st.page_link("pages/5_Focus_Session.py",label="05 · Focus session",icon="⏱️")
    st.page_link("pages/6_Reflection_History.py",label="06 · Reflection & history",icon="📝")
    st.divider(); st.caption("Educational tool · not a diagnostic test")
st.markdown(DARK if st.session_state.theme=="Dark" else LIGHT,unsafe_allow_html=True)

st.markdown('<div class="fl-hero"><div class="fl-kicker">Your personal attention lab</div><div class="fl-title">Understand your <span class="fl-gradient">focus.</span><br>Take back your attention.</div><div class="fl-sub">A short, practical experiment to explore how interruptions affect one task — then turn your observations into a plan you can actually use.</div></div>',unsafe_allow_html=True)
left,right=st.columns([1.35,1],gap="large")
with left:
    st.markdown("### Your workflow")
    steps=[("01","Name the friction","Describe your task, constraints, and usual interruptions."),("02","Run the experiment","Practice, then try quiet and simulated-notification rounds."),("03","Read your observations","Compare accuracy, missed targets, false alarms, and reaction time."),("04","Build a workable plan","Use local guidance or opt in to a Gemini-powered coach."),("05","Focus, then reflect","Run a timed work block and record what you learned.")]
    for n,title,desc in steps:
        st.markdown(f'<div class="fl-card"><span class="fl-kicker">{n}</span><br><b>{title}</b><div class="fl-small">{desc}</div></div>',unsafe_allow_html=True)
with right:
    st.markdown("### Start where you are")
    st.markdown('<div class="fl-card"><h3>🧭 Set up your experiment</h3><p class="fl-small">No API key is needed for intake, trials, scoring, local plans, timers, or reflection.</p></div>',unsafe_allow_html=True)
    if st.button("Describe my focus problem →",type="primary",use_container_width=True): st.switch_page("pages/1_Focus_Intake.py")
    if st.button("Explore the experiment →",use_container_width=True): st.switch_page("pages/2_Experiment.py")
    st.markdown("### A few important boundaries")
    st.info("This short task is an educational demonstration, not a validated cognitive assessment. Device latency, practice, fatigue, chance, and trial order can influence results.")
    try:
        n=len(load_history())
    except Exception: n=0
    st.metric("Saved sessions on this device",n)
    st.caption("Cloud filesystems can be ephemeral. Export history if you want to keep a copy.")
