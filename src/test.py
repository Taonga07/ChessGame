def index_2d(array, index) -> int:
    "convert index of flattened array to 2D array"
    return (index // len(array), index % len(array[0]))
def index_1d(array, index) -> int:
    "convert index of 2D array to flattened array"
    return index[0] * len(array[0]) + index[1]

a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
a_flat = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(index_2d(a, index_1d(a, (1, 1))))
print(index_1d(a, index_2d(a, (1, 1))))