import argparse
from datetime import datetime
import os


def make_head(title: str, category: str, keywords: list) -> str:
    now = datetime.now()
    out = [
        '---',
        f'title: {title}',
        f'category: {category}',
        f'date: {now.year}-{now.month:02d}-{now.day:02d}',
        f'keywords:'
    ]
    out += [f'- {_k}' for _k in keywords]
    out.append(f'layout: post')
    out.append(f'---')
    return '\n'.join(out)


def make_new_post(title: str, category: str, keywords: list):
    if keywords is None:
        keywords = [category]
    out = make_head(title, category, keywords)
    out += '\n\n# Graphics example\n\n'
    out += '![example]({{site.baseurl}}/assets/dinosaur.gif)\n\n'
    out += '# References\n\n'
    out += '| <https://duckduckgo.com/>'
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--post_loc', type=str, default='jekyll/_posts/')
    parser.add_argument('-t', '--title', type=str, default='Title goes here')
    parser.add_argument('-c', '--category', type=str, default='category goes here')
    parser.add_argument('-k', '--keyword', type=str, nargs='+')
    args = parser.parse_args()

    new_post = make_new_post(
        args.title,
        args.category,
        args.keyword
    )
    now = datetime.now()
    fname = os.path.join(args.post_loc, f'{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}{now.minute:02d}.md')
    with open(fname, 'w') as _f:
        _f.write(new_post)
    print(f'Opened new post under \"{fname}\"')
