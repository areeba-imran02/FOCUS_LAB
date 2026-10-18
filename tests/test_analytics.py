from focuslab_core.analytics import exploratory_status, summarize_session
from focuslab_core.storage import save_history, load_history, export_history, clear_history
from focuslab_core.experiment import make_trials

def test_insufficient_ml_data():
    result=exploratory_status([])
    assert result['status']=='Not enough data yet.' and result['model_trained'] is False

def test_session_completeness():
    quiet=[t.to_dict() for t in make_trials('quiet',1)]
    notify=[t.to_dict() for t in make_trials('notifications',2)]
    for trial in quiet+notify:
        trial['response']=False
    m=summarize_session({'quiet':quiet,'notifications':notify})
    assert m['complete'] is True

def test_history_export_and_delete(tmp_path):
    p=tmp_path/'history.json'
    save_history({'task':'test'},p)
    rows=load_history(p)
    assert len(rows)==1 and b'"task": "test"' in export_history(rows)
    clear_history(p)
    assert load_history(p)==[]
