def count_amount(_list: list[set[int]]):
    return sum([len(el) for el in _list])

def count_sum(_list: list[set[int]]):
    return sum([sum(el) for el in _list])

def count_avg(_list: list[set[int]]):
    return count_sum(_list) / count_amount(_list)

def tuple_unite(_list: list[set[int]]):
    return tuple(number for set_el in _list for number in set_el)

if __name__ == '__main__':
    m = [{11, 3, 5}, {2, 17, 87, 32}, {4, 44}, {24, 11, 9, 7, 8}]
    print(count_amount(m))
    print(count_sum(m))
    print(count_avg(m))
    print(tuple_unite(m))
