from csv import DictReader
from pprint import pprint
from pathlib import Path


def main(file: Path):
    result: dict[str, list[tuple]] = {}
    with open(file, 'r', encoding='utf-8') as f:
        fields = ('lastname', 'name', 'patronymic', 'date_of_birth', 'id')
        reader = DictReader(f, fields, delimiter='|')
        for row in reader:
            values = tuple(row.values())
            if values == fields:
                continue
            id = row['id']
            if id in result and all([el != values for el in result[id]]):
                result[id].append(values)
            else:
                result[id] = [values]
    return result

if __name__ == '__main__':
    pprint(main(Path('./example1.csv')))
