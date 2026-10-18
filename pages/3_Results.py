import streamlit as st
from focuslab_core.scoring import score_condition, compare_conditions
from focuslab_core.analytics import exploratory_status

st.set_page_config(page_title="Results · FocusLab",page_icon="📊",layout="wide")
st.title("03 · Your observations")
exp=st.session_state.get("experiment")
if not exp:
    st.info("No experiment is in progress yet. Start with practice on the Experiment page.")
    if st.button("Go to experiment →"): st.switch_page("pages/2_Experiment.py")
    st.stop()
results={c:exp["conditions"][c] for c in ("quiet","notifications")}
metrics={c:score_condition(v) for c,v in results.items()}
complete=all(metrics[c]["trials"]==24 and metrics[c]["completed"] for c in metrics)
if not complete: st.warning("These are partial results. Finish all 24 trials in both conditions for a complete comparison.")
cols=st.columns(2)
for col,c,label in zip(cols,["quiet","notifications"],["Quiet","Simulated notifications"]):
    m=metrics[c]
    with col:
        st.subheader(label)
        st.metric("Accuracy", "—" if m["accuracy"] is None else f"{m['accuracy']:.0%}")
        st.metric("Median correct-target response", "Unavailable" if m["median_rt_ms"] is None else f"{m['median_rt_ms']:.0f} ms")
        st.write({"Trials":m["trials"],"Hits":m["hits"],"Misses":m["misses"],"False alarms":m["false_alarms"],"Correct rejections":m["correct_rejections"]})
comparison=compare_conditions(results["quiet"],results["notifications"])
st.subheader("Condition comparison")
st.dataframe([{"Measure":"Accuracy","Quiet":f"{metrics['quiet']['accuracy']:.0%}" if metrics['quiet']['accuracy'] is not None else "—","Notifications":f"{metrics['notifications']['accuracy']:.0%}" if metrics['notifications']['accuracy'] is not None else "—"},{"Measure":"Median reaction time","Quiet":f"{metrics['quiet']['median_rt_ms']:.0f} ms" if metrics['quiet']['median_rt_ms'] is not None else "Unavailable","Notifications":f"{metrics['notifications']['median_rt_ms']:.0f} ms" if metrics['notifications']['median_rt_ms'] is not None else "Unavailable"},{"Measure":"Missed targets","Quiet":metrics['quiet']['misses'],"Notifications":metrics['notifications']['misses']},{"Measure":"False alarms","Quiet":metrics['quiet']['false_alarms'],"Notifications":metrics['notifications']['false_alarms']}],hide_index=True,use_container_width=True)
st.session_state.experiment_metrics={**metrics,"comparison":comparison}
pred=st.session_state.get("prediction")
if pred: st.markdown("### Prediction check"); st.write(f"Your prediction: **{pred}**. Compare it with the values above; this small task cannot establish a general effect.")
st.info("Interpret cautiously: device latency, practice, fatigue, randomized trial order, and chance may affect these observations. A slower response paired with better accuracy is a trade-off, not a clear winner. No personal attention score or diagnosis is produced.")
status=exploratory_status(st.session_state.get("history",[])); st.caption(f"Exploratory analytics: {status['status']} (minimum threshold: {status['threshold']} completed sessions; no predictive model is trained).")
if st.button("Create a focus plan →",type="primary"): st.switch_page("pages/4_AI_Coach.py")
