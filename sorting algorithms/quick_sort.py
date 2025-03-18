from sorting_algorithm import SortingAlgorithm

class QuickSort(SortingAlgorithm):
    def sort(self, arr, ascending=True):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if (x < pivot and ascending) or (x > pivot and not ascending)]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if (x > pivot and ascending) or (x < pivot and not ascending)]
        return self.sort(left, ascending) + middle + self.sort(right, ascending)
