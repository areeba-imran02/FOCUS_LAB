import streamlit as st
from datetime import datetime, timezone
from focuslab_core.storage import load_history,save_history,export_history,clear_history

st.set_page_config(page_title="Reflection & history · FocusLab",page_icon="📝",layout="wide")
st.title("06 · Reflection & history")
questions=[("helped","What helped you stay on task?"),("interrupted","What interrupted you?"),("keep","Which strategy would you keep?"),("change","What would you change next time?")]
with st.form("reflection"):
    answers={key:st.text_area(label,max_chars=1000) for key,label in questions}
    saved=st.form_submit_button("Save reflection",type="primary")
if saved:
    item={"saved_at":datetime.now(timezone.utc).isoformat(),"task":st.session_state.get("intake",{}).get("task",""),"intake":st.session_state.get("intake",{}),"experiment_metrics":st.session_state.get("experiment_metrics",{}),"reflection":answers,"focus_session":st.session_state.get("focus_session",{})}
    rows=save_history(item);st.session_state.history=rows;st.success("Saved to the current local filesystem. On Streamlit Cloud, files may not persist permanently.")
rows=load_history();st.session_state.history=rows
st.subheader("Optional local history")
st.write(f"{len(rows)} saved reflection(s) found in this runtime.")
if rows:
    for i,item in reversed(list(enumerate(rows))):
        with st.expander(f"{item.get('saved_at','Unknown date')} · {item.get('task') or 'Focus session'}"):
            st.json(item,expanded=False)
    st.download_button("Export history as JSON",data=export_history(rows),file_name="focuslab-history.json",mime="application/json")
else: st.info("No saved history yet. Save a reflection above; history is optional.")
if st.button("Clear local history",type="secondary"):
    clear_history();st.session_state.history=[];st.success("Local history cleared.");st.rerun()
st.caption("Clearing history removes the local JSON file in this runtime. Export a copy first if you need to keep it.")
