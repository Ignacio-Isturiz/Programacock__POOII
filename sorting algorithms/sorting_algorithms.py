import math

def bucket_sort(arr, ascending=True):
    if len(arr) == 0:
        return arr

    bucket_count = round(math.sqrt(len(arr)))
    max_val, min_val = max(arr), min(arr)
    buckets = [[] for _ in range(bucket_count)]

    for num in arr:
        index = math.floor((num - min_val) / (max_val - min_val + 1) * bucket_count)
        buckets[index].append(num)

    for bucket in buckets:
        bucket.sort(reverse=not ascending)

    return [num for bucket in buckets for num in bucket]

def bubble_sort(arr, ascending=True):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if (arr[j] > arr[j + 1] and ascending) or (arr[j] < arr[j + 1] and not ascending):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def counting_sort(arr, ascending=True):
    max_val = max(arr)
    min_val = min(arr)
    range_of_elements = max_val - min_val + 1
    count = [0] * range_of_elements
    output = [0] * len(arr)

    for num in arr:
        count[num - min_val] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for num in reversed(arr):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1

    return output if ascending else output[::-1]

def heap_sort(arr, ascending=True):
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

    return arr if ascending else arr[::-1]

def insertion_sort(arr, ascending=True):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and ((key < arr[j] and ascending) or (key > arr[j] and not ascending)):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr, ascending=True):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = merge_sort(arr[:mid], ascending)
        right = merge_sort(arr[mid:], ascending)

        arr = []
        while left and right:
            if (left[0] < right[0] and ascending) or (left[0] > right[0] and not ascending):
                arr.append(left.pop(0))
            else:
                arr.append(right.pop(0))

        arr.extend(left if left else right)
    return arr

def quick_sort(arr, ascending=True):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left, ascending) + middle + quick_sort(right, ascending) if ascending else quick_sort(right, ascending) + middle + quick_sort(left, ascending)

def radix_sort(arr, ascending=True):
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        arr = counting_sort_by_digit(arr, exp, ascending)
        exp *= 10
    return arr

def counting_sort_by_digit(arr, exp, ascending):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for num in arr:
        index = num // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for num in reversed(arr):
        index = num // exp
        output[count[index % 10] - 1] = num
        count[index % 10] -= 1

    return output if ascending else output[::-1]

def selection_sort(arr, ascending=True):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if (arr[j] < arr[min_idx] and ascending) or (arr[j] > arr[min_idx] and not ascending):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
