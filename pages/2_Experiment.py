import streamlit as st, time, random
from focuslab_core.experiment import make_session, practice_trial, Trial
from focuslab_core.scoring import score_condition

st.set_page_config(page_title="Experiment · FocusLab",page_icon="🧪",layout="wide")
st.title("02 · Attention experiment")
st.warning("Timing is approximate in Streamlit. The app cannot reliably detect a hidden tab or guarantee millisecond stimulus timing. Treat results as a personal demonstration, not a validated test.")
st.markdown("**Target:** respond to a blue circle. Ignore a blue square, purple circle, and purple square.")
st.markdown("<div class='fl-card'><b>Experiment rules</b><br>6 practice trials with feedback · 24 quiet trials · 24 simulated-notification trials · 12 targets and 12 non-targets per condition.</div>",unsafe_allow_html=True)
if "experiment" not in st.session_state: st.session_state.experiment=make_session()
if "exp_started" not in st.session_state: st.session_state.exp_started=False
if st.button("Restart experiment",help="Clears the current in-progress experiment and creates new randomized trial orders"):
    st.session_state.experiment=make_session(); st.session_state.exp_started=False; st.session_state.pop("trial_started_at",None); st.rerun()
if not st.session_state.exp_started:
    st.info("When you begin, each response advances one trial. Use the large controls promptly; browser and rerun delays affect reaction-time estimates.")
    if st.button("Begin six practice trials",type="primary"): st.session_state.exp_started=True; st.session_state.practice_stim=practice_trial(); st.session_state.practice_started=time.monotonic(); st.rerun()
else:
    exp=st.session_state.experiment; practice=int(exp.get("practice",0))
    if practice<6:
        if "practice_stim" not in st.session_state: st.session_state.practice_stim=practice_trial(); st.session_state.practice_started=time.monotonic()
        stim=st.session_state.practice_stim
        st.caption(f"Practice {practice+1} of 6")
        st.markdown("<div style='text-align:center;padding:1rem;border:1px solid #36516a;border-radius:16px'>",unsafe_allow_html=True)
        colors={"blue_circle":("#60A5FA","50%"),"blue_square":("#60A5FA","8px"),"purple_circle":("#A78BFA","50%"),"purple_square":("#A78BFA","8px")}
        color,shape=colors[stim]
        st.markdown(f"<div aria-label='{stim.replace('_',' ')}' style='margin:1.1rem auto;width:100px;height:100px;background:{color};border-radius:{shape}'></div>",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
        a,b=st.columns(2)
        def practice_answer(answer):
            correct=(answer==(stim=="blue_circle")); exp["practice"]=practice+1; st.session_state.experiment=exp; st.session_state.practice_feedback="Correct" if correct else "Not quite"; st.session_state.pop("practice_stim",None); st.rerun()
        if a.button("TARGET — blue circle",type="primary",use_container_width=True): practice_answer(True)
        if b.button("NON-TARGET — ignore",use_container_width=True): practice_answer(False)
        if "practice_feedback" in st.session_state: st.caption(st.session_state.practice_feedback)
    else:
        order=exp["condition_order"]; idx=int(exp.get("active_condition",0))
        if idx>=len(order):
            st.success("Both conditions are complete. Open Results to review your actual observations.")
            if st.button("View results →",type="primary"): st.switch_page("pages/3_Results.py")
        else:
            cond=order[idx]; trials=exp["conditions"][cond]; trial_idx=next((i for i,t in enumerate(trials) if t["response"] is None and not t["timed_out"]),len(trials))
            if trial_idx>=len(trials):
                exp["active_condition"]=idx+1; st.session_state.experiment=exp; st.rerun()
            else:
                t=trials[trial_idx]; stim=t["stimulus"]
                st.subheader("Condition: Quiet" if cond=="quiet" else "Condition: Simulated notifications")
                st.progress(trial_idx/24,text=f"Trial {trial_idx+1} of 24")
                if cond=="notifications": st.warning(random.choice(["New message · simulated","Reminder · simulated","Group chat · simulated"]),icon="🔔")
                st.caption("Respond only if the stimulus is a blue circle.")
                color,shape={"blue_circle":("#60A5FA","50%"),"blue_square":("#60A5FA","8px"),"purple_circle":("#A78BFA","50%"),"purple_square":("#A78BFA","8px")}[stim]
                st.markdown(f"<div style='text-align:center;padding:1rem;border:1px solid #36516a;border-radius:16px'><div aria-label='{stim.replace('_',' ')}' style='margin:1rem auto;width:112px;height:112px;background:{color};border-radius:{shape}'></div></div>",unsafe_allow_html=True)
                if "trial_started_at" not in st.session_state: st.session_state.trial_started_at=time.monotonic()
                def answer(response):
                    elapsed=(time.monotonic()-st.session_state.trial_started_at)*1000
                    t["response"]=response; t["reaction_ms"]=round(elapsed,1) if response else None
                    st.session_state.experiment=exp; st.session_state.pop("trial_started_at",None); st.rerun()
                a,b=st.columns(2)
                if a.button("●  BLUE CIRCLE — target",type="primary",use_container_width=True): answer(True)
                if b.button("Ignore — non-target",use_container_width=True): answer(False)
                if st.button("Mark missed / no response",use_container_width=True): t["timed_out"]=True; t["response"]=None; st.session_state.experiment=exp; st.session_state.pop("trial_started_at",None); st.rerun()
                st.caption("This implementation advances on a click rather than automatically closing a 900 ms window; recorded RT includes Streamlit interaction latency. See README for limitations.")
