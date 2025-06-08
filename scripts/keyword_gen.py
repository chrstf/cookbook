import argparse
import yaml
import os
from pytools.outils import collect_md_head_data
import re


readme_header = '''---
layout: home
title: zettelkasten
permalink: /
---
'''


def collect_all_keywords(fnames: list):
    out = dict()
    for _fn in fnames:
        head = collect_md_head_data(_fn)
        if 'keywords' not in head:
            head['keywords'] = []
        head['fname'] = os.path.split(_fn)[1].split('.')[0]
        out[_fn] = head
    return out


def assign_fnames_to_keywords(collected_kw_data: dict):
    out = dict()
    date_pat = re.compile(r'^\[(\d\d\d\d)-(\d\d)-(\d\d) ')
    for _k in collected_kw_data.keys():
        lnk = f'[{str(collected_kw_data[_k]["date"])} {collected_kw_data[_k]["title"]}]'
        lnk += '('
        lnk += '{{site.baseurl}}'
        lnk += f'/{collected_kw_data[_k]["category"]}'
        lnk += f'/{collected_kw_data[_k]["fname"]}.html'
        lnk += ')'
        for kw in collected_kw_data[_k]['keywords']:
            if kw not in out:
                out[kw] = []
            out[kw].append(lnk)

    # sorting
    for _k in out.keys():
        out[_k] = sorted(
            out[_k],
            key=lambda x: (re.search(date_pat, x).group(1), re.search(date_pat, x).group(2), re.search(date_pat, x).group(3)),
            reverse=True
        )
    return out


def complete_readme(readme_head: str, keywords: dict):
    out = readme_head + '\n'
    out += '## Keywords\n\n'
    out += '; '.join(
        f'[{_item}]('+'{{site.baseurl}}'+f'/#{_item.lower().replace(" ", "-")})' for _item in sorted(keywords)
        # f'[{_item}]' for _item in sorted(keywords)
    )
    out += '\n\n'
    for _k in sorted(keywords):
        out += f'### {_k}\n\n'
        out += '\n'.join(f'- {_item}' for _item in keywords[_k])
        out += '\n\n'
    return out


def run(jekyll_loc: str):
    with open(os.path.join(jekyll_loc, '_config.yml'), 'r') as _f:
        config_data = yaml.safe_load(_f)
    all_posts = [os.path.join(jekyll_loc, f'_posts/{_fn}') for _fn in os.listdir(os.path.join(jekyll_loc, '_posts'))]
    keywords = collect_all_keywords(all_posts)
    keywords = assign_fnames_to_keywords(keywords)
    readme = complete_readme(readme_header, keywords)
    # write README.md file
    readme_loc = os.path.join(jekyll_loc, 'README.md')
    with open(readme_loc, 'w') as _f:
        _f.write(readme)
    print(f'Updated \"{readme_loc}\"')
    # print(readme)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--jekyll_loc', type=str, default='jekyll',
                        help='location of the jekyll data')
    args = parser.parse_args()
    run(args.jekyll_loc)

