import heapq
from sorting_algorithm import SortingAlgorithm

class HeapSort(SortingAlgorithm):
    def sort(self, arr, ascending=True):
        if ascending:
            return [heapq.heappop(arr) for _ in range(len(arr))]
        else:
            arr = [-x for x in arr]
            heapq.heapify(arr)
            return [-heapq.heappop(arr) for _ in range(len(arr))]
