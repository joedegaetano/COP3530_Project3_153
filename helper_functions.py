# Define a function for Shell Sort
def shell_sort(arr,filter_choice):
    n = len(arr)
    gap = n // 2
    if filter_choice == "Best Restaurants":
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and (arr[j - gap]['review_count']) < (temp['review_count']):
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2
    elif filter_choice == "Worst Restaurants":
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and (arr[j - gap]['review_count']) < (temp['review_count']):
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2

