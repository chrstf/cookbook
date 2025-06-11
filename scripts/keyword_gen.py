import argparse
import yaml
import os
from pytools.outils import collect_md_head_data
import re
import json


readme_header = '''---
layout: home
title: N27 cookbook
permalink: /
---
'''


def collect_keywords_n_categories(fnames: list):
    out = dict()
    for _fn in fnames:
        head = collect_md_head_data(_fn)
        if 'keywords' not in head:
            head['keywords'] = []
        if 'category' not in head:
            head['category'] = []
        head['fname'] = os.path.split(_fn)[1].split('.')[0]
        out[_fn] = head
    return out


def assign_fnames_to_keywords(collected_kw_data: dict):
    out = dict()
    date_pat = re.compile(r'^\[(\d\d\d\d)-(\d\d)-(\d\d) ')
    for _k in collected_kw_data.keys():
        lnk = f'[{collected_kw_data[_k]["title"]}]'
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
            #key=lambda x: (re.search(date_pat, x).group(1), re.search(date_pat, x).group(2), re.search(date_pat, x).group(3)),
            #reverse=True
        )
    return out


def assign_fnames_to_categories(collected_data: dict):
    out = dict()
    # date_pat = re.compile(r'^\[(\d\d\d\d)-(\d\d)-(\d\d) ')
    for _k in collected_data.keys():
        lnk = f'[{collected_data[_k]["title"]}]'
        lnk += '('
        lnk += '{{site.baseurl}}'
        lnk += f'/{collected_data[_k]["category"]}'
        lnk += f'/{collected_data[_k]["fname"]}.html'
        lnk += ')'
        if collected_data[_k]['category'] not in out:
            out[collected_data[_k]['category']] = []
        out[collected_data[_k]['category']].append(lnk)

    # sorting
    for _k in out.keys():
        out[_k] = sorted(
            out[_k],
            #key=lambda x: (re.search(date_pat, x).group(1), re.search(date_pat, x).group(2), re.search(date_pat, x).group(3)),
            reverse=True
        )
    return out


def complete_readme_keywords(readme_head: str, keywords: dict):
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


def complete_readme_categories(readme_head: str, _categories: dict):
    out = readme_head + '\n'
    out += '## Keywords\n\n'
    out += '; '.join(
        f'[{_item}]('+'{{site.baseurl}}'+f'/#{_item.lower().replace(" ", "-")})' for _item in sorted(_categories)
        # f'[{_item}]' for _item in sorted(keywords)
    )
    out += '\n\n'
    for _k in sorted(_categories):
        out += f'### {_k}\n\n'
        out += '\n'.join(f'- {_item}' for _item in _categories[_k])
        out += '\n\n'
    return out


def run(jekyll_loc: str):
    with open(os.path.join(jekyll_loc, '_config.yml'), 'r') as _f:
        config_data = yaml.safe_load(_f)
    all_posts = [os.path.join(jekyll_loc, f'_posts/{_fn}') for _fn in os.listdir(os.path.join(jekyll_loc, '_posts'))]
    keywords_n_categories = collect_keywords_n_categories(all_posts)
    keywords = assign_fnames_to_keywords(keywords_n_categories)
    categories = assign_fnames_to_categories(keywords_n_categories)
    #readme = complete_readme_keywords(readme_header, keywords)
    readme = complete_readme_categories(readme_header, categories)
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

