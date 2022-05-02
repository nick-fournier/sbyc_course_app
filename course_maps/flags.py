import os
import pandas as pd
import yaml
from IPython.core.display import HTML


def replace_all(string, target_list):
    for x in target_list:
        string = string.replace(x, '')
    return string


def url_image_index(yaml_path='course_maps/fixtures/flags.yaml'):
    with open(yaml_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


def static_image_index(image_path='course_maps/static/flags'):
    image_list = []
    for f in os.listdir(image_path):
        k = replace_all(os.path.splitext(f)[0].lower(), ['ics_', 'pennant_'])
        image_list.append({'value': k, 'source': f})
    return image_list


def path_to_image_html(src):
    return "<img src=\"{}\" width=\"60\">".format(src)


def html_flag_tables(html_classes):
    flags = pd.DataFrame(url_image_index())
    flag_tables = {}
    for type in ['alphabet', 'numeric']:
        flag_tables[type + '_flag_table'] = flags[flags.type == type].drop(columns='type').to_html(
            classes=html_classes, index=False, escape=False,
            formatters=dict(flag=path_to_image_html)
        )

    return flag_tables

