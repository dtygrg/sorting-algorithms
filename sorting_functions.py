from typing import Optional

from counted_comparison_type import CountedComparisons


def insertion_sort(arr: list[CountedComparisons]):
    for i in range(1, len(arr)):
        num = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > num:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = num

def bubble_sort(arr: list[CountedComparisons]):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def partition(arr: list[CountedComparisons], left: int, right: int) -> int:
    pivot = arr[right]
    i = left - 1
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1

def quick_sort(arr: list[CountedComparisons], left: int=0, right: Optional[int]=None):
    if right is None:
        right = len(arr) - 1
    if left < right:
        p = partition(arr, left, right)
        quick_sort(arr, left, p - 1)
        quick_sort(arr, p + 1, right)

def heapify(arr: list[CountedComparisons], n: int, i: int):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr: list[CountedComparisons]):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

def merge(arr: list[CountedComparisons], left: int, mid: int, right: int):
    num_left = mid - left + 1
    num_right = right - mid

    left_arr = [CountedComparisons(0)] * num_left
    right_arr = [CountedComparisons(0)] * num_right

    for i in range(num_left):
        left_arr[i] = arr[left + i]
    for j in range(num_right):
        right_arr[j] = arr[mid + 1 + j]

    i = j = 0
    k = left

    while i < num_left and j < num_right:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1

    while i < num_left:
        arr[k] = left_arr[i]
        i += 1
        k += 1
    while j < num_right:
        arr[k] = right_arr[j]
        j += 1
        k += 1

def merge_sort(arr: list[CountedComparisons], left: int=0, right: Optional[int]=None):
    if right is None:
        right = len(arr) - 1
    if left < right:
        mid = left + (right - left) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)

def built_in_sort(arr: list[CountedComparisons]):
    arr.sort()
