from pathlib import Path


def collect_prefixes(file: Path):
    res: dict[str, list[str]] = {}
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            for i in range(len(stripped)):
                if stripped[:i+1] in res:
                    res[stripped[:i+1]].append(stripped)
                else:
                    res[stripped[:i+1]] = [stripped]
    return res


if __name__ == '__main__':
    pref_dict = collect_prefixes(Path('./example5.txt'))
    word = input('input word:  ')
    for i in range(len(word) - 1, 0, -1):
        suffix = word[i:]
        if suffix in pref_dict:
            for ending in pref_dict[suffix]:
                print(f'{word[:-len(suffix)]}{suffix}{ending[len(suffix):]}')
