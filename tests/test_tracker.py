import sys
sys.path.append('../src')

import os
import pytest
from tracker import ExperimentTracker


@pytest.fixture
def tracker(tmp_path):
    db = str(tmp_path / "test.db")
    return ExperimentTracker(db)


def test_start_experiment(tracker):
    tracker.start("test_exp", params={'lr': 0.01})
    assert tracker.current['name'] == "test_exp"
    assert tracker.current['id'] is not None


def test_log_metrics(tracker):
    tracker.start("test_exp")
    tracker.log(loss=0.5, accuracy=0.8)
    assert 'loss' in tracker.current['metrics']
    assert tracker.current['metrics']['loss'] == [0.5]
    assert tracker.current['metrics']['accuracy'] == [0.8]


def test_log_multiple_epochs(tracker):
    tracker.start("test_exp")
    tracker.log(loss=1.0)
    tracker.log(loss=0.5)
    tracker.log(loss=0.2)
    assert len(tracker.current['metrics']['loss']) == 3


def test_end_experiment(tracker):
    tracker.start("test_exp")
    tracker.log(loss=0.5)
    exp = tracker.end()
    assert tracker.current is None
    assert 'duration_seconds' in exp['metrics']


def test_get_experiment(tracker):
    tracker.start("test_exp", params={'lr': 0.01}, tags=['test'])
    tracker.log(loss=0.5)
    exp = tracker.end()
    loaded = tracker.get(exp['id'])
    assert loaded['name'] == "test_exp"
    assert loaded['params']['lr'] == 0.01


def test_list_experiments(tracker):
    tracker.start("exp1"); tracker.log(loss=0.5); tracker.end()
    tracker.start("exp2"); tracker.log(loss=0.3); tracker.end()
    exps = tracker.list_experiments()
    assert len(exps) == 2


def test_best_experiment(tracker):
    tracker.start("exp1"); tracker.log(accuracy=0.7); tracker.end()
    tracker.start("exp2"); tracker.log(accuracy=0.9); tracker.end()
    tracker.start("exp3"); tracker.log(accuracy=0.8); tracker.end()
    best, val = tracker.best('accuracy', mode='max')
    assert best['name'] == "exp2"
    assert val == 0.9


def test_best_min(tracker):
    tracker.start("exp1"); tracker.log(loss=0.5); tracker.end()
    tracker.start("exp2"); tracker.log(loss=0.1); tracker.end()
    best, val = tracker.best('loss', mode='min')
    assert best['name'] == "exp2"
    assert val == 0.1


def test_params_saved(tracker):
    params = {'lr': 0.01, 'epochs': 100, 'batch_size': 32}
    tracker.start("test", params=params)
    exp = tracker.end()
    loaded = tracker.get(exp['id'])
    assert loaded['params'] == params


def test_no_active_experiment(tracker):
    with pytest.raises(RuntimeError):
        tracker.log(loss=0.5)