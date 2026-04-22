from storage import Storage
import time


class ExperimentTracker:
    def __init__(self, db_path='experiments.db'):
        self.storage = Storage(db_path)
        self.current = None
        self._start_time = None

    def start(self, name, params=None, tags=None, notes=''):
        self.current = {
            'name': name,
            'params': params or {},
            'metrics': {},
            'tags': tags or [],
            'notes': notes
        }
        self._start_time = time.time()
        self.current['id'] = self.storage.save(self.current)
        print(f"Started experiment: '{name}' (id={self.current['id']})")
        return self

    def log(self, **kwargs):
        if not self.current:
            raise RuntimeError("No active experiment. Call start() first.")
        for key, value in kwargs.items():
            if key not in self.current['metrics']:
                self.current['metrics'][key] = []
            self.current['metrics'][key].append(round(float(value), 6))
        self.storage.save(self.current)
        return self

    def end(self):
        if not self.current:
            return
        elapsed = time.time() - self._start_time
        self.log(duration_seconds=elapsed)
        print(f"Experiment '{self.current['name']}' finished in {elapsed:.2f}s")
        exp = self.current
        self.current = None
        return exp

    def get(self, exp_id):
        return self.storage.load(exp_id)

    def list_experiments(self):
        return self.storage.list_all()

    def best(self, metric, mode='max'):
        experiments = self.storage.list_all()
        best_exp = None
        best_val = None
        for exp in experiments:
            if metric in exp['metrics']:
                vals = exp['metrics'][metric]
                val = max(vals) if mode == 'max' else min(vals)
                if best_val is None or \
                   (mode == 'max' and val > best_val) or \
                   (mode == 'min' and val < best_val):
                    best_val = val
                    best_exp = exp
        return best_exp, best_val

    def summary(self):
        experiments = self.storage.list_all()
        print(f"\n{'='*55}")
        print(f"  ML Experiment Tracker — {len(experiments)} experiments")
        print(f"{'='*55}")
        for exp in experiments:
            print(f"\n  [{exp['id']}] {exp['name']}")
            print(f"      Tags: {exp['tags']}")
            for metric, values in exp['metrics'].items():
                if metric != 'duration_seconds':
                    print(f"      {metric}: {values[-1]:.4f} (best: {max(values):.4f})")
        print(f"{'='*55}\n")