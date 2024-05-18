def main(_list: list[list[int]]):
    return [{f'k{i + 1}': el[i] for i in range(len(el))} for el in _list]

if __name__ == '__main__':
    print(main([[1,2,3], [4,5,6]]))
