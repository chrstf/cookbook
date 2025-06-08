import argparse
import yaml


def read_md(md_loc: str) -> str:
    #  print(md_loc)
    with open(md_loc, 'r') as _f:
        lines = _f.read()
    return lines


def extract_head(md: str) -> str:
    keep = []
    collect = False
    for line in md.splitlines():
        if line[:3] == '---':
            if collect is False:
                collect = True
                continue
            else:
                break
        if collect is True:
            keep.append(line)
    keep = '\n'.join(keep)
    return keep


def collect_md_head_data(md_loc: str) -> dict:
    md = read_md(md_loc)
    md_head = extract_head(md)
    return yaml.safe_load(md_head)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='Location of the markdown file')
    args = parser.parse_args()

    print(collect_md_head_data(args.file))
