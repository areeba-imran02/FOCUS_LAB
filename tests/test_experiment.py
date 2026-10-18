from focuslab_core.experiment import make_trials, make_session

def test_trial_counts_and_distribution():
    for condition in ('quiet','notifications'):
        trials=make_trials(condition,seed=7)
        assert len(trials)==24
        assert sum(t.is_target for t in trials)==12
        assert sum(not t.is_target for t in trials)==12
        assert sum(t.stimulus=='blue_square' for t in trials)==4
        assert sum(t.stimulus=='purple_circle' for t in trials)==4
        assert sum(t.stimulus=='purple_square' for t in trials)==4

def test_seed_reproducibility_and_condition_orders():
    assert [t.stimulus for t in make_trials('quiet',123)] == [t.stimulus for t in make_trials('quiet',123)]
    assert make_session(3)['condition_order']==make_session(3)['condition_order']
    assert set(make_session(4)['condition_order'])=={'quiet','notifications'}
