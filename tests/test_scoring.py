from focuslab_core.experiment import Trial
from focuslab_core.scoring import score_condition, compare_conditions

def test_scoring_formulas_and_missing_rt():
    trials=[Trial('quiet','blue_circle',True,True,300),Trial('quiet','blue_circle',True,False,None),Trial('quiet','blue_square',False,True,250),Trial('quiet','purple_circle',False,False,None)]
    m=score_condition(trials)
    assert m['hits']==1 and m['misses']==1
    assert m['false_alarms']==1 and m['correct_rejections']==1
    assert m['accuracy']==0.5 and m['median_rt_ms']==300
    assert m['completed'] is True

def test_rt_unavailable_when_no_correct_hits():
    m=score_condition([Trial('quiet','blue_circle',True,False,None)])
    assert m['median_rt_ms'] is None

def test_compare():
    a=[Trial('quiet','blue_circle',True,True,400)]
    b=[Trial('notifications','blue_circle',True,True,500)]
    c=compare_conditions(a,b)
    assert c['median_rt_difference_ms']==100
