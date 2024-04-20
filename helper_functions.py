def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and ((arr[j - gap]['score'], arr[j - gap]['review_count']) < (temp['score'], temp['review_count'])):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

def bogo_sort(arr):
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr

def is_sorted(arr):
    for i in range(1, len(arr)):
        if (arr[i]['score'], arr[i]['review_count']) > (arr[i - 1]['score'], arr[i - 1]['review_count']):
            return False
    return True
