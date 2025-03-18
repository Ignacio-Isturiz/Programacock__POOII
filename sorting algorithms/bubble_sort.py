from sorting_algorithm import SortingAlgorithm

class BubbleSort(SortingAlgorithm):
    def sort(self, arr, ascending=True):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if (arr[j] > arr[j+1] and ascending) or (arr[j] < arr[j+1] and not ascending):
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
