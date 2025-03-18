from sorting_algorithm import SortingAlgorithm

class InsertionSort(SortingAlgorithm):
    def sort(self, arr, ascending=True):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and ((arr[j] > key and ascending) or (arr[j] < key and not ascending)):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
