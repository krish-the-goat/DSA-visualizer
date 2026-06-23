"""
Sorting algorithms — Bubble Sort, Merge Sort, Quick Sort, Insertion Sort, Selection Sort.
Each function returns a list of step dicts containing:
  - array: current state of the array
  - comparing: tuple (i, j) of indices being compared, or None
  - swapped: bool indicating if a swap occurred
  - caption: human-readable description of the current step
  - pseudo_line: int indicating which pseudo-code line is active
"""

import random


def generate_random_array(size_min=8, size_max=12, val_min=1, val_max=50):
    """Generates a random array for visualization."""
    size = random.randint(size_min, size_max)
    return [random.randint(val_min, val_max) for _ in range(size)]


# ─── Bubble Sort ──────────────────────────────────────────────────────────────

def bubble_sort(arr):
    arr = arr.copy()
    steps = []
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            steps.append({
                "array": arr.copy(),
                "comparing": (j, j + 1),
                "swapped": False,
                "caption": f"Comparing arr[{j}]={arr[j]} with arr[{j+1}]={arr[j+1]}",
                "pseudo_line": 3,
            })

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append({
                    "array": arr.copy(),
                    "comparing": (j, j + 1),
                    "swapped": True,
                    "caption": f"Swapped arr[{j}]={arr[j]} and arr[{j+1}]={arr[j+1]} ✅",
                    "pseudo_line": 4,
                })

    steps.append({
        "array": arr.copy(),
        "comparing": None,
        "swapped": False,
        "caption": "✅ Array is now sorted!",
        "pseudo_line": 6,
    })

    return steps


# ─── Merge Sort ───────────────────────────────────────────────────────────────

def merge_sort(arr):
    arr = arr.copy()
    steps = []

    def _merge_sort_helper(array, left, right):
        if right - left <= 1:
            return
        mid = (left + right) // 2
        _merge_sort_helper(array, left, mid)
        _merge_sort_helper(array, mid, right)
        _merge(array, left, mid, right)

    def _merge(array, left, mid, right):
        left_half = array[left:mid]
        right_half = array[mid:right]

        i = j = 0
        k = left

        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                array[k] = left_half[i]
                steps.append({
                    "array": array.copy(),
                    "comparing": (k, k),
                    "swapped": True,
                    "caption": f"Merging: placing {left_half[i]} from left half at position {k}",
                    "pseudo_line": 5,
                })
                i += 1
            else:
                array[k] = right_half[j]
                steps.append({
                    "array": array.copy(),
                    "comparing": (k, k),
                    "swapped": True,
                    "caption": f"Merging: placing {right_half[j]} from right half at position {k}",
                    "pseudo_line": 7,
                })
                j += 1
            k += 1

        while i < len(left_half):
            array[k] = left_half[i]
            steps.append({
                "array": array.copy(),
                "comparing": (k, k),
                "swapped": True,
                "caption": f"Copying remaining {left_half[i]} from left half to position {k}",
                "pseudo_line": 8,
            })
            i += 1
            k += 1

        while j < len(right_half):
            array[k] = right_half[j]
            steps.append({
                "array": array.copy(),
                "comparing": (k, k),
                "swapped": True,
                "caption": f"Copying remaining {right_half[j]} from right half to position {k}",
                "pseudo_line": 9,
            })
            j += 1
            k += 1

    _merge_sort_helper(arr, 0, len(arr))

    steps.append({
        "array": arr.copy(),
        "comparing": None,
        "swapped": False,
        "caption": "✅ Array is now sorted!",
        "pseudo_line": 10,
    })

    return steps


# ─── Quick Sort ───────────────────────────────────────────────────────────────

