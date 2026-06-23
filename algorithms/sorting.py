"""
Sorting algorithms ka logic yahan hai.
Har function ek 'steps' list return karta hai — har step mein
array ki state hoti hai us particular moment par.
"""


def bubble_sort(arr):
    arr = arr.copy()
    steps = []
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            steps.append({
                "array": arr.copy(),
                "comparing": (j, j + 1),
                "swapped": False
            })

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append({
                    "array": arr.copy(),
                    "comparing": (j, j + 1),
                    "swapped": True
                })

    steps.append({
        "array": arr.copy(),
        "comparing": None,
        "swapped": False
    })

    return steps


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
                i += 1
            else:
                array[k] = right_half[j]
                j += 1
            k += 1

            steps.append({
                "array": array.copy(),
                "comparing": (k - 1, k - 1),
                "swapped": True
            })

        while i < len(left_half):
            array[k] = left_half[i]
            i += 1
            k += 1
            steps.append({
                "array": array.copy(),
                "comparing": (k - 1, k - 1),
                "swapped": True
            })

        while j < len(right_half):
            array[k] = right_half[j]
            j += 1
            k += 1
            steps.append({
                "array": array.copy(),
                "comparing": (k - 1, k - 1),
                "swapped": True
            })

    _merge_sort_helper(arr, 0, len(arr))

    steps.append({
        "array": arr.copy(),
        "comparing": None,
        "swapped": False
    })

    return steps


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
                "swapped": False
            })

            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
                steps.append({
                    "array": array.copy(),
                    "comparing": (i, j),
                    "swapped": True
                })

        array[i + 1], array[high] = array[high], array[i + 1]
        steps.append({
            "array": array.copy(),
            "comparing": (i + 1, high),
            "swapped": True
        })

        return i + 1

    _quick_sort_helper(arr, 0, len(arr) - 1)

    steps.append({
        "array": arr.copy(),
        "comparing": None,
        "swapped": False
    })

    return steps
