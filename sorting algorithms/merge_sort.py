from sorting_algorithm import SortingAlgorithm

class MergeSort(SortingAlgorithm):
    def sort(self, arr, ascending=True):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = self.sort(arr[:mid], ascending)
            right_half = self.sort(arr[mid:], ascending)

            return self.merge(left_half, right_half, ascending)
        return arr

    def merge(self, left, right, ascending):
        result = []
        while left and right:
            if (left[0] < right[0] and ascending) or (left[0] > right[0] and not ascending):
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left or right)
        return result
