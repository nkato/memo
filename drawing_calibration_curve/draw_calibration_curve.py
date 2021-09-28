from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import gridspec
from sklearn.calibration import calibration_curve

sns.set()
sns.set_style("darkgrid")


def draw_calibration_curve(
    y_true: np.ndarray, y_pred: np.ndarray, n_bins: int = 50, draw_range: Tuple[float, float] = (0.0, 1.0), title: str = ""
) -> None:
    """Drawing calibration curve with matplotlib.

    Args:
        y_true: True targets.
        y_pred: Probabilities of the positive class.
        n_bins: Number of bins to discretize the {draw_range} interval.
        draw_range: Set the x and y limits of the figure.
        title: Figure title.

    Returns:
        None (With drawing figure by plt.show().)
    """
    in_range_idx = np.where((y_pred >= draw_range[0]) & (y_pred <= draw_range[1]))
    y_true_in_range = y_true[in_range_idx]
    y_pred_in_range = y_pred[in_range_idx]
    bins = int(n_bins / (draw_range[1] - draw_range[0]))

    prob_true, prob_pred = calibration_curve(y_true=y_true_in_range, y_prob=y_pred_in_range, n_bins=bins)

    fig = plt.figure(facecolor="white", constrained_layout=True, dpi=150)
    spec = gridspec.GridSpec(ncols=1, nrows=2, height_ratios=[2, 1])

    ax0 = fig.add_subplot(spec[0])
    ax0 = sns.lineplot(x=prob_pred, y=prob_true)
    ax0 = sns.lineplot(x=[0, 1], y=[0, 1], color="gray", alpha=0.5)
    ax0.set(title=title, xlim=draw_range, ylim=draw_range, ylabel="Fraction of positives")

    ax1 = fig.add_subplot(spec[1])
    ax1.hist(y_pred_in_range, range=draw_range, bins=bins)
    ax1.set(xlim=draw_range, xlabel="Mean predicted probability", ylabel="Count")

    plt.show()
