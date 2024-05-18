from pathlib import Path
from datetime import datetime, timedelta


def main(days: int, folder: Path):
    if not folder.is_dir():
        raise ValueError(f'{folder} does not exisits or is not folder')
    if days < 0:
        raise ValueError('`days` arg cannot be less than 0')
    delta = timedelta(days=days)
    for file in folder.iterdir():
        if (
            file.is_file() and
            datetime.now() - datetime.fromtimestamp(file.stat().st_birthtime) >= delta
        ):
            # input(f'Here, {file.name}')
            file.unlink()


if __name__ == '__main__':
    main(1, Path('./test_dir/'))
