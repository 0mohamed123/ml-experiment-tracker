from tracker import ExperimentTracker
import numpy as np
import time


def simulate_training(tracker, name, lr, epochs, noise=0.1):
    tracker.start(
        name=name,
        params={'lr': lr, 'epochs': epochs},
        tags=['simulation', 'demo']
    )
    for epoch in range(epochs):
        loss = 1.0 / (epoch + 1) + np.random.uniform(0, noise)
        acc = min(0.99, 0.5 + epoch * 0.05 + np.random.uniform(0, noise))
        tracker.log(loss=loss, accuracy=acc)
    return tracker.end()


def main():
    tracker = ExperimentTracker('experiments.db')

    print("Running 3 simulated experiments...\n")

    simulate_training(tracker, "baseline_lr0.01", lr=0.01, epochs=10)
    simulate_training(tracker, "high_lr0.1",     lr=0.1,  epochs=10)
    simulate_training(tracker, "low_lr0.001",    lr=0.001, epochs=10)

    tracker.summary()

    best_exp, best_val = tracker.best('accuracy', mode='max')
    print(f"Best experiment: '{best_exp['name']}' with accuracy={best_val:.4f}")


if __name__ == '__main__':
    main()