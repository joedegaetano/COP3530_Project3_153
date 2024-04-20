import random
# Define a function for Shell Sort
def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and (arr[j - gap]['review_count']) < (temp['review_count']):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

def is_sorted(arr):
    """Check if the list of dictionaries is sorted."""
    for i in range(len(arr) - 1):
        print(arr[i]['review_count'])
        if arr[i]['review_count'] > arr[i - 1]['review_count']:
            print("false")
            return False
    return True

def bogo_sort(arr):
    """Implement the Bogo sort algorithm."""
    while not is_sorted(arr):
        random.shuffle(arr)