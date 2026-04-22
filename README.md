# ML Experiment Tracker

![Language](https://img.shields.io/badge/Language-Python-blue)
![Tests](https://img.shields.io/badge/Tests-10%20passing-green)
![Storage](https://img.shields.io/badge/Storage-SQLite-orange)

Lightweight ML experiment tracking tool with SQLite storage.
Log parameters, metrics, and tags — then compare and find the best experiment.

## Demo Output

    Started experiment: 'baseline_lr0.01' (id=1)
    Started experiment: 'high_lr0.1' (id=2)
    Started experiment: 'low_lr0.001' (id=3)

    ML Experiment Tracker - 3 experiments

    [3] low_lr0.001
        Tags: ['simulation', 'demo']
        loss: 0.1766 (best: 1.0526)
        accuracy: 0.9900 (best: 0.9900)

    Best experiment: 'low_lr0.001' with accuracy=0.9900

## Quick Start

    git clone https://github.com/0mohamed123/ml-experiment-tracker.git
    cd ml-experiment-tracker
    pip install numpy

    cd src
    python cli.py

    cd ../tests
    python -m pytest test_tracker.py -v

## Usage

    from tracker import ExperimentTracker

    tracker = ExperimentTracker('experiments.db')

    tracker.start("my_experiment",
        params={'lr': 0.01, 'epochs': 100},
        tags=['CNN', 'CIFAR-10'])

    for epoch in range(100):
        tracker.log(loss=0.5, accuracy=0.8)

    tracker.end()

    # Find best experiment
    best, val = tracker.best('accuracy', mode='max')
    print(f"Best: {best['name']} -> {val:.4f}")

## Features

- Log metrics per epoch with automatic history
- Save hyperparameters and tags per experiment
- SQLite storage — no external dependencies
- Find best experiment by any metric
- Summary report of all experiments