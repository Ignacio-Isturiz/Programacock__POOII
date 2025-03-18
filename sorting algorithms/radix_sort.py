from sorting_algorithm import SortingAlgorithm

class RadixSort(SortingAlgorithm):
    def sort(self, arr, ascending=True):
        if not arr:
            return []

        max_value = max(arr)
        exp = 1
        while max_value // exp > 0:
            arr = self.counting_sort(arr, exp, ascending)
            exp *= 10
        return arr

    def counting_sort(self, arr, exp, ascending):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in reversed(range(n)):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1

        return output if ascending else output[::-1]
