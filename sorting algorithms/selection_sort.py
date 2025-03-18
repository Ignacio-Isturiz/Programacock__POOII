from sorting_algorithm import SortingAlgorithm

class SelectionSort(SortingAlgorithm):
    def sort(self, arr, ascending=True):
        n = len(arr)
        for i in range(n):
            index = i
            for j in range(i + 1, n):
                if (arr[j] < arr[index] and ascending) or (arr[j] > arr[index] and not ascending):
                    index = j
            arr[i], arr[index] = arr[index], arr[i]
        return arr
