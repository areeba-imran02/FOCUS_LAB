import streamlit as st
from focuslab_core.models import Intake
from focuslab_core.config import MAX_INTAKE_CHARS

st.set_page_config(page_title="Focus intake · FocusLab",page_icon="🧭",layout="wide")
st.title("01 · Focus intake")
st.write("Start with your actual day. Unknown details can stay unknown, and every extracted field remains editable.")
if "intake" not in st.session_state: st.session_state.intake=Intake().model_dump()
with st.form("intake_form"):
    problem=st.text_area("What are you trying to do, and what keeps interrupting you?",value=st.session_state.intake.get("problem",""),max_chars=MAX_INTAKE_CHARS,height=120,placeholder="I have 30 minutes to study databases, but I keep checking WhatsApp and don't know where to start.")
    task=st.text_input("Task / desired outcome",value=st.session_state.intake.get("task", ""),max_chars=300,placeholder="Review database normalization")
    minutes=st.slider("Available time (minutes)",5,240,int(st.session_state.intake.get("available_minutes",30)),5)
    options=["Phone / messaging","Social media","Email / notifications","Other browser tabs","People / environment","Worry / mind wandering","Not sure"]
    selected=st.multiselect("Reported distractions",options,default=[x for x in st.session_state.intake.get("distractions",[]) if x in options])
    constraints=st.text_area("Constraints or accommodations (optional)",value=st.session_state.intake.get("constraints",""),max_chars=600,placeholder="Shared room, phone needed for class materials…")
    language=st.selectbox("Preferred language",["English","Urdu","Roman Urdu"],index=["English","Urdu","Roman Urdu"].index(st.session_state.intake.get("language","English")))
    submitted=st.form_submit_button("Save intake",type="primary")
if submitted:
    try:
        st.session_state.intake=Intake(problem=problem,task=task,available_minutes=minutes,distractions=selected,constraints=constraints,language=language).model_dump()
        st.success("Intake saved. You can edit it any time.")
    except Exception as e: st.error(f"Please check your entries: {e}")
st.markdown("### Review your current intake")
st.json(st.session_state.intake,expanded=True)
st.markdown("### Prediction — your expectation, not a measured result")
with st.form("prediction"):
    prediction=st.radio("How do you expect simulated notifications to affect this short task?",["Lower accuracy","Slower responses","Both","Little or no difference","Not sure"],index=0,horizontal=False)
    if st.form_submit_button("Save prediction"):
        st.session_state.prediction=prediction; st.success("Prediction saved for comparison with your results.")
if st.button("Continue to experiment →",type="primary"): st.switch_page("pages/2_Experiment.py")
