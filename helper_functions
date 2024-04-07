# Define a function for Shell Sort
def shell_sort(arr):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and (arr[j - gap]['stars'], arr[j - gap]['review_count']) < (temp['stars'], temp['review_count']):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
