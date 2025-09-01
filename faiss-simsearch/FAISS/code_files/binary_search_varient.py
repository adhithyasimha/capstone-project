def find_element(array, key):
    start = 0
    end = len(array) - 1
    while start <= end:
        mid = (start + end) // 2
        if array[mid] == key:
            return mid
        if array[mid] < key:
            start = mid + 1
        else:
            end = mid - 1
    return -1

data = [1, 3, 5, 7, 9, 11]
key = 7
position = find_element(data, key)
print(f"Found at index: {position}")

