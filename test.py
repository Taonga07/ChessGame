lst1 = [15, 9, 10, 56, 23, 78, 5, 4, 9]
lst2 = [9, 4, 5, 36, 47, 26, 10, 45, 87]
lst3 = [5, 73, 6]
lst = (list(set(lst1) & set(lst2)))
lst3.extend(lst)
print(lst3)