import random
import time
from copy import deepcopy
from itertools import cycle
from typing import Callable, Optional

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import sorting_functions
from counted_comparison_type import CountedComparisons


def is_sorted(arr: list[CountedComparisons]) -> bool:
    for i in range(1, len(arr)):
        if arr[i-1] > arr[i]:
            return False
    return True

def test_sorting(sorting_funcs: list[Callable[[list[CountedComparisons]], None]],
                 num_trials: int,
                 length: int) -> tuple[list[Optional[float]], list[Optional[float]]]:
    unsorted_arrays = [[CountedComparisons(random.random()) for _ in range(length)] for _ in range(num_trials)]
    time_results = []
    comparisons_results = []
    for sorting_func in sorting_funcs:
        arrays_copy = deepcopy(unsorted_arrays)
        correct = True
        total_time = 0
        total_comparisons = 0
        for i in range(num_trials):
            CountedComparisons.reset()
            start_time = time.perf_counter()
            sorting_func(arrays_copy[i])
            end_time = time.perf_counter()
            total_time += end_time - start_time
            total_comparisons += CountedComparisons.get_count()
            if not(is_sorted(arrays_copy[i])):
                print(sorting_func.__name__, "incorrectly sorted.")
                correct = False
                break
        if correct:
            time_results.append(total_time / num_trials)
            comparisons_results.append(total_comparisons / num_trials)
        else:
            time_results.append(None)
            comparisons_results.append(None)

    return time_results, comparisons_results

if __name__ == "__main__":
    sorting_funcs = [sorting_functions.bubble_sort,
                     sorting_functions.insertion_sort,
                     sorting_functions.heap_sort,
                     sorting_functions.quick_sort,
                     sorting_functions.merge_sort,
                     sorting_functions.built_in_sort]

    lengths = np.logspace(1, 6, num=16, dtype=int)
    time_taken = np.full((len(sorting_funcs), len(lengths)), np.nan)
    comparisons = np.full((len(sorting_funcs), len(lengths)), np.nan)

    use_funcs = list(range(len(sorting_funcs)))

    for i, length in tqdm(enumerate(lengths)):
        times, comps = test_sorting([sorting_funcs[idx] for idx in use_funcs], 2, length)
        time_taken[use_funcs, i] = times
        comparisons[use_funcs, i] = comps
        remove_list = [idx for idx in use_funcs if time_taken[idx][i] > 2]
        use_funcs = [idx for idx in use_funcs if idx not in remove_list]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))

    markers = cycle(['o', 's', '^', 'D', 'v', 'P', 'X'])

    # Time taken plot
    ax1.set_xscale('log')
    for i, func in enumerate(sorting_funcs):
        ax1.plot(lengths, time_taken[i, :], label=func.__name__, marker=next(markers), markersize=5)
    ax1.set_title("Time Taken")
    ax1.set_xlabel("Input Size")
    ax1.set_ylabel("Time [sec]")
    ax1.legend(loc="upper left")
    ax1.grid(True, which="both", linestyle="--", alpha=0.6)

    markers = cycle(['o', 's', '^', 'D', 'v', 'P', 'X'])

    # Comparisons plot
    ax2.set_xscale('log')
    for i, func in enumerate(sorting_funcs):
        ax2.plot(lengths, comparisons[i, :], label=func.__name__, marker=next(markers), markersize=5)
    ax2.set_title("Comparisons")
    ax2.set_xlabel("Input Size")
    ax2.set_ylabel("Count")
    ax2.legend(loc="upper left")
    ax2.grid(True, which="both", linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.show()
