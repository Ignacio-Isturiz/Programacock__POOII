from sorting_algorithm import SortingAlgorithm

class BucketSort(SortingAlgorithm):
    def sort(self, arr, ascending=True):
        if not arr:
            return []
        
        max_value = max(arr)
        size = max_value // len(arr) + 1
        buckets = [[] for _ in range(len(arr))]

        for i in arr:
            index = i // size
            buckets[index].append(i)

        for bucket in buckets:
            bucket.sort(reverse=not ascending)

        sorted_arr = [num for bucket in buckets for num in bucket]
        return sorted_arr
