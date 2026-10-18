import streamlit as st, time

st.set_page_config(page_title="Focus session · FocusLab",page_icon="⏱️",layout="wide")
st.title("05 · Focus session")
plan=st.session_state.get("coach_result",{}).get("plan",{})
default_minutes=int(st.session_state.get("intake",{}).get("available_minutes",25))
if "focus_session" not in st.session_state: st.session_state.focus_session={"status":"ready","duration":min(240,max(5,default_minutes)),"remaining":min(240,max(5,default_minutes))*60,"started_at":None,"elapsed_before_pause":0,"task":st.session_state.get("intake",{}).get("task","") or "Work on my priority task","checklist":[],"completion_criteria":"A concrete next outcome is complete."}
s=st.session_state.focus_session
if s["status"]=="ready":
    s["duration"]=st.slider("Session duration (minutes)",5,240,int(s["duration"]),5)
    s["task"]=st.text_input("Task",value=s["task"],max_chars=300)
    s["completion_criteria"]=st.text_input("What counts as done?",value=s["completion_criteria"],max_chars=300)
    suggested=[x["title"] for x in plan.get("steps",[])] or ["Write the next visible task step","Remove one likely distraction","Review progress at the end"]
    s["checklist"]=st.multiselect("Session checklist",suggested,default=suggested[:min(2,len(suggested))])
    if st.button("Start focus session",type="primary"):
        s["remaining"]=s["duration"]*60;s["started_at"]=time.monotonic();s["elapsed_before_pause"]=0;s["status"]="running";st.rerun()
elif s["status"] in ("running","paused"):
    if s["status"]=="running":
        elapsed=s["elapsed_before_pause"]+(time.monotonic()-(s["started_at"] or time.monotonic()));s["remaining"]=max(0,int(s["duration"]*60-elapsed))
        if s["remaining"]==0: s["status"]="finished";st.rerun()
    mins,secs=divmod(s["remaining"],60);st.markdown(f"<div style='text-align:center;padding:2rem;border-radius:20px;border:1px solid #36516a'><div style='font-size:4rem;font-weight:800;font-variant-numeric:tabular-nums'>{mins:02d}:{secs:02d}</div><div>{s['task']}</div></div>",unsafe_allow_html=True)
    st.caption("Countdown refreshes on Streamlit reruns; this is not a background timer and may not update continuously without interaction.")
    a,b,c=st.columns(3)
    if s["status"]=="running" and a.button("Pause",use_container_width=True): s["elapsed_before_pause"]+=time.monotonic()-(s["started_at"] or time.monotonic());s["started_at"]=None;s["status"]="paused";st.rerun()
    if s["status"]=="paused" and a.button("Resume",type="primary",use_container_width=True): s["started_at"]=time.monotonic();s["status"]="running";st.rerun()
    if b.button("Refresh countdown",use_container_width=True): st.rerun()
    if c.button("Finish session",use_container_width=True): s["status"]="finished";st.rerun()
if s["status"]=="finished":
    st.success("Session finished. Take a moment to reflect.")
    if st.button("Reflect on this session →",type="primary"): st.switch_page("pages/6_Reflection_History.py")