def quick_sort(arr):
    arr = arr.copy()
    steps = []

    def _quick_sort_helper(array, low, high):
        if low < high:
            pivot_index = _partition(array, low, high)
            _quick_sort_helper(array, low, pivot_index - 1)
            _quick_sort_helper(array, pivot_index + 1, high)

    def _partition(array, low, high):
        pivot = array[high]
        i = low - 1

        for j in range(low, high):
            steps.append({
                "array": array.copy(),
                "comparing": (j, high),
                "swapped": False,
                "caption": f"Comparing arr[{j}]={array[j]} with pivot={pivot} (at index {high})",
                "pseudo_line": 5,
            })

            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
                steps.append({
                    "array": array.copy(),
                    "comparing": (i, j),
                    "swapped": True,
                    "caption": f"arr[{j}] < pivot → Swapped arr[{i}]={array[i]} and arr[{j}]={array[j]} ✅",
                    "pseudo_line": 7,
                })

        array[i + 1], array[high] = array[high], array[i + 1]
        steps.append({
            "array": array.copy(),
            "comparing": (i + 1, high),
            "swapped": True,
            "caption": f"Placing pivot {pivot} at its final position index {i + 1} ✅",
            "pseudo_line": 8,
        })

        return i + 1

    _quick_sort_helper(arr, 0, len(arr) - 1)

    steps.append({
        "array": arr.copy(),
        "comparing": None,
        "swapped": False,
        "caption": "✅ Array is now sorted!",
        "pseudo_line": 10,
    })

    return steps


# ─── Insertion Sort ───────────────────────────────────────────────────────────

def insertion_sort(arr):
    arr = arr.copy()
    steps = []
    n = len(arr)

    steps.append({
        "array": arr.copy(),
        "comparing": (0, 0),
        "swapped": False,
        "caption": f"Starting: arr[0]={arr[0]} is already sorted (single element).",
        "pseudo_line": 1,
    })

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        steps.append({
            "array": arr.copy(),
            "comparing": (i, i),
            "swapped": False,
            "caption": f"Picking key={key} at index {i}. Shifting larger elements right.",
            "pseudo_line": 2,
        })

        while j >= 0 and arr[j] > key:
            steps.append({
                "array": arr.copy(),
                "comparing": (j, j + 1),
                "swapped": False,
                "caption": f"arr[{j}]={arr[j]} > key={key} → shifting arr[{j}] right",
                "pseudo_line": 4,
            })

            arr[j + 1] = arr[j]
            j -= 1

            steps.append({
                "array": arr.copy(),
                "comparing": (j + 1, j + 2),
                "swapped": True,
                "caption": f"Shifted to arr[{j+2}]. Checking next position.",
                "pseudo_line": 5,
            })

        arr[j + 1] = key
        steps.append({
            "array": arr.copy(),
            "comparing": (j + 1, j + 1),
            "swapped": True,
            "caption": f"Placed key={key} at index {j+1} ✅",
            "pseudo_line": 6,
        })

    steps.append({
        "array": arr.copy(),
        "comparing": None,
        "swapped": False,
        "caption": "✅ Array is now sorted!",
        "pseudo_line": 7,
    })

    return steps


# ─── Selection Sort ───────────────────────────────────────────────────────────

def selection_sort(arr):
    arr = arr.copy()
    steps = []
    n = len(arr)

    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):
            steps.append({
                "array": arr.copy(),
                "comparing": (min_idx, j),
                "swapped": False,
                "caption": f"Searching for minimum: comparing arr[{min_idx}]={arr[min_idx]} with arr[{j}]={arr[j]}",
                "pseudo_line": 3,
            })

            if arr[j] < arr[min_idx]:
                min_idx = j
                steps.append({
                    "array": arr.copy(),
                    "comparing": (min_idx, min_idx),
                    "swapped": False,
                    "caption": f"New minimum found: arr[{min_idx}]={arr[min_idx]}",
                    "pseudo_line": 4,
                })

        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append({
                "array": arr.copy(),
                "comparing": (i, min_idx),
                "swapped": True,
                "caption": f"Swapped arr[{i}]={arr[i]} with minimum arr[{min_idx}]={arr[min_idx]} ✅",
                "pseudo_line": 6,
            })
        else:
            steps.append({
                "array": arr.copy(),
                "comparing": (i, i),
                "swapped": False,
                "caption": f"arr[{i}]={arr[i]} is already the minimum. No swap needed.",
                "pseudo_line": 6,
            })

    steps.append({
        "array": arr.copy(),
        "comparing": None,
        "swapped": False,
        "caption": "✅ Array is now sorted!",
        "pseudo_line": 7,
    })

    return steps
